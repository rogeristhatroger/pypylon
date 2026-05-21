#!/usr/bin/env python3
"""\
Calculate and upload a gain shading set to a Basler runner line scan camera.

This sample demonstrates how to compensate for non-uniform illumination by
computing per-column gain shading coefficients. The workflow is:

  1. Grab an image with shading disabled and compute per-column average
     intensities.
  2. Derive multipliers so that every column is scaled to the maximum
     observed intensity (i.e. the brightest column gets multiplier 1.0).
  3. Encode the multipliers as 16.16 fixed-point values, write a binary
     shading file in the camera's expected format, and upload it via the
     GenICam file stream.
  4. Activate the uploaded shading set and verify the correction by
     grabbing another image and recomputing the Max/Min ratio (which should
     now be close to 1.0).

This sample only applies to Basler runner line scan cameras (GigE).
Other cameras will print a message and exit cleanly.

Note: This sample assumes that the conditions for exposure (illumination,
exposure time, etc.) have been set up to deliver images of uniform intensity,
but that the acquired images are not yet uniform. The computed shading data
compensate the observed non-uniformity.
"""
import sys
import struct
import tempfile
import os
from pypylon import pylon
import numpy as np

# Which shading set to use. Change to 2 for UserGainShading2.
SHADING_SET_INDEX = 1

exit_code = 0


################################################################################
#
# The format of arrays containing intensities or coefficients is:
#
#   If the pixel format is Mono8:
#     array_size == width
#     [value_x0, value_x1, value_x2, ..., value_x(width-1)]
#
#   If the pixel format is RGB8:
#     array_size == 3 * width
#     [red_x0,   red_x1,   ..., red_x(width-1),
#      green_x0, green_x1, ..., green_x(width-1),
#      blue_x0,  blue_x1,  ..., blue_x(width-1)]
#
################################################################################


def average_lines(camera, width, height, num_coeffs):
    """Grab one frame, average pixel intensities across lines (height) for each column."""
    with camera.GrabOne(5000) as grab_result:
        buf = np.frombuffer(grab_result.Buffer, dtype=np.uint8).copy()

    if num_coeffs == 3 * width:
        # RGB mode: buffer is HxWx3 interleaved.
        image = buf.reshape(height, width, 3)
        intensities = np.zeros(num_coeffs, dtype=np.float64)
        intensities[:width] = image[:, :, 0].mean(axis=0)
        intensities[width : 2 * width] = image[:, :, 1].mean(axis=0)
        intensities[2 * width :] = image[:, :, 2].mean(axis=0)
    else:
        # Mono mode.
        image = buf.reshape(height, width)
        intensities = image.mean(axis=0).astype(np.float64)

    return intensities


def calculate_coefficients(width, num_coeffs, intensities):
    """Take the average intensities from ``intensities``, identify the
    minimum and maximum average intensity. For each intensity, calculate
    a multiplier so that the product of the multiplier and the intensity
    equals the maximum intensity (the multiplier for the maximum intensity
    is 1). Store the multipliers back in ``intensities``.
    """
    if num_coeffs == 3 * width:
        for offset in (0, width, 2 * width):
            channel = intensities[offset : offset + width]
            channel_min, channel_max = channel.min(), channel.max()
            print(f"Max = {channel_max / channel_min:.4f} * Min (channel offset {offset})")
            intensities[offset : offset + width] = channel_max / channel
    else:
        col_min, col_max = intensities.min(), intensities.max()
        print(f"Max = {col_max / col_min:.4f} * Min")
        intensities[:] = col_max / intensities

    return intensities


def supports_rgb(camera):
    """Check whether the camera supports any RGB pixel format."""
    try:
        for symbolic in camera.PixelFormat.GetSettableValues():
            if "RGB" in symbolic:
                return True
    except Exception:
        pass
    return False


def create_shading_data(camera, local_filename):
    """Compute gain shading data and write the binary file.

    This function assumes that the conditions for exposure (illumination,
    exposure time, etc.) have been set up to deliver images of uniform
    intensity (gray value), but that the acquired images are not uniform.
    We calculate the gain shading data so that the observed non-uniformity
    will be compensated when the data are applied.
    These data are saved to a local file.
    """
    width = camera.Width.Value
    height = camera.Height.Value

    if supports_rgb(camera):
        camera.PixelFormat.Value = "RGB8"
        bytes_per_pixel = 3
    else:
        camera.PixelFormat.Value = "Mono8"
        bytes_per_pixel = 1

    # Disable gain shading during calibration.
    camera.ShadingSelector.Value = "GainShading"
    camera.ShadingEnable.Value = False

    num_coeffs = bytes_per_pixel * width

    print("Grab frame for averaging.")
    intensities = average_lines(camera, width, height, num_coeffs)
    coefficients = calculate_coefficients(width, num_coeffs, intensities)

    # The multipliers are expressed as 32-bit fixed-point numbers with
    # 16 bits before and 16 bits after the decimal point.
    # The maximum multiplier is limited to 3.99998 (max register value 0x0003FFFF).
    MAX_COEFF = 0x0003FFFF
    fixed_point = np.clip(
        (coefficients * (1 << 16)).astype(np.uint32), 0, MAX_COEFF
    )
    if (fixed_point == MAX_COEFF).any():
        print("Gain shading had to be clipped.")

    # Binary file format:
    #   Header (8 bytes): version(1) type(1) sensorType(1) lineType(1) width(2) reserved(2)
    #   Data: num_coeffs x uint32
    SHADING_VERSION_1 = 0x5A
    SHADING_TYPE_GAIN = 0xC3
    SHADING_SENSOR_LINE = 0x02
    SHADING_LINE_SINGLE = 0x01
    SHADING_LINE_TRI = 0x03

    line_type = SHADING_LINE_TRI if bytes_per_pixel == 3 else SHADING_LINE_SINGLE

    with open(local_filename, "wb") as f:
        header = struct.pack(
            "<BBBBHH",
            SHADING_VERSION_1,
            SHADING_TYPE_GAIN,
            SHADING_SENSOR_LINE,
            line_type,
            width,
            0,
        )
        f.write(header)
        f.write(fixed_point.tobytes())


