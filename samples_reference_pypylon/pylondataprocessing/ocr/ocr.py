#!/usr/bin/env python3
"""\
Demonstrate the OCR Basic vTool with a recipe loaded from file (license required).

The recipe was created with the pylon Viewer Workbench, where it can also
be inspected and modified. It configures an ImageLoading vTool that loads
images from disk. Each loaded image is passed through an OCR Basic vTool
which detects and reads text. The sample collects output data (images and
text strings) via a GenericOutputObserver.
"""
import os
import sys
from pypylon import pylon
from pypylon import pylondataprocessing

COUNT_OF_IMAGES_TO_GRAB = 10

REPLACEMENT_CHAR = "\ufffd"


def get_rejection_char_positions(text):
    """Return positions of UTF-8 rejection characters (U+FFFD) in *text*."""
    return [i for i, ch in enumerate(text) if ch == REPLACEMENT_CHAR]


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
        recipe_file = os.path.join(this_dir, "ocr.precipe")
        recipe.Load(recipe_file)

        # Set up correct image path to samples.
        samples_dir = os.path.dirname(os.path.dirname(this_dir))
        images_path = os.path.join(samples_dir, "images", "ocr")
        recipe.GetParameter(
            "ImageLoading/@vTool/SourcePath"
        ).SetValue(images_path)

        # This is where the output goes.
        recipe.RegisterAllOutputsObserver(
            result_collector, pylon.RegistrationMode_Append
        )

        # Start the processing.
        recipe.Start()

        # Flag to store mode change of OCR Basic vTool.
        use_character_set_all = False

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

                text_array = result["Texts"]
                if not text_array.HasError():
                    print("Texts:")
                    for index in range(text_array.NumArrayValues):
                        text = text_array[index].ToString()
                        print(f"  {index}: {text}")

                        # Characters that couldn't be detected are replaced by
                        # the UTF-8 replacement character U+FFFD.
                        positions = get_rejection_char_positions(text)
                        if positions:
                            print("  Characters at the following positions "
                                  "couldn't be detected:",
                                  ", ".join(str(p) for p in positions))
                else:
                    print("An error occurred during processing (pin 'Texts'):",
                          text_array.ErrorDescription)
                print()
            else:
                raise RuntimeError("Result timeout")

            # Switch character set after first full image loop.
            if i >= COUNT_OF_IMAGES_TO_GRAB // 2 and not use_character_set_all:
                print("Switch to character set 'All' to demonstrate correct"
                      " OCR detection.\n")
                recipe.GetParameter(
                    "OcrBasic/@vTool/CharacterSet"
                ).SetValue("All")
                use_character_set_all = True

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
