# 10. Performance Optimization

## Why Grab Strategies Exist

Industrial cameras often produce images at a constant and potentially very high rate (e.g. 60–200+ FPS). In many applications, the processing pipeline (Python, OpenCV, AI inference, etc.) cannot keep up with this rate.

This creates a fundamental mismatch:

```PlainText
Camera (Producer) → fast
Application (Consumer) → slower
```

Without a strategy, buffers would either:

- grow indefinitely (not possible)
- overflow randomly (undesirable)

Grab strategies define **how the system behaves under load**.

---

## Internal Model

```PlainText
Camera → Frame Stream → Buffer Queue → RetrieveResult() → Application
```

If the application is slower than the camera:

```PlainText
Queue fills up → decision required
```

This is where the grab strategy applies.

---

## Strategy Behavior in Detail

### LatestImageOnly

**Behavior:**

- Keeps only the most recent frame
- Older frames are dropped while the application is busy

**Timeline Example:**

```PlainText
Camera:    F1 → F2 → F3 → F4
App reads:        →    F4
Dropped:   F1, F2, F3
```

**Implications:**

- ✅ Always see the most recent state
- ✅ Minimal latency
- ❌ Frame loss occurs

**Typical Use Cases:**

- Live display (GUI)
- Operator monitoring
- Real-time visualization

---

### OneByOne

**Behavior:**

- Every frame is queued and processed in order
- No frames are intentionally dropped

**Timeline Example:**

```PlainText
Camera:    F1 → F2 → F3 → F4
App reads: F1 → F2 → F3 → F4
```

**Implications:**

- ✅ No frame loss (ideal for analysis/recording)
- ✅ Deterministic processing order
- ❌ Higher latency if processing is slow
- ❌ Risk of buffer overflow if sustained overload

**Typical Use Cases:**

- Inspection systems
- Image recording
- Measurement tasks

---

## Tradeoff: Latency vs Completeness

| Strategy | Latency | Frame Loss | Determinism |
| --- | --- | --- | --- |
| LatestImageOnly | Low | Yes | Low |
| OneByOne | High (if slow) | No | High |

---

## Buffer Configuration

Buffers act as a temporary reservoir between camera and application.

```Python
camera.MaxNumBuffer = 20
```

Increasing buffers:

- ✅ tolerates temporary slowdowns
- ❌ increases memory usage
- ❌ increases latency (queue grows)

---

## When to Use Which Strategy

### Use LatestImageOnly if:

- you need *current* information
- frame drops are acceptable
- latency must be minimal

### Use OneByOne if:

- every frame matters
- results must be reproducible
- processing speed ≈ acquisition speed

---

## Key Insight

There is no "best" strategy.

The correct choice depends on whether your system prioritizes:

- **freshness (low latency)** → LatestImageOnly
- **completeness (no loss)** → OneByOne

---
