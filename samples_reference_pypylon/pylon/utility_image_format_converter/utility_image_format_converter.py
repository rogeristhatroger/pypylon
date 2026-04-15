#!/usr/bin/env python3
"""\
Demonstrate ImageFormatConverter: build a synthetic RGB image, convert to Mono16, then GrabOne
with optional Mono8 conversion. The in-memory image is a simple NumPy gradient attached as RGB8.

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

exit_code = 0

def _print_first_six_bytes(image, message=None):
    # First six raw bytes (works for packed formats such as Mono16).
    if message:
        print()
        print(message, end=" ")
    print()
    print("First six bytes of the image:")
    buf = image.Buffer
    for i in range(min(6, len(buf))):
        print(f"0x{buf[i]:02x}", end=" ")
    print()


try:
    # Create converter, set output format, optional multithreading.
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_Mono16
    converter.OutputBitAlignment.Value = pylon.OutputBitAlignment_MsbAligned

    # Use all available threads for conversion.
    converter.MaxNumThreads.SetToMaximum()

    # Synthetic RGB8 gradient for a reproducible in-memory source.
    xs = np.arange(IMAGE_WIDTH, dtype=np.uint32)
    ys = np.arange(IMAGE_HEIGHT, dtype=np.uint32)[:, None]
    arr = np.empty((IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
    arr[:, :, 0] = (xs * 255 // max(IMAGE_WIDTH - 1, 1)).astype(np.uint8)
    arr[:, :, 1] = (ys * 255 // max(IMAGE_HEIGHT - 1, 1)).astype(np.uint8)
    arr[:, :, 2] = ((xs + ys) * 255 // (IMAGE_WIDTH + IMAGE_HEIGHT)).astype(np.uint8)
    image_rgb8_packed = pylon.PylonImage()
    image_rgb8_packed.AttachArray(arr, pylon.PixelType_RGB8packed)
    _print_first_six_bytes(image_rgb8_packed, "Source image.")

    # Convert returns the destination PylonImage.
    target_image = converter.Convert(image_rgb8_packed)
    _print_first_six_bytes(target_image, "Converted image.")

    # --- Second converter: GrabOne, then ImageHasDestinationFormat / optional Convert.
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("\nUsing device:", camera.DeviceInfo.ModelName)
        print()

        converter2 = pylon.ImageFormatConverter()
        converter2.OutputPixelFormat = pylon.PixelType_Mono8
        converter2.MaxNumThreads.SetToMaximum()
        
        print("Waiting for an image to be grabbed.")
        with camera.GrabOne(GRAB_ONE_TIMEOUT_MS) as grab_result:
            if grab_result.GrabSucceeded():
                if converter2.ImageHasDestinationFormat(grab_result):
                    # Already Mono8; skip conversion to save work.
                    _print_first_six_bytes(grab_result, "Grabbed image.")
                else:
                    _print_first_six_bytes(grab_result, "Grabbed image.")
                    target_grab = converter2.Convert(grab_result)
                    _print_first_six_bytes(target_grab, "Converted image.")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
