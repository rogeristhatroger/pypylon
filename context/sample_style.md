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
except Exception as e:
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

- **Catch `Exception`, not `BaseException`.** The top-level handler must use
  `except Exception as e:` so that `SystemExit` (from `sys.exit()`) and
  `KeyboardInterrupt` propagate normally without an extra `except SystemExit:
  raise` guard.

- **Import order.** Place standard-library imports first (`import sys`), then
  pypylon imports (`from pypylon import pylon`, `from pypylon import genicam`),
  then any other third-party imports. Import only the modules that are actually
  used in the sample.

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
  | `grab_result.GetPixelType()` | `grab_result.PixelType` |
  | `grab_result.GetBlockID()` | `grab_result.BlockID` |
  | `image.GetBuffer()` | `image.Buffer` |
  | `image.GetPixelType()` | `image.PixelType` |
  | `camera.DeviceInfo.GetDeviceClass()` | `camera.DeviceInfo.DeviceClass` |
  | `param.GetMin()` | `param.Min` |
  | `param.GetMax()` | `param.Max` |
  | `param.GetInc()` | `param.Inc` |

  The same principle applies to **pylondataprocessing** types:

  | Avoid | Prefer |
  |---|---|
  | `variant.GetErrorDescription()` | `variant.ErrorDescription` |
  | `variant.GetDataType()` | `variant.DataType` |
  | `variant.GetContainerType()` | `variant.ContainerType` |
  | `variant.GetNumArrayValues()` | `variant.NumArrayValues` |
  | `variant.GetArrayValue(i)` | `variant[i]` |
  | `region.GetReferenceHeight()` | `region.ReferenceHeight` |
  | `region.GetDataSize()` | `region.DataSize` |
  | `region.GetRegionType()` | `region.RegionType` |
  | `result_collector.GetWaitObject()` | `result_collector.WaitObject` |

- **Use `.Value` property for straightforward parameter reads and writes.**
  Camera parameter nodes support a `.Value` property that is more Pythonic
  than the `.GetValue()` / `.SetValue()` methods. Prefer `.Value` for
  simple reads and unconditional writes:

  | Avoid | Prefer |
  |---|---|
  | `camera.PixelFormat.SetValue("Mono8")` | `camera.PixelFormat.Value = "Mono8"` |
  | `camera.Width.SetValue(640)` | `camera.Width.Value = 640` |
  | `camera.Gain.GetValue()` | `camera.Gain.Value` |
  | `camera.ReverseX.SetValue(False)` | `camera.ReverseX.Value = False` |
  | `camera.ExposureTime.GetValue()` | `camera.ExposureTime.Value` |

  **Use `.SetValue()` when extra parameters are needed** — for example,
  value correction modes that `.Value =` does not support:
  ```python
  camera.Width.SetValue(640, pylon.IntegerValueCorrection_Nearest)
  exposure.SetValue(1000.0, pylon.FloatValueCorrection_ClipToRange)
  ```

  **Use `.TrySetValue()` when setting an optional parameter:**
  This is only applicable when the parameter may not be settable on all devices or in all states.
  If you expect the parameter to be settable and want to fail loudly if it is not, keep using `.Value = <value>`
  and let it throw an exception if the parameter is not settable.
  Instead of writing this for enumeration parameters:
  ```python
  if camera.PixelFormat.IsWritable() and camera.PixelFormat.CanSetValue("Mono8"):
      camera.PixelFormat.Value = "Mono8"
  ```
  write this:
  ```python
  camera.PixelFormat.TrySetValue("Mono8")  # no-op if not settable
  ```
  Or instead of writing this:
  ```python
  if camera.Width.IsWritable():
      camera.Width.SetValue(1000)
  ```
  write this:
  ```python
  camera.Width.TrySetValue(1000)  # no-op if not settable, fails if 1000 is not in range or not a valid value
  ```

  **Keep `.SetToMaximum()` / `.SetToMinimum()` / `.SetValuePercentOfRange()`**
  — these have no `.Value` equivalent.

- **Prefer parameter methods over free-standing genicam helpers.**
  Use methods on the parameter object directly instead of passing the
  parameter to `genicam.IsReadable()` / `genicam.IsWritable()`. If
  `genicam` is only imported for these helpers, remove the import.

  | Avoid | Prefer |
  |---|---|
  | `genicam.IsReadable(param)` | `param.IsReadable()` |
  | `genicam.IsWritable(param)` | `param.IsWritable()` |
  | `param.ToString() if genicam.IsReadable(param) else "N/A"` | `param.GetValueOrDefault("N/A")` |
  | `for s in param.Symbolics:` `try: param.SetValue(s)` `except: pass` | `for s in param.GetSettableValues():` `param.SetValue(s)` |

  **Note:** `GetSettableValues()` only returns entries that are currently
  settable — it is a *filtered* subset of `GetAllValues()`. Use `GetAllValues()`
  when you need all implemented entries (e.g. listing or comparing), and
  `GetSettableValues()` only when you want to skip non-settable ones.
  In comparison `Symbolics` is a list of all entries available in the node map,
  some of these may never be settable on a given device.

