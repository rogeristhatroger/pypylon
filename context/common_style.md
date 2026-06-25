# pypylon Coding Style

This file defines the coding style and API idioms for all pypylon code —
samples, unit tests, and your own applications. The sample- and test-specific
conventions in [sample_style.md](sample_style.md) and
[test_style.md](test_style.md) build on these rules.

## Naming conventions

- **Use Python naming conventions.** Use `snake_case` for variable and function
  names, following standard Python conventions (PEP 8). Use `UPPER_SNAKE_CASE`
  for module-level constants.
  For example, use `exit_code` instead of `exitCode`, and use
  `DEFAULT_EXPOSURE_TIME` instead of `DefaultExposureTime`.

- **Avoid abbreviations in identifiers.** Use descriptive names for variables,
  functions, and classes, and avoid abbreviations that may be unclear to
  readers.
  For example, use `exposure_time` instead of `exp_time`, and use
  `CameraConfiguration` instead of `CamConfig`.

## Prefer the pylon parameter API over the GenICam node API

- **Properties over getter/setter methods.** Use properties instead of explicit
  getter and setter methods.
  For example, use `camera.NodeMap` instead of `camera.GetNodeMap()`.

  Use the Pythonic property syntax and convenience shortcuts provided by pypylon
  instead of the underlying C++-style accessor methods. Examples:

  | Avoid | Prefer |
  |---|---|
  | `pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())` | `pylon.InstantCamera(pylon.FirstFound)` |
  | `camera.GetDeviceInfo().GetModelName()` | `camera.DeviceInfo.ModelName` |
  | `grab_result.GetWidth()` | `grab_result.Width` |
  | `image.GetBuffer()` | `image.Buffer` |
  | `param.GetMin()` | `param.Min` |

  …and likewise for other simple zero-argument accessors that pypylon exposes
  as properties (`Height`, `ErrorCode`, `PixelType`, `BlockID`, `DeviceClass`,
  `Max`, `Inc`, …) — read `GetX()` as the property `X`. This applies only where
  a property actually exists: do not mechanically drop `Get` from methods that
  take arguments or that pypylon does not expose as a property.

  The same principle applies to **pylondataprocessing** types — use the
  property instead of the getter (`variant.ErrorDescription`,
  `region.RegionType`, `result_collector.WaitObject`), and index array
  variants directly with `variant[i]` instead of `variant.GetArrayValue(i)`.

- **Direct parameter access over node map lookup.** Use direct parameter
  properties on the camera object instead of calling `GetNode` on a node map.
  For example, use `camera.ExposureTime` instead of
  `camera.NodeMap.GetNode("ExposureTime")`, and use
  `camera.StreamGrabberNodeMap.Type` instead of
  `camera.StreamGrabberNodeMap.GetNode("Type")`.
  Note: If a parameter is accessed that does not exist,
  a PlaceholderParameter is returned instead of throwing an exception.
  Parameters that are absent from the node map will appear empty,
  non-readable and non-writable.

- **pylon parameter API over GenICam node API.** Use the convenience methods of
  the pylon parameter API (`pylon.Parameter` and its derived classes) instead of
  the lower-level GenICam API (`genicam.INode` and its derived classes).
  For example, use `camera.ExposureTime.SetToMinimum()` instead of
  `camera.ExposureTime.Value = camera.ExposureTime.Min`.

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

## Reading and writing parameter values

- **Use the `.Value` property for straightforward parameter reads and writes.**
  Camera parameter nodes support a `.Value` property that is more Pythonic
  than the `.GetValue()` / `.SetValue()` methods. Prefer `.Value` for
  simple reads and unconditional writes:

  | Avoid | Prefer |
  |---|---|
  | `camera.PixelFormat.SetValue("Mono8")` | `camera.PixelFormat.Value = "Mono8"` |
  | `camera.Gain.GetValue()` | `camera.Gain.Value` |

  The same applies to any parameter type (`Width`, `ExposureTime`,
  `ReverseX`, …).

  **Always go through `.Value` (or `.SetValue()`); never assign to the
  parameter directly.** The bare-assignment form `camera.Gain = 42` is
  deprecated (it prevents full typing support) — write `camera.Gain.Value = 42`.

- **Use `.SetValue()` when extra parameters are needed** — for example,
  value correction modes that `.Value =` does not support:
  ```python
  camera.Width.SetValue(640, pylon.IntegerValueCorrection_Nearest)
  exposure.SetValue(1000.0, pylon.FloatValueCorrection_ClipToRange)
  ```

- **Keep `.SetToMaximum()` / `.SetToMinimum()` / `.SetValuePercentOfRange()`**
  — these have no `.Value` equivalent.

## Availability and safe access

