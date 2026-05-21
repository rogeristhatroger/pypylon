#!/usr/bin/env python3
"""\
Demonstrate how to handle region data using the Region Morphology vTool
(license required).

No camera is used in this sample. An RLE32 input region (a 10x10 pixel
block) is constructed programmatically by the script and passed to a recipe
containing a Region Morphology vTool via TriggerUpdate(). The vTool
processes the region and returns output regions with their bounding boxes
and RLE32 run-length entries.
"""
import os
import struct
import sys
from pypylon import pylon
from pypylon import pylondataprocessing

COUNT_OF_INPUT_REGION_ENTRIES = 10
REGION_ENTRY_START_X = 15
REGION_ENTRY_END_X = REGION_ENTRY_START_X + 9
REGION_ENTRY_START_Y = 21

RLE32_ENTRY_SIZE = struct.calcsize("iii")

exit_code = 0
try:
    # This object is used for collecting the output data.
    # It must be created before the recipe so that it outlives it.
    result_collector = pylondataprocessing.GenericOutputObserver()

    with pylondataprocessing.Recipe() as recipe:
        # Load the recipe file.
        this_dir = os.path.dirname(__file__)
        recipe_file = os.path.join(this_dir, "region.precipe")
        recipe.Load(recipe_file)

        # Register the helper object for receiving all output data.
        recipe.RegisterAllOutputsObserver(
            result_collector, pylon.RegistrationMode_Append
        )

        # Compute region size.
        data_size = pylondataprocessing.ComputeRegionSize(
            pylondataprocessing.RegionType_RLE32,
            COUNT_OF_INPUT_REGION_ENTRIES,
        )

        # Create region.
        input_region = pylondataprocessing.Region(
            pylondataprocessing.RegionType_RLE32,
            data_size,
            640, 480,
            REGION_ENTRY_START_X, REGION_ENTRY_START_Y,
            REGION_ENTRY_END_X - REGION_ENTRY_START_X + 1,
            COUNT_OF_INPUT_REGION_ENTRIES,
        )

        # Create region data representing a 10x10 matrix.
        # Every region entry is one horizontal run-length line.
        mem = input_region.GetMemoryView()
        for i in range(COUNT_OF_INPUT_REGION_ENTRIES):
            struct.pack_into(
                "iii", mem, i * RLE32_ENTRY_SIZE,
                REGION_ENTRY_START_X,
                REGION_ENTRY_END_X,
                i + REGION_ENTRY_START_Y,
            )

        print("Input Region:\n")
        print("Reference Height:       ", input_region.ReferenceHeight)
        print("Reference Width:        ", input_region.ReferenceWidth)
        print("Bounding Box Top Left X:", input_region.BoundingBoxTopLeftX)
        print("Bounding Box Top Left Y:", input_region.BoundingBoxTopLeftY)
        print("Bounding Box Height:    ", input_region.BoundingBoxHeight)
        print("Bounding Box Width:     ", input_region.BoundingBoxWidth)
        print("Data Size:              ", input_region.DataSize)
        print()

        # Start the processing.
        recipe.Start()

        # Trigger the recipe with the region as input data.
        region_variant = pylondataprocessing.Variant(input_region)
        recipe.TriggerUpdate({"Regions": region_variant}, 40)

        if result_collector.WaitObject.Wait(5000):
            result = result_collector.RetrieveResult()

            region_variant_array = result["Regions"]
            if not region_variant_array.HasError():
                print("Output Regions:\n")
                for index in range(region_variant_array.NumArrayValues):
                    output_region = region_variant_array[index].ToRegion()
                    print(f"Region {index}:")
                    print("  Reference Height:       ",
                          output_region.ReferenceHeight)
                    print("  Reference Width:        ",
                          output_region.ReferenceWidth)
                    print("  Bounding Box Top Left X:",
                          output_region.BoundingBoxTopLeftX)
                    print("  Bounding Box Top Left Y:",
                          output_region.BoundingBoxTopLeftY)
                    print("  Bounding Box Height:    ",
                          output_region.BoundingBoxHeight)
                    print("  Bounding Box Width:     ",
                          output_region.BoundingBoxWidth)
                    print("  Data Size:              ",
                          output_region.DataSize)

                    if (output_region.RegionType
                            == pylondataprocessing.RegionType_RLE32):
                        print("  Region Entries:\n")
                        for entry in output_region.ToArray():
                            print(f"    Line:   {entry.Y}")
                            print(f"    StartX: {entry.StartX}")
                            print(f"    EndX:   {entry.EndX}")
                            print()
                    print()
            else:
                print("An error occurred during processing (pin 'Regions'):",
                      region_variant_array.ErrorDescription)
        else:
            raise RuntimeError("Result timeout")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
