# 14. Multi-Camera Systems

This chapter explains how to design, configure, and operate systems that use multiple cameras simultaneously. Multi-camera setups are common in industrial applications such as inspection, 3D reconstruction, and synchronized data acquisition.

---

## Why Use Multiple Cameras?

Multi-camera systems are used when a single camera is not sufficient to capture all required information.

Typical reasons:

- capturing different viewpoints of an object
- increasing field of view
- increasing throughput
- parallel inspection of multiple objects

---

## Fundamental Challenges

Working with multiple cameras introduces several challenges:

- synchronization (timing)
- bandwidth limitations (especially GigE)
- CPU load (processing multiple streams)
- device identification and mapping

---

## Device Identification

Each camera must be uniquely identified, typically by its serial number.

```python
for d in devices:
    print(d.tSerialNumber)
```

Mapping example:

```text
Camera 40123456 → Left view
Camera 40123478 → Right view
```

Avoid using indices such as `devices[0]`, because enumeration order is not stable.

---

## Creating Multiple Camera Instances

```python
from pypylon import pylon

factory = pylon.TlFactory.GetInstance()
devices = factory.EnumerateDevices()

cameras = []

for device in devices:
    camera = pylon.InstantCamera(factory.CreateDevice(device))
    camera.Open()
    cameras.append(camera)
```

This creates and opens one camera instance per detected device.

---

## Sequential vs Parallel Acquisition

### Sequential Acquisition

```text
Cam1 → Capture → Process
Cam2 → Capture → Process
```

- simple to implement
- not time-synchronized
- slower overall

---

### Parallel Acquisition

```text
Cam1 → Capture →
                → Process
Cam2 → Capture →
```

- cameras acquire simultaneously
- required for synchronization
- higher CPU and bandwidth requirements

---

## Synchronization Methods

### Software Synchronization

- trigger cameras via software
- limited precision
- affected by OS scheduling

Example:

```python
camera.ExecuteSoftwareTrigger()
```

---

### Hardware Synchronization (Recommended)

```text
Master camera → trigger signal → Slave cameras
```

- precise timing
- deterministic behavior
- required for stereo or measurement systems

---

## Bandwidth Considerations (GigE)

Multiple GigE cameras share the same network bandwidth.

Potential problems:

- packet loss
- dropped frames
- increased latency

Mitigation strategies:

- use dedicated NICs
- enable jumbo frames
- reduce ROI or frame rate
- configure packet delay

---

## Processing Architecture

### Single-Threaded

```text
Acquire all → process all
```

- simple
- limited scalability

---

### Multi-Threaded (Recommended)

```text
Camera threads → queue → processing threads
```

- scalable
- better CPU utilization
- more complex to implement

---

## Example Pattern

### Basic Multi-Camera Loop (Sequential Polling)

```python
from pypylon import pylon

def process(image):
    print(image.shape)

factory = pylon.TlFactory.GetInstance()
devices = factory.EnumerateDevices()

cameras = [pylon.InstantCamera(factory.CreateDevice(device)) for device in devices]

for camera in cameras:
    camera.Open()
    camera.StartGrabbing()

while any(camera.IsGrabbing() for camera in cameras):
    for camera in cameras:
        if camera.IsGrabbing():
            with camera.RetrieveResult(1000) as result:
                if result.GrabSucceeded():
                    image = result.Array.copy()
                    # Do processing on image here, e.g. call a function.
                    process(image)
```

---

### Advanced Approach: InstantCameraArray (Recommended)

pypylon provides a dedicated abstraction for multi-camera setups: `InstantCameraArray`.

This class manages multiple cameras and provides a **single unified `RetrieveResult()` call**, including information about which camera delivered the image.

```python
from pypylon import pylon

def process(image):
    print(image.shape)

COUNT_OF_IMAGES_TO_GRAB = 100
RETRIEVE_TIMEOUT_MS = 5000

factory = pylon.TlFactory.GetInstance()
devices = factory.EnumerateDevices()

with pylon.InstantCameraArray(len(devices)) as cameras:

    for i, camera in enumerate(cameras):
        camera.Attach(factory.CreateDevice(devices[i]))
        print("Using device:", camera.DeviceInfo.ModelName)

    cameras.StartGrabbing()

    for i in range(COUNT_OF_IMAGES_TO_GRAB):
        if not cameras.IsGrabbing():
            break

        with cameras.RetrieveResult(
            RETRIEVE_TIMEOUT_MS,
            pylon.TimeoutHandling_ThrowException
        ) as result:

            if result.GrabSucceeded():
                cam_idx = result.GetCameraContext()
                print(f"Camera {cam_idx}: {cameras[cam_idx].DeviceInfo.ModelName}")
                image = result.Array.copy()
                # Do processing on image here, e.g. call a function.
		process(image)
            else:
                print("Error:", result.ErrorDescription)
```

---

### Why InstantCameraArray Is Important

Compared to manual looping, this approach provides:

- single acquisition loop for all cameras
- automatic camera context tracking (`GetCameraContext()`)
- simpler synchronization handling
- more efficient thread usage

Conceptually:

```text
Multiple Cameras → InstantCameraArray → Unified RetrieveResult() → Processing
```

---

## Practical Design Guidelines

- always identify cameras via serial number
- prefer hardware synchronization
- reduce bandwidth where possible (ROI, FPS)
- use separate processing threads for scalability
- monitor system load (CPU, network)

---

## Common Pitfalls

- relying on device index
- exceeding network bandwidth
- ignoring synchronization requirements
- blocking processing in acquisition loop

---

## Conceptual System Overview

```text
Multiple Cameras → Acquisition → Buffers → Processing → Results
```

---

## Key Takeaways

- multi-camera systems require careful design
- synchronization is critical for many applications
- bandwidth and CPU must be considered early
- scalable architectures use parallel processing

