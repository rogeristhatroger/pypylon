from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon, genicam
from unittest import mock
import unittest
import warnings
import sys

def _make_mono8_image(width=64, height=48):
    """Return a valid Mono8 PylonImage filled with a saw-tooth byte pattern."""
    image_mono8 = pylon.PylonImage.Create(pylon.PixelType_Mono8, width, height)
    with image_mono8.GetArrayZeroCopy() as numpy_array:
        for y in range(image_mono8.Height):
            for x in range(image_mono8.Width):
                numpy_array[y, x] = (x + y) % 256
    return image_mono8

def _make_sawtooth_image(pixel_type, width=64, height=48):
    """Return a PylonImage of the given pixel type filled with a saw-tooth byte pattern."""
    if pixel_type == pylon.PixelType_Mono8:
        return _make_mono8_image(width, height)
    import numpy as np
    image = pylon.PylonImage.Create(pixel_type, width, height)
    with image.GetArrayZeroCopy(raw=True) as buf:
        buf[:] = np.arange(buf.size, dtype=np.uint8)
    return image


def _camera_available():
    try:
        tlf = pylon.TlFactory.GetInstance()
        return len(tlf.EnumerateDevices()) > 0
    except Exception:
        return False


def _pylon_image_window_available():
    return sys.platform == "win32" and hasattr(pylon, "PylonImageWindow")


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
        image = _make_sawtooth_image(pylon.PixelType_Mono8)
        # On Windows this opens a window; on other platforms it's a no-op or
        # uses cv2. Either way it should not raise.
        pylon.DisplayImage(1, image)
        if _pylon_image_window_available():
            window = pylon.PylonImageWindow()
            window.Attach(1)
            window.Close()

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
        if _pylon_image_window_available():
            window = pylon.PylonImageWindow()
            window.Attach(1)
            window.Close()

    def test_display_image_accepts_pylon_data_component(self):
        if not _camera_available():
            self.skipTest("No camera available (real or emulated)")
        with self.create_first() as camera:
            camera.Open()
            grab_result = camera.GrabOne(5000)
        component = grab_result.GetFirstImageDataComponent()
        try:
            pylon.DisplayImage(1, component)
        finally:
            component.Release()
            grab_result.Release()
            if _pylon_image_window_available():
                window = pylon.PylonImageWindow()
                window.Attach(1)
                window.Close()


