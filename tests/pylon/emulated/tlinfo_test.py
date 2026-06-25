"""\
This unit test checks the pypylon API exposed by `src/pylon/TlInfo.i`.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class TlInfoTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_construction(self):
        """Default construction produces a usable empty TlInfo."""
        info = pylon.TlInfo()
        self.assertIsNotNone(info)

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

    def test_equality(self):
        """Two TlInfo objects with the same TlInfo-specific properties compare equal."""
        info1 = pylon.TlInfo()
        info1.FileName = "producer.cti"
        info1.InfoID = "Basler/GenTL/1.0"
        info1.ModelName = "pylon GenTL Producer"
        info1.Version = "1.0.0"
        info2 = pylon.TlInfo()
        info2.FileName = "producer.cti"
        info2.InfoID = "Basler/GenTL/1.0"
        info2.ModelName = "pylon GenTL Producer"
        info2.Version = "1.0.0"
        self.assertEqual(info1, info2)

    def test_inequality(self):
        """Changing a TlInfo property changes equality."""
        info1 = pylon.TlInfo()
        info1.FileName = "producer_a.cti"
        info2 = pylon.TlInfo()
        info2.FileName = "producer_b.cti"
        self.assertNotEqual(info1, info2)

    def test_less_than(self):
        """Less-than orders TlInfo objects by DeviceClass rank (USB < GigE per pylon/Info.h)."""
        # CInfoBase::operator< documents the rule:
        # USB < GigE < CameraLink < GenTL (incl. CXP) < unknown < CamEmu.
        usb = pylon.TlInfo()
        usb.DeviceClass = "BaslerUsb"
        gige = pylon.TlInfo()
        gige.DeviceClass = "BaslerGigE"
        self.assertTrue(usb < gige)
        self.assertFalse(gige < usb)

    def test_less_than_same_device_class_not_less(self):
        """Less-than returns False in both directions when two TlInfo objects share the same DeviceClass."""
        left = pylon.TlInfo()
        left.DeviceClass = "BaslerGigE"
        right = pylon.TlInfo()
        right.DeviceClass = "BaslerGigE"
        self.assertFalse(left < right)
        self.assertFalse(right < left)

    # ------------------------------------------------------------------
    # CTlInfo-specific properties (from TlInfo.i)
    # ADD_PROP_GETSET(TlInfo, FileName)
    # ADD_PROP_GETSET(TlInfo, InfoID)
    # ADD_PROP_GETSET(TlInfo, ModelName)
    # ADD_PROP_GETSET(TlInfo, Version)
    # ------------------------------------------------------------------

    def test_file_name(self):
        """FileName property round-trips correctly."""
        info = pylon.TlInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsFileNameAvailable())
        self.assertEqual(info.FileName, pylon.TlInfo.GetPropertyNotAvailable())
        info.FileName = "producer.cti"
        self.assertTrue(info.IsFileNameAvailable())
        self.assertEqual(info.FileName, "producer.cti")

        # --- legacy: named getter / setter ---
        info.SetFileName("updated.cti")
        self.assertEqual(info.GetFileName(), "updated.cti")

        # --- generic: dict-style interface ---
        info[pylon.FileNameKey] = "dict.cti"
        self.assertEqual(info["FileName"], "dict.cti")

    def test_info_id(self):
        """InfoID property round-trips correctly."""
        info = pylon.TlInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsInfoIDAvailable())
        self.assertEqual(info.InfoID, pylon.TlInfo.GetPropertyNotAvailable())
        info.InfoID = "Basler/GenTL/1.0"
        self.assertTrue(info.IsInfoIDAvailable())
        self.assertEqual(info.InfoID, "Basler/GenTL/1.0")

        # --- legacy: named getter / setter ---
        info.SetInfoID("Basler/GenTL/2.0")
        self.assertEqual(info.GetInfoID(), "Basler/GenTL/2.0")

        # --- generic: dict-style interface ---
        info[pylon.InfoIDKey] = "Basler/GenTL/3.0"
        self.assertEqual(info["InfoID"], "Basler/GenTL/3.0")

    def test_model_name(self):
        """ModelName property round-trips correctly."""
        info = pylon.TlInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsModelNameAvailable())
        self.assertEqual(info.ModelName, pylon.TlInfo.GetPropertyNotAvailable())
        info.ModelName = "pylon GenTL Producer"
        self.assertTrue(info.IsModelNameAvailable())
        self.assertEqual(info.ModelName, "pylon GenTL Producer")

        # --- legacy: named getter / setter ---
        info.SetModelName("Updated Producer")
        self.assertEqual(info.GetModelName(), "Updated Producer")

        # --- generic: dict-style interface ---
        info[pylon.ModelNameKey] = "Dict Producer"
        self.assertEqual(info["ModelName"], "Dict Producer")

    def test_version(self):
        """Version property round-trips correctly."""
        info = pylon.TlInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsVersionAvailable())
        self.assertEqual(info.Version, pylon.TlInfo.GetPropertyNotAvailable())
        info.Version = "1.0.0"
        self.assertTrue(info.IsVersionAvailable())
        self.assertEqual(info.Version, "1.0.0")

        # --- legacy: named getter / setter ---
        info.SetVersion("2.0.0")
        self.assertEqual(info.GetVersion(), "2.0.0")

        # --- generic: dict-style interface ---
        info[pylon.VersionKey] = "3.0.0"
        self.assertEqual(info["Version"], "3.0.0")


if __name__ == "__main__":
    unittest.main()
