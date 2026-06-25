#!/usr/bin/env python3
"""\
Demonstrate DSNU/PRNU shading correction on a Basler racer 2 line scan camera.

This sample creates a shading correction data set using the camera's built-in
calibration, then verifies the result by grabbing corrected images. The
BslShadingCorrection* nodes drive the entire workflow on-camera.

This sample only applies to Basler racer 2 cameras. Other cameras will print
a message and exit cleanly.

Note: The conditions for exposure (illumination, exposure time, etc.) should
be set up to deliver correct images for the correction type selected (DSNU
or PRNU). Refer to the camera documentation for guidance.
"""
import sys
import time
from pypylon import pylon

COUNT_OF_IMAGES_TO_GRAB = 5

exit_code = 0
try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        # Use continuous acquisition configuration.
        camera.RegisterConfiguration(
            pylon.AcquireContinuousConfiguration(),
            pylon.RegistrationMode_ReplaceAll,
            pylon.Cleanup_Delete
        )

        # Only line scan cameras with BslShadingCorrectionSelector support
        # this workflow.
        is_linescan = (
            camera.DeviceScanType.IsReadable()
            and camera.DeviceScanType.Value == "Linescan"
        )
        has_shading = camera.BslShadingCorrectionSelector.IsWritable()

        if not (is_linescan and has_shading):
            print("Only racer 2 line scan cameras support this shading correction workflow.")
            sys.exit(0)

        # Disable Reverse X and set ROI to maximum width.
        camera.OffsetX.TrySetToMinimum()
        camera.Width.TrySetToMaximum()
        camera.ReverseX.Value = False

        # Select DSNU shading correction in User mode, set index 1.
        camera.BslShadingCorrectionSelector.Value = "DSNU"
        camera.BslShadingCorrectionMode.Value = "User"
        camera.BslShadingCorrectionSetIndex.Value = 1

        # Start acquisition — the camera will grab 256 images internally to
        # build the shading data.
        camera.StartGrabbing()

        camera.BslShadingCorrectionSetCreate.Execute()

        print("Generating shading correction data", end="")
        while camera.BslShadingCorrectionSetCreateStatus.Value == "Active":
            print(".", end="", flush=True)
            time.sleep(0.001)
        print("done.")

        camera.StopGrabbing()

        # Verify the shading set loaded correctly.
        if camera.BslShadingCorrectionSetStatus.Value == "Ok":
            print("Successfully loaded Shading Correction")

            # Grab a few corrected images.
            camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

            while camera.IsGrabbing():
                with camera.RetrieveResult(
                    5000, pylon.TimeoutHandling_ThrowException
                ) as grab_result:
                    if grab_result.GrabSucceeded():
                        # Some camera models use a GenICam Generic Data Container (GenDC) format.
                        # For single grabbed images, a data component is emulated automatically.
                        # pylon provides a data component wrapper to handle both cases uniformly.
                        with grab_result.GetFirstImageDataComponent() as image_data_component:
                            img = image_data_component.Array
                            print(
                                f"SizeX: {image_data_component.Width}; "
                                f"SizeY: {image_data_component.Height}; "
                                f"Gray value of first pixel: {img[0, 0]}"
                            )
                            pylon.DisplayImage(1, image_data_component)
                    else:
                        print(
                            "Error:",
                            f"{grab_result.ErrorCode:#x}",
                            grab_result.ErrorDescription
                        )
        else:
            print("Shading Correction could not be loaded.")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
