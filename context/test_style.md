# Test Style

This file defines a common style for pypylon unit tests.

A unit test should cover the public pypylon API introduced by a given `.i`
file (e.g. `src/pylon/DeviceInfo.i`) with a level of detail that matches the
binding:

- Prefer direct tests of the public objects, properties, methods, and functions
  that users actually call.
- Prefer small usage-oriented examples that show the intended Python syntax.
- Add broader coverage when it protects an important binding contract, not just
  because a complete inventory is possible.

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

Tests are grouped in a class that inherits from a test case class, e.g. `PylonParameterTestCase`
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

- **Usage examples first.** When possible, write tests so they also act as
  small syntax examples. A reader should be able to look at the test and learn
  how to construct the object, access the property, or call the helper.
  Favor short, direct examples like `deviceinfo_test.py` over large inventories
  of names, helper tables, or set-based surface comparisons.

## Enum Bindings

Enum-like bindings often need a simpler style than class-heavy wrappers.
The default pattern is the one used by `variantdatatype_test.py`: short,
explicit checks of the public names a user is expected to read and use.

- **Tests should read like examples.** Prefer direct assertions on the public
  constants and helpers that users actually call. Use exact values when they
  are part of the public contract or make the example clearer.

- **Prefer representative examples over inventories.** Cover a few meaningful
  cases instead of rebuilding the full enum in Python. When enum values feed
  helpers, prefer small usage examples such as
  `GetPixelColorFilter(pylon.PixelType_BayerRG8)`, and include at least one per
  helper family. Where a boundary is easy to misread (planar vs. packed, Bayer
  vs. mono, legacy naming vs. actual behavior), use a small contrast set of 2-4
  related assertions rather than a single example, and add any distinct
  error or legacy/public case.

- **Keep representative cases visible.** For a small fixed example set, prefer
  explicit assertions to loops, even when each case needs a simple availability
  guard. This keeps the tested public names easy to read, review, and reuse.

- **Assert opaque values by invariant, not by encoding.** If an enum value is
  an internal or bit-packed encoding rather than a user-facing contract, do not
  hard-code the number. Test documented invariants such as sentinel values,
  distinctness, or specific cross-value relationships instead.

- **Keep structure local and simple.** Avoid large module-level lists,
  throwaway aliases, broad negative coverage, and tiny loops when explicit
  assertions are clearer. Use exhaustive surface checks only when they protect
  an important binding contract or known regression risk.
