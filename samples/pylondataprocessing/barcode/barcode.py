#!/usr/bin/env python3
"""\
Demonstrate the Barcode vTool with a recipe loaded from file (license required).

The recipe was created with the pylon Viewer Workbench, where it can also
be inspected and modified. It configures a Camera vTool that grabs images
from the camera emulator. Each grabbed image is passed through a Barcode
vTool which detects and decodes barcodes. The sample collects output data
(images and barcode strings) via a GenericOutputObserver.
"""
import os
import sys
from pypylon import pylon
from pypylon import pylondataprocessing

PYLON_CAMEMU = 1
os.environ["PYLON_CAMEMU"] = str(PYLON_CAMEMU)
COUNT_OF_IMAGES_TO_GRAB = 100

exit_code = 0
try:
    # This object is used for collecting the output data.
    # It must be created before the recipe so that it outlives it.
    result_collector = pylondataprocessing.GenericOutputObserver()
    
    # Create a recipe object representing a recipe file created using
    # the pylon Viewer Workbench.
    with pylondataprocessing.Recipe() as recipe:
        # Load the recipe file.
        this_dir = os.path.dirname(__file__)
        recipe_file = os.path.join(this_dir, "barcode.precipe")
        recipe.Load(recipe_file)

        # Now we allocate all resources we need. This includes the camera device.
        recipe.PreAllocateResources()

        # Set up correct image path to samples.
        samples_dir = os.path.dirname(os.path.dirname(this_dir))
        images_path = os.path.join(samples_dir, "images", "barcode")
        recipe.GetParameter(
            "MyCamera/@CameraDevice/ImageFilename"
        ).Value = images_path

        # This is where the output goes.
        recipe.RegisterAllOutputsObserver(
            result_collector, pylon.RegistrationMode_Append
        )

        # Start the processing.
        recipe.Start()

        for i in range(COUNT_OF_IMAGES_TO_GRAB):
            if result_collector.WaitObject.Wait(5000):
                result = result_collector.RetrieveResult()

                image_variant = result["Image"]
                if not image_variant.HasError():
                    image = image_variant.ToImage()
                    img = image.Array
                    print(f"SizeX: {image.Width}; SizeY: {image.Height}; "
                        f"Gray value of first pixel: {img[0, 0]}")
                    pylon.DisplayImage(1, image)
                    image.Release()
                else:
                    print("An error occurred during processing (pin 'Image'):",
                          image_variant.ErrorDescription)

                barcode_array = result["Barcodes"]
                if not barcode_array.HasError():
                    print("Barcodes:")
                    for index in range(barcode_array.NumArrayValues):
                        print(f"  {index}: {barcode_array[index].ToString()}")
                else:
                    print("An error occurred during processing (pin 'Barcodes'):",
                          barcode_array.ErrorDescription)
                print()
            else:
                raise RuntimeError("Result timeout")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
