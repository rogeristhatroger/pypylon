#!/usr/bin/env python3
"""\
This sample illustrates how to use the Auto Functions feature of Basler cameras.

The sample demonstrates gain, exposure, and white-balance auto functions in
"Once" and "Continuous" modes. It supports both SFNC 1.x and SFNC 2.0+
parameter naming where required.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""

import os
import sys
from pypylon import pylon

# Constants for auto functions configuration
COUNT_OF_IMAGES_TO_GRAB = 20
RETRIEVE_TIMEOUT_MS = 5000

# Set the exposure time ranges for luminance control.
# Some cameras have a very high upper limit.
# To avoid excessive execution times of the sample, we use 1000000 us (1 s) as the upper limit.
# If you need longer exposure times, you can set this to the maximum value.
MAX_AUTO_EXPOSURE_TIME_US = 1_000_000

# Target value for luminance control on SFNC2 based cameras:
# A value of 0.3 means that the target brightness is 30 % of the maximum brightness of the raw pixel value read out
# from the sensor.
# A value of 0.4 means 40 % and so forth.
TARGET_BRIGHTNESS_SFNC2 = 0.3
# Target value for luminance control on SFNC1 based cameras:
# The value is always expressed as an 8 bit value regardless of the current pixel data output format,
# i.e., 0 -> black, 255 -> white.
TARGET_BRIGHTNESS_SFNC1 = 80

MAX_ONCE_FRAMES = 100
DISPLAY_WINDOW_ID = 1


def is_debugger_attached():
    """Return True when running under an attached debugger."""
    # PyDev/PyCharm can run with a debugger even when gettrace() is not reliable.
    return (
        sys.gettrace() is not None
        or "pydevd" in sys.modules
        or "pydevd_pycharm" in sys.modules
        or os.environ.get("PYCHARM_HOSTED") == "1"
    )


def maximize_image_aoi(camera):
    """Maximize the grabbed image area when parameters are available."""
    camera.OffsetX.TrySetToMinimum()
    camera.OffsetY.TrySetToMinimum()
    camera.Width.TrySetToMaximum()
    camera.Height.TrySetToMaximum()


def configure_auto_function_brightness_roi(camera):
    """Configure ROI/AOI used for luminance statistics."""
    if camera.AutoFunctionROISelector.IsWritable():
        camera.AutoFunctionROISelector.Value = "ROI1"
        camera.AutoFunctionROIUseBrightness.TrySetValue(True)
        camera.AutoFunctionROISelector.Value = "ROI2"
        camera.AutoFunctionROIUseBrightness.TrySetValue(False)

        camera.AutoFunctionROISelector.Value = "ROI1"
        camera.AutoFunctionROIOffsetX.TrySetToMinimum()
        camera.AutoFunctionROIOffsetY.TrySetToMinimum()
        camera.AutoFunctionROIWidth.TrySetToMaximum()
        camera.AutoFunctionROIHeight.TrySetToMaximum()
    elif camera.AutoFunctionAOISelector.IsWritable():
        camera.AutoFunctionAOISelector.Value = "AOI1"
        camera.AutoFunctionAOIOffsetX.TrySetToMinimum()
        camera.AutoFunctionAOIOffsetY.TrySetToMinimum()
        camera.AutoFunctionAOIWidth.TrySetToMaximum()
        camera.AutoFunctionAOIHeight.TrySetToMaximum()


def configure_auto_function_white_balance_roi(camera):
    """Configure ROI/AOI used for white-balance statistics."""
    if camera.AutoFunctionROISelector.IsWritable():
        camera.AutoFunctionROISelector.Value = "ROI1"
        camera.AutoFunctionROIUseWhiteBalance.TrySetValue(False)
        camera.AutoFunctionROISelector.Value = "ROI2"
        camera.AutoFunctionROIUseWhiteBalance.TrySetValue(True)

        camera.AutoFunctionROISelector.Value = "ROI2"
        camera.AutoFunctionROIOffsetX.TrySetToMinimum()
        camera.AutoFunctionROIOffsetY.TrySetToMinimum()
        camera.AutoFunctionROIWidth.TrySetToMaximum()
        camera.AutoFunctionROIHeight.TrySetToMaximum()
    elif camera.AutoFunctionAOISelector.IsWritable():
        camera.AutoFunctionAOISelector.Value = "AOI1"
        camera.AutoFunctionAOIOffsetX.TrySetToMinimum()
        camera.AutoFunctionAOIOffsetY.TrySetToMinimum()
        camera.AutoFunctionAOIWidth.TrySetToMaximum()
        camera.AutoFunctionAOIHeight.TrySetToMaximum()


def configure_target_brightness(camera):
    """Set brightness target according to SFNC version."""
    if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
        camera.AutoTargetBrightness.TrySetValue(TARGET_BRIGHTNESS_SFNC2)
    else:
        camera.AutoTargetValue.TrySetValue(TARGET_BRIGHTNESS_SFNC1)


def get_parameter_unit(parameter, default_unit=""):
    """Return the engineering unit of a GenICam parameter when available."""
    try:
        unit = parameter.GetUnit()
    except:
        try:
            unit = parameter.Unit
        except:
            unit = ""

    if unit:
        return unit
    return default_unit


def is_color_camera(camera):
    """Return True when at least one Bayer pixel format is settable."""
    for pixel_format in camera.PixelFormat.GetSettableValues():
        if "Bayer" in pixel_format:
            return True
    return False


def retrieve_one_result(camera):
    """Retrieve one image to drive the auto-function state machine."""
    with camera.RetrieveResult(
        RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
    ) as grab_result:
        if grab_result.GrabSucceeded():
            if not is_debugger_attached():
                pylon.DisplayImage(DISPLAY_WINDOW_ID, grab_result)
                # For demonstration purposes only. Wait until the image is shown.
                pylon.WaitObject().Sleep(100)
        else:
            print(
                "Grab failed:",
                f"{grab_result.ErrorCode:#x}",
                grab_result.ErrorDescription,
            )


def auto_gain_once(camera):
    """Execute AutoGain in 'Once' mode until convergence."""
    if not camera.GainAuto.IsWritable():
        print("The camera does not support Gain Auto.")
        return

    maximize_image_aoi(camera)
    configure_auto_function_brightness_roi(camera)
    configure_target_brightness(camera)

    print("Trying 'GainAuto = Once'.")
    if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0: #Cameras based on SFNC 2.0 or later, e.g., USB cameras
        print("Initial Gain =", camera.Gain.GetValueOrDefault(0.0))
        camera.AutoGainLowerLimit.TrySetToMinimum()
        camera.AutoGainUpperLimit.TrySetToMaximum()
    else:
        print("Initial Gain =", camera.GainRaw.GetValueOrDefault(0))
        camera.AutoGainRawLowerLimit.TrySetToMinimum()
        camera.AutoGainRawUpperLimit.TrySetToMaximum()

    camera.GainAuto.Value = "Once"

    frame_count = 0
    while camera.GainAuto.GetValueOrDefault("Off") != "Off":
        retrieve_one_result(camera)
        frame_count += 1
        if frame_count > MAX_ONCE_FRAMES:
            raise TimeoutError("The adjustment of auto gain did not finish.")

    print("GainAuto went back to 'Off' after", frame_count, "frames.")
    if camera.Gain.IsReadable():
        print("Final Gain =", camera.Gain.GetValueOrDefault(0.0))
    else:
        print("Final Gain =", camera.GainRaw.GetValueOrDefault(0))
    print()


def auto_gain_continuous(camera):
    """Execute AutoGain in 'Continuous' mode while grabbing."""
    if not camera.GainAuto.IsWritable():
        print("The camera does not support Gain Auto.")
        return

    maximize_image_aoi(camera)
    configure_auto_function_brightness_roi(camera)
    configure_target_brightness(camera)

    print("Trying 'GainAuto = Continuous'.")
    if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0: # Cameras based on SFNC 2.0 or later, e.g., USB cameras
        print("Initial Gain =", camera.Gain.GetValueOrDefault(0.0))
    else:
        print("Initial Gain =", camera.GainRaw.GetValueOrDefault(0))

    camera.GainAuto.Value = "Continuous"

    for _ in range(COUNT_OF_IMAGES_TO_GRAB):
        retrieve_one_result(camera)

    camera.GainAuto.Value = "Off"

    if camera.Gain.IsReadable():
        print("Final Gain =", camera.Gain.GetValueOrDefault(0.0))
    else:
        print("Final Gain =", camera.GainRaw.GetValueOrDefault(0))
    print()


def auto_exposure_once(camera):
    """Execute AutoExposure in 'Once' mode until convergence."""
    if not camera.ExposureAuto.IsWritable():
        print("The camera does not support Exposure Auto.")
        return

    maximize_image_aoi(camera)
    configure_auto_function_brightness_roi(camera)
    configure_target_brightness(camera)

    print("Trying 'ExposureAuto = Once'.")
    if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0: # Cameras based on SFNC 2.0 or later, e.g., USB cameras
        unit = get_parameter_unit(camera.ExposureTime, "us")
        print("Initial exposure time =", camera.ExposureTime.GetValueOrDefault(0), unit)
        camera.AutoExposureTimeLowerLimit.TrySetToMinimum()
        camera.AutoExposureTimeUpperLimit.SetValue(
            MAX_AUTO_EXPOSURE_TIME_US,
            pylon.FloatValueCorrection_ClipToRange,
        )
    else:
        unit = get_parameter_unit(camera.ExposureTimeAbs, "us")
        print(
            "Initial exposure time =",
            camera.ExposureTimeAbs.GetValueOrDefault(0),
            unit,
        )
        camera.AutoExposureTimeAbsLowerLimit.TrySetToMinimum()
        camera.AutoExposureTimeAbsUpperLimit.SetValue(
            MAX_AUTO_EXPOSURE_TIME_US,
            pylon.FloatValueCorrection_ClipToRange,
        )

    camera.ExposureAuto.Value = "Once"

    # Grab images until auto function converges
    frame_count = 0
    while camera.ExposureAuto.GetValueOrDefault("Off") != "Off":
        retrieve_one_result(camera)
        frame_count += 1
        if frame_count > MAX_ONCE_FRAMES:
            raise TimeoutError("The adjustment of auto exposure did not finish.")

    print("ExposureAuto went back to 'Off' after", frame_count, "frames.")
    if camera.ExposureTime.IsReadable():
        print("Final exposure time =", camera.ExposureTime.GetValueOrDefault(0), unit)
    else:
        print(
            "Final exposure time =",
            camera.ExposureTimeAbs.GetValueOrDefault(0),
            unit,
        )
    print()


def auto_exposure_continuous(camera):
    """Execute AutoExposure in 'Continuous' mode while grabbing."""
    if not camera.ExposureAuto.IsWritable():
        print("The camera does not support Exposure Auto.")
        return

    maximize_image_aoi(camera)
    configure_auto_function_brightness_roi(camera)
    configure_target_brightness(camera)

    print("Trying 'ExposureAuto = Continuous'.")
    if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0: # Cameras based on SFNC 2.0 or later, e.g., USB cameras
        unit = get_parameter_unit(camera.ExposureTime, "us")
        print("Initial exposure time =", camera.ExposureTime.GetValueOrDefault(0), unit)
    else:
        unit = get_parameter_unit(camera.ExposureTimeAbs, "us")
        print(
            "Initial exposure time =",
            camera.ExposureTimeAbs.GetValueOrDefault(0),
            unit,
        )

    camera.ExposureAuto.Value = "Continuous"

    for _ in range(COUNT_OF_IMAGES_TO_GRAB):
        retrieve_one_result(camera)

    camera.ExposureAuto.Value = "Off"

    if camera.ExposureTime.IsReadable():
        print("Final exposure time =", camera.ExposureTime.GetValueOrDefault(0), unit)
    else:
        print(
            "Final exposure time =",
            camera.ExposureTimeAbs.GetValueOrDefault(0),
            unit,
        )
    print()


def print_balance_ratio(camera, message):
    """Print red/green/blue balance ratios."""
    print(message, end=" ")
    ratio_parameter = camera.BalanceRatio if camera.BalanceRatio.IsReadable() else camera.BalanceRatioAbs

    camera.BalanceRatioSelector.Value = "Red"
    red_value = ratio_parameter.GetValueOrDefault(0)
    camera.BalanceRatioSelector.Value = "Green"
    green_value = ratio_parameter.GetValueOrDefault(0)
    camera.BalanceRatioSelector.Value = "Blue"
    blue_value = ratio_parameter.GetValueOrDefault(0)

    print(f"R = {red_value}   G = {green_value}   B = {blue_value}")


def auto_white_balance(camera):
    """Carry out white balance using BalanceWhiteAuto = Once."""
    if not camera.BalanceWhiteAuto.IsWritable():
        print("The camera does not support Balance White Auto.")
        return

    if not is_color_camera(camera):
        print("White balance auto is only available for color cameras.")
        return

    maximize_image_aoi(camera)
    configure_auto_function_white_balance_roi(camera)

    print("Trying 'BalanceWhiteAuto = Once'.")
    print_balance_ratio(camera, "Initial balance ratio:")

    camera.BalanceWhiteAuto.Value = "Once"

    frame_count = 0
    while camera.BalanceWhiteAuto.GetValueOrDefault("Off") != "Off":
        retrieve_one_result(camera)
        frame_count += 1
        if frame_count > MAX_ONCE_FRAMES:
            raise TimeoutError("The adjustment of auto white balance did not finish.")

    print("BalanceWhiteAuto went back to 'Off' after", frame_count, "frames.")
    print_balance_ratio(camera, "Final balance ratio:")
    print()


exit_code = 0
try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        camera.TestImageSelector.TrySetValue("Off")
        camera.TestPattern.TrySetValue("Off")

        if camera.DeviceScanType.GetValueOrDefault("Areascan") != "Areascan":
            print("Only area scan cameras support auto functions.")
        else:
            camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
            try:
                auto_gain_once(camera)
                auto_gain_continuous(camera)
                auto_exposure_once(camera)
                auto_exposure_continuous(camera)
                auto_white_balance(camera)
                print("Auto functions demonstration complete.")
            finally:
                camera.StopGrabbing()

except Exception as e:
    print("An exception occurred:", e)
    import traceback

    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)