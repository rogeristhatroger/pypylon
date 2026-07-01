# 2. Installation and Environment Setup

## Install pylon SDK

Install the pylon software suite from Basler together with installing pypylon and required supplementary packages, e.g. for 3D cameras.

Note: The pypylon wheel package already includes the pylon C++ runtimes and vTools. It works immediately for transport layers that don’t require any extra drivers.


Recommended components:

- USB/GigE drivers
- CXP GenTL producer and drivers (if using CXP cameras)
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
