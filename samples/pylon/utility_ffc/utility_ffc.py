#!/usr/bin/env python3
"""\
Demonstrate Flat-Field Correction (FFC) with Basler boost V cameras.

The goal of FFC is to create a more accurate and evenly-illuminated
representation of the original image. The correction computes per-column
DSNU (Dark Signal Non-Uniformity) and PRNU (Photo Response Non-Uniformity)
coefficients from dark and bright reference images, then uploads them to
the camera.

Workflow:
  1. Grab several dark images (low exposure) and compute per-column averages
     to obtain the DSNU baseline.
  2. Grab several bright images (higher exposure) and compute per-column
     averages for the PRNU response.
  3. Calculate DSNU and PRNU correction coefficients from the two data sets.
  4. Write the coefficients to the camera's BslFlatFieldCorrection registers
     and save to flash memory.

This sample only works with specific Basler boost V CXP camera models:
  boA9344-70cc, boA9344-70cm, boA5120-150cc, boA5120-150cm,
  boA5120-230cc, boA5120-230cm

Other cameras will print a message and exit cleanly.

This sample requires a lot of processing power and execution may take a
long time in debug configurations.

The user is prompted to enter exposure times for the dark and bright
reference images interactively.
"""
import sys
from pypylon import pylon
import numpy as np

NUMBER_OF_IMAGES_TO_GRAB = 5

SUPPORTED_MODELS = {
    "boA9344-70cc", "boA9344-70cm",
    "boA5120-150cc", "boA5120-150cm",
    "boA5120-230cc", "boA5120-230cm",
}

exit_code = 0


def process_images(camera, width, height):
    """Grab images, compute per-column mean intensities and overall mean pixel value.

    Creates an image buffer based on the arithmetic mean of all images
    grabbed and creates a row of correction values for DSNU and PRNU
    coefficients calculation.
    """
    # StartGrabbingMax automatically stops after NUMBER_OF_IMAGES_TO_GRAB
    # images have been retrieved.
    camera.StartGrabbingMax(NUMBER_OF_IMAGES_TO_GRAB)

    print("Please wait. Images are being grabbed.")
    succeeded_grabs = 0
    accumulator = np.zeros(width, dtype=np.float64)

    while camera.IsGrabbing():
        with camera.RetrieveResult(
            5000, pylon.TimeoutHandling_ThrowException
        ) as grab_result:
            if grab_result.GrabSucceeded():
                # Some camera models use a GenICam Generic Data Container (GenDC) format.
                # For single grabbed images, a data component is emulated automatically.
                # pylon provides a data component wrapper to handle both cases uniformly.
                with grab_result.GetFirstImageDataComponent() as image_data_component:
                    image = image_data_component.Array
                    # image shape: (height, width) for Mono8
                    column_sums = image.astype(np.float64).sum(axis=0)
                    accumulator += column_sums
                    succeeded_grabs += 1
            else:
                print(
                    "Error:",
                    f"{grab_result.ErrorCode:#x}",
                    grab_result.ErrorDescription
                )

    if succeeded_grabs == 0:
        raise pylon.RuntimeException("No images were grabbed successfully.")

    # Division by succeeded_grabs is necessary because we summed the pixel values.
    # Division by height is necessary for mean pixel value per column.
    mean_of_columns = accumulator / (succeeded_grabs * height)
    mean_pixel_value = float(mean_of_columns.mean())

    return mean_pixel_value, mean_of_columns


def find_boost_camera():
    """Search for an FFC-compatible boost camera on a CXP transport layer."""
    tl_factory = pylon.TlFactory.GetInstance()

    for device_info in tl_factory.EnumerateDevices():
        model = device_info.ModelName
        if model in SUPPORTED_MODELS:
            camera = pylon.InstantCamera(tl_factory.CreateDevice(device_info))
            print(f"Starting FFC with device: {model} ({device_info.SerialNumber})")
            return camera

    return None


