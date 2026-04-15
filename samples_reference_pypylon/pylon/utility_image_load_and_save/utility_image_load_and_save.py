#!/usr/bin/env python3
"""\
Illustrate how to load and save images using PylonImage and ImagePersistence.

The ImagePersistence class provides static functions for loading and saving
images. It uses the image class related interfaces of pylon.

The PylonImage class can be used as target for loading images.

The grab result can be passed directly to the function that saves an image to
disk.

SampleImageCreator is not exposed in pypylon so deterministic RGB gradients
are used instead while keeping the same save, load, and grabbed-image workflow.

Output files are written to the current working directory: SyntheticImage.tiff,
SyntheticImage.png, GrabbedImage.png, and on Windows SyntheticImage.bmp and
SyntheticImage_*.jpg.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon
import numpy as np

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
GRAB_ONE_TIMEOUT_MS = 1000
OUTPUT_STEM = "SyntheticImage"


def _synthetic_rgb_gradient(width, height, dtype):
    """Return an (H, W, 3) array: R = horizontal ramp, G = vertical, B = diagonal sum."""
    xs = np.arange(width, dtype=np.uint32)
    ys = np.arange(height, dtype=np.uint32)[:, None]
    maxv = int(np.iinfo(dtype).max)
    w1 = max(width - 1, 1)
    h1 = max(height - 1, 1)
    arr = np.empty((height, width, 3), dtype=dtype)
    arr[:, :, 0] = (xs * maxv // w1).astype(dtype)
    arr[:, :, 1] = (ys * maxv // h1).astype(dtype)
    arr[:, :, 2] = ((xs + ys) * maxv // (width + height)).astype(dtype)
    return arr


exit_code = 0
try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        # Saving images using the ImagePersistence class.

        # Synthetic RGB gradient instead of SampleImageCreator Mandelbrot.
        # Create a sample image.
        arr16 = _synthetic_rgb_gradient(IMAGE_WIDTH, IMAGE_HEIGHT, np.uint16)
        image_rgb16 = pylon.PylonImage()
        image_rgb16.AttachArray(arr16, pylon.PixelType_RGB16packed)

        # If required the image is automatically converted to a new image and then saved.
        # An image with a bit depth higher than 8 Bit is stored with 16 Bit bit depth
        # if supported by the image file format. In this case the pixel data is MSB aligned.
        # If more control over the conversion is required then the ImageFormatConverter class
        # can be used to convert the input image before saving it (not shown).
        image_rgb16.Save(pylon.ImageFileFormat_Tiff, f"{OUTPUT_STEM}.tiff")

        can_tiff = image_rgb16.CanSaveWithoutConversion(pylon.ImageFileFormat_Tiff)
        print(
            "The image",
            "can" if can_tiff else "can not",
            "be saved without conversion as tiff.",
        )

        if sys.platform == "win32":
            # The PylonImage class provides a member function for saving images for
            # convenience. This function calls ImagePersistence.Save().
            image_rgb16.Save(pylon.ImageFileFormat_Bmp, f"{OUTPUT_STEM}.bmp")

            # CanSaveWithoutConversion() can be used to check whether a conversion
            # is performed when saving the image.
            can_bmp = image_rgb16.CanSaveWithoutConversion(pylon.ImageFileFormat_Bmp)
            print(
                "The image",
                "can" if can_bmp else "can not",
                "be saved without conversion as bmp.",
            )

        image_rgb16.Save(pylon.ImageFileFormat_Png, f"{OUTPUT_STEM}.png")

        # Loading images.

        # Create pylon images.
        image_from_tiff = pylon.PylonImage()

        # Load the tiff image directly via the ImagePersistence interface.
        image_from_tiff.Load(f"{OUTPUT_STEM}.tiff")
        ok_rgb16 = image_from_tiff.PixelType == pylon.PixelType_RGB16packed
        print(
            "The pixel type of the image is "
            + ("not " if not ok_rgb16 else "")
            + "RGB16packed."
        )

        if sys.platform == "win32":
            image_from_bmp = pylon.PylonImage()
            image_from_bmp.Load(f"{OUTPUT_STEM}.bmp")

            # The format of the loaded image from the bmp file is BGR8packed instead of
            # the original RGB16packed format because it had to be converted for saving
            # it in the bmp format.
            ok_bgr8 = image_from_bmp.PixelType == pylon.PixelType_BGR8packed
            print(
                "The pixel type of the image is "
                + ("not " if not ok_bgr8 else "")
                + "BGR8packed."
            )

        # Selecting the image quality when saving in JPEG format.
        # Create a sample image.
        arr8 = _synthetic_rgb_gradient(IMAGE_WIDTH, IMAGE_HEIGHT, np.uint8)
        image_rgb8 = pylon.PylonImage()
        image_rgb8.AttachArray(arr8, pylon.PixelType_RGB8packed)

        # The JPEG image quality can be adjusted in the range from 0 to 100.
        ipo = pylon.ImagePersistenceOptions()
        # Set the lowest quality value.
        ipo.SetQuality(0)

        # Save the image.
        image_rgb8.Save(pylon.ImageFileFormat_Jpeg, f"{OUTPUT_STEM}_0.jpg", ipo)

        # Set the highest quality value.
        ipo.SetQuality(100)

        # Save the image.
        image_rgb8.Save(pylon.ImageFileFormat_Jpeg, f"{OUTPUT_STEM}_100.jpg", ipo)

        # Saving grabbed images.
        print()
        print("Waiting for an image to be grabbed.")
        camera.Open()
        # Try to get a grab result.
        with camera.GrabOne(GRAB_ONE_TIMEOUT_MS) as grab_result:
            if grab_result.GrabSucceeded():
                # The pylon grab result provides a cast operator
                # to the IImage interface. This makes it possible to pass a grab result
                # directly to the function that saves an image to disk.
                save_img = pylon.PylonImage()
                try:
                    save_img.AttachGrabResultBuffer(grab_result)
                    save_img.Save(pylon.ImageFileFormat_Png, "GrabbedImage.png")
                finally:
                    save_img.Release()

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
