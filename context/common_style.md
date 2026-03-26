# Common Style

This file defines style rules that apply to all pypylon code — both samples
and unit tests.

## Style

- **Properties over getter/setter methods.** Use properties instead of explicit
  getter and setter methods.
  For example, use `camera.NodeMap` instead of `camera.GetNodeMap()`.

- **Direct parameter access over node map lookup.** Use direct parameter
  properties on the camera object instead of calling `GetNode` on a node map.
  For example, use `camera.ExposureTime` instead of
  `camera.NodeMap.GetNode("ExposureTime")`, and use
  `camera.StreamGrabberNodeMap.Type` instead of
  `camera.StreamGrabberNodeMap.GetNode("Type")`.
  Note: pylon maintains a list of known parameter names. Names not on that list
  are only exposed as direct properties if the corresponding node is present in
  the node map. Known names that are absent from the node map will appear empty,
  non-readable and non-writable.

- **pylon parameter API over GenICam node API.** Use the convenience methods of
  the pylon parameter API (`pylon.Parameter` and its derived classes) instead of
  the lower-level GenICam API (`genicam.INode` and its derived classes).
  For example, use `camera.ExposureTime.SetToMinimum()` instead of
  `camera.ExposureTime.Value = camera.ExposureTime.Min`.

- **`IsReadable()` / `IsWritable()` for availability checks.** Use the
  `IsReadable()` and `IsWritable()` methods of the pylon parameter API to check
  whether a node is available before using it.
  For example, use `if camera.ExposureTime.IsWritable():` instead of
  `if genicam.IsWritable(camera.ExposureTime)`.

- **Safe access for optionally available parameters.** When it is not known
  whether a parameter exists or is accessible on a given device, use
  `GetValueOrDefault()` or other `*OrDefault()` methods, or `TrySetValue()`
  and other `Try*()` methods.
  For example, use `camera.ExposureTime.GetValueOrDefault(default_value)`
  instead of unconditionally reading `camera.ExposureTime.Value`.

- **Naming conventions.** Use `snake_case` for variable and function names,
  following standard Python conventions (PEP 8). Use `UPPER_SNAKE_CASE` for
  module-level constants.
  For example, use `exit_code` instead of `exitCode`, and use
  `DEFAULT_EXPOSURE_TIME` instead of `DefaultExposureTime`.