try:
    camera = find_boost_camera()
    if camera is None:
        print("Couldn't find any FFC-compatible CXP device.")
        print("Supported models:", ", ".join(sorted(SUPPORTED_MODELS)))
        sys.exit(1)

    # The context manager ensures the camera is closed even if an exception occurs.
    with camera:
        print("Using device:", camera.DeviceInfo.ModelName)

        # FFC works only with Mono8 images.
        camera.PixelFormat.TrySetValue("Mono8")
        camera.OffsetX.TrySetToMinimum()
        camera.Width.TrySetToMaximum()
        camera.OffsetY.TrySetToMinimum()
        camera.Height.TrySetToMaximum()

        width = camera.Width.Value
        height = camera.Height.Value

        print(f"Pixel format: {camera.PixelFormat.Value}")
        print(f"Image width: {width}")
        print(f"Image height: {height}")

        exposure_min = camera.ExposureTime.Min
        exposure_max = camera.ExposureTime.Max

        # --- Dark images ---
        dark_exposure = float(input(
            f"Enter a valid exposure time between {exposure_min:.1f} and "
            f"{exposure_max:.1f} [us] for a dark image: "
        ))
        print(f"Exposure time for dark image is: {dark_exposure:.1f} us")
        camera.ExposureTime.SetValue(dark_exposure, pylon.FloatValueCorrection_ClipToRange)

        # dx: mean values over every column (height) for dark images.
        # d_mean: mean pixel value over all dark images.
        d_mean, dx = process_images(camera, width, height)

        # --- Bright images ---
        bright_exposure = float(input(
            f"Enter a valid exposure time between {exposure_min:.1f} and "
            f"{exposure_max:.1f} [us] for a bright image: "
        ))
        print(f"Exposure time for bright image is: {bright_exposure:.1f} us")
        camera.ExposureTime.SetValue(bright_exposure, pylon.FloatValueCorrection_ClipToRange)

        # gx: mean values over every column (height) for bright images.
        # g_mean: mean pixel value over all bright images.
        g_mean, gx = process_images(camera, width, height)

        # --- Quality checks ---
        if d_mean > 40.0:
            print("It looks like the mean dark image isn't dark enough because "
                  "the dmean value is a little bit high.")
        if g_mean < 150.0:
            print("It looks like the mean bright image is too dark because "
                  "the gmean value is a little bit low.")
        if g_mean > 210.0:
            print("It looks like the mean bright image is too bright because "
                  "the gmean value is a little bit high.")

        # --- Calculate Dark Signal Non-Uniformity (DSNU) coefficients ---
        dsnu_coefficients = np.clip(np.round(dx).astype(np.int64), 0, 127).astype(np.uint8)

        # --- Calculate Photo Response Non-Uniformity (PRNU) coefficients ---
        prnu_raw = 128.0 * g_mean / (gx - dx + 1.0)
        prnu_coefficients = np.clip(np.round(prnu_raw).astype(np.int64), 0, 511).astype(np.uint16)

        # --- Write coefficients to camera ---
        print(f"\nWriting {width} DSNU/PRNU coefficients to camera...")
        for i in range(width):
            camera.BslFlatFieldCorrectionCoeffX.SetValue(
                i, pylon.IntegerValueCorrection_Nearest
            )
            camera.BslFlatFieldCorrectionCoeffDSNU.SetValue(
                int(dsnu_coefficients[i]), pylon.IntegerValueCorrection_Nearest
            )
            camera.BslFlatFieldCorrectionCoeffPRNU.SetValue(
                int(prnu_coefficients[i]), pylon.IntegerValueCorrection_Nearest
            )

        # Save mean dark pixel value.
        d_mean_clamped = int(np.clip(round(d_mean), 0, 127))
        camera.BslFlatFieldCorrectionDMean.Value = d_mean_clamped

        # Save to flash memory.
        camera.BslFlatFieldCorrectionSaveToFlash.Execute()
        print("FFC coefficients saved to flash memory.")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
