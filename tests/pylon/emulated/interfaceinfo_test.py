"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylon/InterfaceInfo.i.

InterfaceInfo.i renames Pylon::CInterfaceInfo to pylon.InterfaceInfo,
includes <pylon/InterfaceInfo.h>, and adds a single CInterfaceInfo-specific
property via ADD_PROP_GETSET:

    * InterfaceID

All other behaviour exposed on pylon.InterfaceInfo comes from the CInfoBase
contract mapped in src/pylon/Info.i, which is covered by info_test.py.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class InterfaceInfoTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_construction(self):
        """Default construction produces a valid empty InterfaceInfo."""
        info = pylon.InterfaceInfo()
        self.assertIsNotNone(info)

    def test_copy_construction(self):
        """Copy construction produces an InterfaceInfo equal to the original."""
        original = pylon.InterfaceInfo()
        original.InterfaceID = "eth0"
        original.FriendlyName = "Test Interface"
        copy = pylon.InterfaceInfo(original)
        self.assertEqual(copy.InterfaceID, original.InterfaceID)
        self.assertEqual(copy.FriendlyName, original.FriendlyName)

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

    def test_equality(self):
        """Two InterfaceInfo objects with the same properties compare equal."""
        info = pylon.InterfaceInfo()
        info.InterfaceID = "eth0"
        self.assertEqual(info, pylon.InterfaceInfo(info))

    def test_inequality(self):
        """Two InterfaceInfo objects with different InterfaceID values do not compare equal."""
        info1 = pylon.InterfaceInfo()
        info1.InterfaceID = "eth0"
        info2 = pylon.InterfaceInfo()
        info2.InterfaceID = "eth1"
        self.assertNotEqual(info1, info2)

    # ------------------------------------------------------------------
    # CInterfaceInfo-specific properties (from InterfaceInfo.i)
    # ADD_PROP_GETSET(InterfaceInfo, InterfaceID)
    # ------------------------------------------------------------------

    def test_interface_id(self):
        """InterfaceID property round-trips correctly."""
        info = pylon.InterfaceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsInterfaceIDAvailable())
        self.assertEqual(info.InterfaceID, pylon.InterfaceInfo.GetPropertyNotAvailable())
        info.InterfaceID = "eth0"
        self.assertTrue(info.IsInterfaceIDAvailable())
        self.assertEqual(info.InterfaceID, "eth0")

        # --- legacy: named getter / setter ---
        info.SetInterfaceID("eth1")
        self.assertEqual(info.GetInterfaceID(), "eth1")

        # --- generic: dict-style interface ---
        info[pylon.InterfaceIDKey] = "eth2"
        self.assertEqual(info["InterfaceID"], "eth2")


if __name__ == "__main__":
    unittest.main()
