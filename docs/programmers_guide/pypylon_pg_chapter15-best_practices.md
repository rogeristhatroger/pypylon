# 15. Best Practices

This chapter summarizes proven recommendations for building robust, efficient, and maintainable pypylon applications in production environments.

---

## Resource Management

Always ensure that camera resources are properly acquired and released.

```Python
with pylon.InstantCamera(pylon.FirstFound) as camera:
    # use camera
```

Benefits:

- automatic cleanup
- exception safety
- prevents resource leaks

---

## Device Identification

Never rely on device indices:

```Python
devices[0]  # not stable!
```

Instead, use unique identifiers:

- serial number
- user-defined name

---

## Performance Optimization

### Use Appropriate Grab Strategy

- `LatestImageOnly` → low latency
- `OneByOne` → complete processing

---

### Reduce Data at Source

- use ROI
- reduce resolution
- lower frame rate if possible

---

### Avoid Unnecessary Copies

- copy only when required
- reuse buffers when possible

---

## Threading Design

### Separate Acquisition and Processing

```PlainText
Camera → Queue → Processing
```

Benefits:

- better CPU utilization
- avoids blocking acquisition

---

### Use Producer–Consumer Pattern

- acquisition thread pushes images
- processing thread(s) consume them

---

### Use Thread-Safe Queues

```Python
import queue
q = queue.Queue()
```

---

## Multi-Stage Pipelines

Structure complex applications as pipelines:

```PlainText
Grab → Preprocess → Analyze → Output
```

Guidelines:

- each stage has one responsibility
- communicate via queues
- allow independent scaling per stage

---

## Error Handling

### Always Check Grab Success

```Python
if grab_result.GrabSucceeded():
    process(grab_result.Array)
else:
    log_error(grab_result.ErrorDescription)
```

---

### Handle Exceptions Gracefully

```Python
try:
    # acquisition code
    pass
except Exception as e:
    log_error(e)
```

---

### Implement Recovery Logic

```PlainText
Error → StopGrabbing → Retry → Continue
```

---

## Shutdown Strategy

Implement clean shutdown mechanisms:

- use `threading.Event`
- avoid blocking calls without timeout
- stop acquisition explicitly

```Python
stop_event.set()
camera.StopGrabbing()
```

---

## OpenCV Integration Rules

- run `imshow()` only in main thread
- avoid GUI in worker threads

---

## System Monitoring

Track key metrics:

- frame rate
- processing latency
- queue sizes
- CPU usage

---

## Configuration Management

- store camera parameters externally
- avoid hard-coded values
- validate configuration at startup

---

## Testing Recommendations

- test with real hardware
- simulate load conditions
- verify recovery behavior

---

## Common Pitfalls

- using image buffers after release
- blocking queues indefinitely
- ignoring synchronization requirements
- mixing UI and worker threads

---

## Conceptual Overview

```PlainText
Reliable system = correct architecture + error handling + performance tuning
```

---

## Key Takeaways

- design for robustness from the start
- separate concerns (acquisition vs processing)
- validate every external interaction
- plan for failure and recovery

---
