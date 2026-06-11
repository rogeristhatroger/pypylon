# 17. Recipes

This chapter provides practical, ready-to-use code snippets for common pypylon tasks. These recipes can be used as building blocks for real-world applications.

---

## Single Image Snapshot

Capture a single image and process it.

```Python
from pypylon import pylon

def process(img):
    print(img.shape)

factory = pylon.TlFactory.GetInstance()

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.Open()
    camera.StartGrabbingMax(1)

    with camera.RetrieveResult(5000) as result:
        if result.GrabSucceeded():
            img = result.Array.copy()
            process(img)
```

---

## Continuous Acquisition Loop

Process images continuously.

```Python
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

while camera.IsGrabbing():
    with camera.RetrieveResult(5000) as result:
        if result.GrabSucceeded():
            process(result.Array.copy())
```

---

## Save Image to Disk

```Python
import cv2

cv2.imwrite("image.png", img)
```

---

## Software Trigger

```Python
camera.TriggerMode.Value = "On"
camera.ExecuteSoftwareTrigger()
```

---

## Hardware Trigger Setup

```Python
camera.TriggerMode.Value = "On"
camera.TriggerSource.Value = "Line1"
```

---

## Set Exposure and Gain

```Python
camera.ExposureAuto.Value = "Off"
camera.ExposureTime.Value = 3000

camera.GainAuto.Value = "Off"
camera.Gain.Value = 5
```

---

## Set ROI

```Python
camera.StopGrabbing()

camera.Width.Value = 640
camera.Height.Value = 480

camera.StartGrabbing()
```

---

## Convert to OpenCV Format

```Python
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed

img = converter.Convert(result).GetArray()
```

---

## Display Image with OpenCV

```Python
import cv2

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Capture with Timeout Handling

```Python
from pypylon import pylon

try:
    with camera.RetrieveResult(
        1000,
        pylon.TimeoutHandling_ThrowException
    ) as result:
        if result.GrabSucceeded():
            process(result.Array.copy())

except Exception as e:
    log_error(e)
```

---

## Multi-Camera Setup

Using multiple cameras efficiently is best done with `InstantCameraArray`. It allows grabbing from all cameras in a single loop.

```Python
from pypylon import pylon

RETRIEVE_TIMEOUT_MS = 5000

factory = pylon.TlFactory.GetInstance()
devices = factory.EnumerateDevices()
camera_count = len(devices)

with pylon.InstantCameraArray(camera_count) as cameras:
    # Attach devices
    for i, cam in enumerate(cameras):
        cam.Attach(factory.CreateDevice(devices[i]))
        print("Using device:", cam.DeviceInfo.ModelName)

    # Start acquisition
    cameras.StartGrabbing()

    while cameras.IsGrabbing():
        with cameras.RetrieveResult(
            RETRIEVE_TIMEOUT_MS,
            pylon.TimeoutHandling_ThrowException
        ) as grab_result:

            if grab_result.GrabSucceeded():

                # Identify source camera
                cam_idx = grab_result.GetCameraContext()
                cam_name = cameras[cam_idx].DeviceInfo.ModelName

                # Access image data (GenDC-safe)
                img = grab_result.Array

                print(
                    f"Camera {cam_idx}: {cam_name}"
                    f" SizeX: {grab_result.Width} SizeY: {grab_result.Height} "
                    f" First pixel: {img[0, 0]}"
                )

            else:
                print("Error:", grab_result.ErrorCode, grab_result.ErrorDescription)
```

---

## Threaded Processing

```Python
import threading
import queue

q = queue.Queue()

def grab_loop():
    while camera.IsGrabbing():
        with camera.RetrieveResult(5000) as result:
            if result.GrabSucceeded():
                q.put(result.Array.copy())


def process_loop():
    while True:
        img = q.get()
        process(img)
        q.task_done()
```

---

## Safe Shutdown Pattern

```Python
import threading

stop_event = threading.Event()

while not stop_event.is_set():
    # processing loop
    pass

stop_event.set()
camera.StopGrabbing()
```

---

## Recording Video

```Python
import cv2

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 30, (640, 480))

out.write(img)
```

---

## Basic Processing Example (ROI + Decision)

```Python
import numpy as np

roi = img[100:200, 200:300]
mean = np.mean(roi)

if mean > 100:
    print("OK")
else:
    print("NOK")
```

---

## Conceptual Overview

```PlainText
Camera → Acquisition → Processing → Output
```

---

## Key Takeaways

- recipes accelerate development
- combine multiple recipes to build systems
- adapt examples to your specific use case

---
