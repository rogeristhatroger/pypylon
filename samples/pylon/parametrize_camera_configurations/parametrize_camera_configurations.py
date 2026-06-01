#!/usr/bin/env python3
"""\
Demonstrate standard and custom configuration event handlers for an InstantCamera.

The instant camera allows to install event handlers for configuration purposes
and for handling the grab results. This is very useful for handling standard
camera setups and image processing tasks.

This sample shows how to use configuration event handlers by applying the standard
configurations and registering sample configuration event handlers.

Configuration event handlers are derived from ConfigurationEventHandler.
If the configuration event handler is registered, its methods are called when the
state of the instant camera object changes, e.g. when the camera is opened or closed.

The standard configuration event handlers override the OnOpened method. The overridden
method parametrizes the camera.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon

COUNT_OF_IMAGES_TO_GRAB = 3
TIMEOUT_MS = 5000
TRIGGER_READY_TIMEOUT_MS = 1000

exit_code = 0
camera = None


class SampleImageEventHandler(pylon.ImageEventHandler):
    """ImageEventHandler to print image dimensions for each successfully grabbed image."""

    def OnImageGrabbed(self, camera, grab_result):
        if grab_result.GrabSucceeded():
            # Some camera models use a GenICam Generic Data Container (GenDC) format.
            # For single grabbed images, a data component is emulated automatically.
            # pylon provides a data component wrapper to handle both cases uniformly.
            with grab_result.GetFirstImageDataComponent() as image_data_component:
                print(f"Image event: SizeX: {image_data_component.Width}; SizeY: {image_data_component.Height}")


class PixelFormatAndAoiConfiguration(pylon.ConfigurationEventHandler):
    """ConfigurationEventHandler to set pixel format to Mono8 and adjust the AOI on open."""

    def OnOpened(self, camera):
        camera.OffsetX.TrySetToMinimum()
        camera.OffsetY.TrySetToMinimum()
        camera.Width.SetToMaximum()
        camera.Height.SetValuePercentOfRange(50.0)
        camera.PixelFormat.TrySetValue("Mono8")


class VerboseConfigurationEventHandler(pylon.ConfigurationEventHandler):
    """ConfigurationEventHandler to print a message on camera open and close events."""

    def OnOpened(self, camera):
        print("Configuration event: camera opened.")

    def OnClosed(self, camera):
        print("Configuration event: camera closed.")


def _retrieve_one(camera):
    """Retrieve one grab result and print its dimensions and first pixel value."""
    with camera.RetrieveResult(TIMEOUT_MS, pylon.TimeoutHandling_ThrowException) as grab_result:
        if grab_result.GrabSucceeded():
            # Some camera models use a GenICam Generic Data Container (GenDC) format.
            # For single grabbed images, a data component is emulated automatically.
            # pylon provides a data component wrapper to handle both cases uniformly.
            with grab_result.GetFirstImageDataComponent() as image_data_component:
                img = image_data_component.Array
                print(f"SizeX: {image_data_component.Width}; SizeY: {image_data_component.Height}; "
                    f"Gray value of first pixel: {img[0, 0]}")
        else:
            print("Error: ", f"{grab_result.ErrorCode:#x}", grab_result.ErrorDescription)


def _grab_one_via_start(camera):
    """Start a single-image grab and retrieve the result."""
    camera.StartGrabbingMax(1)
    _retrieve_one(camera)


try:
    # Create an instant camera object with the first camera device found.
    camera = pylon.InstantCamera(pylon.FirstFound)

    print("Using device:", camera.DeviceInfo.ModelName)
    print()

    # For demonstration purposes only, register an image event handler
    # printing out information about the grabbed images.
    camera.RegisterImageEventHandler(
        SampleImageEventHandler(),
        pylon.RegistrationMode_Append,
        pylon.Cleanup_Delete,
    )

    print("Grab using continuous acquisition:")
    print()

    # Register the standard configuration event handler for setting up the camera
    # for continuous acquisition.
    # By setting the registration mode to RegistrationMode_ReplaceAll, the new
    # configuration handler replaces the default configuration handler that has been
    # automatically registered when creating the instant camera object.
    camera.RegisterConfiguration(
        pylon.AcquireContinuousConfiguration(),
        pylon.RegistrationMode_ReplaceAll,
        pylon.Cleanup_Delete,
    )

    # The camera's Open() method calls the configuration handler's OnOpened() method
    # that applies the required parameter modifications.
    camera.Open()

    # The registered configuration event handler has done its parametrization now.
    # Additional parameters could be set here.

    # Grab some images for demonstration.
    camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)
    while camera.IsGrabbing():
        _retrieve_one(camera)

    camera.Close()

    print("Grab using software trigger mode:")
    print()

    # Register the standard configuration event handler for setting up the camera
    # for software triggering.
    # The current configuration is replaced by the software trigger configuration
    # by setting the registration mode to RegistrationMode_ReplaceAll.
    camera.RegisterConfiguration(
        pylon.SoftwareTriggerConfiguration(),
        pylon.RegistrationMode_ReplaceAll,
        pylon.Cleanup_Delete,
    )

    # StartGrabbing() calls the camera's Open() automatically if the camera is
    # not open yet. The Open method calls the configuration handler's OnOpened()
    # method that sets the required parameters for enabling software triggering.
    camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)
    while camera.IsGrabbing():
        # Execute the software trigger. The call waits up to 1000 ms for the
        # camera to be ready to be triggered.
        camera.WaitForFrameTriggerReady(
            TRIGGER_READY_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
        )
        camera.ExecuteSoftwareTrigger()
        _retrieve_one(camera)

    print("Grab using single frame acquisition:")
    print()

    # Register the standard configuration event handler for configuring single
    # frame acquisition. The previous configuration is removed by setting the
    # registration mode to RegistrationMode_ReplaceAll.
    camera.RegisterConfiguration(
        pylon.AcquireSingleFrameConfiguration(),
        pylon.RegistrationMode_ReplaceAll,
        pylon.Cleanup_Delete,
    )

    # GrabOne calls StartGrabbing and StopGrabbing internally.
    # As seen above, Open() is called by StartGrabbing and the OnOpened() method
    # of the AcquireSingleFrameConfiguration handler is called.
    with camera.GrabOne(TIMEOUT_MS) as grab_result:
        pass

    # To continuously grab single images it is much more efficient to open the
    # camera before grabbing.
    # Note: The software trigger mode (see above) should be used for grabbing
    # single images if you want to maximize frame rate.
    camera.Open()

    # Now, the camera parameters are applied in the OnOpened method of the
    # configuration object. Additional parameters could be set here.

    # Grab some images for demonstration.
    for _ in range(COUNT_OF_IMAGES_TO_GRAB):
        with camera.GrabOne(TIMEOUT_MS) as grab_result:
            pass

    camera.Close()

    print("Grab using multiple configuration objects:")
    print()

    # Register the standard event handler for configuring single frame acquisition.
    camera.RegisterConfiguration(
        pylon.AcquireSingleFrameConfiguration(),
        pylon.RegistrationMode_ReplaceAll,
        pylon.Cleanup_Delete,
    )

    # Register an additional configuration handler to set the image format and
    # adjust the AOI. By setting the registration mode to RegistrationMode_Append,
    # the configuration handler is added instead of replacing the already
    # registered configuration handler.
    camera.RegisterConfiguration(
        PixelFormatAndAoiConfiguration(),
        pylon.RegistrationMode_Append,
        pylon.Cleanup_Delete,
    )

    # Register the handler object and define Cleanup_None so that it is not
    # deleted by the camera object. It must be ensured that the configuration
    # handler lives at least until the handler is deregistered.
    temp_handler = VerboseConfigurationEventHandler()
    camera.RegisterConfiguration(
        temp_handler, pylon.RegistrationMode_Append, pylon.Cleanup_None
    )

    # Grab an image for demonstration. Configuration events are printed.
    print("Grab, configuration events are printed:")
    print()
    _grab_one_via_start(camera)

    # Deregister the event handler.
    camera.DeregisterConfiguration(temp_handler)

    # Grab an image for demonstration. Configuration events are not printed.
    print()
    print("Grab, configuration events are not printed:")
    print()
    _grab_one_via_start(camera)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1
finally:
    if camera is not None:
        camera.Close()

sys.exit(exit_code)
