#!/usr/bin/env python3
"""\
Save and load the camera feature node map to or from a .pfs (Pylon Feature Stream) file.

FeaturePersistence writes the opened device's parameters to disk and can read them
back into the node map; loading with validation checks that stored values apply.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon

# The name of the pylon feature stream file.
FILENAME = "NodeMap.pfs"

exit_code = 0

try:
    # Create an instant camera object with the camera device found first.
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        print("Saving camera's node map to file...")
        # Save the content of the camera's node map into the file.
        pylon.FeaturePersistence.Save(FILENAME, camera.NodeMap)

        print("Reading file back to camera's node map...")
        # Read the content of the file back to the camera's node map with enabled validation.
        pylon.FeaturePersistence.Load(FILENAME, camera.NodeMap, True)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
