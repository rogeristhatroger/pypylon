#!/usr/bin/env python3
"""\
Demonstrate sequencer-driven image acquisition with three different image heights.

This sample shows how to grab images using the sequencer feature of a camera.
Three sequence sets are used for image acquisition. Each sequence set
uses a different image height.

If the camera does not expose sequencer nodes, the sample prints a message and
exits cleanly.
"""
import sys
from pypylon import pylon

COUNT_OF_IMAGES_TO_GRAB = 10
TRIGGER_READY_TIMEOUT_MS = 1000
RETRIEVE_TIMEOUT_MS = 5000

exit_code = 0
try:
    with pylon.InstantCamera() as camera:

        camera.Attach(pylon.FirstFound)

        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        # Register the standard configuration event handler for enabling software
        # triggering. The software trigger configuration handler replaces the
        # default configuration as all currently registered configuration handlers
        # are removed by setting the registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration(
            pylon.SoftwareTriggerConfiguration(),
            pylon.RegistrationMode_ReplaceAll,
            pylon.Cleanup_Delete
        )

        camera.Open()

        use_sfnc2 = camera.SequencerMode.IsWritable()
        use_sfnc1 = not use_sfnc2 and camera.SequenceEnable.IsWritable()

        if not use_sfnc2 and not use_sfnc1:
            print("The sequencer feature is not available for this camera.")
            sys.exit(0)

        if use_sfnc2:
            # Cameras based on SFNC 2.0 or later, e.g., USB cameras

            # Disable the sequencer before changing parameters. The parameters under
            # control of the sequencer are locked when the sequencer is enabled.
            camera.SequencerMode.Value = "Off"
            camera.SequencerConfigurationMode.Value = "Off"

            # Maximize the grabbed image area of interest (Image AOI).
            camera.OffsetX.TrySetToMinimum()
            camera.OffsetY.TrySetToMinimum()
            camera.Width.SetToMaximum()
            camera.Height.SetToMaximum()

            # Set the pixel data format.
            # This parameter may be locked when the sequencer is enabled.
            camera.PixelFormat.TrySetValue("Mono8")

            # Set up sequence sets and turn sequencer configuration mode on.
            camera.SequencerConfigurationMode.Value = "On"

            initial_set = camera.SequencerSetSelector.Min
            inc_set = camera.SequencerSetSelector.Inc
            current_set = initial_set

            # Set the parameters for step 0; quarter height image.
            camera.SequencerSetSelector.Value = initial_set
            # Reset on software signal 1.
            camera.SequencerPathSelector.Value = 0
            camera.SequencerSetNext.Value = initial_set
            camera.SequencerTriggerSource.Value = "SoftwareSignal1"
            # Advance on Frame Start or Exposure Start (depends on camera family).
            camera.SequencerPathSelector.Value = 1
            if not camera.SequencerTriggerSource.TrySetValue("FrameStart"):
                camera.SequencerTriggerSource.Value = "ExposureStart"

            camera.SequencerSetNext.Value = current_set + inc_set
            camera.Height.SetValuePercentOfRange(25.0)
            camera.SequencerSetSave.Execute()

            # Set the parameters for step 1; half height image.
            current_set += inc_set
            camera.SequencerSetSelector.Value = current_set
            camera.SequencerSetNext.Value = current_set + inc_set
            camera.Height.SetValuePercentOfRange(50.0)
            camera.SequencerSetSave.Execute()

            # Set the parameters for step 2; full height image.
            current_set += inc_set
            camera.SequencerSetSelector.Value = current_set
            camera.SequencerSetNext.Value = initial_set
            camera.Height.SetValuePercentOfRange(100.0)
            camera.SequencerSetSave.Execute()

            # Enable the sequencer feature.
            # From here on you can't change the sequencer settings anymore.
            camera.SequencerConfigurationMode.Value = "Off"
            camera.SequencerMode.Value = "On"
        else:
            # Disable the sequencer before changing parameters. The parameters under
            # control of the sequencer are locked when the sequencer is enabled.
            camera.SequenceEnable.Value = False
            # Turn configuration mode off if available. Not supported by all cameras.
            camera.SequenceConfigurationMode.TrySetValue("Off")

            # Maximize the grabbed image area of interest (Image AOI).
            camera.OffsetX.TrySetToMinimum()
            camera.OffsetY.TrySetToMinimum()
            camera.Width.SetToMaximum()
            camera.Height.SetToMaximum()

            # Set the pixel data format.
            camera.PixelFormat.TrySetValue("Mono8")

            # Turn configuration mode on if available. Not supported by all cameras.
            camera.SequenceConfigurationMode.TrySetValue("On")

            # Configure how the sequence will advance. 'Auto' refers to the auto
            # sequence advance mode. The advance from one sequence set to the next
            # will occur automatically with each image acquired. After the end of
            # the sequence set cycle was reached a new sequence set cycle will start.
            camera.SequenceAdvanceMode.Value = "Auto"

            # Our sequence sets relate to three steps (0..2).
            camera.SequenceSetTotalNumber.Value = 3

            # Set the parameters for step 0; quarter height image.
            camera.SequenceSetIndex.Value = 0
            camera.Height.SetValuePercentOfRange(25.0)
            camera.SequenceSetStore.Execute()

            # Set the parameters for step 1; half height image.
            camera.SequenceSetIndex.Value = 1
            camera.Height.SetValuePercentOfRange(50.0)
            camera.SequenceSetStore.Execute()

            # Set the parameters for step 2; full height image.
            camera.SequenceSetIndex.Value = 2
            camera.Height.SetValuePercentOfRange(100.0)
            camera.SequenceSetStore.Execute()

            # Turn configuration mode off if available.
            camera.SequenceConfigurationMode.TrySetValue("Off")

            # Enable the sequencer feature.
            # From here on you can't change the sequencer settings anymore.
            camera.SequenceEnable.Value = True

        # Start the grabbing of COUNT_OF_IMAGES_TO_GRAB images.
        camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

        # StopGrabbing is called automatically by the RetrieveResult method
        # when COUNT_OF_IMAGES_TO_GRAB images have been retrieved.
        while camera.IsGrabbing():
            # Execute the software trigger. Wait up to 1000 ms for the camera to
            # be ready for trigger.
            if camera.WaitForFrameTriggerReady(
                TRIGGER_READY_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
            ):
                camera.ExecuteSoftwareTrigger()

                # Wait for an image and then retrieve it.
                with camera.RetrieveResult(
                    RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
                ) as grab_result:
                    if grab_result.GrabSucceeded():
                        # Some camera models use a GenICam Generic Data Container (GenDC) format.
                        # For single grabbed images, a data component is emulated automatically.
                        # pylon provides a data component wrapper to handle both cases uniformly.
                        with grab_result.GetFirstImageDataComponent() as image_data_component:
                            pylon.DisplayImage(1, image_data_component)

                            img = image_data_component.Array
                            print(f"SizeX: {image_data_component.Width}; SizeY: {image_data_component.Height}; "
                                  f"Gray value of first pixel: {img[0, 0]}")
                    else:
                        print("Error:", f"{grab_result.ErrorCode:#x}", grab_result.ErrorDescription)

        # Disable the sequencer.
        if use_sfnc2:
            camera.SequencerMode.Value = "Off"
        else:
            camera.SequenceEnable.Value = False

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
