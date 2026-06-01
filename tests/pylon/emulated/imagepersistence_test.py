"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylon/ImagePersistence.i and the enums declared in
include/pylon/ImagePersistence.h.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import os
import tempfile
import unittest

class ImagePersistenceTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _grab_mono8(self):
        """Return a successfully grabbed Mono8 frame from the emulator."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            grab_result = camera.GrabOne(5000)
            self.assertTrue(grab_result.GrabSucceeded(), "GrabOne() on emulator must succeed")
            self.assertEqual(grab_result.PixelType, pylon.PixelType_Mono8)
            self._grab_results.append(grab_result)
            return grab_result

    def _tmp_path(self, suffix):
        """Return a temporary file path with a unicode prefix and the given suffix (deleted on tearDown).

        The unicode prefix (e.g. 'pylön_') exercises the full unicode path support in Save/Load.
        """
        fd, path = tempfile.mkstemp(prefix="pylön_", suffix=suffix)
        os.close(fd)
        os.unlink(path)
        self._tmp_files.append(path)
        return path

    def _save_and_get_path(self, image, fmt, suffix):
        """Save image to a temp file and return the path."""
        path = self._tmp_path(suffix)
        pylon.ImagePersistence.Save(fmt, path, image)
        return path

    def setUp(self):
        self._tmp_files = []
        self._grab_results = []

    def tearDown(self):
        for grab_result in self._grab_results:
            try:
                # Grab results from camera devices typically occupy a buffer pool slot or several MB of memory,
                # so it is good practice to always release them explicitly when they are no longer needed.
                grab_result.Release()
            except Exception:
                pass
        for path in self._tmp_files:
            try:
                os.unlink(path)
            except FileNotFoundError:
                pass

    # ------------------------------------------------------------------
    # EImageFileFormat enum
    # ------------------------------------------------------------------

    def test_image_file_format_enum_values(self):
        """All EImageFileFormat constants are exposed on pylon with their documented integer values."""
        self.assertEqual(pylon.ImageFileFormat_Bmp,  0)
        self.assertEqual(pylon.ImageFileFormat_Tiff, 1)
        self.assertEqual(pylon.ImageFileFormat_Jpeg, 2)
        self.assertEqual(pylon.ImageFileFormat_Png,  3)
        self.assertEqual(pylon.ImageFileFormat_Raw,  4)
        self.assertEqual(pylon.ImageFileFormat_Dng,  5)

    def test_image_file_format_enum_values_are_distinct(self):
        """Every EImageFileFormat value is unique."""
        values = [
            pylon.ImageFileFormat_Bmp,
            pylon.ImageFileFormat_Tiff,
            pylon.ImageFileFormat_Jpeg,
            pylon.ImageFileFormat_Png,
            pylon.ImageFileFormat_Raw,
            pylon.ImageFileFormat_Dng,
        ]
        self.assertEqual(len(values), len(set(values)))

    # ------------------------------------------------------------------
    # %rename directives: CImagePersistence -> ImagePersistence,
    #                     CImagePersistenceOptions -> ImagePersistenceOptions
    # ------------------------------------------------------------------

    def test_renamed_classes_are_exposed(self):
        """ImagePersistence and ImagePersistenceOptions are exposed on pylon under their renamed names."""
        self.assertTrue(hasattr(pylon, "ImagePersistence"))
        self.assertTrue(hasattr(pylon, "ImagePersistenceOptions"))

    def test_c_prefixed_names_are_hidden(self):
        """The original C-prefixed class names are not exposed on pylon."""
        self.assertFalse(hasattr(pylon, "CImagePersistence"))
        self.assertFalse(hasattr(pylon, "CImagePersistenceOptions"))

    # ------------------------------------------------------------------
    # Ignored overloads are not exposed
    # ------------------------------------------------------------------

    def test_raw_buffer_save_overload_is_hidden(self):
        """The Save(format, filename, void*, ...) raw-buffer overload is not exposed in Python."""
        # Passing 9 positional args matching the ignored raw-buffer signature
        # must raise TypeError because only the IImage overload is mapped.
        grab_result = self._grab_mono8()
        path = self._tmp_path(".bmp")
        with self.assertRaises(TypeError):
            pylon.ImagePersistence.Save(
                pylon.ImageFileFormat_Bmp,
                path,
                None,                            # pBuffer — not an IImage
                grab_result.PayloadSize,         # bufferSize
                pylon.PixelType_Mono8,           # pixelType
                grab_result.Width,               # width
                grab_result.Height,              # height
                0,                               # paddingX
                pylon.ImageOrientation_TopDown,  # orientation
            )

    def test_raw_geometry_can_save_without_conversion_overload_is_hidden(self):
        """CanSaveWithoutConversion(format, EPixelType, ...) raw-geometry overload is not exposed."""
        with self.assertRaises(TypeError):
            pylon.ImagePersistence.CanSaveWithoutConversion(
                pylon.ImageFileFormat_Bmp,
                pylon.PixelType_Mono8,           # pixelType — not an IImage
                640, 480, 0,
                pylon.ImageOrientation_TopDown,
            )

    def test_load_from_memory_is_hidden(self):
        """LoadFromMemory is not exposed on pylon.ImagePersistence."""
        self.assertFalse(hasattr(pylon.ImagePersistence, "LoadFromMemory"))

    # ------------------------------------------------------------------
    # ImagePersistenceOptions
    # ------------------------------------------------------------------

    def test_image_persistence_options_default_quality(self):
        """Default-constructed ImagePersistenceOptions reports quality 90."""
        options = pylon.ImagePersistenceOptions()
        self.assertEqual(options.GetQuality(), 90)
        self.assertEqual(options.Quality, 90)

    def test_image_persistence_options_set_quality_roundtrip(self):
        """SetQuality(n) is readable through GetQuality() for boundary and mid values."""
        options = pylon.ImagePersistenceOptions()
        for quality in (0, 50, 100):
            with self.subTest(quality=quality):
                options.SetQuality(quality)
                self.assertEqual(options.GetQuality(), quality)
                options.Quality = quality
                self.assertEqual(options.Quality, quality)

    def test_two_options_instances_are_independent(self):
        """Two ImagePersistenceOptions instances do not share state."""
        options_a = pylon.ImagePersistenceOptions()
        options_b = pylon.ImagePersistenceOptions()
        options_a.SetQuality(10)
        options_b.SetQuality(90)
        self.assertEqual(options_a.GetQuality(), 10)
        self.assertEqual(options_b.GetQuality(), 90)

    # ------------------------------------------------------------------
    # Save / Load — lossless formats (TIFF, BMP, PNG)
    # ------------------------------------------------------------------

    def test_save_and_load_roundtrip_tiff(self):
        """Save(Tiff, path, grab_result) + Load(path) produces a Mono8 image with the same dimensions."""
        path = self._tmp_path(".tiff")
        grab_result = self._grab_mono8()
        pylon.ImagePersistence.Save(pylon.ImageFileFormat_Tiff, path, grab_result)
        self.assertTrue(os.path.isfile(path))
        with pylon.ImagePersistence.Load(path) as loaded_image:
            self.assertIsInstance(loaded_image, pylon.PylonImage)
            self.assertEqual(loaded_image.GetPixelType(), pylon.PixelType_Mono8)
            self.assertEqual(loaded_image.Width, grab_result.Width)
            self.assertEqual(loaded_image.Height, grab_result.Height)

    def test_save_and_load_roundtrip_bmp(self):
        """Save(Bmp, path, grab_result) + Load(path) produces an image with the same dimensions."""
        path = self._tmp_path(".bmp")
        grab_result = self._grab_mono8()
        # BMP does not natively support Mono8; pylon converts it to BGR8 on save.
        pylon.ImagePersistence.Save(pylon.ImageFileFormat_Bmp, path, grab_result)
        self.assertTrue(os.path.isfile(path))
        with pylon.ImagePersistence.Load(path) as loaded_image:
            self.assertIsInstance(loaded_image, pylon.PylonImage)
            self.assertEqual(loaded_image.Width, grab_result.Width)
            self.assertEqual(loaded_image.Height, grab_result.Height)

    def test_save_and_load_roundtrip_png(self):
        """Save(Png, path, grab_result) + Load(path) produces an image with the same dimensions."""
        path = self._tmp_path(".png")
        grab_result = self._grab_mono8()
        pylon.ImagePersistence.Save(pylon.ImageFileFormat_Png, path, grab_result)
        self.assertTrue(os.path.isfile(path))
        with pylon.ImagePersistence.Load(path) as loaded_image:
            self.assertIsInstance(loaded_image, pylon.PylonImage)
            self.assertEqual(loaded_image.Width, grab_result.Width)
            self.assertEqual(loaded_image.Height, grab_result.Height)

    def test_save_accepts_pylon_image_as_source(self):
        """Save accepts a PylonImage (IImage) as the source, not just a grab result."""
        grab_result = self._grab_mono8()
        path = self._save_and_get_path(grab_result, pylon.ImageFileFormat_Tiff, ".tiff")
        with pylon.ImagePersistence.Load(path) as source_image:
            path2 = self._tmp_path(".tiff")
            pylon.ImagePersistence.Save(pylon.ImageFileFormat_Tiff, path2, source_image)
            self.assertTrue(os.path.isfile(path2))
            self.assertGreater(os.path.getsize(path2), 0)


    # ------------------------------------------------------------------
    # Save with options — JPEG quality
    # ------------------------------------------------------------------

    def test_save_jpeg_with_quality_options(self):
        """Save(Jpeg, path, image, options) accepts an ImagePersistenceOptions object."""
        grab_result = self._grab_mono8()
        for quality in (0, 100):
            with self.subTest(quality=quality):
                path = self._tmp_path(".jpg")
                options = pylon.ImagePersistenceOptions()
                options.SetQuality(quality)
                pylon.ImagePersistence.Save(
                    pylon.ImageFileFormat_Jpeg, path, grab_result, options
                )
                self.assertTrue(os.path.isfile(path))
                self.assertGreater(os.path.getsize(path), 0)

    def test_save_jpeg_higher_quality_produces_larger_file(self):
        """JPEG file at quality=100 is larger than at quality=0 for the same source image."""
        grab_result = self._grab_mono8()
        path_low = self._tmp_path(".jpg")
        path_high = self._tmp_path(".jpg")
        options = pylon.ImagePersistenceOptions()
        options.SetQuality(0)
        pylon.ImagePersistence.Save(pylon.ImageFileFormat_Jpeg, path_low, grab_result, options)
        options.SetQuality(100)
        pylon.ImagePersistence.Save(pylon.ImageFileFormat_Jpeg, path_high, grab_result, options)
        self.assertGreater(os.path.getsize(path_high), os.path.getsize(path_low))

    def test_save_without_options_uses_default_quality(self):
        """Save without an options argument writes a valid JPEG (uses the default quality 90)."""
        path = self._tmp_path(".jpg")
        grab_result = self._grab_mono8()
        pylon.ImagePersistence.Save(pylon.ImageFileFormat_Jpeg, path, grab_result)
        self.assertTrue(os.path.isfile(path))
        self.assertGreater(os.path.getsize(path), 0)

    # ------------------------------------------------------------------
    # CanSaveWithoutConversion — IImage overload
    # ------------------------------------------------------------------

    def test_can_save_without_conversion_mono8_to_tiff(self):
        """CanSaveWithoutConversion(Tiff, Mono8 image) returns True (natively supported)."""
        grab_result = self._grab_mono8()
        self.assertTrue(
            pylon.ImagePersistence.CanSaveWithoutConversion(
                pylon.ImageFileFormat_Tiff, grab_result
            )
        )

    def test_can_save_without_conversion_mono8_to_bmp(self):
        """CanSaveWithoutConversion(Bmp, Mono8 image) returns True."""
        grab_result = self._grab_mono8()
        self.assertTrue(
            pylon.ImagePersistence.CanSaveWithoutConversion(
                pylon.ImageFileFormat_Bmp, grab_result
            )
        )

    def test_can_save_without_conversion_mono8_to_png(self):
        """CanSaveWithoutConversion(Png, Mono8 image) returns True."""
        grab_result = self._grab_mono8()
        self.assertTrue(
            pylon.ImagePersistence.CanSaveWithoutConversion(
                pylon.ImageFileFormat_Png, grab_result
            )
        )

    def test_can_save_without_conversion_accepts_pylon_image(self):
        """CanSaveWithoutConversion accepts a PylonImage (IImage) as source."""
        grab_result = self._grab_mono8()
        path = self._save_and_get_path(grab_result, pylon.ImageFileFormat_Tiff, ".tiff")
        with pylon.ImagePersistence.Load(path) as pylon_image:
            result = pylon.ImagePersistence.CanSaveWithoutConversion(
                pylon.ImageFileFormat_Tiff, pylon_image
            )
            self.assertIsInstance(result, bool)
            self.assertTrue(result)

    def test_can_save_without_conversion_returns_bool(self):
        """CanSaveWithoutConversion always returns a bool."""
        grab_result = self._grab_mono8()
        for fmt in (
            pylon.ImageFileFormat_Bmp,
            pylon.ImageFileFormat_Tiff,
            pylon.ImageFileFormat_Jpeg,
            pylon.ImageFileFormat_Png,
        ):
            with self.subTest(fmt=fmt):
                result = pylon.ImagePersistence.CanSaveWithoutConversion(fmt, grab_result)
                self.assertIsInstance(result, bool)

    # ------------------------------------------------------------------
    # Load — returns a context-manager-compatible PylonImage
    # ------------------------------------------------------------------

    def test_load_returns_pylon_image_as_context_manager(self):
        """Load(path) returns a PylonImage that works as a context manager."""
        path = self._tmp_path(".tiff")
        grab_result = self._grab_mono8()
        pylon.ImagePersistence.Save(pylon.ImageFileFormat_Tiff, path, grab_result)
        with pylon.ImagePersistence.Load(path) as loaded_image:
            self.assertIsInstance(loaded_image, pylon.PylonImage)
            self.assertTrue(loaded_image.thisown)
            self.assertGreater(loaded_image.Width, 0)
            self.assertGreater(loaded_image.Height, 0)

    def test_load_nonexistent_file_raises(self):
        """Load() raises an exception when the file does not exist."""
        with self.assertRaises(Exception):
            pylon.ImagePersistence.Load("/nonexistent/path/to/image.tiff")

    def test_load_result_is_independent_between_calls(self):
        """Two consecutive Load() calls return independent PylonImage instances."""
        grab_result = self._grab_mono8()
        path = self._save_and_get_path(grab_result, pylon.ImageFileFormat_Tiff, ".tiff")
        image_a = pylon.ImagePersistence.Load(path)
        image_b = pylon.ImagePersistence.Load(path)
        self.assertIsNot(image_a, image_b)
        self.assertTrue(image_a.thisown)
        self.assertTrue(image_b.thisown)

    # ------------------------------------------------------------------
    # Save — PylonDataComponent as source
    # ------------------------------------------------------------------

    def test_save_accepts_pylon_data_component_as_source(self):
        """Save accepts a PylonDataComponent (IImage) obtained via GrabResult.GetFirstImageDataComponent()."""
        grab_result = self._grab_mono8()
        component = grab_result.GetFirstImageDataComponent()
        try:
            path = self._tmp_path(".tiff")
            pylon.ImagePersistence.Save(pylon.ImageFileFormat_Tiff, path, component)
            with pylon.ImagePersistence.Load(path) as loaded:
                self.assertEqual(loaded.Width, grab_result.Width)
                self.assertEqual(loaded.Height, grab_result.Height)
        finally:
            component.Release()

    # ------------------------------------------------------------------
    # Save — PylonImage created via AttachGrabResultBuffer as source
    # ------------------------------------------------------------------

    def test_save_accepts_pylon_image(self):
        """Save accepts a PylonImage."""
        grab_result = self._grab_mono8()
        image = pylon.PylonImage()
        image.AttachGrabResultBuffer(grab_result)
        try:
            path = self._tmp_path(".tiff")
            pylon.ImagePersistence.Save(pylon.ImageFileFormat_Tiff, path, image)
            with pylon.ImagePersistence.Load(path) as loaded:
                self.assertEqual(loaded.Width, grab_result.Width)
                self.assertEqual(loaded.Height, grab_result.Height)
                self.assertEqual(loaded.GetPixelType(), pylon.PixelType_Mono8)
        finally:
            image.Release()

    # ------------------------------------------------------------------
    # PylonImage.Save / PylonImage.Load convenience methods
    # ------------------------------------------------------------------

    def test_pylon_image_save_and_load_convenience_methods(self):
        """PylonImage.Save() and PylonImage.Load() are convenience wrappers for ImagePersistence."""
        path = self._tmp_path(".tiff")
        grab_result = self._grab_mono8()
        # Save via ImagePersistence to create the file
        pylon.ImagePersistence.Save(pylon.ImageFileFormat_Tiff, path, grab_result)
        # Load via the PylonImage instance method
        with pylon.PylonImage() as pylon_image:
            pylon_image.Load(path)
            self.assertEqual(pylon_image.GetPixelType(), pylon.PixelType_Mono8)
            self.assertEqual(pylon_image.Width, grab_result.Width)
            self.assertEqual(pylon_image.Height, grab_result.Height)
            # Save back via the instance method
            path2 = self._tmp_path(".tiff")
            pylon_image.Save(pylon.ImageFileFormat_Tiff, path2)
            self.assertTrue(os.path.isfile(path2))


if __name__ == "__main__":
    unittest.main()

