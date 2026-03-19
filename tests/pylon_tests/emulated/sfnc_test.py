from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest

class SfncTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Camera SFNC version
    # ------------------------------------------------------------------

    def test_sfnc_camera_version(self):
        """GetSfncVersion returns Sfnc_VersionUndefined for the emulated camera."""
        camera = self.create_first()
        camera.Open()
        sfnc = pylon.GetSfncVersion(camera.GetNodeMap()) # Emu has no SFNC version, so this should return Sfnc_VersionUndefined
        self.assertEqual(sfnc, pylon.Sfnc_VersionUndefined)
        self.assertEqual("<VersionInfo 0.0.0>", str(sfnc))
        camera.Close()

    # ------------------------------------------------------------------
    # Exact version numbers encoded in each constant's name
    # ------------------------------------------------------------------

    def test_sfnc_version_undefined_is_0_0_0(self):
        v = pylon.Sfnc_VersionUndefined
        self.assertEqual(0, v.getMajor())
        self.assertEqual(0, v.getMinor())
        self.assertEqual(0, v.getSubminor())

    def test_sfnc_1_2_1_is_1_2_1(self):
        v = pylon.Sfnc_1_2_1
        self.assertEqual(1, v.getMajor())
        self.assertEqual(2, v.getMinor())
        self.assertEqual(1, v.getSubminor())

    def test_sfnc_1_3_0_is_1_3_0(self):
        v = pylon.Sfnc_1_3_0
        self.assertEqual(1, v.getMajor())
        self.assertEqual(3, v.getMinor())
        self.assertEqual(0, v.getSubminor())

    def test_sfnc_1_4_0_is_1_4_0(self):
        v = pylon.Sfnc_1_4_0
        self.assertEqual(1, v.getMajor())
        self.assertEqual(4, v.getMinor())
        self.assertEqual(0, v.getSubminor())

    def test_sfnc_1_5_0_is_1_5_0(self):
        v = pylon.Sfnc_1_5_0
        self.assertEqual(1, v.getMajor())
        self.assertEqual(5, v.getMinor())
        self.assertEqual(0, v.getSubminor())

    def test_sfnc_1_5_1_is_1_5_1(self):
        v = pylon.Sfnc_1_5_1
        self.assertEqual(1, v.getMajor())
        self.assertEqual(5, v.getMinor())
        self.assertEqual(1, v.getSubminor())

    def test_sfnc_2_0_0_is_2_0_0(self):
        v = pylon.Sfnc_2_0_0
        self.assertEqual(2, v.getMajor())
        self.assertEqual(0, v.getMinor())
        self.assertEqual(0, v.getSubminor())

    def test_sfnc_2_1_0_is_2_1_0(self):
        v = pylon.Sfnc_2_1_0
        self.assertEqual(2, v.getMajor())
        self.assertEqual(1, v.getMinor())
        self.assertEqual(0, v.getSubminor())

    def test_sfnc_2_2_0_is_2_2_0(self):
        v = pylon.Sfnc_2_2_0
        self.assertEqual(2, v.getMajor())
        self.assertEqual(2, v.getMinor())
        self.assertEqual(0, v.getSubminor())

    def test_sfnc_2_3_0_is_2_3_0(self):
        v = pylon.Sfnc_2_3_0
        self.assertEqual(2, v.getMajor())
        self.assertEqual(3, v.getMinor())
        self.assertEqual(0, v.getSubminor())

    def test_sfnc_2_4_0_is_2_4_0(self):
        v = pylon.Sfnc_2_4_0
        self.assertEqual(2, v.getMajor())
        self.assertEqual(4, v.getMinor())
        self.assertEqual(0, v.getSubminor())

    def test_sfnc_2_5_0_is_2_5_0(self):
        v = pylon.Sfnc_2_5_0
        self.assertEqual(2, v.getMajor())
        self.assertEqual(5, v.getMinor())
        self.assertEqual(0, v.getSubminor())

    # ------------------------------------------------------------------
    # Constants are ordered strictly as expected
    # ------------------------------------------------------------------

    def test_sfnc_constants_ordering(self):
        """The Sfnc_* constants are strictly ascending in version order."""
        self.assertLess(pylon.Sfnc_VersionUndefined, pylon.Sfnc_1_2_1)
        self.assertLess(pylon.Sfnc_1_2_1,            pylon.Sfnc_1_3_0)
        self.assertLess(pylon.Sfnc_1_3_0,            pylon.Sfnc_1_4_0)
        self.assertLess(pylon.Sfnc_1_4_0,            pylon.Sfnc_1_5_0)
        self.assertLess(pylon.Sfnc_1_5_0,            pylon.Sfnc_1_5_1)
        self.assertLess(pylon.Sfnc_1_5_1,            pylon.Sfnc_2_0_0)
        self.assertLess(pylon.Sfnc_2_0_0,            pylon.Sfnc_2_1_0)
        self.assertLess(pylon.Sfnc_2_1_0,            pylon.Sfnc_2_2_0)
        self.assertLess(pylon.Sfnc_2_2_0,            pylon.Sfnc_2_3_0)
        self.assertLess(pylon.Sfnc_2_3_0,            pylon.Sfnc_2_4_0)
        self.assertLess(pylon.Sfnc_2_4_0,            pylon.Sfnc_2_5_0)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()