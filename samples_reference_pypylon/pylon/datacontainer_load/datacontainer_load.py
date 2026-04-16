#!/usr/bin/env python3
"""\
This sample shows how to load and inspect a GenDC data container.

GenDC (Generic Data Container) is used by 3D cameras such as Basler blaze
to deliver multiple data components (e.g. range, intensity, confidence) in
a single acquisition. The sample loads a pre-recorded .gendc file, prints
metadata for each component, and displays displayable components using
pylon.DisplayImage.

This sample does not require camera hardware; it operates on a .gendc file
shipped in the samples_reference_pypylon/images/3d/ directory.
"""
import os
import sys
from pypylon import pylon

# Path to the pre-recorded GenDC file relative to this script.
GENDC_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "images", "3d", "little_boxes.gendc"
)

exit_code = 0
try:
    pylon_data_container = pylon.PylonDataContainer()
    pylon_data_container.Load(GENDC_FILE)

    print("Component count:", pylon_data_container.DataComponentCount)
    print()

    # Iterate all data components in the container.
    for index in range(pylon_data_container.DataComponentCount):
        # The context manager releases the component automatically.
        with pylon_data_container.GetDataComponentByIndex(index) as component:
            print(f"Component {index}")
            print(f"  ComponentType : {component.ComponentType}")
            print(f"  PixelType     : {component.PixelType}")
            print(f"  SizeX         : {component.Width}")
            print(f"  SizeY         : {component.Height}")
            print(f"  OffsetX       : {component.OffsetX}")
            print(f"  OffsetY       : {component.OffsetY}")
            print(f"  PaddingX      : {component.PaddingX}")
            print(f"  DataSize      : {component.DataSize}")
            print(f"  TimeStamp     : {component.TimeStamp}")

            print(f"  First pixel   : {component.Array[0, 0]}")

            # Coord3D_ABC32f contains 3D point cloud data that cannot be
            # rendered as a 2D image; skip it for display.
            if component.PixelType != pylon.PixelType_Coord3D_ABC32f:
                pylon.DisplayImage(index, component)

            print()

    pylon_data_container.Release()

    try:
        input("Press Enter to exit ...")
    except EOFError:
        pass

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
