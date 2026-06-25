#!/usr/bin/env python3
"""\
Demonstrate programmatically creating a data processing recipe with BuildersRecipe.

Instead of loading a pre-built recipe file, a BuildersRecipe is assembled in
code: A Camera vTool and a Format Converter vTool are added, then wired
together. The sample lists available vTool types, creates outputs for both
the original and converted images, and grabs a configurable number of frames.
"""
import os
import sys

# For the sake of demonstration, enable an emulated camera device.
PYLON_CAMEMU = 1
os.environ["PYLON_CAMEMU"] = str(PYLON_CAMEMU)

from pypylon import pylon
from pypylon import pylondataprocessing

COUNT_OF_IMAGES_TO_GRAB = 10

CAMERA_VTOOL_UUID = "846bca11-6bf2-4895-88c4-fe038f5a659c"
FORMAT_CONVERTER_VTOOL_UUID = "4049ea56-3827-4faf-9478-c3ba02e4a0cb"

exit_code = 0
try:
    # This object is used for collecting the output data.
    result_collector = pylondataprocessing.GenericOutputObserver()

    # Create a new builder's recipe.
    with pylondataprocessing.BuildersRecipe() as recipe:
        # Use GetAvailableVToolTypeIDs() to retrieve a list of all available
        # vTool types.
        vtool_types = recipe.GetAvailableVToolTypeIDs()
        print("Available vTool types:")
        for type_id in vtool_types:
            display_name = recipe.GetVToolDisplayNameForTypeID(type_id)
            print(f"  Type ID: '{type_id}' : Display Name: '{display_name}'")

        # Use AddVTool to add vTools to the recipe.
        recipe.AddVTool("MyCamera", CAMERA_VTOOL_UUID)
        recipe.AddVTool("MyConverter", FORMAT_CONVERTER_VTOOL_UUID)

        # Use GetVToolIdentifiers() to retrieve a list of all vTools that are
        # currently in the recipe.
        vtool_names = recipe.GetVToolIdentifiers()
        print()
        print("vTools in recipe:")
        for name in vtool_names:
            print(f"  vTool Name '{name}' : type: '{recipe.GetVToolTypeID(name)}'")

        # Use AddOutput() to add outputs to your recipe.
        recipe.AddOutput(
            "OriginalImage", pylondataprocessing.VariantDataType_PylonImage
        )
        recipe.AddOutput(
            "ConvertedImage", pylondataprocessing.VariantDataType_PylonImage
        )

        # Use AddConnection() to create connections between vTool pins
        # and/or the inputs or outputs of the recipe.
        recipe.AddConnection(
            "camera_to_converter", "MyCamera.Image", "MyConverter.Image"
        )
        recipe.AddConnection(
            "converter_to_output", "MyConverter.Image",
            "<RecipeOutput>.ConvertedImage"
        )
        recipe.AddConnection(
            "camera_to_output", "MyCamera.Image",
            "<RecipeOutput>.OriginalImage"
        )

        # Use GetConnectionIdentifiers() to retrieve a list of all connections.
        connection_names = recipe.GetConnectionIdentifiers()
        print()
        print("Connections in recipe:")
        for name in connection_names:
            print(f"  Connection Name '{name}'")

        # Register the helper object for receiving all output data.
        recipe.RegisterAllOutputsObserver(
            result_collector, pylon.RegistrationMode_Append
        )

        # Change the output format of the image format converter.
        recipe.GetParameter(
            "MyConverter/@vTool/OutputPixelFormat"
        ).Value = "BGR8Packed"

        # Now, we can run the recipe as usual.
        recipe.Start()

        for i in range(COUNT_OF_IMAGES_TO_GRAB):
            if result_collector.WaitObject.Wait(5000):
                result = result_collector.RetrieveResult()

                variant = result["OriginalImage"]
                if not variant.HasError():
                    image = variant.ToImage()
                    print(f"OriginalImage  — SizeX: {image.Width}; SizeY: {image.Height}; "
                        f"Pixel Type: {image.PixelType}")
                    image.Release()
                else:
                    print("Error:", variant.ErrorDescription)

                variant = result["ConvertedImage"]
                if not variant.HasError():
                    image = variant.ToImage()
                    print(f"ConvertedImage — SizeX: {image.Width}; SizeY: {image.Height}; "
                        f"Pixel Type: {image.PixelType}")
                    image.Release()
                else:
                    print("Error:", variant.ErrorDescription)
            else:
                raise RuntimeError("Result timeout")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
