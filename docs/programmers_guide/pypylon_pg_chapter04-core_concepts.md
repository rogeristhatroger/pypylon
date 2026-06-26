# 4. Core Concepts

## Acquisition Lifecycle

```PlainText
Camera → Transport → Buffer Queue → Application
                         ↑
                   RetrieveResult()
```

### Mental Model

- Camera runs asynchronously
- Python retrieves synchronously
- Buffers decouple both domains

---

## Blocking Behavior

```PlainText
RetrieveResult() → waits until frame or timeout
```

Slow processing leads to backlog and dropped frames.

---

## GenICam Nodes

### What is a GenICam Node?

A *GenICam Node* represents a single configurable feature or property of a camera. Nodes are part of the GenICam standard, which provides a uniform way to access camera functionality independent of the hardware vendor.

Each node behaves like a strongly-typed parameter and exposes:

- a name (e.g. `ExposureTime`)

`ExposureTime`

- a data type (float, integer, enum, etc.)
- access rights (read-only or read/write)
- valid value ranges or options

In pypylon, nodes are accessed as attributes of the camera object and provide methods like:

```Python
exposure_time = camera.ExposureTime   # read exposure time in microseconds
camera.ExposureTime.Value = 3000  # value is in microseconds; check Increment and ValueRange for valid precision
```

### Common Node Types

- Float: ExposureTime (continuous values, continuous-like values that map to discrete hardware settings)
- Integer: Width (discrete values)
- Enum: TriggerMode (predefined string values)
- Bool: AcquisitionFrameRateEnable (true/false)
- Command: ExecuteSoftwareTrigger (executes an action)

Understanding nodes is essential because *all camera configuration in pypylon is performed through them*.

### pylon Parameters

pylon parameters wrap GenICam nodes and provide an extended consistent interface for reading and writing values. They also handle type conversion, range checking, and access mode handling.

If a node is not found the `pylon.PlaceholderParameter` is returned, which allows your code to handle missing nodes gracefully. This is often a scenario in setups where different camera models or firmware versions may have different available features.

```Python
var = camera.NotThere.GetValueOrDefault(1)
camera.NotThere.TrySetValue(3000)
```
---

## State Constraints

Some settings require acquisition to stop:

```Python
camera.StopGrabbing()
camera.Width.Value = 640
camera.StartGrabbing()
```

---
