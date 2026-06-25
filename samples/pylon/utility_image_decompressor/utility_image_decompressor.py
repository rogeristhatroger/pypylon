#!/usr/bin/env python3
"""\
Demonstrate Compression Beyond: enable, decompress, and compare lossless vs lossy modes.

This sample illustrates how to enable the Compression Beyond feature in Basler
cameras and how to decompress images using the ImageDecompressor class.

Compression Beyond reduces the bandwidth needed for image transfer. The camera
compresses image data before sending it; the application uses
ImageDecompressor to recover the original image. Both lossless and lossy
(fix-ratio) compression modes are demonstrated when available.

This sample requires a camera that supports the ImageCompressionMode feature.
If the connected device does not support compression, the sample exits
cleanly.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon


def _show_image(image, message=None):
    """Display an image and print its first six bytes."""
    pylon.DisplayImage(1, image)
    if message:
        print(f"\n{message}")
    buf = image.Buffer
    print("First six bytes of the image:")
    print(" ".join(f"0x{buf[i]:02x}" for i in range(min(6, len(buf)))))


def _print_compression_info(info):
    """Print all fields of the compression info dictionary."""
    print()
    print("Compression info:")
    for key, val in info.to_dict().items():
        print(f"  {key}: {val}")


exit_code = 0
try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:

        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        # Check if the camera supports compression.
        if not camera.ImageCompressionMode.IsWritable():
            print("This camera does not support compression.")
            sys.exit(0)

        # Remember the original compression mode.
        old_compression_mode = camera.ImageCompressionMode.Value
        print("Old compression mode:", old_compression_mode)

        # Set the compression mode to BaslerCompressionBeyond if available.
        if not camera.ImageCompressionMode.TrySetValue("BaslerCompressionBeyond"):
            print("BaslerCompressionBeyond is not available on this device.")
            sys.exit(0)
        print("New compression mode:", camera.ImageCompressionMode.Value)

        # After enabling the compression, we can read the compression rate option.
        if camera.ImageCompressionRateOption.IsReadable():
            old_rate_option = camera.ImageCompressionRateOption.Value
            print("Old compression rate option:", old_rate_option)
        else:
            old_rate_option = None

        # Configure lossless compression.
        if camera.ImageCompressionRateOption.TrySetValue("Lossless"):
            print("New compression rate option:", camera.ImageCompressionRateOption.Value)

        # Create the decompressor and initialize it with the camera's node map.
        decompressor = pylon.ImageDecompressor()
        try:
            decompressor.SetCompressionDescriptor(camera.NodeMap)
            print("Initialized decompressor from camera node map.")
        except Exception:
            print()
            print("The decompressor cannot be initialized on this device.")
            print("(Typically only cameras with hardware Compression Beyond provide"
                  " the descriptor.)")
            # Restore original settings before exiting.
            # Rate option must be restored first as the rate can't be changed
            # when compression itself is turned off.
            if old_rate_option is not None:
                camera.ImageCompressionRateOption.Value = old_rate_option
            camera.ImageCompressionMode.TrySetValue(old_compression_mode)
            sys.exit(0)

        grab_ok = False
        with camera.GrabOne(1000) as grab_result:
            if grab_result.GrabSucceeded():
                grab_ok = True
                # Fetch compression info and check whether the image was compressed.
                info = decompressor.GetCompressionInfo(grab_result)
                if info is not None:
                    _print_compression_info(info)

                    if info.hasCompressedImage:
                        if info.compressionStatus == pylon.CompressionStatus_Ok:
                            payload = grab_result.PayloadSize
                            decompressed_size = info.decompressedPayloadSize
                            if decompressed_size > 0:
                                ratio = payload / decompressed_size * 100.0
                                print(f"\nTransferred payload: {payload}")
                                print(f"Compression ratio: {ratio:.1f}%")

                            # Decompress the image.
                            target_image = decompressor.DecompressImage(grab_result)
                            _show_image(target_image, "Decompressed image.")
                        else:
                            print("There was an error while the camera was compressing the image.")
                    else:
                        # No decompression is needed because it is already an uncompressed image.
                        # (This can happen if the transport layer supports transparent decompressing.)
                        _show_image(grab_result, "Grabbed image.")
                else:
                    # No decompression is required because the image has never been compressed.
                    # (This can happen if compression was accidentally turned off after
                    # initializing the decompressor class.)
                    _show_image(grab_result, "Grabbed image.")
            else:
                print("Error:", f"{grab_result.ErrorCode:#x}", grab_result.ErrorDescription)

        if grab_ok and camera.ImageCompressionRateOption.IsWritable():
            # Take another picture with lossy compression (if available).
            print()
            print("--- Switching to Fix Ratio compression ---")
            print()

            if camera.ImageCompressionRateOption.TrySetValue("FixRatio"):
                print("New compression rate option:", camera.ImageCompressionRateOption.Value)

                # After changing the compression parameters, the decompressor
                # MUST be reconfigured.
                decompressor.SetCompressionDescriptor(camera.NodeMap)

                with camera.GrabOne(1000) as grab_result:
                    if grab_result.GrabSucceeded():
                        info = decompressor.GetCompressionInfo(grab_result)
                        if info is not None:
                            _print_compression_info(info)

                            if info.hasCompressedImage and info.compressionStatus == pylon.CompressionStatus_Ok:
                                payload = grab_result.PayloadSize
                                decompressed_size = info.decompressedPayloadSize
                                if decompressed_size > 0:
                                    ratio = payload / decompressed_size * 100.0
                                    print(f"\nTransferred payload: {payload}")
                                    print(f"Compression ratio: {ratio:.1f}%")

                                target_image = decompressor.DecompressImage(grab_result)
                                _show_image(target_image, "Decompressed image.")
                            else:
                                # No decompression is needed because it is already an
                                # uncompressed image.
                                _show_image(grab_result, "Grabbed image.")
                        else:
                            _show_image(grab_result, "Grabbed image.")
            else:
                print("FixRatio compression is not available.")

        # Restore original compression mode. Compression rate option must be
        # restored first as the rate can't be changed when compression itself
        # is turned off.
        if old_rate_option is not None:
            camera.ImageCompressionRateOption.SetValue(old_rate_option)
        camera.ImageCompressionMode.TrySetValue(old_compression_mode)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
