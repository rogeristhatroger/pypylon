"""\
This unit test checks the Region type bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class RegionTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Construction / copy semantics
    # ------------------------------------------------------------------

    def test_init(self):
        """Region exposes its geometry both as methods and as properties."""
        empty_region = pylondataprocessing.Region()
        self.assertFalse(empty_region.IsValid())
        self.assertFalse(empty_region.HasBoundingBox())
        self.assertFalse(empty_region.HasReferenceSize())
        self.assertFalse(empty_region.IsUnique())
        self.assertFalse(empty_region.IsReadOnly())
        self.assertFalse(empty_region.IsUserBufferAttached())
        self.assertEqual(empty_region.GetBoundingBoxTopLeftX(), 0)
        self.assertEqual(empty_region.GetBoundingBoxTopLeftY(), 0)
        self.assertEqual(empty_region.GetBoundingBoxWidth(), 0)
        self.assertEqual(empty_region.GetBoundingBoxHeight(), 0)
        self.assertEqual(empty_region.GetReferenceWidth(), 0)
        self.assertEqual(empty_region.GetReferenceHeight(), 0)
        self.assertEqual(empty_region.GetAllocatedBufferSize(), 0)
        self.assertEqual(empty_region.GetDataSize(), 0)
        self.assertEqual(empty_region.GetRegionType(), pylondataprocessing.RegionType_Undefined)
        empty_region.Release()

        # CRegion(ERegionType regionType,
        #         size_t dataSize,
        #         uint32_t referenceWidth = 0,
        #         uint32_t referenceHeight = 0,
        #         int32_t boundingBoxTopLeftX = 0,
        #         int32_t boundingBoxTopLeftY = 0,
        #         uint32_t boundingBoxWidth = 0,
        #         uint32_t boundingBoxHeight = 0);
        region = pylondataprocessing.Region(pylondataprocessing.RegionType_RLE32, 12, 100, 200, 10, 11, 12, 13)
        self.assertTrue(region.IsValid())
        self.assertTrue(region.HasBoundingBox())
        self.assertTrue(region.HasReferenceSize())
        self.assertTrue(region.IsUnique())
        self.assertFalse(region.IsReadOnly())
        self.assertFalse(region.IsUserBufferAttached())
        self.assertEqual(region.GetReferenceWidth(), 100)
        self.assertEqual(region.GetReferenceHeight(), 200)
        self.assertEqual(region.GetBoundingBoxTopLeftX(), 10)
        self.assertEqual(region.GetBoundingBoxTopLeftY(), 11)
        self.assertEqual(region.GetBoundingBoxWidth(), 12)
        self.assertEqual(region.GetBoundingBoxHeight(), 13)
        self.assertEqual(region.GetAllocatedBufferSize(), 12)
        self.assertEqual(region.GetDataSize(), 12)
        self.assertEqual(region.GetRegionType(), pylondataprocessing.RegionType_RLE32)
        self.assertEqual(region.ReferenceWidth, 100)
        self.assertEqual(region.ReferenceHeight, 200)
        self.assertEqual(region.BoundingBoxTopLeftX, 10)
        self.assertEqual(region.BoundingBoxTopLeftY, 11)
        self.assertEqual(region.BoundingBoxWidth, 12)
        self.assertEqual(region.BoundingBoxHeight, 13)
        self.assertEqual(region.AllocatedBufferSize, 12)
        self.assertEqual(region.DataSize, 12)
        self.assertEqual(region.RegionType, pylondataprocessing.RegionType_RLE32)
        shared_region = pylondataprocessing.Region(region)
        self.assertFalse(region.IsUnique())
        self.assertFalse(shared_region.IsUnique())
        region.Release()
        self.assertFalse(region.IsValid())
        self.assertFalse(region.IsUnique())
        self.assertTrue(shared_region.IsUnique())
        copied_region = pylondataprocessing.Region()
        copied_region.CopyRegion(shared_region)  # deep copy
        self.assertTrue(copied_region.IsValid())
        self.assertTrue(shared_region.IsUnique())
        self.assertTrue(copied_region.IsUnique())

    # ------------------------------------------------------------------
    # RLE32 buffer access
    # ------------------------------------------------------------------

    def test_rle32(self):
        """Region buffers can be accessed by memory view, ToArray and GetBuffer."""
        region = pylondataprocessing.Region(pylondataprocessing.RegionType_RLE32, 24, 100, 200, 10, 11, 12, 13)
        data = region.GetMemoryView()  # no copy, direct access
        data_as_int32 = data.cast('i')  # switch view to 4 byte integer
        data_as_int32[0] = 101
        data_as_int32[1] = 134
        data_as_int32[2] = 210

        data_as_int32[3] = 102
        data_as_int32[4] = 103
        data_as_int32[5] = 211
        data = None
        data_as_int32 = None

        entries = region.ToArray()
        self.assertEqual(entries[0].StartX, 101)
        self.assertEqual(entries[0].EndX, 134)
        self.assertEqual(entries[0].Y, 210)

        self.assertEqual(entries[1].StartX, 102)
        self.assertEqual(entries[1].EndX, 103)
        self.assertEqual(entries[1].Y, 211)
        region.Resize(36)
        self.assertEqual(region.GetDataSize(), 36)
        data = region.GetMemoryView()
        data_as_int32 = data.cast('i')
        data_as_int32[6] = 104
        data_as_int32[7] = 105
        data_as_int32[8] = 212
        entries = region.ToArray()  # copies
        self.assertEqual(entries[0].StartX, 101)
        self.assertEqual(entries[0].EndX, 134)
        self.assertEqual(entries[0].Y, 210)

        self.assertEqual(entries[1].StartX, 102)
        self.assertEqual(entries[1].EndX, 103)
        self.assertEqual(entries[1].Y, 211)

        self.assertEqual(entries[2].StartX, 104)
        self.assertEqual(entries[2].EndX, 105)
        self.assertEqual(entries[2].Y, 212)

        buffer = region.GetBuffer()  # copies
        buffer_as_int32 = memoryview(buffer).cast('i')

        self.assertEqual(buffer_as_int32[0], 101)
        self.assertEqual(buffer_as_int32[1], 134)
        self.assertEqual(buffer_as_int32[2], 210)
        self.assertEqual(buffer_as_int32[3], 102)
        self.assertEqual(buffer_as_int32[4], 103)
        self.assertEqual(buffer_as_int32[5], 211)
        self.assertEqual(buffer_as_int32[6], 104)
        self.assertEqual(buffer_as_int32[7], 105)
        self.assertEqual(buffer_as_int32[8], 212)

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def test_reset(self):
        """Reset reconfigures the region geometry and buffer size."""
        region = pylondataprocessing.Region(pylondataprocessing.RegionType_RLE32, 24, 100, 200, 10, 11, 12, 13)
        region.Reset(pylondataprocessing.RegionType_RLE32, 36, 101, 201, 20, 31, 42, 53)
        self.assertEqual(region.GetReferenceWidth(), 101)
        self.assertEqual(region.GetReferenceHeight(), 201)
        self.assertEqual(region.GetBoundingBoxTopLeftX(), 20)
        self.assertEqual(region.GetBoundingBoxTopLeftY(), 31)
        self.assertEqual(region.GetBoundingBoxWidth(), 42)
        self.assertEqual(region.GetBoundingBoxHeight(), 53)
        self.assertEqual(region.GetAllocatedBufferSize(), 36)
        self.assertEqual(region.GetDataSize(), 36)


if __name__ == "__main__":
    unittest.main()