- **`IsReadable()` / `IsWritable()` / `IsValid()` for availability checks.** Use the
  `IsReadable()` and `IsWritable()` methods of the pylon parameter API to check
  whether a node is available before using it.
  For example, use `if camera.ExposureTime.IsWritable():` instead of
  `if genicam.IsWritable(camera.ExposureTime)`.

- **Safe access for optionally available parameters.** When it is not known
  whether a parameter exists or is accessible on a given device, use
  `GetValueOrDefault()` or other `*OrDefault()` methods, or `TrySetValue()`
  and other `Try*()` pattern methods.
  For example, use `camera.ExposureTime.GetValueOrDefault(default_value)`
  instead of unconditionally reading `camera.ExposureTime.Value`.

- **Use `.TrySetValue()` when setting an optional parameter.**
  This applies when the parameter may not be settable on all devices or in all
  states. If you expect it to be settable and want to fail loudly otherwise,
  keep `.Value = <value>` and let it throw. Otherwise replace the explicit
  writability guard:
  ```python
  # Instead of:
  if camera.PixelFormat.IsWritable() and camera.PixelFormat.CanSetValue("Mono8"):
      camera.PixelFormat.Value = "Mono8"
  # write:
  camera.PixelFormat.TrySetValue("Mono8")  # no-op if not settable
  ```

- **Use `TrySetValue` to replace `try: SetValue() except: pass` — but only
  when the suppressed failure is "not settable".** `TrySetValue` attempts the
  write and returns `True` on success or `False` when the parameter is not
  currently writable or the value cannot be applied in the current state. It is
  **not** a blanket exception suppressor: it still raises for an invalid
  argument, such as a value outside the allowed range, an invalid enumeration
  entry, or a wrong type.

  So only collapse a `try/except` into `TrySetValue` when the `except` existed
  solely to ignore the *not-settable* case. If the `except` was also masking
  invalid-value or other errors, keep handling those explicitly rather than
  silently dropping them.
  ```python
  # Before — the except only guards against the parameter being non-writable
  try:
      param.SetValue("ExposureEnd")
  except Exception:
      pass

  # After — TrySetValue covers exactly that case
  param.TrySetValue("ExposureEnd")  # False if not writable; still raises if writing the value to the device failed.
  ```
  `TrySetValue` and the other `Try*` pattern methods are available on all
  parameters.

  **Caveat:** `TrySetValue` only handles *value-not-settable*. If
  the call itself may throw, keep a `try/except` around the `GetParameter()`
  call:
  ```python
  try:
      chunk_activation_successful = recipe.GetParameter(
          "MyCamera/@CameraDevice/ChunkModeActive"
      ).TrySetValue(True)
  except genicam.GenericException:
      chunk_activation_successful = False
  ```

## Resource management with `with`

- **Use context managers for resource cleanup.** Where possible, use `with`
  statements to ensure pylon objects are released automatically, even if an
  error occurs. A camera and a grab result are both context managers; retrieve
  the result inside the open camera while it is grabbing:
  ```python
  with pylon.InstantCamera(pylon.FirstFound) as camera:
      # camera is open and ready to use here
      camera.StartGrabbingMax(1)
      with camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as grab_result:
          if grab_result.GrabSucceeded():
              img = grab_result.Array
              ...
      # grab result is released automatically; pylon reuses the underlying buffer from its pool
      # camera is closed automaticallyally
  ```

  The same applies to other pylon resources. For objects without context-manager
  support, pair acquisition with a `try`/`finally`:
  ```python
  with tl_factory.TransportLayer(pylon.BaslerGigEDeviceClass) as transport_layer:
      with transport_layer.InterfaceNodeMap(interface_info) as nodemap:
          ...
      # interface and transport_layer are closed and destroyed automatically
  ```

## Pre-`Open()` patterns

- **Do not call `camera.Open()` inside a `with` block** when the device is
  attached at construction (e.g. `pylon.InstantCamera(pylon.FirstFound)`).
  `InstantCamera.__enter__` already calls `Open()` in that case, so an
  explicit call is redundant — `Open()` on an already-open camera is a
  **no-op** (no events fire, no callbacks re-register).

- **Pre-`Open()` settings.** Some InstantCamera-level parameters and
  registration calls must take effect *before* `Open()` runs. Because
  `Open()` cannot re-open an already-open camera, you must construct
  without a device so that `__enter__` skips the implicit `Open()`:

  **`RegisterConfiguration` with `OnOpened` logic:** `OnOpened` fires
  during `Open()`. If the handler is registered after `__enter__` already
  opened the camera, `OnOpened` never fires. If the code changes the device
  attached to the instant camera and registers a configuration, the
  configuration must be registered before `Open()`:
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
  If the code only uses one device and does not change it, the configuration
  can be applied after the `Open()` call:
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
