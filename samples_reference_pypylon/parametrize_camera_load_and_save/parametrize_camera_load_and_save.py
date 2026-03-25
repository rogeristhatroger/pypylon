#!/usr/bin/env python3
"""\
Save and load the camera feature node map to or from a .pfs (Pylon Feature Stream) file.

FeaturePersistence writes the opened device's parameters to disk and can read them
back into the node map; loading with validation checks that stored values apply.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to CreateFirstDevice: https://docs.baslerweb.com/camera-emulation
"""
import sys

from pypylon import pylon

# The name of the pylon feature stream file (same basename as the C++ sample).
FILENAME = "NodeMap.pfs"

exit_code = 0

try:
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    print("Using device:", camera.GetDeviceInfo().GetModelName())
    print()

    camera.Open()

    print("Saving camera's node map to file...")
    pylon.FeaturePersistence.Save(FILENAME, camera.NodeMap)

    print("Reading file back to camera's node map...")
    pylon.FeaturePersistence.Load(FILENAME, camera.NodeMap, True)

    camera.Close()

except BaseException as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
