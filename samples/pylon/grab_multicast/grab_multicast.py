#!/usr/bin/env python3
"""\
Open a GigE camera in multicast mode and receive a multicast stream.

Two instances of this sample must be started on different computers. The
first, started in control mode, has full access to the GigE camera. The
second, started in monitor mode, cannot control the camera but does receive
multicast stream data.

To try the sample:
  1. Start the sample on computer A in control mode first.
  2. Once it is grabbing, start the sample on computer B in monitor mode.

The mode is selected via the ``--mode`` command-line argument
(``control`` or ``monitor``). Multicast streaming requires a real GigE
Vision camera; the Basler Camera Emulation transport layer does not
support it.
"""
import argparse
import sys
from pypylon import pylon


class SampleImageEventHandler(pylon.ImageEventHandler):
    """Print the size of every grabbed image."""

    def OnImageGrabbed(self, camera, grab_result):
        print("SampleImageEventHandler.OnImageGrabbed called.")
        # Some camera models use a GenICam Generic Data Container (GenDC) format.
        # For single grabbed images, a data component is emulated automatically.
        # pylon provides a data component wrapper to handle both cases uniformly.
        with grab_result.GetFirstImageDataComponent() as image_data_component:
            print(f"SizeX: {image_data_component.Width}")
            print(f"SizeY: {image_data_component.Height}")


COUNT_OF_IMAGES_TO_GRAB = 100
RETRIEVE_TIMEOUT_MS = 5000

# Select control vs. monitor mode from the command line so the sample can be
# launched non-interactively on both hosts involved in a multicast session.
parser = argparse.ArgumentParser(description="Multicast GigE grab sample.")
parser.add_argument(
    "--mode",
    choices=("control", "monitor"),
    default=None,
    help="Open the camera in control or monitor mode (default: control).",
)
args = parser.parse_args()
if args.mode is None:
    print(
        "No --mode argument provided, defaulting to control mode.\n"
        "Pass '--mode monitor' on a second host to receive the multicast "
        "stream from this controller."
    )
    args.mode = "control"
monitor_mode = args.mode == "monitor"
print(f"Starting in {args.mode} mode.")

exit_code = 0
try:
    # MonitorModeActive and configuration handlers must be set before Open(),
    # so construct the InstantCamera without a device and attach explicitly.
    with pylon.InstantCamera() as camera:
        if monitor_mode:
            # Register an empty configuration to replace the default one.
            # Default configuration handlers would try to write parameters
            # that are not writable on a monitor-mode (read-only) camera.
            camera.RegisterConfiguration(
                None, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None
            )
            camera.MonitorModeActive.Value = True

        camera.RegisterImageEventHandler(
            SampleImageEventHandler(),
            pylon.RegistrationMode_Append,
            pylon.Cleanup_Delete,
        )

        # Attach the first found GigE Vision camera.
        camera.Attach(
            {"DeviceClass": pylon.BaslerGigEDeviceClass}, pylon.FirstFound
        )

        print("Using device:", camera.DeviceInfo.ModelName)

        camera.MaxNumBuffer.Value = COUNT_OF_IMAGES_TO_GRAB

        camera.Open()

        if monitor_mode:
            # Select the transmission type. If the camera is already being
            # controlled by another application and is configured for
            # multicast, the active camera configuration can be reused
            # (IP address and port are picked up automatically).
            camera.StreamGrabberNodeMap.TransmissionType.Value = "UseCameraConfig"

            # Alternatively, the stream grabber can be set explicitly to
            # multicast. In that case the destination IP and port must be
            # set as well, e.g.:
            #   camera.StreamGrabberNodeMap.TransmissionType.Value = "Multicast"
            #   camera.StreamGrabberNodeMap.DestinationAddr.Value = "239.0.0.1"
            #   camera.StreamGrabberNodeMap.DestinationPort.Value = 49152

            destination_address = camera.StreamGrabberNodeMap.DestinationAddr.Value
            destination_port = camera.StreamGrabberNodeMap.DestinationPort.Value
            if destination_address == "0.0.0.0" or destination_port == 0:
                print(
                    "Failed to open stream grabber (monitor mode): the "
                    "controlling application has not started acquisition yet."
                )
                print(
                    "Start the controlling application before the monitor "
                    "application."
                )
                sys.exit(0)
        else:
            # In control mode, configure the camera and the stream for
            # multicast. The default destination IP address and port are
            # used (239.0.0.1 and 49152).
            camera.StreamGrabberNodeMap.TransmissionType.Value = "Multicast"

            # Maximize the image area of interest (Image AOI).
            camera.OffsetX.TrySetToMinimum()
            camera.OffsetY.TrySetToMinimum()
            camera.Width.TrySetToMaximum()
            camera.Height.TrySetToMaximum()

            camera.PixelFormat.Value = "Mono8"

        # Start the grabbing of COUNT_OF_IMAGES_TO_GRAB images.
        camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

        # StopGrabbing() is called automatically by RetrieveResult() when
        # COUNT_OF_IMAGES_TO_GRAB images have been retrieved.
        while camera.IsGrabbing():
            # Wait for an image and retrieve it. The image is handled by
            # the registered image event handler.
            with camera.RetrieveResult(
                RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
            ) as grab_result:
                pass

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
