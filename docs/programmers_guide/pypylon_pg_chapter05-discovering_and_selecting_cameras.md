# 5. Discovering and Selecting Cameras

Before an application can use a camera, it must first *discover* which cameras are available on the system. This process is called **enumeration**.

## Why Enumeration Exists

Unlike consumer cameras (e.g. webcams), industrial cameras are not automatically tied to a single application. Instead:

- Multiple cameras may be connected at the same time
- Cameras may be connected via different transport layers (USB, GigE, etc.)
- Cameras may appear/disappear dynamically (hot-plugging, network changes)

Enumeration allows your application to:

- detect all currently available cameras
- identify them reliably
- select the correct one for your task

### Conceptual View

```PlainText
System Startup
     ↓
Transport Layers scan for devices
     ↓
Detected Camera List (Enumeration)
     ↓
Application selects a camera
```

---

## Enumerating Cameras

```Python
factory = pylon.TlFactory.GetInstance()
```

The **transport layer factory** is the entry point into the pylon ecosystem. It is responsible for:

- discovering cameras
- creating device instances
- abstracting the underlying transport (USB, GigE, etc.)

Think of it as a *device manager*.


```Python
device_info_list = factory.EnumerateDevices()
```

This returns a list of device descriptors. Each entry contains metadata about a detected camera, such as:

- model name
- serial number (unique identifier)
- interface type (USB, GigE)

Example:

```Python
for device_info in device_info_list:
    print(device_info.GetFriendlyName())
    print(device_info.GetSerialNumber())
```

---

## Selecting a Camera

### By Serial Number (Recommended)

```Python
serial_number = "123456"

for device_info in device_info_list:
    if device_info.GetSerialNumber() == serial_number:
        camera = pylon.InstantCamera(factory.CreateDevice(device_info))
```

### Why Not Use Index?

⚠️ Never rely on index order. It changes depending on the number of cameras connected.

```Python
device_info_list[0]
```

---

## Practical Use Cases

### Single Camera System

- Simply use `pylon.InstantCamera(pylon.FirstFound)`

- sufficient for testing or simple setups
- for single camera use cases you can let pylon find your camera by passing the required properties as a dictionary
- for multiple cameras it is recommended to first enumerate and then select the desired camera by its unique identifier, e.g. serial number to avoid the overhead of multiple device enumerations

```Python
camera = pylon.InstantCamera({pylon.SerialNumberKey : serial_number}, pylon.FirstFound)
```

### Multi-Camera System

- enumerate all cameras
- map by serial number or user-defined name

### Production Systems

- store camera identifiers in configuration files
- validate presence at startup
- fail fast if expected camera is missing

---

## Key Takeaway

Enumeration is essential because it makes your application:

- robust to hardware changes
- independent of connection order
- scalable to multiple cameras

Without proper enumeration, systems become fragile and difficult to maintain.

---