- **Use `TrySetValue` to replace `try: SetValue() except: pass`.**
  When a `SetValue` call is wrapped in a bare `try/except` only to swallow
  failure, replace it with `TrySetValue`, which returns `True` on success
  and `False` on failure without throwing:
  ```python
  # Before
  try:
      param.SetValue("ExposureEnd")
  except Exception:
      pass

  # After
  param.TrySetValue("ExposureEnd")
  ```
  `TrySetValue` or other try pattern methods are available on all parameters.

  **Caveat:** `TrySetValue` only handles *value-not-settable*. If
  the call itself may throw, keep a `try/except` around the `GetParameter()`
  call:
  ```python
  try:
      chunks_available = recipe.GetParameter(
          "MyCamera/@CameraDevice/ChunkModeActive"
      ).TrySetValue(True)
  except genicam.GenericException:
      chunks_available = False
  ```

- **Use context managers for resource cleanup.** Where possible, use `with`
  statements to ensure pylon objects are released automatically:
  ```python
  with pylon.InstantCamera(pylon.FirstFound) as camera:
      # camera is open and ready to use here
      ...
  # camera is closed automatically

  with camera.RetrieveResult(timeout_ms, pylon.TimeoutHandling_ThrowException) as grab_result:
      if grab_result.GrabSucceeded():
          img = grab_result.Array
        ...
  # grab result is released automatically, pylon uses a buffer pool so the underlying buffer is reused

  tl = tl_factory.CreateTl("BaslerGigE")
  try:
      with tl.InterfaceNodeMap(interface_info) as nodemap:
          ...
      # interface is closed and destroyed automatically
  finally:
      tl_factory.ReleaseTl(tl)
  ```

- **Do not call `camera.Open()` inside a `with` block** when the device is
  attached at construction (e.g. `pylon.InstantCamera(pylon.FirstFound)`).
  `InstantCamera.__enter__` already calls `Open()` in that case, so an
  explicit call is redundant — `Open()` on an already-open camera is a
  **no-op** (no events fire, no callbacks re-register).

  **Pre-`Open()` settings.** Some InstantCamera-level parameters and
  registration calls must take effect *before* `Open()` runs. Because
  `Open()` cannot re-open an already-open camera, you must construct
  without a device so that `__enter__` skips the implicit `Open()`:

  **`RegisterConfiguration` with `OnOpened` logic:** `OnOpened` fires
  during `Open()`. If the handler is registered after `__enter__` already
  opened the camera, `OnOpened` never fires:
  If the code changes the device attached to the instant camera register a configuration,
  the configuration must be registered before `Open()`:
  ```python
  with pylon.InstantCamera() as camera:
      camera.RegisterConfiguration(
          pylon.SoftwareTriggerConfiguration(),
          pylon.RegistrationMode_ReplaceAll,
          pylon.Cleanup_Delete,
      )
      camera.Attach(pylon.FirstFound)
      camera.Open()  # OnOpened fires here and calls pylon.SoftwareTriggerConfiguration.ApplyConfiguration(camera.NodeMap) 
      ...
  ```
  If the code only uses one device and does not change it, the configuration can be applied after the Open() call:
  ```python
  with pylon.InstantCamera(pylon.FirstFound) as camera:
      # camera is open and ready to use here
      pylon.SoftwareTriggerConfiguration.ApplyConfiguration(camera.NodeMap)
      ...
  ```

  **`GrabCameraEvents`:** This flag is not writable once the camera is
  open (raises `AccessException`). It must be set before `Open()`:
  ```python
  with pylon.InstantCamera() as camera:
      camera.GrabCameraEvents.Value = True
      camera.Attach(pylon.FirstFound)
      camera.Open()
      ...
  ```

  **`MonitorModeActive`:** This flag controls the device access mode
  (read-only monitor) and must be set before `Open()`:
  ```python
  with pylon.InstantCamera() as camera:
      camera.MonitorModeActive.Value = True
      camera.Attach(pylon.FirstFound)
      camera.Open()
      ...
  ```

**`pylon module sample naming rules`:** Samples are named according to the following rules:
- Use lower snake case (e.g. `grab.py`, not `Grab.py` or `grabImages.py`).
- Use descriptive names that indicate the sample's purpose.
- Prefix rules:
  - `grab_` — samples that illustrate image grabbing.
  - `parametrize_` — samples that illustrate camera parameter access and configuration.
  - `utility_` — samples that use the optional pylon utility C++ library.
  - `gige_` — samples that illustrate features specific to GigE cameras.
  - No prefix — samples that do not fall into any of the above categories; name them according to their purpose.
~~~~