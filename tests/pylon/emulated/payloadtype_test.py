"""\
This unit test checks the public payload type constants from
src/pylon/PayloadType.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class PayloadTypeTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # %ignore directives from PayloadType.i
    #     %ignore PayloadType;
    # ------------------------------------------------------------------

    def test_ignored_names_are_not_exposed(self):
        """The %ignore-d PayloadType type alias must not appear on pylon."""
        self.assertFalse(hasattr(pylon, "PayloadType"))

    # ------------------------------------------------------------------
    # EPayloadType enum values
    # ------------------------------------------------------------------

    def test_payload_type_basic_constants(self):
        """Basic payload kinds keep their documented enum values."""
        self.assertEqual(pylon.PayloadType_Undefined, -1)
        self.assertEqual(pylon.PayloadType_Image, 0)
        self.assertEqual(pylon.PayloadType_RawData, 1)
        self.assertEqual(pylon.PayloadType_File, 2)
        self.assertIsInstance(pylon.PayloadType_Image, int)

    def test_payload_type_chunk_and_gendc_constants(self):
        """Structured payload kinds continue the public enum values in order."""
        self.assertEqual(pylon.PayloadType_ChunkData, 3)
        self.assertEqual(pylon.PayloadType_GenDC, 4)

    def test_payload_type_high_bit_device_specific_constant(self):
        """Device-specific payloads use the documented high-bit marker value."""
        self.assertEqual(pylon.PayloadType_DeviceSpecific, 0x8000)
        self.assertGreater(
            pylon.PayloadType_DeviceSpecific,
            pylon.PayloadType_GenDC,
        )


if __name__ == "__main__":
    unittest.main()