def upload_file(camera, camera_filename, local_filename):
    """Upload a local binary file to the camera's internal file system.

    The C++ sample uses GenApi::ODevFileStream for a one-call transfer.
    pypylon does not expose ODevFileStream, so this function performs the
    equivalent operation manually via FileSelector / FileOperationSelector /
    FileAccessBuffer GenICam nodes.
    """
    with open(local_filename, "rb") as f:
        data = f.read()
    if not data:
        return

    nodemap = camera.NodeMap

    # Select the file on the camera.
    file_selector = pylon.EnumParameter(nodemap, "FileSelector")
    file_selector.Value = camera_filename

    file_operation_selector = pylon.EnumParameter(nodemap, "FileOperationSelector")
    file_access_buffer = pylon.RegisterParameter(nodemap, "FileAccessBuffer")
    file_access_offset = pylon.IntegerParameter(nodemap, "FileAccessOffset")
    file_access_length = pylon.IntegerParameter(nodemap, "FileAccessLength")
    file_operation_execute = pylon.CommandParameter(nodemap, "FileOperationExecute")
    file_operation_status = pylon.EnumParameter(nodemap, "FileOperationStatus")

    # Open file for writing.
    file_operation_selector.Value = "Open"
    pylon.EnumParameter(nodemap, "FileOpenMode").Value = "Write"
    file_operation_execute.Execute()
    if file_operation_status.Value != "Success":
        raise pylon.RuntimeException("Failed to open camera file for writing.")

    # Write data in chunks.
    max_chunk = file_access_buffer.Length
    offset = 0
    while offset < len(data):
        chunk = data[offset : offset + max_chunk]
        file_operation_selector.Value = "Write"
        file_access_offset.Value = offset
        file_access_length.Value = len(chunk)
        file_access_buffer.Set(chunk)
        file_operation_execute.Execute()
        if file_operation_status.Value != "Success":
            raise pylon.RuntimeException(
                f"Failed to write to camera file at offset {offset}."
            )
        offset += len(chunk)

    # Close the file.
    file_operation_selector.Value = "Close"
    file_operation_execute.Execute()


def check_shading_data(camera):
    """Activate the uploaded shading set and verify correction quality.

    After activating and enabling the shading data, grab one image and
    recalculate the multipliers. They should now be close to 1.0, meaning
    the non-uniformity has been compensated.
    """
    width = camera.Width.Value
    height = camera.Height.Value
    bytes_per_pixel = 3 if supports_rgb(camera) else 1
    num_coeffs = bytes_per_pixel * width

    # Activate and enable the gain shading set.
    camera.ShadingSelector.Value = "GainShading"
    if SHADING_SET_INDEX == 1:
        camera.ShadingSetSelector.Value = "UserShadingSet1"
    else:
        camera.ShadingSetSelector.Value = "UserShadingSet2"
    camera.ShadingSetActivate.Execute()
    camera.ShadingEnable.Value = True

    # Grab image and recompute multipliers to show the corrected Max/Min ratio.
    print()
    print("After applying shading correction:")
    intensities = average_lines(camera, width, height, num_coeffs)
    calculate_coefficients(width, num_coeffs, intensities)


try:
    # Only look for GigE cameras (runner cameras are GigE).
    device_list = pylon.TlFactory.GetInstance().EnumerateDevices(
        [{pylon.DeviceClassKey : pylon.BaslerGigEDeviceClass}]
    )

    gige_camera_info = device_list[0] if device_list else None

    if gige_camera_info is None:
        raise pylon.RuntimeException("No GigE camera found.")

    with pylon.InstantCamera(tl_factory.CreateDevice(gige_camera_info)) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        # Use single-frame configuration for shading calibration.
        camera.RegisterConfiguration(
            pylon.AcquireSingleFrameConfiguration(),
            pylon.RegistrationMode_ReplaceAll,
            pylon.Cleanup_Delete,
        )

        camera.Open()

        # Only line scan cameras support gain shading.
        if not (
            camera.DeviceScanType.IsReadable()
            and camera.DeviceScanType.Value == "Linescan"
        ):
            print("Only line scan cameras support gain shading.")
            sys.exit(0)

        local_filename = os.path.join(tempfile.gettempdir(), "ShadingData.bin")

        if SHADING_SET_INDEX == 1:
            camera_filename = "UserGainShading1"
        else:
            camera_filename = "UserGainShading2"

        create_shading_data(camera, local_filename)
        upload_file(camera, camera_filename, local_filename)
        check_shading_data(camera)

        # Clean up the local temporary file.
        try:
            os.remove(local_filename)
        except OSError:
            pass

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
