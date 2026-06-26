# 16. Troubleshooting

This chapter helps diagnose and resolve common issues encountered when working with pypylon and industrial cameras. It focuses on practical debugging strategies and typical failure scenarios.

---

## Typical Symptoms and Causes

| Symptom | Possible Cause |
| --- | --- |
| No camera detected | Driver missing, cable issue, SDK not installed |
| Timeout in `RetrieveResult()` | Trigger misconfiguration, no signal, wrong timeout |
| Dropped frames | Bandwidth limitation, slow processing |
| Grab errors | Network instability, packet loss |
| Application freezes | Blocking calls, deadlocks, queue overflow |

---

## Camera Detection Issues

### Check Hardware

- verify cable connection
- verify camera power
- try a different USB port or Ethernet cable

### Check Software

- ensure pylon SDK is installed
- verify drivers are loaded
- test with pylon Viewer

---

## Timeout Problems

### Common Causes

- Trigger mode enabled but no trigger signal
- Exposure time too long
- Timeout value too low

### Debug Strategy

```Python
camera.TriggerMode
camera.TriggerSource
```

Disable trigger for testing:

```Python
camera.TriggerMode.Value = "Off"
```

---

## Grab Errors

### Symptoms

```Python
if not grab_result.GrabSucceeded():
    print(grab_result.ErrorDescription)
```

### Typical Causes

- network congestion (GigE)
- insufficient bandwidth
- unstable connection

---

## Image Corruption and Frame Loss

### Causes

- packet loss (GigE cameras)
- CPU overload
- insufficient buffers

### Mitigation

- enable jumbo frames
- increase `MaxNumBuffer`
- reduce ROI or FPS

---

## Performance Issues

### Signs

- rising latency
- increasing queue sizes
- dropped frames

### Debug Strategy

- measure FPS
- monitor CPU usage
- inspect queue sizes

---

## Threading Problems

### Common Issues

- deadlocks due to blocking `queue.get()`
- threads not stopping on shutdown

### Fixes

- use timeouts:

```Python
q.get(timeout=0.1)
```

- use stop signals:

```Python
stop_event = threading.Event()
```

---

## OpenCV GUI Issues

### Symptoms

```PlainText
QObject::killTimer error
```

### Cause

- GUI functions executed in worker thread

### Fix

- run `cv2.imshow()` only in main thread

---

## Network Issues (GigE)

### Symptoms

- packet loss
- frame drops

### Mitigation

- use dedicated NIC
- enable jumbo frames
- adjust packet delay

---

## Debugging Checklist

- is the camera detected?
- does pylon Viewer work?
- is TriggerMode correct?
- is bandwidth sufficient?
- is CPU overloaded?
- are queues blocking?

---

## Logging Recommendations

Use structured logging instead of print:

```Python
import logging
logging.exception("Camera error")
```

---

## Conceptual Debug Model

```PlainText
Hardware → Transport → Driver → Application
```

Identify which layer causes the issue.

---

## Key Takeaways

- most issues are configuration or timing related
- always isolate hardware vs software problems
- monitor system resources continuously
- use systematic debugging approach

---
