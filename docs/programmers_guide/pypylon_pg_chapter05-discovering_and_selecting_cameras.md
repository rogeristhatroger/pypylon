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
devices = pylon.TlFactory.GetInstance().EnumerateDevices()
```

This returns a list of device descriptors. Each entry contains metadata about a detected camera, such as:

- model name
- serial number (unique identifier)
- interface type (USB, GigE)

Example:

```Python
for d in devices:
    print(d.GetFriendlyName())
    print(d.GetSerialNumber())
```

---

## Selecting a Camera

### By Serial Number (Recommended)

```Python
serial = "123456"

for d in devices:
    if d.GetSerialNumber() == serial:
        cam = pylon.InstantCamera(factory.CreateDevice(d))
```

### Why Not Use Index?

⚠️ Never rely on index order.

```Python
devices[0]
```

This is unreliable because:

- enumeration order may change
- devices may be added or removed
- USB/GigE discovery timing varies

---

## Practical Use Cases

### Single Camera System

- Simply use `pylon.InstantCamera(pylon.FirstFound)`

- sufficient for testing or simple setups

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
