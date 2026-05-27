"""\
This unit test checks the mapped pypylon API introduced by src/pylon/PylonImage.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
from pypylon import genicam
import unittest
import os

class PylonImageTestSuite(PylonEmuTestCase):

    def test_empty_pylon_image(self):
        testee = pylon.PylonImage()
        self.assertEqual(testee.PixelType, pylon.PixelType_Undefined)
        self.assertEqual(testee.IsValid(), False)
        self.assertEqual(testee.Width, 0)
        self.assertEqual(testee.Height, 0)
        self.assertEqual(testee.PaddingX, 0)
        self.assertEqual(testee.ImageSize, 0)
        self.assertEqual(testee.AllocatedBufferSize, 0)
        self.assertEqual(testee.Orientation, pylon.ImageOrientation_TopDown)
        self.assertEqual(testee.GetPixelType(), pylon.PixelType_Undefined)
        self.assertEqual(testee.GetWidth(), 0)
        self.assertEqual(testee.GetHeight(), 0)
        self.assertEqual(testee.GetPaddingX(), 0)
        self.assertEqual(testee.GetImageSize(), 0)
        self.assertEqual(testee.GetOrientation(), pylon.ImageOrientation_TopDown)
        self.assertEqual(testee.GetAllocatedBufferSize(), 0)
        try:
            testee.ImageFormat
        except ValueError:
            pass
        else:
            self.fail("Exception not raised.")
        try:
            testee.GetImageFormat()
        except ValueError:
            pass
        else:
            self.fail("Exception not raised.")
        try:
            testee.Array
        except ValueError:
            pass
        else:
            self.fail("Exception not raised.")
        testee.Buffer

    def test_container_load(self):
        testee = pylon.PylonImage()
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'barcode01.png')
        testee.Load(filename)
        self.assertEqual(testee.PixelType, pylon.PixelType_Mono8)
        self.assertEqual(testee.IsValid(), True)
        self.assertEqual(testee.Width, 1920)
        self.assertEqual(testee.Height, 1200)
        self.assertEqual(testee.PaddingX, 0)
        self.assertEqual(testee.ImageSize, 1920 * 1200)
        self.assertEqual(testee.AllocatedBufferSize, 1920 * 1200)
        self.assertEqual(testee.Orientation, pylon.ImageOrientation_TopDown)
        self.assertEqual(testee.Array[0,0], 143)
        self.assertEqual(testee.GetBuffer()[0], 143)
        self.assertEqual(testee.GetMemoryView()[0], 143)
        testee.Release()

    def test_container_load_zero_copy(self):
        testee = pylon.PylonImage()
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'barcode01.png')
        testee.Load(filename)
        with testee.GetArrayZeroCopy() as zc:
            self.assertEqual(zc[0,0], 143)
        testee.Release()

    def test_attacharray(self):
        """AttachArray attaches an existing numpy array as the image buffer without copying."""
        import numpy as np
        import sys

        img = pylon.PylonImage()
        arr = np.random.randint(0, 256, (480, 640), dtype=np.uint8)

        arr_refcount_0 = sys.getrefcount(arr)
        img.AttachArray(arr, pylon.PixelType_Mono8)
        # check proper refcounting attach
        self.assertEqual( sys.getrefcount(arr) , arr_refcount_0 + 1)

        # check that img and array have same content
        self.assertEqual(np.all(arr == img.Array), True)

        del img
        # check proper refcounting free
        self.assertEqual( sys.getrefcount(arr), arr_refcount_0)

    # ------------------------------------------------------------------
    # Packed pixel format (Mono12p sawtooth) — ImageFormatConverter._Unpack
    # path exercised through GetArray / GetArrayZeroCopy
    # ------------------------------------------------------------------

    #: Dimensions for the synthetic Mono12p test image.
    #: Width must be even so each row packs into whole 3-byte groups.
    _PACKED_WIDTH  = 4
    _PACKED_HEIGHT = 2
    #: Value step for the sawtooth pattern (all values fit in 12 bits).
    _PACKED_STEP   = 256

    @staticmethod
    def _pack_mono12p(pixel_values):
        """Pack a flat sequence of 12-bit integer values into a Mono12p byte buffer.

        Mono12p layout for each pair (p0, p1):
          byte 0 : p0[7:0]
          byte 1 : p0[11:8]  (lower nibble)  |  p1[3:0]  (upper nibble)
          byte 2 : p1[11:4]
        """
        packed = bytearray()
        for i in range(0, len(pixel_values), 2):
            p0 = int(pixel_values[i])     & 0xFFF
            p1 = int(pixel_values[i + 1]) & 0xFFF
            packed.append(p0 & 0xFF)
            packed.append(((p0 >> 8) & 0x0F) | ((p1 & 0x0F) << 4))
            packed.append((p1 >> 4) & 0xFF)
        return bytes(packed)

    def _make_mono12p_sawtooth_image(self):
        """Return (PylonImage, pixel_values_flat) for a synthetic Mono12p sawtooth test image.

        The pixel values are a sawtooth that increments by _PACKED_STEP for each
        pixel and wraps at 4096 (12-bit range).  Every value is distinct for the
        chosen image size, making per-pixel verification straightforward.
        """
        num_pixels = self._PACKED_WIDTH * self._PACKED_HEIGHT
        pixel_values = [(i * self._PACKED_STEP) % 4096 for i in range(num_pixels)]
        packed = self._pack_mono12p(pixel_values)
        image = pylon.PylonImage()
        image.AttachMemoryView(
            memoryview(packed),
            pylon.PixelType_Mono12p,
            self._PACKED_WIDTH,
            self._PACKED_HEIGHT,
            0,
        )
        return image, pixel_values

    def test_packed_get_image_format_raises_value_error(self):
        """GetImageFormat raises ValueError for a packed pixel type (Mono12p)."""
        image, _ = self._make_mono12p_sawtooth_image()
        with self.assertRaises(ValueError):
            image.GetImageFormat()

    def test_packed_get_array_returns_uint16_shaped_height_by_width(self):
        """GetArray on a packed Mono12p image returns a uint16 ndarray shaped (height, width)."""
        import numpy as np
        image, _ = self._make_mono12p_sawtooth_image()
        result = image.GetArray()
        self.assertEqual(result.dtype, np.uint16)
        self.assertEqual(result.shape, (self._PACKED_HEIGHT, self._PACKED_WIDTH))

    def test_packed_get_array_decodes_sawtooth_pixel_values_correctly(self):
        """GetArray on a Mono12p image decodes every pixel to its expected 12-bit value (LsbAligned)."""
        import numpy as np
        image, pixel_values = self._make_mono12p_sawtooth_image()
        result = image.GetArray()
        expected = np.array(pixel_values, dtype=np.uint16).reshape(
            self._PACKED_HEIGHT, self._PACKED_WIDTH
        )
        np.testing.assert_array_equal(result, expected)

    def test_packed_get_array_raw_returns_uint8_packed_buffer(self):
        """GetArray(raw=True) on a Mono12p image returns the raw packed bytes as a uint8 array."""
        import numpy as np
        image, pixel_values = self._make_mono12p_sawtooth_image()
        raw = image.GetArray(raw=True)
        self.assertEqual(raw.dtype, np.uint8)
        # Mono12p: 3 bytes per pair of pixels
        expected_size = self._PACKED_WIDTH * self._PACKED_HEIGHT * 3 // 2
        self.assertEqual(len(raw), expected_size)
        expected_bytes = np.frombuffer(self._pack_mono12p(pixel_values), dtype=np.uint8)
        np.testing.assert_array_equal(raw, expected_bytes)

    def test_packed_get_array_zero_copy_decodes_sawtooth_pixel_values_correctly(self):
        """GetArrayZeroCopy on a Mono12p image unpacks via CPylonImage fallback and returns correct uint16 values."""
        import numpy as np
        image, pixel_values = self._make_mono12p_sawtooth_image()
        expected = np.array(pixel_values, dtype=np.uint16).reshape(
            self._PACKED_HEIGHT, self._PACKED_WIDTH
        )
        with image.GetArrayZeroCopy() as result:
            self.assertEqual(result.dtype, np.uint16)
            self.assertEqual(result.shape, (self._PACKED_HEIGHT, self._PACKED_WIDTH))
            np.testing.assert_array_equal(result, expected)



if __name__ == "__main__":
    unittest.main()
