from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
from unittest import mock
import unittest
import warnings
import sys


def _camera_available():
    try:
        tlf = pylon.TlFactory.GetInstance()
        return len(tlf.EnumerateDevices()) > 0
    except Exception:
        return False


class PylonGUITestSuite(PylonEmuTestCase):

    def test_display_image_is_callable(self):
        self.assertTrue(callable(pylon.DisplayImage))

    def test_display_image_rejects_string(self):
        with self.assertRaises(TypeError):
            pylon.DisplayImage(1, "not an image")

    def test_display_image_rejects_int(self):
        with self.assertRaises(TypeError):
            pylon.DisplayImage(1, 42)

    def test_display_image_rejects_none(self):
        with self.assertRaises(TypeError):
            pylon.DisplayImage(1, None)

    def test_display_image_rejects_numpy_array(self):
        import numpy as np
        arr = np.zeros((480, 640), dtype=np.uint8)
        with self.assertRaises(TypeError):
            pylon.DisplayImage(1, arr)

    def test_display_image_accepts_pylon_image(self):
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48)
        # On Windows this opens a window; on other platforms it's a no-op or
        # uses cv2. Either way it should not raise.
        pylon.DisplayImage(1, image)

    def test_display_image_accepts_grab_result(self):
        if not _camera_available():
            self.skipTest("No camera available (real or emulated)")
        camera = self.create_first()
        camera.Open()
        camera.StartGrabbing(1)
        with camera.RetrieveResult(5000) as grab_result:
            self.assertTrue(grab_result.GrabSucceeded())
            pylon.DisplayImage(1, grab_result)
        camera.Close()


def _make_fallback_display():
    """Build a fresh fallback DisplayImage matching the logic in PylonGUI.i."""
    supported = (pylon.PylonImage, pylon.GrabResult)
    state = {"cv2": None}  # None=unchecked, False=unavailable, module ref
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed

    def _cv2_display(cv2, winIndex, image):
        pt = image.PixelType if hasattr(image, "PixelType") else None
        if pt is not None and pylon.IsBayer(pt):
            arr = converter.Convert(image).Array
        else:
            arr = image.Array
        cv2.imshow(f"pylon {winIndex}", arr)
        cv2.waitKey(1)

    def DisplayImage(winIndex, image):
        if not isinstance(image, supported):
            raise TypeError(
                f"Expected PylonImage or GrabResult, got {type(image).__name__}"
            )
        if state["cv2"] is False:
            return
        if state["cv2"] is None:
            try:
                import cv2
                _cv2_display(cv2, winIndex, image)
                state["cv2"] = cv2
            except Exception:
                state["cv2"] = False
                warnings.warn(
                    "pylon.DisplayImage requires Windows or opencv-python "
                    "(cv2) with GUI support; call ignored on this platform.",
                    stacklevel=2,
                )
            return
        _cv2_display(state["cv2"], winIndex, image)

    return DisplayImage, state


class PylonGUIFallbackTestSuite(PylonEmuTestCase):
    """Tests for the non-native (cv2 fallback) DisplayImage path.

    The fallback can also be activated at import time by setting
    PYLON_GUITEST=1 in the environment. These tests use monkey-patching
    instead so that each test method starts with a clean fallback state.
    """

    def setUp(self):
        self._orig = pylon.DisplayImage
        self._fallback, self._state = _make_fallback_display()
        pylon.DisplayImage = self._fallback

    def tearDown(self):
        pylon.DisplayImage = self._orig

    def test_fallback_rejects_bad_type(self):
        with self.assertRaises(TypeError):
            pylon.DisplayImage(1, "bad")

    def test_fallback_warns_once_when_cv2_missing(self):
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48)
        with mock.patch.dict(sys.modules, {"cv2": None}):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                pylon.DisplayImage(1, image)
                self.assertEqual(len(w), 1)
                self.assertIn("opencv-python", str(w[0].message))

            # Second call should be silent
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                pylon.DisplayImage(1, image)
                self.assertEqual(len(w), 0)

    def test_fallback_uses_cv2_when_available(self):
        mock_cv2 = mock.MagicMock()
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48)
        with mock.patch.dict(sys.modules, {"cv2": mock_cv2}):
            pylon.DisplayImage(1, image)
            mock_cv2.imshow.assert_called_once()
            mock_cv2.waitKey.assert_called_once_with(1)

    def test_fallback_converts_bayer_to_bgr(self):
        import numpy as np
        mock_cv2 = mock.MagicMock()
        image = pylon.PylonImage.Create(pylon.PixelType_BayerRG8, 64, 48)
        with mock.patch.dict(sys.modules, {"cv2": mock_cv2}):
            pylon.DisplayImage(1, image)
            mock_cv2.imshow.assert_called_once()
            arr = mock_cv2.imshow.call_args[0][1]
            self.assertEqual(arr.ndim, 3, "Bayer should be converted to 3-channel BGR")
            self.assertEqual(arr.shape[2], 3)

    def test_fallback_passes_mono_directly(self):
        import numpy as np
        mock_cv2 = mock.MagicMock()
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48)
        with mock.patch.dict(sys.modules, {"cv2": mock_cv2}):
            pylon.DisplayImage(1, image)
            mock_cv2.imshow.assert_called_once()
            arr = mock_cv2.imshow.call_args[0][1]
            self.assertEqual(arr.ndim, 2, "Mono8 should stay 2D")

    def test_fallback_cv2_reuses_on_second_call(self):
        mock_cv2 = mock.MagicMock()
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48)
        with mock.patch.dict(sys.modules, {"cv2": mock_cv2}):
            pylon.DisplayImage(1, image)
            pylon.DisplayImage(2, image)
            self.assertEqual(mock_cv2.imshow.call_count, 2)


if __name__ == "__main__":
    unittest.main()
