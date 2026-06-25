# Sample Style

This file defines a common style for pypylon samples. It covers only what is
specific to samples. All API and coding idioms live in 
[common_style.md](common_style.md) and apply here too.

## Layout

Each sample lives in its own folder, with the script named after the folder:
`samples/<module>/<name>/<name>.py`, where `<module>` is `pylon` or
`pylondataprocessing`.

- Co-locate per-sample files (e.g. `.precipe` recipes) in the sample folder and
  load them relative to `__file__`.
- Shared image/data assets live under `samples/images/<kind>/`; reference them
  relative to `__file__` instead of copying them into the sample folder.
- Shared helper modules (event printers, image creator) live in
  `samples/common/`; samples import them by prepending that directory (relative
  to `__file__`) to `sys.path`.

## Header

The **Header** and **Base Structure** below apply to every runnable sample
under `pylon/` and `pylondataprocessing/`. Helper modules in `samples/common/`
are the exception — see [Shared helper modules](#shared-helper-modules).

Every runnable sample begins with the following shebang line:
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

Every runnable sample uses the top-level `try` / `except` / `sys.exit`
skeleton below after the header. `pylondataprocessing` samples follow the same
structure, importing `pylondataprocessing` instead of (or in addition to)
`pylon`.

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

## Sample naming rules

Across all modules, use lower `snake_case` for sample folders and their script
(e.g. `grab.py`, not `Grab.py` or `grabImages.py`) and choose a descriptive
name that indicates the sample's purpose.

**`pylon` module** samples additionally use a topic prefix:

- `grab_` — samples that illustrate image grabbing.
- `parametrize_` — samples that illustrate camera parameter access and configuration.
- `utility_` — samples that use the optional pylon utility C++ library.
- `gige_` — samples that illustrate features specific to GigE cameras.
- No prefix — samples that do not fall into any of the above categories; name them according to their purpose.

**`pylondataprocessing` module** samples do not use the `pylon` prefixes above;
name them after the feature they demonstrate (e.g. `barcode`, `ocr`, `region`).

## Shared helper modules

`samples/common/` holds reusable helper modules imported by samples (e.g.
`camera_event_printer.py`, `sample_image_creator.py`), not standalone samples.
They are importable library modules, so their structure differs from a runnable
sample:

- They are flat modules in `samples/common/` (not one-per-folder); name each in
  `snake_case` after the helper it provides.
- **No shebang** and **no top-level `try` / `except` / `sys.exit` skeleton** —
  a helper is imported, not run directly.
- Start with a one-line module docstring, then imports, then the reusable
  classes/functions (each with its own docstring).
- The API and coding idioms in [common_style.md](common_style.md) apply.
