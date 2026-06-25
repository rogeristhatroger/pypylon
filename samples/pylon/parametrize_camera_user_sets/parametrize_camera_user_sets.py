#!/usr/bin/env python3
"""\
Demonstrate loading, saving, and restoring camera user sets.

Demonstrates how to use user configuration sets (user sets) and how to configure
the camera to start up with the user defined settings of user set 1.

You can also configure your camera using the pylon Viewer and store your custom
settings in a user set of your choice.

Note: Different camera families implement different versions of the Standard
Feature Naming Convention (SFNC). That's why the name and the type of the
parameters used can be different.

ATTENTION: Executing this sample will overwrite all current settings in user set 1.

Note: The Basler Camera Emulation does not support user sets.
"""
import sys
from pypylon import pylon

exit_code = 0
try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        # Check if the device supports user sets.
        if not camera.UserSetSelector.IsWritable():
            raise pylon.RuntimeException("The device doesn't support user sets.")

        if not camera.UserSetSelector.CanSetValue("UserSet1"):
            print("This environment exposes no writable user-set slot beyond 'Default'.")
        else:
            # Remember the current default user set selector so we can restore it later
            # when cleaning up.
            if camera.UserSetDefault.IsReadable():
                # Cameras based on SFNC 2.0 or later, e.g., USB cameras
                old_default_value = camera.UserSetDefault.Value
            else:
                old_default_value = camera.UserSetDefaultSelector.Value

            # Load default settings.
            print("Loading default settings")
            camera.UserSetSelector.Value = "Default"
            camera.UserSetLoad.Execute()

            # Set gain and exposure time values.
            # The camera won't let you set specific values when related auto functions
            # are active. So we need to disable the related auto functions before
            # setting the values.
            print("Turning off Gain Auto and Exposure Auto.")
            camera.GainAuto.TrySetValue("Off")
            camera.ExposureAuto.TrySetValue("Off")

            if camera.Gain.IsWritable():
                # Cameras based on SFNC 2.0 or later, e.g., USB cameras
                camera.Gain.SetToMinimum()
                camera.ExposureTime.SetToMinimum()
            else:
                camera.GainRaw.SetToMinimum()
                camera.ExposureTimeRaw.SetToMinimum()

            # Save to user set 1.
            #
            # ATTENTION:
            # This will overwrite all settings previously saved in user set 1.
            print("Saving currently active settings to user set 1.")
            camera.UserSetSelector.Value = "UserSet1"
            camera.UserSetSave.Execute()

            # Show default settings.
            print()
            print("Loading default settings.")
            camera.UserSetSelector.Value = "Default"
            camera.UserSetLoad.Execute()
            print("Default settings")
            print("================")
            if camera.Gain.IsReadable():
                # Cameras based on SFNC 2.0 or later, e.g., USB cameras
                print("Gain          :", camera.Gain.Value)
                print("Exposure time :", camera.ExposureTime.Value)
            else:
                print("Gain          :", camera.GainRaw.Value)
                print("Exposure time :", camera.ExposureTimeRaw.Value)

            # Show user set 1 settings.
            print()
            print("Loading user set 1 settings.")
            camera.UserSetSelector.Value = "UserSet1"
            camera.UserSetLoad.Execute()
            print("User set 1 settings")
            print("===================")
            if camera.Gain.IsReadable():
                # Cameras based on SFNC 2.0 or later, e.g., USB cameras
                print("Gain          :", camera.Gain.Value)
                print("Exposure time :", camera.ExposureTime.Value)
            else:
                print("Gain          :", camera.GainRaw.Value)
                print("Exposure time :", camera.ExposureTimeRaw.Value)

            # Set user set 1 as default user set:
            # When the camera wakes up it will be configured
            # with the settings from user set 1.
            if camera.UserSetDefault.IsWritable():
                # Cameras based on SFNC 2.0 or later, e.g., USB cameras
                camera.UserSetDefault.Value = "UserSet1"

                # Restore the default user set selector.
                camera.UserSetDefault.Value = old_default_value
            elif camera.UserSetDefaultSelector.IsWritable():
                camera.UserSetDefaultSelector.Value = "UserSet1"

                # Restore the default user set selector.
                camera.UserSetDefaultSelector.Value = old_default_value
            else:
                print("Default user-set selector nodes are not exposed in this environment.")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
