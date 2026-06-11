# 7. Working with Images

This chapter explains how image data is represented in pypylon, how to safely access it, and how to prepare it for further processing (e.g. with NumPy, OpenCV, or AI frameworks).

---

## Image Representation

In pypylon, images are exposed as **NumPy arrays**, which makes them directly usable in scientific and machine vision workflows.

Typical flow:

```PlainText
Camera → GrabResult → Buffer → NumPy Array
```

---

## Accessing Image Data

```Python
img = result.Array.copy()
```

### Why .copy() is Important

- `result.Array` is a **view into an internal buffer**
- The buffer is released when leaving the `with` block
- Accessing the array afterward can lead to invalid memory access

✅ Correct usage:

```Python
with camera.RetrieveResult(5000) as result:
    if result.GrabSucceeded():
        img = result.Array.copy()
```

---

## Image Shape and Format

The shape of the array depends on the pixel format:

| Pixel Format | Shape Example |
| --- | --- |
| Mono8 | (height, width) |
| RGB8/BGR8 | (height, width, 3) |

You can inspect the shape directly:

```Python
print(img.shape)
```

---

## Pixel Format Conversion

Depending on the camera configuration, the raw image format may not be directly usable.

Example: converting to BGR (OpenCV-compatible)

```Python
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed

img = converter.Convert(result).GetArray()
```

### Why Conversion Is Needed

- Cameras often output raw or Bayer formats
- Applications typically expect: 
    - BGR (OpenCV)
    - RGB (visualization)

---

## Common Pitfalls

### 1. Using Data After Buffer Release

```Python
with camera.RetrieveResult(...) as result:
    img = result.Array

# ❌ Unsafe: img may now reference invalid memory
```

✅ Always use `.copy()` if needed outside the block.

---

### 2. Ignoring Pixel Format

- Wrong color interpretation
- Incorrect processing results

Always verify or explicitly set the format.

---

### 3. Performance Overheads

- Copying large images costs time
- Conversion adds CPU load

Strategies:

- reduce ROI (see Chapter 8)
- avoid unnecessary conversions

---

## Integration with Processing Pipelines

Because images are NumPy arrays, they can be used directly with:

### OpenCV

```Python
import cv2

cv2.imshow("image", img)
cv2.waitKey(1)
```

### NumPy Operations

```Python
mean = img.mean()
```

### AI / ML Frameworks

- PyTorch
- TensorFlow

---

## Conceptual Pipeline

```PlainText
Camera → GrabResult → NumPy Array → Processing → Output
```

This is the central data flow of most computer vision systems.

---

## Key Takeaways

- Images are provided as NumPy arrays
- Always copy buffer data when needed
- Be aware of pixel formats
- Conversion may be required for downstream processing

---

## Practical NumPy Example (Meaningful Image Processing)

The following example demonstrates how to perform a small but realistic image processing pipeline using NumPy.

### Example Code

```Python
import numpy as np
from pypylon import pylon

# Create camera
factory = pylon.TlFactory.GetInstance()

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.Open()

    camera.StartGrabbingMax(100)

    while camera.IsGrabbing():
        with camera.RetrieveResult(5000) as result:
            if result.GrabSucceeded():
                img = result.Array.copy()

                if img.ndim == 3:
                    gray = img.mean(axis=2)
                else:
                    gray = img

                norm = gray / 255.0

                binary = norm > 0.5

                mean_intensity = norm.mean()
                bright_pixel_ratio = binary.mean()

                print(f"Mean intensity: {mean_intensity:.3f}")
                print(f"Bright pixels: {bright_pixel_ratio*100:.1f}%")
```

---

## Step-by-Step Explanation

### Grayscale Conversion

```Python
gray = img.mean(axis=2)
```

### Normalization

```Python
norm = gray / 255.0
```

### Thresholding

```Python
binary = norm > 0.5
```

### Statistical Evaluation

```Python
mean_intensity = norm.mean()
bright_pixel_ratio = binary.mean()
```

---

## Conceptual Pipeline

```PlainText
Raw Image → NumPy Array → Processing → Features → Decision
```

---

## Why This Matters

NumPy enables fast, vectorized image processing directly on acquired images.