@unittest.skipUnless(
    _pylon_image_window_available(),
    "PylonImageWindow is available on Windows builds with HAVE_PYLON_GUI",
)
class PylonImageWindowTestSuite(PylonEmuTestCase):

    def _create_window(self, win_index):
        window = pylon.PylonImageWindow()
        window.Create(win_index)
        return window

    def _grab_result(self):
        with self.create_first() as camera:
            camera.Open()
            return camera.GrabOne(5000)

    def test_pylon_image_window_default_construction_is_invalid(self):
        """Default construction creates an invalid PylonImageWindow."""
        window = pylon.PylonImageWindow()
        self.assertFalse(window.IsValid())

    def test_pylon_image_window_get_window_index_tracks_validity(self):
        """GetWindowIndex reflects the created window index and resets after Close()."""
        window = pylon.PylonImageWindow()
        invalid_index = window.GetWindowIndex()
        window.Create(26)
        try:
            self.assertTrue(window.IsValid())
            self.assertEqual(window.GetWindowIndex(), 26)
        finally:
            window.Close()
        self.assertFalse(window.IsValid())
        self.assertEqual(window.GetWindowIndex(), invalid_index)

    def test_pylon_image_window_create_with_all_five_arguments(self):
        """Create accepts all five arguments: winIndex, x, y, nWidth, nHeight."""
        window = pylon.PylonImageWindow()
        window.Create(25, 10, 20, 320, 240)
        window.Show()
        try:
            self.assertTrue(window.IsValid())
            self.assertEqual(window.GetWindowIndex(), 25)
        finally:
            window.Close()

    def test_pylon_image_window_get_window_handle_returns_native_handle(self):
        """GetWindowHandle returns a native non-zero window handle for a created window."""
        window = self._create_window(27)
        try:
            handle = window.GetWindowHandle()
            self.assertIsInstance(handle, int)
            self.assertGreater(handle, 0)
        finally:
            window.Close()

    def test_pylon_image_window_get_window_handle_raises_when_invalid(self):
        """GetWindowHandle raises when the window has not been created."""
        window = pylon.PylonImageWindow()
        with self.assertRaises(genicam.InvalidArgumentException):
            window.GetWindowHandle()

    def test_pylon_image_window_is_visible_returns_false_when_invalid(self):
        """IsVisible returns False for a window that has not been created (does not raise)."""
        window = pylon.PylonImageWindow()
        self.assertFalse(window.IsVisible())

    def test_pylon_image_window_attach_and_detach_round_trip_window_index(self):
        """Detach returns the current window index and Attach restores it on another object."""
        window = self._create_window(28)
        attached_window = pylon.PylonImageWindow()
        try:
            detached_index = window.Detach()
            self.assertEqual(detached_index, 28)
            self.assertFalse(window.IsValid())
            attached_window.Attach(detached_index)
            self.assertTrue(attached_window.IsValid())
            self.assertEqual(attached_window.GetWindowIndex(), detached_index)
        finally:
            attached_window.Close()
            window.Close()

    def test_pylon_image_window_show_hide_and_is_visible_are_callable(self):
        """Show, Hide, and IsVisible can be called for a created window without raising."""
        window = self._create_window(29)
        try:
            self.assertIsInstance(window.IsVisible(), bool)
            window.Show()
            window.SetImage(_make_mono8_image(200, 100))
            self.assertTrue(window.IsVisible())
            self.assertTrue(window.IsValid())
            self.assertIsInstance(window.IsVisible(), bool)
            window.Hide()
            self.assertTrue(window.IsValid())
            self.assertIsInstance(window.IsVisible(), bool)
            self.assertTrue(window.IsVisible())
        finally:
            window.Close()

    def test_pylon_image_window_close_invalidates_the_object(self):
        """Close destroys the window and leaves the object invalid."""
        window = self._create_window(30)
        self.assertTrue(window.Close())
        self.assertFalse(window.IsValid())
        self.assertFalse(window.Close())

    def test_pylon_image_window_set_image_accepts_grab_result(self):
        """SetImage accepts a GrabResult instance."""
        if not _camera_available():
            self.skipTest("No camera available (real or emulated)")
        grab_result = self._grab_result()
        window = self._create_window(31)
        try:
            self.assertTrue(grab_result.GrabSucceeded())
            window.SetImage(grab_result)
            window.SetImage(grab_result.GetFirstImageDataComponent())
        finally:
            window.Close()
            grab_result.Release()

    def test_display_image_accepts_pylon_image_when_window_available(self):
        """DisplayImage accepts a PylonImage when PylonImageWindow is available."""
        image = _make_sawtooth_image(pylon.PixelType_Mono8)
        pylon.DisplayImage(22, image)
        window = pylon.PylonImageWindow()
        window.Attach(22)
        window.Close()

    def test_display_image_accepts_grab_result_when_window_available(self):
        """DisplayImage accepts a GrabResult when PylonImageWindow is available."""
        if not _camera_available():
            self.skipTest("No camera available (real or emulated)")
        grab_result = self._grab_result()
        try:
            self.assertTrue(grab_result.GrabSucceeded())
            pylon.DisplayImage(23, grab_result)
        finally:
            grab_result.Release()
            window = pylon.PylonImageWindow()
            window.Attach(23)
            window.Close()

    def test_display_image_accepts_pylon_data_component_when_window_available(self):
        """DisplayImage accepts a PylonDataComponent when PylonImageWindow is available."""
        if not _camera_available():
            self.skipTest("No camera available (real or emulated)")
        grab_result = self._grab_result()
        component = grab_result.GetFirstImageDataComponent()
        try:
            self.assertTrue(component.IsValid())
            pylon.DisplayImage(24, component)
        finally:
            component.Release()
            grab_result.Release()
            window = pylon.PylonImageWindow()
            window.Attach(24)
            window.Close()


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
        image = _make_sawtooth_image(pylon.PixelType_Mono8)
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
        image = _make_sawtooth_image(pylon.PixelType_Mono8)
        with mock.patch.dict(sys.modules, {"cv2": mock_cv2}):
            pylon.DisplayImage(1, image)
            mock_cv2.imshow.assert_called_once()
            mock_cv2.waitKey.assert_called_once_with(1)

    def test_fallback_converts_bayer_to_bgr(self):
        mock_cv2 = mock.MagicMock()
        image = _make_sawtooth_image(pylon.PixelType_BayerRG8)
        with mock.patch.dict(sys.modules, {"cv2": mock_cv2}):
            pylon.DisplayImage(1, image)
            mock_cv2.imshow.assert_called_once()
            arr = mock_cv2.imshow.call_args[0][1]
            self.assertEqual(arr.ndim, 3, "Bayer should be converted to 3-channel BGR")
            self.assertEqual(arr.shape[2], 3)

    def test_fallback_passes_mono_directly(self):
        mock_cv2 = mock.MagicMock()
        image = _make_sawtooth_image(pylon.PixelType_Mono8)
        with mock.patch.dict(sys.modules, {"cv2": mock_cv2}):
            pylon.DisplayImage(1, image)
            mock_cv2.imshow.assert_called_once()
            arr = mock_cv2.imshow.call_args[0][1]
            self.assertEqual(arr.ndim, 2, "Mono8 should stay 2D")

    def test_fallback_cv2_reuses_on_second_call(self):
        mock_cv2 = mock.MagicMock()
        image = _make_sawtooth_image(pylon.PixelType_Mono8)
        with mock.patch.dict(sys.modules, {"cv2": mock_cv2}):
            pylon.DisplayImage(1, image)
            pylon.DisplayImage(2, image)
            self.assertEqual(mock_cv2.imshow.call_count, 2)


if __name__ == "__main__":
    unittest.main()
