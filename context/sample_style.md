# Sample Style

This file defines a common style for pypylon samples.

## Header

Every sample begins with the following shebang line:
```python
#!/usr/bin/env python3
```

This is followed by the module docstring. The docstring starts with a brief
one-line description, followed by a more detailed explanation. Example:
```python
"""\
This sample illustrates how to grab and process images using InstantCamera.

Images are grabbed and processed asynchronously: while the application handles
one buffer, acquisition of the next buffer can proceed in parallel.

InstantCamera uses a pool of buffers to retrieve image data from the device.
When a buffer is ready, you get a grab result; call Release() on it when
finished so the buffer can be reused.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
```

## Base Structure

A sample's base structure after the header looks like this:

```python
import sys
from pypylon import pylon

# Add constants here, if applicable.

exit_code = 0
try:
    # Add the actual sample code here.
except BaseException as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
```

## Style

The common style rules in [common_style.md](common_style.md) apply.
The following additional rules are specific to samples:

- **Exit code.** Initialize `exit_code = 0` before the `try` block and set it
  to a non-zero value inside the `except` block. Pass it to `sys.exit()` at the
  end of the script.

- **Import order.** Place standard-library imports first (`import sys`), then
  pypylon imports (`from pypylon import pylon`, `from pypylon import genicam`),
  then any other third-party imports. Import only the modules that are actually
  used in the sample.

- **Avoid abbreviations in identifiers.** Use descriptive names for variables,
  functions, and classes, and avoid abbreviations that may be unclear to readers.
  For example, use `exposure_time` instead of `exp_time`, and use
  `CameraConfiguration` instead of `CamConfig`.

- **Prefer properties and shorthand helpers over verbose getters/setters.**
  Use the Pythonic property syntax and convenience shortcuts provided by
  pypylon instead of the underlying C++ style accessor methods. Examples:

  | Avoid | Prefer |
  |---|---|
  | `pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())` | `pylon.InstantCamera(pylon.FirstFound)` |
  | `camera.GetDeviceInfo().GetModelName()` | `camera.DeviceInfo.ModelName` |
  | `grab_result.GetWidth()` | `grab_result.Width` |
  | `grab_result.GetHeight()` | `grab_result.Height` |
  | `grab_result.GetErrorCode()` | `grab_result.ErrorCode` |
  | `grab_result.GetErrorDescription()` | `grab_result.ErrorDescription` |

- **Use context managers for cameras and grab results.** Where possible, use
  `with` statements to ensure cameras are closed and grab results are released
  automatically. For example:
  ```python
  with pylon.InstantCamera(pylon.FirstFound) as camera:
      ...
  # The camera is automatically closed here
  ```
  Similarly for grab results:
  ```python
  with camera.RetrieveResult(timeout_ms, pylon.TimeoutHandling_ThrowException) as grab_result:
      if grab_result.GrabSucceeded():
          img = grab_result.Array
          ...
  # The grab result is automatically released here
  ```
