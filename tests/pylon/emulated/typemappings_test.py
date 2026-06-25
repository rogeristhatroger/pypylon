"""\
This unit test checks the mapped pypylon API introduced by src/pylon/TypeMappings.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon, genicam
import unittest


# All GenICam exception classes re-exported on pylon by TypeMappings.i.
MAPPED_EXCEPTION_NAMES = (
    "GenericException",
    "BadAllocException",
    "InvalidArgumentException",
    "OutOfRangeException",
    "PropertyException",
    "RuntimeException",
    "LogicalErrorException",
    "AccessException",
    "TimeoutException",
    "DynamicCastException",
)


class TypeMappingsTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Ignored typedefs
    # %ignore String_t;
    # %ignore StringList_t;
    # ------------------------------------------------------------------

    def test_string_typedef_is_not_exposed(self):
        """Pylon::String_t is %ignore-d and must not appear on pylon."""
        self.assertFalse(hasattr(pylon, "String_t"))

    def test_string_list_typedef_is_not_exposed(self):
        """Pylon::StringList_t is %ignore-d and must not appear on pylon."""
        self.assertFalse(hasattr(pylon, "StringList_t"))

    # ------------------------------------------------------------------
    # String_t <-> Python str mapping
    # ------------------------------------------------------------------

    def test_string_getter_returns_python_str(self):
        """A property returning String_t is exposed as a native Python str."""
        info = pylon.DeviceInfo()
        info.FriendlyName = "hello"
        self.assertIsInstance(info.FriendlyName, str)
        self.assertEqual(info.FriendlyName, "hello")

    def test_string_setter_accepts_python_str(self):
        """A property accepting String_t accepts a native Python str."""
        info = pylon.DeviceInfo()
        info.ModelName = "acA1920-40um"
        self.assertEqual(info.ModelName, "acA1920-40um")

    def test_string_round_trip_preserves_unicode(self):
        """String_t preserves non-ASCII (UTF-8) content across a set/get round-trip."""
        info = pylon.DeviceInfo()
        unicode_value = "naïve café"
        info.FriendlyName = unicode_value
        self.assertEqual(info.FriendlyName, unicode_value)

    def test_string_round_trip_preserves_empty_string(self):
        """String_t preserves an explicitly set empty value across a set/get round-trip."""
        info = pylon.DeviceInfo()
        info.FriendlyName = ""
        self.assertEqual(info.FriendlyName, "")

    # ------------------------------------------------------------------
    # StringList_t <-> Python sequence of str mapping
    # ------------------------------------------------------------------

    def test_string_list_returned_as_iterable_of_str(self):
        """A method returning StringList_t yields an iterable of Python str values."""
        info = pylon.DeviceInfo()
        info.ModelName = "M"
        info.VendorName = "V"
        count, names = info.GetPropertyNames()
        self.assertEqual(count, len(names))
        for name in names:
            self.assertIsInstance(name, str)
        self.assertIn("ModelName", names)
        self.assertIn("VendorName", names)

    def test_string_list_returned_empty_when_no_properties_set(self):
        """A method returning StringList_t yields an empty sequence when no properties are set."""
        info = pylon.DeviceInfo()
        count, names = info.GetPropertyNames()
        self.assertEqual(count, 0)
        self.assertEqual(len(names), 0)

    # ------------------------------------------------------------------
    # Exception aliases re-exported on pylon (%pythoncode block)
    # ------------------------------------------------------------------

    def test_all_mapped_exceptions_are_exposed_on_pylon(self):
        """Every GenICam exception listed in TypeMappings.i is accessible on pylon."""
        for exception_name in MAPPED_EXCEPTION_NAMES:
            with self.subTest(exception=exception_name):
                self.assertTrue(
                    hasattr(pylon, exception_name),
                    "pylon.%s is missing" % exception_name,
                )

    def test_pylon_exception_aliases_are_identical_to_genicam(self):
        """Each pylon.<Exception> is the same class object as pypylon.genicam.<Exception>."""
        for exception_name in MAPPED_EXCEPTION_NAMES:
            with self.subTest(exception=exception_name):
                self.assertIs(
                    getattr(pylon, exception_name),
                    getattr(genicam, exception_name),
                )

    def test_mapped_exceptions_derive_from_generic_exception(self):
        """Every mapped pylon exception is a subclass of GenericException (and of Python's Exception)."""
        for exception_name in MAPPED_EXCEPTION_NAMES:
            with self.subTest(exception=exception_name):
                exception_class = getattr(pylon, exception_name)
                self.assertTrue(issubclass(exception_class, Exception))
                self.assertTrue(issubclass(exception_class, pylon.GenericException))

    # ------------------------------------------------------------------
    # Exception catchability across the pylon / genicam alias boundary
    # ------------------------------------------------------------------

    def _raise_invalid_argument(self):
        """Trigger a real pylon-side InvalidArgumentException from the emulator."""
        # IsPersistentIpActive raises when the IP configuration property is
        # not set on the DeviceInfo; this exercises a real C++-side throw
        # that the %types directive in TypeMappings.i must translate into
        # the Python GenICam exception hierarchy.
        pylon.DeviceInfo().IsPersistentIpActive()

    def test_pylon_raise_is_catchable_via_pylon_generic_exception(self):
        """A pylon-raised exception is catchable via pylon.GenericException."""
        with self.assertRaises(pylon.GenericException):
            self._raise_invalid_argument()

    def test_pylon_raise_is_catchable_via_genicam_generic_exception(self):
        """A pylon-raised exception is catchable via genicam.GenericException (cross-module alias)."""
        with self.assertRaises(genicam.GenericException):
            self._raise_invalid_argument()

    def test_pylon_raise_is_catchable_via_specific_pylon_alias(self):
        """A pylon-raised exception is catchable via its specific pylon.<Subclass> alias."""
        with self.assertRaises(pylon.InvalidArgumentException):
            self._raise_invalid_argument()

    def test_pylon_raise_is_catchable_via_specific_genicam_alias(self):
        """A pylon-raised exception is catchable via its specific genicam.<Subclass> alias."""
        with self.assertRaises(genicam.InvalidArgumentException):
            self._raise_invalid_argument()


if __name__ == "__main__":
    unittest.main()
