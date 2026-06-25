"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylon/Info.i.

Info.i defines the CInfoBase contract that every concrete Info subclass
(DeviceInfo, InterfaceInfo, TlInfo) inherits, namely:

    * The five CInfoBase properties declared via ADD_PROP_GETSET:
      FriendlyName, FullName, VendorName, DeviceClass, TLType.
    * The IProperties methods exposed on CInfoBase (GetPropertyNames,
      GetPropertyAvailable, GetPropertyValue, SetPropertyValue, IsSubset,
      IsUserProvided, GetPropertyNotAvailable).
    * The Python dict-style extensions added in %pythoncode
      (keys, values, items, __getitem__, __setitem__, __iter__,
      __contains__, to_dict, update).

Each test is parametrized with subTest over all concrete Info subclasses to
confirm the Info.i mappings behave identically regardless of which CInfoBase
derivative is used.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


# All concrete CInfoBase subclasses that inherit the Info.i contract.
INFO_CLASSES = (
    ("DeviceInfo", pylon.DeviceInfo),
    ("InterfaceInfo", pylon.InterfaceInfo),
    ("TlInfo", pylon.TlInfo),
)

# The five properties added to CInfoBase via ADD_PROP_GETSET in Info.i,
# paired with a sample value for round-trip checks.
CINFO_BASE_PROPERTIES = (
    ("FriendlyName", "Test Friendly"),
    ("FullName", "Test Full Name"),
    ("VendorName", "Test Vendor"),
    ("DeviceClass", "BaslerUsb"),
    ("TLType", "U3V"),
)


class InfoTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_construction(self):
        """Default construction produces a valid empty Info instance for every subclass."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                self.assertIsNotNone(info)

    # ------------------------------------------------------------------
    # CInfoBase comparison operators (from Info.i via <pylon/Info.h>)
    #     bool operator==( const CInfoBase& rhs ) const;
    #     bool operator <( const CInfoBase& rhs ) const;
    #         Documented ordering by device class:
    #         USB < GigE < CameraLink < GenTL (incl. CXP) < unknown < CamEmu.
    # ------------------------------------------------------------------

    def test_equality(self):
        """operator== compares equal for two Info objects with identical CInfoBase properties."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info1 = cls()
                info1.FriendlyName = "F"
                info1.VendorName = "V"
                info2 = cls()
                info2.FriendlyName = "F"
                info2.VendorName = "V"
                self.assertEqual(info1, info2)

    def test_inequality(self):
        """operator== returns False when any CInfoBase property differs."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info1 = cls()
                info1.FriendlyName = "F"
                info2 = cls()
                info2.FriendlyName = "Other"
                self.assertNotEqual(info1, info2)

    def test_less_than_by_device_class(self):
        """operator< orders by DeviceClass rank: USB < GigE < CL < GenTL < unknown < CamEmu."""
        # Ordered list of DeviceClass values from "least" to "greatest"
        # according to CInfoBase::operator< documented in pylon/Info.h.
        # The sentinel "SomethingUnknown" represents the documented "unknown
        # device classes" bucket: a DeviceClass string that does not match
        # any known pylon category (anything starting with "Basler..." is
        # classified by the pylon implementation rather than treated as
        # unknown, so the sentinel intentionally does not use that prefix).
        ordered_device_classes = [
            "BaslerUsb",           # USB
            "BaslerGigE",          # GigE
            "BaslerCameraLink",    # CameraLink
            "BaslerGenTlConsumer", # GenTL (incl. CXP)
            "SomethingUnknown",    # unknown device classes
            "BaslerCamEmu",        # CamEmu (sorts last)
        ]
        for name, cls in INFO_CLASSES:
            for i in range(len(ordered_device_classes) - 1):
                low_class = ordered_device_classes[i]
                high_class = ordered_device_classes[i + 1]
                with self.subTest(info_class=name, low=low_class, high=high_class):
                    low = cls()
                    low.DeviceClass = low_class
                    high = cls()
                    high.DeviceClass = high_class
                    self.assertTrue(low < high)
                    self.assertFalse(high < low)

    def test_less_than_same_device_class_not_less(self):
        """operator< returns False in both directions when two Info objects share the same DeviceClass."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                left = cls()
                left.DeviceClass = "BaslerUsb"
                right = cls()
                right.DeviceClass = "BaslerUsb"
                self.assertFalse(left < right)
                self.assertFalse(right < left)

    # ------------------------------------------------------------------
    # CInfoBase properties (from Info.i)
    # ADD_PROP_GETSET(CInfoBase, FriendlyName)
    # ADD_PROP_GETSET(CInfoBase, FullName)
    # ADD_PROP_GETSET(CInfoBase, VendorName)
    # ADD_PROP_GETSET(CInfoBase, DeviceClass)
    # ADD_PROP_GETSET(CInfoBase, TLType)
    # ------------------------------------------------------------------

    def _assert_property_round_trip(self, cls, prop_name, value):
        """Exercise the property / legacy / dict interfaces for one CInfoBase property."""
        info = cls()
        is_available = getattr(info, "Is%sAvailable" % prop_name)
        getter = getattr(info, "Get%s" % prop_name)
        setter = getattr(info, "Set%s" % prop_name)
        key_constant = getattr(pylon, "%sKey" % prop_name)

        # --- recommended: property interface ---
        self.assertFalse(is_available())
        self.assertEqual(getattr(info, prop_name), cls.GetPropertyNotAvailable())
        setattr(info, prop_name, value)
        self.assertTrue(is_available())
        self.assertEqual(getattr(info, prop_name), value)

        # --- legacy: named getter / setter ---
        updated_value = value + "_updated"
        setter(updated_value)
        self.assertEqual(getter(), updated_value)

        # --- generic: dict-style interface ---
        dict_value = value + "_dict"
        info[key_constant] = dict_value
        self.assertEqual(info[prop_name], dict_value)

    def test_friendly_name(self):
        """FriendlyName round-trips on every Info subclass."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                self._assert_property_round_trip(cls, "FriendlyName", "Test Friendly")

    def test_full_name(self):
        """FullName round-trips on every Info subclass."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                self._assert_property_round_trip(cls, "FullName", "Test Full Name")

    def test_vendor_name(self):
        """VendorName round-trips on every Info subclass."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                self._assert_property_round_trip(cls, "VendorName", "Test Vendor")

    def test_device_class(self):
        """DeviceClass round-trips on every Info subclass."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                self._assert_property_round_trip(cls, "DeviceClass", "BaslerUsb")

    def test_tl_type(self):
        """TLType round-trips on every Info subclass."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                self._assert_property_round_trip(cls, "TLType", "U3V")

    # ------------------------------------------------------------------
    # IProperties methods (from Info.i)
    #     static const char* GetPropertyNotAvailable();
    #     virtual int GetPropertyNames( StringList_t& ) const;
    #     virtual bool GetPropertyAvailable( const String_t& Name ) const;
    #     virtual bool GetPropertyValue( const String_t& Name, String_t& Value ) const;
    #     virtual IProperties& SetPropertyValue( const String_t& Name, const String_t& Value );
    #     virtual bool IsUserProvided() const;
    #     virtual bool IsSubset( const IProperties& Subset ) const;
    # ------------------------------------------------------------------

    def test_get_property_not_available(self):
        """GetPropertyNotAvailable returns the same sentinel string on every subclass."""
        sentinel = pylon.DeviceInfo.GetPropertyNotAvailable()
        self.assertIsInstance(sentinel, str)
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                self.assertEqual(cls.GetPropertyNotAvailable(), sentinel)
                self.assertEqual(cls().GetPropertyNotAvailable(), sentinel)

    def test_get_property_names(self):
        """GetPropertyNames / keys() return all set property names as strings."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                info.FriendlyName = "F"
                info.VendorName = "V"
                count, names = info.GetPropertyNames()
                self.assertEqual(count, len(names))
                self.assertIn("FriendlyName", names)
                self.assertIn("VendorName", names)
                self.assertTrue(all(isinstance(n, str) for n in names))
                self.assertEqual(list(info.keys()), list(names))

    def test_get_property_available(self):
        """GetPropertyAvailable returns True for a set property and False for an unknown key."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                info.FriendlyName = "F"
                self.assertTrue(info.GetPropertyAvailable("FriendlyName"))
                self.assertFalse(info.GetPropertyAvailable("NonExistentKey"))

    def test_get_property_value(self):
        """GetPropertyValue returns (True, value) for a known key and (False, ...) for an unknown one."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                info.VendorName = "Basler"
                ok, value = info.GetPropertyValue("VendorName")
                self.assertTrue(ok)
                self.assertEqual(str(value), "Basler")
                ok_missing, _ = info.GetPropertyValue("NonExistentKey")
                self.assertFalse(ok_missing)

    def test_set_property_value(self):
        """SetPropertyValue sets a CInfoBase property accessible through the typed getter."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                info.SetPropertyValue("FriendlyName", "FromGeneric")
                self.assertEqual(info.FriendlyName, "FromGeneric")

    def test_is_subset(self):
        """IsSubset returns True when all properties of the subset match."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                info.FriendlyName = "F"
                info.VendorName = "V"
                subset = cls()
                subset.FriendlyName = "F"
                self.assertTrue(info.IsSubset(subset))

    def test_is_subset_mismatch(self):
        """IsSubset returns False when a subset property does not match."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                info.FriendlyName = "F"
                other = cls()
                other.FriendlyName = "Other"
                self.assertFalse(info.IsSubset(other))

    def test_is_user_provided(self):
        """IsUserProvided returns True for a user-constructed Info instance."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                self.assertIsInstance(info.IsUserProvided(), bool)
                self.assertTrue(info.IsUserProvided())

    # ------------------------------------------------------------------
    # Python dict interface (added in Info.i via %extend Pylon::CInfoBase)
    # ------------------------------------------------------------------

    def test_dict_getitem(self):
        """info[key] returns the same value as the typed property getter."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                info.FriendlyName = "F"
                self.assertEqual(info["FriendlyName"], "F")

    def test_dict_getitem_missing_raises_key_error(self):
        """info[key] raises KeyError when the property has not been set."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                with self.assertRaises(KeyError):
                    _ = info["NonExistentKey"]

    def test_dict_setitem(self):
        """info[key] = value sets the property accessible via the typed getter."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                info["FriendlyName"] = "F"
                self.assertEqual(info.FriendlyName, "F")

    def test_dict_contains(self):
        """'key' in info returns True for a set property and False for an unknown key."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                info.FriendlyName = "F"
                self.assertIn("FriendlyName", info)
                self.assertNotIn("NonExistentKey", info)

    def test_dict_iter(self):
        """Iterating over info yields all set property name strings."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                info.FriendlyName = "F"
                info.VendorName = "V"
                iterated = list(info)
                self.assertIn("FriendlyName", iterated)
                self.assertIn("VendorName", iterated)

    def test_dict_keys_values_items(self):
        """keys(), values(), and items() return consistent parallel sequences."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                info.FriendlyName = "F"
                info.VendorName = "V"
                self.assertEqual(
                    list(info.items()),
                    list(zip(info.keys(), info.values())),
                )

    def test_dict_to_dict(self):
        """to_dict() returns a plain Python dict with all set CInfoBase properties."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                for prop_name, value in CINFO_BASE_PROPERTIES:
                    setattr(info, prop_name, value)
                as_dict = info.to_dict()
                self.assertIsInstance(as_dict, dict)
                for prop_name, value in CINFO_BASE_PROPERTIES:
                    self.assertEqual(as_dict[prop_name], value)

    def test_dict_update(self):
        """update() sets multiple CInfoBase properties from a plain dict."""
        for name, cls in INFO_CLASSES:
            with self.subTest(info_class=name):
                info = cls()
                info.update({"FriendlyName": "F", "VendorName": "V"})
                self.assertEqual(info.FriendlyName, "F")
                self.assertEqual(info.VendorName, "V")


if __name__ == "__main__":
    unittest.main()
