"""\
This unit test checks chunk image grabbing for USB cameras,
covering the grab-with-chunks workflow from the grab_chunk_image sample.
"""
from pylonusbtestcase import PylonTestCase
from pypylon import pylon
import unittest


COUNT_OF_IMAGES_TO_GRAB = 5
RETRIEVE_TIMEOUT_MS = 5000


class ChunkImageTestSuite(PylonTestCase):

    # ------------------------------------------------------------------
    # Chunk image grabbing
    # ------------------------------------------------------------------

    def test_grab_chunk_image(self):
        """Grab images with chunk data and verify payload type, CRC, and timestamp."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:

            if not camera.ChunkModeActive.TrySetValue(True):
                self.skipTest("Camera does not support chunk mode.")

            # Enable timestamp chunks.
            camera.ChunkSelector.Value = "Timestamp"
            camera.ChunkEnable.Value = True

            # Enable CRC checksum chunks.
            camera.ChunkSelector.Value = "PayloadCRC16"
            camera.ChunkEnable.Value = True

            camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

            while camera.IsGrabbing():
                with camera.RetrieveResult(
                    RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
                ) as grab_result:
                    self.assertEqual(
                        pylon.PayloadType_ChunkData,
                        grab_result.PayloadType,
                        "Expected chunk data payload type.",
                    )

                    self.assertTrue(grab_result.HasCRC(), "No CRC available.")
                    self.assertTrue(grab_result.CheckCRC(), "CRC check failed.")

                    self.assertTrue(
                        grab_result.ChunkTimestamp.IsReadable(),
                        "ChunkTimestamp chunk is not readable.",
                    )

            camera.ChunkModeActive.Value = False


if __name__ == "__main__":
    unittest.main()
