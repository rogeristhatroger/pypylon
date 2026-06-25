#!/usr/bin/env python3
"""\
Mimic the 'Automatic Image Adjustment' button of the pylon Viewer.

This sample configures a camera for optimum image quality under current
lighting conditions by enabling the auto gain, auto exposure, and auto
white-balance functions in "once" mode. After the auto functions have
converged, the camera parameters remain at the automatically determined
values.

The procedure handles both SFNC 1.x (typically GigE cameras) and
SFNC 2.0+ (typically USB cameras) parameter naming conventions.

Steps performed:
  1. Set a compatible pixel format (color preferred, mono as fallback).
  2. Disable the test image generator.
  3. Configure the Auto Function ROI to cover the full sensor area.
  4. Set auto-adjustment parameters (gamma, target brightness, gain and
     exposure limits, auto-function profile).
  5. Enable GainAuto, ExposureAuto, and BalanceWhiteAuto in "Once" mode.
  6. Grab 20 images so the auto functions can analyse and converge.
"""
import sys
from pypylon import pylon

COUNT_OF_IMAGES_TO_GRAB = 20
RETRIEVE_TIMEOUT_MS = 5000
MAX_AUTO_EXPOSURE_TIME_US = 1_000_000


def set_compatible_pixel_format(camera):
    """Set one of several pixel formats compatible with auto functions.

    Tries color-capable formats first and falls back to Mono8.
    """
    compatible_formats = [
        "YUV422_YUYV_Packed",
        "YCbCr422_8",
        "BayerBG8",
        "BayerRG8",
        "BayerGR8",
        "BayerGB8",
        "Mono8",
    ]
    if not camera.PixelFormat.TrySetValue(compatible_formats):
        print("  Could not set a compatible pixel format.")


def disable_test_image(camera):
    """Disable the test image generator if available."""
    camera.TestImageSelector.TrySetValue("Off")
    camera.TestPattern.TrySetValue("Off")


def configure_auto_function_roi_sfnc1(camera):
    """Configure Auto Function AOI for SFNC 1.x cameras."""
    if not camera.AutoFunctionAOISelector.IsWritable():
        return

    camera.AutoFunctionAOISelector.SetValue("AOI1")
    camera.AutoFunctionAOIUsageIntensity.TrySetValue(True)
    camera.AutoFunctionAOIUsageWhiteBalance.TrySetValue(True)
    camera.AutoFunctionAOIOffsetX.SetToMinimum()
    camera.AutoFunctionAOIOffsetY.SetToMinimum()
    camera.AutoFunctionAOIWidth.SetToMaximum()
    camera.AutoFunctionAOIHeight.SetToMaximum()


def configure_auto_function_roi_sfnc2(camera):
    """Configure Auto Function ROI for SFNC 2.0+ cameras."""
    if not camera.AutoFunctionROISelector.IsWritable():
        return

    camera.AutoFunctionROISelector.SetValue("ROI1")
    camera.AutoFunctionROIUseBrightness.TrySetValue(True)
    camera.AutoFunctionROIUseWhiteBalance.TrySetValue(True)
    camera.AutoFunctionROIOffsetX.SetToMinimum()
    camera.AutoFunctionROIOffsetY.SetToMinimum()
    camera.AutoFunctionROIWidth.SetToMaximum()
    camera.AutoFunctionROIHeight.SetToMaximum()


def configure_auto_parameters_sfnc1(camera):
    """Set auto-adjustment limits and profile for SFNC 1.x cameras."""
    camera.ProcessedRawEnable.TrySetValue(True)
    camera.GammaEnable.TrySetValue(True)
    camera.GammaSelector.TrySetValue("sRGB")
    camera.AutoTargetValue.TrySetValue(80)
    camera.AutoFunctionProfile.TrySetValue("GainMinimum")
    camera.AutoGainRawLowerLimit.TrySetToMinimum()
    camera.AutoGainRawUpperLimit.TrySetToMaximum()
    camera.AutoExposureTimeAbsLowerLimit.TrySetToMinimum()
    camera.AutoExposureTimeAbsUpperLimit.TrySetToMaximum()


def configure_auto_parameters_sfnc2(camera):
    """Set auto-adjustment limits and profile for SFNC 2.0+ cameras."""
    camera.AutoTargetBrightness.TrySetValue(0.3)
    camera.AutoFunctionProfile.TrySetValue("MinimizeGain")
    camera.AutoGainLowerLimit.TrySetToMinimum()
    camera.AutoGainUpperLimit.TrySetToMaximum()

    if camera.AutoExposureTimeUpperLimit.IsReadable():
        upper_limit = camera.AutoExposureTimeUpperLimit.Max
        if upper_limit > MAX_AUTO_EXPOSURE_TIME_US:
            upper_limit = MAX_AUTO_EXPOSURE_TIME_US
        camera.AutoExposureTimeUpperLimit.TrySetValue(upper_limit)


def enable_auto_functions(camera):
    """Enable gain, exposure, and white-balance auto functions in 'Once' mode."""
    camera.GainSelector.TrySetValue("All")
    camera.GainAuto.TrySetValue("Once")
    camera.ExposureAuto.TrySetValue("Once")
    camera.BalanceWhiteAuto.TrySetValue("Once")

    if camera.GetSfncVersion() < pylon.Sfnc_2_0_0:
        camera.LightSourceSelector.TrySetValue("Daylight")
    else:
        camera.LightSourcePreset.TrySetValue("Daylight5000K")


exit_code = 0
try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        is_sfnc2 = camera.GetSfncVersion() >= pylon.Sfnc_2_0_0

        # 1. Set a compatible pixel format.
        print("Setting a compatible pixel format.")
        set_compatible_pixel_format(camera)

        # 2. Disable test image generator.
        print("Disabling test image generator.")
        disable_test_image(camera)

        # 3. Configure the Auto Function ROI to cover the full sensor.
        print("Resetting Auto Function ROI to full sensor area.")
        if is_sfnc2:
            configure_auto_function_roi_sfnc2(camera)
        else:
            configure_auto_function_roi_sfnc1(camera)

        # 4. Set auto-adjustment parameters.
        print("Setting acquisition parameters to automatic mode.")
        if is_sfnc2:
            configure_auto_parameters_sfnc2(camera)
        else:
            configure_auto_parameters_sfnc1(camera)

        # 5. Enable auto functions in "Once" mode.
        print("Enabling auto functions (Once).")
        enable_auto_functions(camera)

        # 6. Grab images so the auto functions can analyse and converge.
        print(f"Grabbing {COUNT_OF_IMAGES_TO_GRAB} images for auto adjustment.")
        camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

        for i in range(COUNT_OF_IMAGES_TO_GRAB):
            with camera.RetrieveResult(
                RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
            ) as grab_result:
                if grab_result.GrabSucceeded():
                    # Some camera models use a GenICam Generic Data Container (GenDC) format.
                    # For single grabbed images, a data component is emulated automatically.
                    # pylon provides a data component wrapper to handle both cases uniformly.
                    with grab_result.GetFirstImageDataComponent() as image_data_component:
                        print(
                            f"  Image {i + 1}: {image_data_component.Width}x{image_data_component.Height},"
                            f" first pixel = {image_data_component.Array.flat[0]}"
                        )
                        pylon.DisplayImage(0, image_data_component)
                else:
                    print(
                        f"  Image {i + 1} error:"
                        f" {grab_result.ErrorCode:#x}"
                        f" {grab_result.ErrorDescription}"
                    )

        camera.StopGrabbing()
        print()
        print("Automatic image adjustment complete.")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
