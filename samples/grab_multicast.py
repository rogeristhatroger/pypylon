#!/usr/bin/env python
"""
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pypylon API documentation.

    This sample demonstrates how to open a camera in multicast mode
    and how to receive a multicast stream.

    Two instances of this application must be started simultaneously on different computers.
    The first application started on computer A acts as the controlling application and has full access to the GigE camera.
    The second instance started on computer B opens the camera in monitor mode.
    This instance is not able to control the camera but can receive multicast streams.

    To get the sample running, start this application first on computer A in control mode.
    After computer A has begun to receive frames, start the second instance of this
    application on computer B in monitor mode.
"""
from pypylon import pylon
from pypylon import genicam

import sys

from samples.cameraeventprinter import CameraEventPrinter

# Example of an image event handler.
class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        print("CSampleImageEventHandler.OnImageGrabbed called.")
        print(f"XSize {grabResult.Width}")
        print(f"YSize {grabResult.Height}")


# Number of images to be grabbed.
COUNT_OF_IMAGES_TO_GRAB = 100

# The exit code of the sample application.
exit_code = 0

try:
    # Create an instant camera object with the GigE Vision camera device found first.
    camera_traits = {"DeviceClass":pylon.BaslerGigEDeviceClass}
    with pylon.InstantCamera() as camera:
        try:
            camera.Attach( camera_traits, pylon.FirstFound )
            camera.MaxNumBuffer.Value = COUNT_OF_IMAGES_TO_GRAB
            count = 5
            monitor_mode = None
            while count > 0:
                value = input("Start multicast sample in (c)ontrol or in (m)onitor mode? (c/m) ")
                if value in ("c","C"):
                    monitor_mode = False
                    break
                if value in ("m","M"):
                    monitor_mode = True
                    break

            if monitor_mode:
                # register an empty configuration event handler to replace the default one
                camera.RegisterConfiguration(None, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)

            camera.RegisterImageEventHandler(SampleImageEventHandler(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

            # Monitor mode selected.
            if monitor_mode:
                # Set MonitorModeActive to true to act as monitor
                camera.MonitorModeActive.Value = True

                # Open the camera.
                camera.Open()

                # Select transmission type.If the camera is already controlled by another application
                # and configured for multicast, the active camera configuration can be used
                # (IP Address and Port will be set automatically).
                camera.StreamGrabberNodeMap.TransmissionType.Value ="UseCameraConfig"

                # Alternatively, the stream grabber could be explicitly set to "multicast"...
                # In this case, the IP Address and the IP port must also be set.
                #
                # camera.GetStreamGrabberParams().TransmissionType.Value = "Multicast"
                # camera.GetStreamGrabberParams().DestinationAddr.Value = "239.0.0.1"
                # camera.GetStreamGrabberParams().DestinationPort.Value = 49152

                destination_address = camera.GetStreamGrabberNodeMap.DestinationAddr.Value
                destination_port = camera.StreamGrabberNodeMap.DestinationPort.Value
                if  destination_address != "0.0.0.0" and  destination_port != 0:
                    camera.StartGrabbing(COUNT_OF_IMAGES_TO_GRAB)
                else:
                    print("Failed to open stream grabber (monitor mode): The acquisition is not yet started by the controlling application.")
                    print("Start the controlling application before starting the monitor application")
            else:
                # Open the camera.
                camera.Open()

                # Set transmission type to "multicast"...
                # In this case, the IP Address and the IP port must also be set.

                camera.StreamGrabberNodeMap.TransmissionType.Value = "Multicast"
                # camera.GetStreamGrabberParams().DestinationAddr.Value = "239.0.0.1"    // These are default values.
                # camera.GetStreamGrabberParams().DestinationPort.Value = 49152;

                # Maximize the image area of interest (Image AOI).
                offset_x = pylon.IntegerParameter(camera.NodeMap, "OffsetX")
                offset_y = pylon.IntegerParameter(camera.NodeMap,"OffsetY")
                width = pylon.IntegerParameter(camera.NodeMap,"Width")
                height = pylon.IntegerParameter(camera.NodeMap,"Height")

                offset_x.TrySetToMinimum()
                offset_y.TrySetToMinimum()
                width.TrySetToMaximum()
                height.TrySetToMaximum()
                if (height>8192):
                    height=8192

                # Set the pixel data format.
                camera.PixelFormat.Value = "Mono8"

            camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

            # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
            # when COUNT_OF_IMAGES_TO_GRAB images have been retrieved.
            while camera.IsGrabbing():
                # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
                with camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as grab_result:
                    # image is displayed in event handler.
                    pass

        except genicam.RuntimeException:
            print("No GigE Vision camera found")

except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)

