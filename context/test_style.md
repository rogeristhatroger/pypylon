# Test Style

This file defines a common style for pypylon unit tests.

A unit test checks all of the mapped pypylon API introduced by a given `.i`
file (e.g. `src/pylon/DeviceInfo.i`) in all relevant variations:

- Mapped objects
- Mapped C++ class members
- Mapped C++ overloads
- Added Python properties
- Added Python methods
- Added C++ methods
- Mapped C/C++ functions

The style rules below apply whenever they are relevant to what is being tested.
If a rule does not apply to a specific test (e.g. the test is intentionally
exercising the GenICam node API), it may be ignored for that test.

## Header

Every test file starts with a module docstring that briefly describes what
the file covers:
```python
"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/DeviceInfo.i.
"""
```

## Base Structure

Tests are grouped in a class that inherits from a test case classe, e.g. `PylonParameterTestCase`
(which itself extends `unittest.TestCase`). `setUp` and `tearDown` are
handled by the base class; override them only when additional setup is
needed (e.g. connecting a test port).

```python
from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest


class MyParameterTestSuite(PylonParameterTestCase):

    # ------------------------------------------------------------------
    # Construction / Attach / Release
    # ------------------------------------------------------------------

    def test_my_parameter_construction_default(self):
        """Default construction produces an invalid parameter."""
        p = pylon.MyParameter()
        self.assertFalse(p.IsValid())
```

## Style

The common style rules in [common_style.md](common_style.md) apply.
The following additional rules are specific to unit tests:

- **Test method naming.** Name test methods as
  `test_<aspect_under_test>`, using `snake_case` throughout.
  For example: `test_get_value_or_default_write_only`.

- **Test method docstrings.** Every test method must have a one-line docstring
  that describes the expected behaviour in plain English.
  For example: `"""GetValueOrDefault returns default when parameter is write-only."""`

- **Section grouping.** Group related test methods with a comment divider:
  ```python
  # ------------------------------------------------------------------
  # Construction / Attach / Release
  # ------------------------------------------------------------------
  ```

- **Import order.** Place local test-infrastructure imports first
  (`from parametertestcase import PylonParameterTestCase`), then pypylon
  imports (`from pypylon import pylon, genicam`), then standard-library
  imports (`import unittest`). Import only what is actually used.
