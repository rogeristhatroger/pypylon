# 11. Error Handling and Recovery

Industrial camera systems operate in environments where failures are not only possible but expected. Unlike typical desktop applications, these systems often run continuously and interact with external hardware.

Typical sources of errors include:

- network interruptions, especially with GigE cameras
- USB disconnects
- missing or unstable trigger signals
- CPU overload or slow image processing
- bandwidth limitations
- invalid or state-dependent camera configuration

Because of this, error handling is not optional — it is a core part of system design.

---

## Why Error Handling is Important

In real-world systems, a camera application may run for hours, days, or continuously in production.

```PlainText
System starts → runs normally → transient failure occurs
```

Without proper handling:

```PlainText
Unhandled exception → application crashes → acquisition stops
```

With proper handling:

```PlainText
Failure → detect → recover → continue
```

The goal is not to prevent every possible failure. The goal is to make failures visible, controlled, and recoverable.

---

## Types of Errors in pypylon

Different error types require different handling strategies.

---

### 1. Grab Errors — Frame-Level Failures

A grab error means that a grab result was returned, but the image itself is not valid.

```Python
with camera.RetrieveResult(2000) as result:
    if result.GrabSucceeded():
        image = result.Array.copy()
    else:
        print(result.ErrorCode)
        print(result.ErrorDescription)
```

Typical causes:

- packet loss on GigE connections
- insufficient bandwidth
- temporary transport-layer problems
- camera or driver instability

This kind of error often affects only a single frame. The application can usually log the problem, skip the frame, and continue acquisition.

---

### 2. Timeout Errors — No Frame Arrived

A timeout occurs when `RetrieveResult()` waits for an image, but no image arrives within the configured timeout.

```Python
with camera.RetrieveResult(
    1000,
    pylon.TimeoutHandling_ThrowException
) as result:
    image = result.Array.copy()
```

Typical causes:

- trigger mode is enabled, but no trigger signal arrives
- the camera is not grabbing
- exposure time is longer than expected
- the timeout value is too short
- the camera configuration is inconsistent

Timeouts are especially common in triggered systems. A timeout does not always mean the camera is broken; it often means that the application is waiting for an event that never happened.

---

### 3. Runtime Exceptions — System-Level Failures

Runtime exceptions indicate that something outside a single image failed.

Examples include:

- camera unplugged
- network connection lost
- device reset
- invalid camera state
- invalid parameter access

```Python
try:
    # acquisition code
    pass
except Exception as e:
    print("Camera error:", e)
```

These errors usually require recovery logic, such as stopping acquisition, waiting, re-enumerating cameras, or reopening the device.

---

## Error Handling Strategies

A robust system usually combines multiple strategies.

---

### Strategy 1: Per-Frame Handling

Use this when the camera is still running, but individual frames may fail.

```Python
with camera.RetrieveResult(2000) as result:
    if result.GrabSucceeded():
        process(result.Array.copy())
    else:
        log_error(result.ErrorDescription)
```

This approach is useful when occasional frame loss is acceptable. It keeps the acquisition loop alive and avoids stopping the whole system for one bad image.

Typical use cases:

- live display
- monitoring systems
- non-critical image streams

---

### Strategy 2: Exception Handling

Use `try` / `except` around operations that may fail at runtime.

```Python
try:
    with camera.RetrieveResult(
        2000,
        pylon.TimeoutHandling_ThrowException
    ) as result:
        if result.GrabSucceeded():
            process(result.Array.copy())

except Exception as e:
    print("Error:", e)
```

This prevents the application from crashing immediately. However, catching the exception alone is not enough. The application must also decide whether to continue, retry, reset acquisition, or shut down safely.

---

### Strategy 3: Recovery Loop — Recommended Pattern

A recovery loop combines error detection with automatic recovery.

```Python
import time

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.Open()

    while True:
        try:
            if not camera.IsGrabbing():
                camera.StartGrabbing()

            with camera.RetrieveResult(
                2000,
                pylon.TimeoutHandling_ThrowException
            ) as result:

                if result.GrabSucceeded():
                    image = result.Array.copy()
                    process(image)
                else:
                    log_error(result.ErrorDescription)

        except Exception as e:
            log_error(f"Acquisition error: {e}")

            if camera.IsGrabbing():
                camera.StopGrabbing()

            time.sleep(0.5)
```

---

## What the Recovery Loop Actually Does

```PlainText
1. Acquisition runs normally
2. An error occurs
3. An exception is raised
4. The exception handler logs the problem
5. StopGrabbing() resets the acquisition pipeline
6. The application waits briefly
7. The loop retries acquisition
```

This pattern allows a system to recover from temporary failures without manual intervention.

---

## Why StopGrabbing() Matters

After an acquisition error, internal buffers or the grabbing state may no longer represent a clean acquisition pipeline.

```PlainText
Error → uncertain acquisition state → reset required
```

Calling `StopGrabbing()` helps to:

- stop the current acquisition operation
- release or recycle internal buffers
- prepare the camera for a clean restart

This does not solve every possible hardware failure, but it is often the first safe recovery step.

---

## Camera Disconnect Handling

A physical disconnect is one of the most important real-world failure cases.

```PlainText
Camera unplugged → communication lost → exception
```

A robust application should assume that hardware can disappear at any time.

A typical recovery sequence is:

```PlainText
Detect error
   ↓
Stop acquisition
   ↓
Wait briefly
   ↓
Re-enumerate cameras if needed
   ↓
Reconnect or report fatal failure
```

For production systems, reconnect logic is often implemented at a higher level than the basic grab loop.

---

## Resource Safety

Using `with` for grab results is essential.

```Python
with camera.RetrieveResult(...) as result:
    image = result.Array.copy()
```

This ensures that the grab result is released even if an exception occurs inside the block.

Without proper cleanup:

```PlainText
Unreleased grab results → buffers unavailable → acquisition stalls
```

This is why all examples in this guide use context managers for grab results.

---

## Logging Instead of Printing

For examples, `print()` is simple and readable. In production, prefer the Python `logging` module.

```Python
import logging

logging.exception("Camera acquisition failed")
```

Logging provides timestamps, severity levels, persistent files, and better diagnostics for long-running systems.

---

## Recoverable vs Fatal Errors

Not all errors should be handled the same way.

| Error | Typical Handling |
| --- | --- |
| Single failed frame | Log and continue |
| Timeout in trigger mode | Check trigger configuration or retry |
| Temporary bandwidth issue | Log, reduce load, continue |
| Camera disconnected | Stop, re-enumerate, reconnect |
| Missing required camera at startup | Fail fast |
| Invalid configuration | Stop and report error |

A production application should clearly distinguish between errors that can be retried and errors that require operator intervention.

---

## Key Takeaways

- Errors are normal in industrial environments
- Handle both frame-level errors and system-level exceptions
- Use timeouts deliberately
- Use `with` to guarantee resource cleanup

`with`

- Implement recovery loops for unattended systems
- Use logging and clear error classification in production

A well-designed error handling strategy enables stable, autonomous camera applications.

---
