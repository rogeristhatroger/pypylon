# 1. Introduction

## What is pypylon?

pypylon is the official Python wrapper for the Basler pylon Camera Software Suite. It enables Python applications to control and acquire images from Basler industrial cameras using the GenICam standard.

## Use Cases

- Machine vision systems
- Robotics and automation
- Scientific imaging
- Quality inspection
- AI pipelines

## Software Stack

```PlainText
Python Application
     ↓
pypylon (Python API)
     ↓
pylon SDK (C++)
     ↓
GenTL Transport Layer
     ↓
Camera Hardware
```

Understanding this layered architecture helps debug issues (driver, transport, or application level).

---
