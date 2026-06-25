#!/usr/bin/env python3
"""\
Trigger simultaneous image acquisition on multiple GigE cameras via ACTION_CMD.

An action command lets you trigger several GigE Vision cameras at the same
time, rather than sending software triggers one by one. This sample uses
InstantCameraArray together with ActionTriggerConfiguration to set up the
cameras, then issues an action command through the GigE transport layer.

This sample requires at least one (preferably two) GigE Vision cameras on
the same subnet. Only GigE cameras support action commands.
"""
import sys
import random
from pypylon import pylon

# Limits the amount of cameras used for grabbing.
# It is important to manage the available bandwidth when grabbing with multiple
# cameras. This applies, for instance, if two GigE cameras are connected to the
# same network adapter via a switch. To manage the bandwidth, the GevSCPD
# interpacket delay parameter and the GevSCFTD transmission delay parameter can
# be set for each GigE camera device.
MAX_CAMERAS_TO_USE = 2

RETRIEVE_TIMEOUT_MS = 5000

exit_code = 0
try:
    tl_factory = pylon.TlFactory.GetInstance()

    # Get the GigE transport layer.
    # We'll need it later to issue the action commands.
    with tl_factory.TransportLayer("BaslerGigE") as gige_tl:
        if gige_tl is None:
            print("GigE transport layer not found. Please make sure the pylon GigE transport layer is installed.")
            sys.exit(1)

        # Enumerate only GigE cameras.
        all_device_infos = gige_tl.EnumerateDevices()
        if not all_device_infos:
            raise pylon.RuntimeException("No GigE cameras present.")

        # Only use cameras in the same subnet as the first one.
        first_subnet = all_device_infos[0].SubnetAddress
        usable_device_infos = [all_device_infos[0]]
        for info in all_device_infos[1:]:
            if len(usable_device_infos) >= MAX_CAMERAS_TO_USE:
                break
            if info.SubnetAddress == first_subnet:
                usable_device_infos.append(info)
            else:
                print(
                    "Camera will not be used because it is in a different subnet:",
                    info.SubnetAddress
                )

        # Generate a random device key and a fixed group key.
        device_key = random.randint(0, 0xFFFFFFFF)
        group_key = 0x112233

        with pylon.InstantCameraArray(len(usable_device_infos)) as cameras:
            for i, cam in enumerate(cameras):
                cam.Attach(tl_factory.CreateDevice(usable_device_infos[i]))

                # ActionTriggerConfiguration sets DeviceKey, GroupKey, GroupMask
                # and configures the camera FrameTrigger to wait for an action
                # command.
                cam.RegisterConfiguration(
                    pylon.ActionTriggerConfiguration(
                        device_key, group_key, pylon.AllGroupMask
                    ),
                    pylon.RegistrationMode_Append,
                    pylon.Cleanup_Delete
                )

                cam.SetCameraContext(i)

                print(f"Using device    : {usable_device_infos[i].ModelName}")
                print(f"Using camera nr.: {i}")
                print(f"IP Address      : {usable_device_infos[i].IpAddress}")
                print()

            # Open all cameras — this applies the ActionTriggerConfiguration.
            cameras.Open()

            print("Issuing an action command.")

            # Start grabbing on all cameras. They won't transmit image data
            # until an action command with matching keys arrives.
            cameras.StartGrabbing()

            # Issue the action command to all devices on the subnet.
            # The devices with a matching DeviceKey, GroupKey and valid
            # GroupMask will grab an image.
            action_command = gige_tl.ActionCommand(
                device_key, group_key, pylon.AllGroupMask, first_subnet
            )
            action_command.IssueNoWait()

            # Retrieve one image per camera.
            for _ in range(len(usable_device_infos)):
                if not cameras.IsGrabbing():
                    break

                # RetrieveResult will return grab results in the order they
                # arrive.
                with cameras.RetrieveResult(
                    RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
                ) as grab_result:
                    # When the cameras in the array are created the camera
                    # context value is set to the index of the camera in the
                    # array. The camera context is a user-settable value.
                    # This value is attached to each grab result and can be
                    # used to determine the camera that produced the grab
                    # result.
                    camera_index = grab_result.GetCameraContext()

                    if grab_result.GrabSucceeded():
                        camera_info = cameras[camera_index].DeviceInfo
                        print(
                            f"Camera {camera_index}: "
                            f"{camera_info.ModelName} "
                            f"({camera_info.IpAddress})"
                        )

                        # Some camera models use a GenICam Generic Data Container (GenDC) format.
                        # For single grabbed images, a data component is emulated automatically.
                        # pylon provides a data component wrapper to handle both cases uniformly.
                        with grab_result.GetFirstImageDataComponent() as image_data_component:
                            # DisplayImage supports up to 32 image windows.
                            if camera_index <= 31:
                                pylon.DisplayImage(camera_index, image_data_component)

                            img = image_data_component.Array
                            print(f"GrabSucceeded: {grab_result.GrabSucceeded()}")
                            print(f"Gray value of first pixel: {img[0, 0]}")
                        print()
                    else:
                        # If a buffer has been incompletely grabbed, the
                        # network bandwidth is possibly insufficient for
                        # transferring multiple images simultaneously.
                        # See note above MAX_CAMERAS_TO_USE.
                        print(
                            "Error:",
                            f"{grab_result.ErrorCode:#x}",
                            grab_result.ErrorDescription
                        )

            # In case you want to trigger again you should wait for the camera
            # to become trigger-ready before issuing the next action command.
            # To avoid overtriggering you should call
            # cameras[0].WaitForFrameTriggerReady
            # (see grab_using_grab_loop_thread sample for details).

            cameras.StopGrabbing()

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
