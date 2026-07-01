# 6. Image Acquisition

## Continuous Acquisition

```Python
with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    while camera.IsGrabbing():
        with camera.RetrieveResult(5000) as grab_result:
            if grab_result.GrabSucceeded():
                image = grab_result.Array
```

---

## Grab Strategies (Overview)

Grab strategies define how images are handled in the internal buffer queue when the camera produces frames faster than the application consumes them.

In simple terms, they answer the question:

"What should happen if new images arrive while the application is still processing older ones?"

### Common Strategies

#### LatestImageOnly

- Only the newest image is kept
- Older frames may be discarded

#### OneByOne

- All frames are queued and processed in order
- No frames are dropped (unless buffers overflow)

---

### Conceptual Behavior

```PlainText
Camera → [F1, F2, F3, F4]

LatestImageOnly:
                → keep F4 only

OneByOne:
                → process F1 → F2 → F3 → F4
```

---

### When to Use Which?

- Use **LatestImageOnly** for:
    - live display
    - GUIs
    - low-latency systems
- Use **OneByOne** for:
    - inspection systems
    - recording
    - deterministic processing

👉 A detailed explanation of tradeoffs and internal behavior is provided in **Chapter 10 (Performance Optimization)**.

---
