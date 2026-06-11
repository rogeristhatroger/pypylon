
# 9. Triggered Acquisition

Triggered acquisition is used when image capture must happen at a **specific, well-defined moment in time**, rather than continuously.

In many machine vision systems, it is not sufficient to simply grab images at a fixed frame rate. Instead, images need to be synchronized with external events such as:

- a moving object reaching a specific position
- a sensor detecting a part
- a PLC signal in an automation system
- a lighting pulse or strobe event

## When to Use Triggered Acquisition

Use triggered acquisition when:

- **Timing is critical**
  - The image must correspond exactly to a physical event

- **Motion must be frozen precisely**
  - e.g. capturing fast-moving objects at the same position

- **External systems control the process**
  - PLCs, sensors, encoders, or other hardware define when to capture

- **Deterministic behavior is required**
  - Each trigger results in exactly one frame with defined timing

## Why It Matters

Without triggering the camera runs freely and frames may miss the relevant moment.

With triggering an external event triggers the camera which results in an capturing the object at the exacty right moment.

This ensures that:

- images are synchronized with the real world
- measurements are repeatable
- systems behave deterministically

## Typical Use Cases

| Use Case | Why Triggering is Needed |
|----------|--------------------------|
| Conveyor belt inspection | Capture part at exact position |
| High-speed sorting | Precise timing per object |
| Robotics | Synchronize with robot motion |
| Measurement systems | Ensure repeatable acquisition |

---

## Workflow

```text
Trigger → Exposure → Readout → Transfer → App
```

The **trigger** lets the camera start an **exposure** that is than **read out** from the sensor, being preprocessed, **transfered** to the host and then passed on to the **application**.

---

## Software Trigger

A **software trigger** lets you start an **exposure** via a software call instead of an external hardware event. This might me interessting when the source is not a hardware event but a state change of the computing system. This might not be as precise as a hardware trigger but well enough for the problem and easier than connecting an output from the computing system to the camera or cameras.

```python
camera.TriggerMode.Value = "On"
camera.TriggerSource .Value = "Software"
camera.TriggerSelector.Value = "FrameStart"

camera.ExecuteSoftwareTrigger()
```

### Complete Example: Periodic Software Trigger (1 Hz)

The following example uses a software trigger to start the exposure of an image every second.

```python
import time
from pypylon import pylon

def process(image):
    h, w = image.shape[:2]
    center_pixel = image[h // 2, w // 2]
    print("Center pixel:", center_pixel)

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.Open()

    # Enable trigger mode
    camera.TriggerSelector.Value = "FrameStart"
    camera.TriggerMode.Value = "On"
    camera.TriggerSource.Value = "Software"

    camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

    try:
        while camera.IsGrabbing():
            camera.ExecuteSoftwareTrigger()

            with camera.RetrieveResult(2000) as result:
                if result.GrabSucceeded():
                    img = result.Array.copy()
                    process(img)
                else:
                    print("Grab failed:", result.ErrorDescription)

            time.sleep(1.0)

    finally:
        camera.StopGrabbing()
```

---

## Hardware Trigger

If a **software trigger** is not precise enough for the problem or an hardware signal is allready available it might be nessesary or easier to use a **hardware trigger**. In this case, **depending on the camera model** there are one or more inputs available that can act as a **trigger input**. A **rising edge** or **falling edge** can be used to trigger an event like **start of exposure** of the camera.

```python
camera.TriggerSource.Value = "Line1"
camera.TriggerSelector.Value = "FrameStart"
camera.TriggerActivation.Value = "RisingEdge"
```

### Complete Example: Hardware Trigger Acquisition

The following example uses the input "Line1" on the first camera found to start the exposure and outputs the center pixel.

```python
from pypylon import pylon

def process(image):
    h, w = image.shape[:2]
    center_pixel = image[h // 2, w // 2]
    print("Center pixel:", center_pixel)

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.Open()

    # Configure hardware trigger
    camera.TriggerSelector.Value = "FrameStart"
    camera.TriggerMode.Value = "On"
    camera.TriggerActivation.Value = "RisingEdge"
    camera.TriggerSource.Value = "Line1"

    camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

    try:
        while camera.IsGrabbing():
            with camera.RetrieveResult(5000) as result:
                if result.GrabSucceeded():
                    img = result.Array.copy()
                    process(img)
                else:
                    print("Grab failed:", result.ErrorDescription)

    finally:
        camera.StopGrabbing()
```
