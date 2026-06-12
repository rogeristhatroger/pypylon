#!/usr/bin/env python3
"""\
This sample shows how to grab images, convert them for OpenCV, display each
frame, and record a short video clip.

Camera sensors deliver images in a wide range of pixel formats — Bayer
patterns (BayerBG8, BayerRG12, …), packed mono (Mono10p, Mono12packed),
YUV, or plain Mono8. OpenCV expects BGR8 for color video, so a raw camera
buffer cannot be passed to cv2.VideoWriter or cv2.imshow directly.
pylon.ImageFormatConverter handles the conversion: It debayers, unpacks,
and reorders channels in a single call, producing BGR8 frames that OpenCV
can consume immediately.

The sample grabs for a fixed duration, writes every converted frame to an
AVI file using the MJPG codec, and shows a live preview via
pylon.DisplayImage.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import os
import sys
import time
from pypylon import pylon
import cv2

RECORD_DURATION_S = 5
TIMEOUT_MS = 5000
VIDEO_CODEC = "MJPG"
VIDEO_FPS = 20.0
VIDEO_FILENAME = os.path.join(os.path.dirname(__file__), "output.avi")

exit_code = 0
try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)

        # Camera images may use pixel formats that OpenCV cannot consume
        # directly (Bayer patterns, packed mono formats, etc.).
        # ImageFormatConverter converts each frame to BGR8packed — the
        # standard Blue-Green-Red 8-bit layout that OpenCV expects.
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment.Value = pylon.OutputBitAlignment_MsbAligned

        frame_width = camera.Width.Value
        frame_height = camera.Height.Value

        # Set up the OpenCV video writer.
        fourcc = cv2.VideoWriter_fourcc(*VIDEO_CODEC)
        writer = cv2.VideoWriter(
            VIDEO_FILENAME, fourcc, VIDEO_FPS, (frame_width, frame_height)
        )
        if not writer.isOpened():
            raise RuntimeError(f"Could not open video writer for {VIDEO_FILENAME}")

        print(
            f"Recording {RECORD_DURATION_S}s of video to {VIDEO_FILENAME} "
            f"({frame_width}x{frame_height} @ {VIDEO_FPS} fps) ..."
        )

        # Grab with LatestImageOnly to minimize latency — each
        # RetrieveResult returns the most recent frame, discarding
        # older queued buffers.
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        frame_count = 0
        start_time = time.monotonic()

        while camera.IsGrabbing():
            if time.monotonic() - start_time >= RECORD_DURATION_S:
                break

            with camera.RetrieveResult(
                TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
            ) as grab_result:
                if grab_result.GrabSucceeded():
                    # Some camera models use a GenICam Generic Data Container (GenDC) format.
                    # For single grabbed images, a data component is emulated automatically.
                    # pylon provides a data component wrapper to handle both cases uniformly.
                    with grab_result.GetFirstImageDataComponent() as image_data_component:
                        converted = converter.Convert(image_data_component)
                        writer.write(converted.Array)
                        frame_count += 1

                        pylon.DisplayImage(1, image_data_component)
                else:
                    print(
                        "Error:",
                        f"{grab_result.ErrorCode:#x}",
                        grab_result.ErrorDescription
                    )

        camera.StopGrabbing()
        writer.release()

        elapsed = time.monotonic() - start_time
        print(
            f"Saved {frame_count} frames in {elapsed:.1f}s "
            f"(effective {frame_count / max(elapsed, 0.001):.1f} fps)."
        )

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
