# 2. Installation and Environment Setup

## Install pylon SDK

Install the SDK from Basler before installing pypylon.

Recommended components:

- Runtime
- USB/GigE drivers
- pylon Viewer

## Install pypylon

```Shell
pip install pypylon
```

## Verify Installation

```Python
from pypylon import pylon

factory = pylon.TlFactory.GetInstance()
devices = factory.EnumerateDevices()

print("Detected:", len(devices))
```

## GigE Optimization

- Dedicated NIC
- Jumbo frames (MTU 9000)
- Disable energy saving

---
