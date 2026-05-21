#!/usr/bin/env python3
"""\
This sample illustrates how to load and save images.

The ImagePersistence class provides static functions for
loading and saving images.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""

import sys
import os

# Make the shared samples/include/ helpers importable.
_INCLUDE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "include")
)
if _INCLUDE_DIR not in sys.path:
    sys.path.insert(0, _INCLUDE_DIR)

from pypylon import pylon
import sample_image_creator

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
GRAB_ONE_TIMEOUT_MS = 1000
OUTPUT_STEM = "MandelbrotFractal"

# The exit code of the sample application.
exit_code = 0

try:
    # Create an instant camera object with the camera device found first.
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        # Print the model name of the camera.
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        with sample_image_creator.create_mandelbrot_fractal( pylon.PixelType_RGB16packed, IMAGE_WIDTH, IMAGE_HEIGHT ) as image_rgb16_packed:
            # If required the image is automatically converted to a new image and then saved.
            # An image with a bit depth higher than 8 Bit is stored with 16 Bit bit depth
            # if supported by the image file format. In this case the pixel data is MSB aligned.
            # If more control over the conversion is required then the ImageFormatConverter class
            # can be used to convert the input image before saving it (not shown).
            pylon.ImagePersistence.Save( pylon.ImageFileFormat_Tiff, f"{OUTPUT_STEM}.tiff", image_rgb16_packed )

            print("The image",
                  "can" if pylon.ImagePersistence.CanSaveWithoutConversion( pylon.ImageFileFormat_Tiff, image_rgb16_packed ) else "can not",
                  "be saved without conversion as tiff.")


            # The PylonImage class provides a member function
            # for saving images for convenience. This function calls pylon.ImagePersistence.Save().
            image_rgb16_packed.Save( pylon.ImageFileFormat_Bmp, f"{OUTPUT_STEM}.bmp" )
            print("The image",
                  "can" if pylon.ImagePersistence.CanSaveWithoutConversion( pylon.ImageFileFormat_Bmp, image_rgb16_packed ) else "can not",
                  "be saved without conversion as bmp.")



        # Load the tiff image directly via the ImagePersistence interface.
        with pylon.ImagePersistence.Load(f"{OUTPUT_STEM}.tiff") as image_rgb16_packed_from_tiff:
            print("The pixel type of the image is",
                  "" if image_rgb16_packed_from_tiff.GetPixelType() == pylon.PixelType_RGB16packed else "not",
                  "RGB16packed.")


            # The PylonImage class provides a member function
            # for saving images for convenience. This function calls pylon.ImagePersistence.Load().
        with pylon.PylonImage() as image_bgr8_packed_from_bmp:
            image_bgr8_packed_from_bmp.Load(f"{OUTPUT_STEM}.bmp")

            # The format of the loaded image from the bmp file is BGR8packed instead of the original RGB16packed format because
            # it had to be converted for saving it in the bmp format.
            print("The pixel type of the image is",
                  "" if image_bgr8_packed_from_bmp.GetPixelType() == pylon.PixelType_RGB8packed else "not",
                  "RGB8packed.")


        # Selecting the image quality when saving in JPEG format.

        # Create a sample image.
        with sample_image_creator.create_mandelbrot_fractal( pylon.PixelType_RGB8packed, IMAGE_WIDTH, IMAGE_HEIGHT ) as image_rgb8_packed:
            # The JPEG image quality can be adjusted in the range from 0 to 100.
            additional_options = pylon.ImagePersistenceOptions()

            # Set the lowest quality value.
            additional_options.Quality = 0

            # Save the image.
            pylon.ImagePersistence.Save(pylon.ImageFileFormat_Jpeg, f"{OUTPUT_STEM}_0.jpg", image_rgb8_packed, additional_options)

            # Set the highest quality value.
            additional_options.Quality = 100

            # Save the image.
            pylon.ImagePersistence.Save(pylon.ImageFileFormat_Jpeg, f"{OUTPUT_STEM}_100.jpg", image_rgb8_packed, additional_options)


        # Saving grabbed images.
        print("Waiting for an image to be grabbed.")

        # The Python API differs from the C++ API, as in python the grab result ptr is not passed to the function
        # but the grab result is returned instead.
        with camera.GrabOne(GRAB_ONE_TIMEOUT_MS) as grab_result:
            # Python does not support cast operators the same way as C++ does but you can
            # pass values of any type as a parameter to a function. In this case an IImage,
            # CGrabResultPtr as well as a CPylonDataComponent can be passed and are cast the
            # same way as in C++.
            if grab_result:
                pylon.ImagePersistence.Save(pylon.ImageFileFormat_Png, "GrabbedImage.png", grab_result)

except BaseException as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
