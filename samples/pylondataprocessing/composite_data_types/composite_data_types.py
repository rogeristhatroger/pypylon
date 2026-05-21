#!/usr/bin/env python3
"""\
Demonstrate handling composite data types with the pylon data processing API
(no license required).

The recipe was created with the pylon Viewer Workbench, where it can also
be inspected and modified. It configures a Camera vTool and a shape-detection
vTool. The camera emulator provides images of shapes from disk. For each
image, the recipe outputs detected bounding boxes as RectangleF composite
data. The sample prints the center, width, height, and rotation of each
detected box.
"""
import os
import sys
from pypylon import pylon
from pypylon import pylondataprocessing

PYLON_CAMEMU = 1
os.environ["PYLON_CAMEMU"] = str(PYLON_CAMEMU)
COUNT_OF_IMAGES_TO_GRAB = 24

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
        recipe_file = os.path.join(
            this_dir, "composite_data_types.precipe"
        )
        recipe.Load(recipe_file)

        # Now we allocate all resources we need. This includes the camera device.
        recipe.PreAllocateResources()

        # Set up correct image path to samples.
        samples_dir = os.path.dirname(os.path.dirname(this_dir))
        images_path = os.path.join(samples_dir, "images", "shapes")
        recipe.GetParameter(
            "MyCamera/@CameraDevice/ImageFilename"
        ).SetValue(images_path)

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
                    pylon.DisplayImage(1, image)
                    image.Release()
                else:
                    print("An error occurred during processing (pin 'Image'):",
                          image_variant.ErrorDescription)

                boxes_array = result["Boxes"]
                if not boxes_array.HasError():
                    print(f"########## Image {i} ##########")
                    print()
                    boxes = boxes_array.ToData()
                    for box in boxes:
                        print(f"RectangleF {{")
                        print(f"  Center: {{")
                        print(f"    X: {box.Center.X},")
                        print(f"    Y: {box.Center.Y}")
                        print(f"  }},")
                        print(f"  Width:    {box.Width},")
                        print(f"  Height:   {box.Height},")
                        print(f"  Rotation: {box.Rotation}")
                        print(f"}}")
                    print()
                else:
                    print("An error occurred during processing (pin 'Boxes'):",
                          boxes_array.ErrorDescription)
            else:
                raise RuntimeError("Result timeout")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
