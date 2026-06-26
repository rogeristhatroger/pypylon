# 12. Threading and Concurrency

This chapter explains how threading and concurrency are used in pypylon applications, and how to structure acquisition and processing pipelines for performance and scalability.

---

## Conceptual Model

```text
Camera → Native Thread → Buffer Queue → Python Application
```

- The camera acquisition runs in a **native (C++) thread** inside pylon
- Your Python code retrieves images from a **buffer queue**
- This separation enables asynchronous acquisition

---

## Why Threading Matters

In many applications, image acquisition is faster than processing:

```text
Camera → 100 FPS
Processing → 20 FPS
```

Without concurrency:

- buffers fill up
- frames are dropped
- latency increases

---

## Basic Execution Model

### Single-Threaded Approach

```text
Acquire → Process → Acquire → Process
```

Example:

```python
while camera.IsGrabbing():
    with camera.RetrieveResult(5000) as grab_result:
        if grab_result.GrabSucceeded():
            image = grab_result.Array
            process(image)
```

### Limitations

- processing blocks acquisition
- poor CPU utilization
- limited scalability

---

## Producer–Consumer Pattern (Recommended)

```text
Acquisition Thread → Queue → Worker Thread(s)
```

### Concept

- **Producer**: grabs images and pushes them into a queue
- **Consumer**: processes images independently

---

## Example Implementation using an own Thread

Node: You can use the grab loop thread provided by the InstantCamera (see the grab_using_grab_loop_thread sample), but here is a custom implementation for demonstration:

```python
import threading
import queue
from pypylon import pylon

def process(image):
    print(image.shape)

image_queue = queue.Queue(maxsize=10)

# Producer thread
def grab_loop(camera):
    while camera.IsGrabbing():
        with camera.RetrieveResult(5000) as grab_result:
            if grab_result.GrabSucceeded():
                image = grab_result.Array
                image_queue.put(image)

# Consumer thread
def process_loop():
    while True:
        image = image_queue.get()
        process(image)
        image_queue.task_done()

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.StartGrabbing()

    grab_thread = threading.Thread(target=grab_loop, args=(camera,))
    processing_thread = threading.Thread(target=process_loop)

    grab_thread.start()
    processing_thread.start()

    grab_thread.join()
    image_queue.join()
```

---

## Queue Behavior and Backpressure

```text
Queue full → producer blocks → acquisition slows down
```

Strategies:

- increase queue size
- drop frames manually
- use `LatestImageOnly`

---

## Combining with Grab Strategies

- `LatestImageOnly` → reduces backlog
- `OneByOne` → ensures completeness

Best practice:

```text
LatestImageOnly + queue → responsive systems
OneByOne + logging → analysis systems
```

---

## Thread Safety Considerations

- avoid sharing mutable data without locks
- copy images before passing to other threads, e.g. by using the Array function.
- use `queue.Queue` for safe communication

---

## CPU Utilization

Parallel processing allows:

- better CPU usage
- separation of concerns
- scalable architectures

```text
Core 1 → Acquisition
Core 2 → Processing
Core 3 → AI
```

---

## When to Use Multiple Threads

Use threading when:

- processing is slower than acquisition
- multiple processing stages exist
- real-time responsiveness is required

Avoid threading when:

- processing is trivial
- system complexity must be minimal

---

## Advanced Patterns (Overview)

### Multi-Stage Pipeline

A multi-stage pipeline splits image processing into independent steps that run concurrently and exchange data via queues.

```text
Grab → Preprocess → Analyze → Display
```

---

### Multi-Consumer Setup

```text
Producer → Queue → multiple processing threads
```

---

## Conceptual Pipeline

```text
Camera → Queue → Processing → Results
```

---

## Key Takeaways

- acquisition and processing should be decoupled
- use producer-consumer pattern for scalability
- queues provide safe thread communication
- threading improves performance but increases complexity

---
