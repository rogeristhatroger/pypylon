#!/usr/bin/env python3
"""\
Demonstrate the PylonImage class for creating, copying, and manipulating images.

PylonImage supports handling image buffers of various pixel types. It provides
methods for creating, resetting, copying, and releasing image data. The image
class implements reference counting: assigning one image to another shares the
underlying buffer rather than copying data. Use IsUnique() to check whether a
buffer is exclusively owned by one image object.

Zero-copy buffer access is available via GetArrayZeroCopy (numpy array backed
by the image buffer) and GetMemoryView (raw writable memoryview). These are
useful for filling or inspecting image data without allocating a copy.

PylonImage can also wrap grab result buffers (via AttachGrabResultBuffer) so
that the data remains available after the grab result is released. Images can
be saved to and loaded from files in various formats.

Additionally, GetAoi() creates partial images derived from a source image
(e.g. thumbnail images for displaying defects). GetPlane() provides access to
individual planes of a planar image. Neither method copies image data.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import ctypes
import sys
from pypylon import pylon
import numpy as np

WIDTH = 640
HEIGHT = 480


def print_image_info(label, image):
    """Print a summary of PylonImage properties."""
    pixel_type = image.GetPixelType()
    try:
        # Use GetMemoryView() to obtain the real internal C++ buffer pointer.
        mv = image.GetMemoryView()
        buf_ptr = hex(ctypes.addressof(ctypes.c_char.from_buffer(mv)))
    except Exception:
        buf_ptr = "N/A"
    print(label)
    print(f"  Width: {image.Width:,}  Height: {image.Height:,}"
          f"  PixelType: {pixel_type:#010x}  IsPacked: {str(pylon.IsPacked(pixel_type)):>5}"
          f"  IsUnique: {str(image.IsUnique()):>5}")
    print(f"  ImageSize: {image.ImageSize:,}"
          f"  AllocatedBufferSize: {image.AllocatedBufferSize:,}"
          f"  Buffer: {buf_ptr}")


exit_code = 0
try:
    # ----------------------------------------------------------------
    # The PylonImage basics.
    # ----------------------------------------------------------------
    print("-" * 60)
    print("The PylonImage basics.")
    print()

    # Create a pylon image with the given properties.
    image_mono8 = pylon.PylonImage.Create(pylon.PixelType_Mono8, WIDTH, HEIGHT)
    print_image_info("The properties of the newly created image.", image_mono8)

    # GetArrayZeroCopy provides direct access to the internal image buffer as
    # a NumPy array. The array format depends on the pixel type. For this
    # example Mono8 is used, so each pixel is a single uint8 value, and we
    # can fill a synthetic grayscale image by writing pixel values directly.
    # The context manager ensures the buffer stays locked while the array is
    # in use; on exit, the lock is released and the array becomes invalid.
    with image_mono8.GetArrayZeroCopy() as numpy_array:
        for y in range(image_mono8.Height):
            for x in range(image_mono8.Width):
                numpy_array[y, x] = (x + y) % 256

    image_mono8.Save(pylon.ImageFileFormat_Png, "grayscale_image.png")

    # If the pylon image object is copied or assigned then no image data copy
    # is made. All objects reference the same buffer now.
    same_image_a = pylon.PylonImage(image_mono8)
    print()
    print_image_info("The properties of the copied image.", same_image_a)
    print()
    print("After copy, original is unique:", image_mono8.IsUnique())
    print("After copy, copy is unique:    ", same_image_a.IsUnique())

    # The CopyImage method can be used to create a full copy of an image.
    copied_image = pylon.PylonImage()
    copied_image.CopyImage(image_mono8)
    print()
    print_image_info("The properties of a full copy of the test image.", copied_image)

    # The Release() method can be used to release any data.
    same_image_a.Release()
    print()
    print("After releasing the copy, original is unique:", image_mono8.IsUnique())

    # A newly created image object is empty.
    reused_image = pylon.PylonImage()
    print()
    print_image_info("A newly created image object.", reused_image)

    # The Reset() method can be used to reset the image properties
    # and allocate a new buffer if required.
    reused_image.Reset(pylon.PixelType_Mono8, WIDTH, HEIGHT)
    print_image_info(
        "After resetting the image properties. A new buffer is allocated.",
        reused_image,
    )

    # Reset() never decreases the allocated buffer size if the
    # new image fits into the current buffer.
    reused_image.Reset(pylon.PixelType_Mono8, WIDTH // 2, HEIGHT)
    print_image_info(
        "After resetting to a smaller image. The buffer is reused.",
        reused_image,
    )

    # A new buffer is allocated because the old buffer is
    # too small for the new image.
    reused_image.Reset(pylon.PixelType_Mono8, WIDTH * 2, HEIGHT)
    print_image_info(
        "After resetting to a larger image. A new buffer is allocated.",
        reused_image,
    )

    # ----------------------------------------------------------------
    # The PylonImage and grab results.
    # ----------------------------------------------------------------
    print()
    print("-" * 60)
    print("The PylonImage and grab results.")
    print()

    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        print("Waiting for an image to be grabbed.")
        with camera.GrabOne(1000) as grab_result:
            if grab_result.GrabSucceeded():
                # A pylon grab result can be used with AttachGrabResultBuffer.
                image = pylon.PylonImage()
                image.AttachGrabResultBuffer(grab_result)
                print()
                print_image_info(
                    "The properties of an image with an attached grab result.",
                    image,
                )

                pixel_type = grab_result.PixelType
                width = grab_result.Width
                height = grab_result.Height

        # Now the grab result is released (exited context). The grab result
        # buffer is now only held by the pylon image.
        print_image_info("After the grab result has been released.", image)

        image.Save(pylon.ImageFileFormat_Png, "_grab_result_image.png")
        print("Saved grab result image to _grab_result_image.png")

        # If a grab result is referenced then always a new buffer is allocated
        # on reset.
        image.Reset(pixel_type, width // 2, height)
        print()
        print_image_info(
            "After resetting while a grab result was referenced.", image
        )

    # ----------------------------------------------------------------
    # Loading and saving.
    # Please look at the utility_image_load_and_save sample for more details.
    # ----------------------------------------------------------------
    print()
    print("-" * 60)
    print("Loading and saving.")
    print()

    # Using synthetic RGB gradient.
    image_saved = pylon.PylonImage.Create(
        pylon.PixelType_RGB8packed, WIDTH, HEIGHT
    )

    # Use GetArrayZeroCopy to fill the image with a synthetic RGB gradient.
    with image_saved.GetArrayZeroCopy() as numpy_array:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                numpy_array[y, x, 0] = x % 256
                numpy_array[y, x, 1] = y % 256
                numpy_array[y, x, 2] = (x + y) % 256

    # Save the image. The image is automatically converted to a format that
    # can be saved if needed.
    image_saved.Save(pylon.ImageFileFormat_Tiff, "_utility_image_saved.tiff")
    print("Saved synthetic image to _utility_image_saved.tiff")

    image_loaded = pylon.PylonImage()
    image_loaded.Load("_utility_image_saved.tiff")
    print_image_info("The properties of the loaded image.", image_loaded)

    # ----------------------------------------------------------------
    # The GetAoi method.
    # ----------------------------------------------------------------
    print()
    print("-" * 60)
    print("The GetAoi method.")

    sample_image = image_saved
    print()
    print_image_info("The properties of the sample image.", sample_image)

    top_left_x = WIDTH // 4
    top_left_y = HEIGHT // 2
    aoi_width = WIDTH // 4
    aoi_height = HEIGHT // 4

    # Create a new pylon image containing the AOI.
    # No image data is copied. The same image buffer is referenced.
    # The padding property of the pylon image object is used to skip over
    # the part of a line outside of the AOI.
    aoi = sample_image.GetAoi(top_left_x, top_left_y, aoi_width, aoi_height)
    print_image_info("After creating an AOI.", aoi)

    # CopyImage can be used to create a full copy of the AOI.
    copied_aoi = pylon.PylonImage()
    copied_aoi.CopyImage(aoi)
    print_image_info("The properties of a full copy of the AOI image.", copied_aoi)

    # GetAoi can be applied again for the AOI image.
    aoi_from_aoi = aoi.GetAoi(
        aoi_width // 4, aoi_height // 4, aoi_width // 2, aoi_height // 2
    )

    # An AOI image is still valid if the source image object has been
    # destroyed or the image data has been released.
    aoi.Release()
    sample_image.Release()

    print_image_info("After creating an AOI of an AOI.", aoi_from_aoi)

    # ----------------------------------------------------------------
    # The GetPlane method.
    # ----------------------------------------------------------------
    print()
    print("-" * 60)
    print("The GetPlane method.")
    print()

    image_rgb8_planar = pylon.PylonImage.Create(
        pylon.PixelType_RGB8planar, WIDTH, HEIGHT
    )

    # GetArrayZeroCopy does not support RGB8planar, so access the buffer
    # directly via GetMemoryView and reshape to (3, HEIGHT, WIDTH) planes.
    mv = image_rgb8_planar.GetMemoryView()
    planar_arr = np.asarray(mv).reshape(3, HEIGHT, WIDTH)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            planar_arr[0, y, x] = 3 * x % 256
            planar_arr[1, y, x] = 2 * y % 256
            planar_arr[2, y, x] = (x + y) % 256
    # The numpy array holds a reference to the memoryview's buffer, so
    # delete it first, then release the memoryview to free the lock.
    del planar_arr
    mv.release()

    # Save the image. The image is automatically converted to a format that
    # can be saved if needed.
    image_rgb8_planar.Save(pylon.ImageFileFormat_Png, "_planar_image.png")
    print("Saved synthetic image to _planar_image.png")

    # Create images to access the planes of the planar image.
    # No image data is copied. The same image buffer is referenced.
    # The buffer start is the start of the plane and the pixel type is set
    # to the corresponding pixel type of a plane.
    red_plane = image_rgb8_planar.GetPlane(0)
    green_plane = image_rgb8_planar.GetPlane(1)
    blue_plane = image_rgb8_planar.GetPlane(2)

    print()
    print_image_info("Red plane:", red_plane)
    print_image_info("Green plane:", green_plane)
    print_image_info("Blue plane:", blue_plane)

    print("Set red plane to zero.")
    # Use GetMemoryView on the plane for zero-copy write access.
    mv = red_plane.GetMemoryView()
    plane_arr = np.asarray(mv).reshape(HEIGHT, WIDTH)
    plane_arr[:] = 0
    del plane_arr
    mv.release()

    image_rgb8_planar.Save(pylon.ImageFileFormat_Png, "_planar_image_2.png")
    print("Saved synthetic image to _planar_image_2.png")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
