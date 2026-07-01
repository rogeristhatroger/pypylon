# 1. Introduction

## What is pypylon?

pypylon is the official Python language binding for the Basler pylon C++ APIs. It enables Python applications to control and acquire images from Basler machine vision products, e.g. cameras.

## Use Cases

- Machine vision systems
- Robotics and automation
- Scientific imaging
- Quality inspection
- AI pipelines
- and many more...

## Software Stack

```PlainText
Python Application
     ↓
pypylon (Python API)
     ↓
pylon SDKs (C++)
     ↓
GenTL and pylon Transport Layer
     ↓
Camera and Grabber Hardware
```

Understanding this layered architecture helps debug issues (driver, transport, or application level).

---
