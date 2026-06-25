"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/FeaturePersistence.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import tempfile
import os
import unittest


class FeaturePersistenceTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Save / Load
    # ------------------------------------------------------------------

    def test_save_and_load(self):
        """Save writes camera features to a file and Load restores them."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.SetToMinimum()
            with tempfile.NamedTemporaryFile(prefix="pylön_", suffix=".pfs", delete=False) as file:
                file_path = file.name
            try:
                pylon.FeaturePersistence.Save(file_path, camera.NodeMap)
                camera.Width.SetToMaximum()
                pylon.FeaturePersistence.Load(file_path, camera.NodeMap)
                self.assertEqual(camera.Width.Value, camera.Width.Min)
            finally:
                os.remove(file_path)

    def test_save_and_load_validate_false(self):
        """Load with validate=False restores features without strict validation."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.SetToMinimum()
            with tempfile.NamedTemporaryFile(prefix="pylön_", suffix=".pfs", delete=False) as file:
                file_path = file.name
            try:
                pylon.FeaturePersistence.Save(file_path, camera.NodeMap)
                camera.Width.SetToMaximum()
                pylon.FeaturePersistence.Load(file_path, camera.NodeMap, False)
                self.assertEqual(camera.Width.Value, camera.Width.Min)
            finally:
                os.remove(file_path)

    # ------------------------------------------------------------------
    # SaveToString / LoadFromString
    # ------------------------------------------------------------------

    def test_save_to_string_and_load_from_string(self):
        """SaveToString serializes features to a string and LoadFromString restores them."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.SetToMinimum()
            camera_state = pylon.FeaturePersistence.SaveToString(camera.NodeMap)
            camera.Width.SetToMaximum()
            pylon.FeaturePersistence.LoadFromString(camera_state, camera.NodeMap)
            self.assertEqual(camera.Width.Value, camera.Width.Min)

    def test_save_to_string_and_load_from_string_validate_false(self):
        """LoadFromString with validate=False restores features without strict validation."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.SetToMinimum()
            camera_state = pylon.FeaturePersistence.SaveToString(camera.NodeMap)
            camera.Width.SetToMaximum()
            pylon.FeaturePersistence.LoadFromString(camera_state, camera.NodeMap, False)
            self.assertEqual(camera.Width.Value, camera.Width.Min)


if __name__ == "__main__":
    unittest.main()
