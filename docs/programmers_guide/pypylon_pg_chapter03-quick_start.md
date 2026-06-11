# 3. Quick Start

This chapter provides a **gentle entry point** into pypylon by walking through a minimal working example and explaining *how the system behaves conceptually*. The goal is not only to show code that works, but to build an intuition you can reuse in more complex systems.

---

## What This Example Demonstrates

In its simplest form, image acquisition with pypylon follows a consistent pattern:

```PlainText
Discover camera → Open → Start grabbing → Retrieve image → Process
```

The example below performs exactly these steps once, which makes it ideal for:

- verifying that your installation works
- testing camera connectivity
- understanding the acquisition lifecycle

---

## Minimal Working Example

```Python
from pypylon import pylon

factory = pylon.TlFactory.GetInstance()

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.Open()

    camera.StartGrabbingMax(1)

    with camera.RetrieveResult(5000) as result:
        if result.GrabSucceeded():
            image = result.Array.copy()
            print(image.shape)
```

---

## Step-by-Step Explanation

### 1. Access the Factory

```Python
factory = pylon.TlFactory.GetInstance()
```

The **transport layer factory** is the entry point into the pylon ecosystem. It is responsible for:

- discovering cameras
- creating device instances
- abstracting the underlying transport (USB, GigE, etc.)

Think of it as a *device manager*.

---

### 2. Create and Manage the Camera

```Python
with pylon.InstantCamera(pylon.FirstFound) as camera:
```

This line does two important things:

- selects the **first available camera**
- wraps it in an `InstantCamera` object for easy use

`InstantCamera`

Using `with` ensures that:

- resources are released automatically
- the camera is properly closed even if an error occurs

---

### 3. Open the Camera

```Python
camera.Open()
```

Opening establishes the connection and transitions the camera into a state where:

- parameters can be configured
- acquisition can be started

---

### 4. Start Acquisition

```Python
camera.StartGrabbingMax(1)
```

This starts the acquisition engine and tells the camera to:

- acquire exactly **one frame**
- then stop automatically

This is ideal for testing because it avoids infinite loops.

---

### 5. Retrieve the Result

```Python
with camera.RetrieveResult(5000) as result:
```

This call blocks until:

- a frame is available **or**
- the timeout (5000 ms) is reached

Internally, you are pulling an image from a **buffer queue**.

---

### 6. Validate the Grab

```Python
if result.GrabSucceeded():
```

Even if a result is returned, the acquisition may have failed (e.g. transport errors). Always check success before using the data.

---

### 7. Copy the Image Data

```Python
image = result.Array.copy()
```

This is **critical**:

- `result.Array` points to a temporary buffer

`result.Array`

- the memory becomes invalid after leaving the `with` block

`with`

Copying ensures the image remains valid.

---

### 8. Use the Image

```Python
print(image.shape)
```

This simply confirms that:

- the image exists
- the data has a valid shape

---

## Mental Model: What Happens Internally

```PlainText
Camera (hardware)
      ↓
Transport layer (USB/GigE)
      ↓
pylon driver + buffers
      ↓
RetrieveResult()
      ↓
NumPy array (your application)
```

Key idea:

- the **camera runs asynchronously** (producing frames)
- your Python code **consumes frames synchronously**

Buffers sit in between and decouple both worlds.

---

## Key Takeaways

- Always open the camera explicitly
- Always check `GrabSucceeded()`

`GrabSucceeded()`

- Always copy image data before leaving the result scope
- Use `StartGrabbingMax(1)` for simple tests

`StartGrabbingMax(1)`

- Use `with` to ensure safe resource handling

`with`

Once you understand this pattern, you can scale it to:

- continuous acquisition loops
- triggered systems
- multi-camera setups

---
