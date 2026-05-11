"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/WaitObject.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import time
import unittest


SIGNAL_WAIT_TIMEOUT_MS = 5000
NEGATIVE_WAIT_TIMEOUT_MS = 250
WAIT_EX_NEGATIVE_TIMEOUT_MS = 50
WAIT_ZERO_MAX_ELAPSED_MS = 500
SLEEP_DURATION_MS = 200
SLEEP_MIN_RATIO = 0.8
SLEEP_MAX_OVERHEAD_MS = 500


class WaitObjectTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # WaitObject construction
    # ------------------------------------------------------------------

    def test_default_construction(self):
        """Default-constructed WaitObject is not valid."""
        wait_object = pylon.WaitObject()
        self.assertFalse(wait_object.IsValid())

    # ------------------------------------------------------------------
    # WaitObject from camera (grab result wait object)
    # ------------------------------------------------------------------

    def test_grab_result_wait_object_is_valid(self):
        """GrabResultWaitObject obtained from a grabbing camera is valid."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            wait_object = camera.GetGrabResultWaitObject()
            self.assertTrue(wait_object.IsValid())

    def test_grab_result_wait_object_signals_on_image(self):
        """GrabResultWaitObject becomes signaled when a grab result is ready."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            wait_object = camera.GetGrabResultWaitObject()
            self.assertTrue(wait_object.Wait(SIGNAL_WAIT_TIMEOUT_MS))

    def test_grab_stop_wait_object_is_valid(self):
        """GrabStopWaitObject obtained from a camera is valid."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            wait_object = camera.GetGrabStopWaitObject()
            self.assertTrue(wait_object.IsValid())

    def test_grab_stop_wait_object_not_signaled_while_grabbing(self):
        """GrabStopWaitObject is not signaled while the camera is grabbing."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            wait_object = camera.GetGrabStopWaitObject()
            self.assertFalse(wait_object.Wait(NEGATIVE_WAIT_TIMEOUT_MS))

    def test_grab_stop_wait_object_signals_after_stop(self):
        """GrabStopWaitObject becomes signaled after grabbing is stopped."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            wait_object = camera.GetGrabStopWaitObject()
            camera.StopGrabbing()
            self.assertTrue(wait_object.Wait(SIGNAL_WAIT_TIMEOUT_MS))

    # ------------------------------------------------------------------
    # WaitObject.Wait timeout behaviour
    # ------------------------------------------------------------------

    def test_wait_timeout_returns_false(self):
        """Wait returns False when the timeout elapses without signal."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            wait_object = camera.GetGrabStopWaitObject()
            self.assertFalse(wait_object.Wait(NEGATIVE_WAIT_TIMEOUT_MS))

    def test_wait_zero_timeout(self):
        """Wait with zero timeout returns immediately."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            wait_object = camera.GetGrabStopWaitObject()
            start = time.monotonic()
            wait_object.Wait(0)
            elapsed_ms = (time.monotonic() - start) * 1000
            self.assertLess(elapsed_ms, WAIT_ZERO_MAX_ELAPSED_MS)

    # ------------------------------------------------------------------
    # WaitObject.WaitEx
    # ------------------------------------------------------------------

    def test_wait_ex_timeout(self):
        """WaitEx returns waitex_timeout when the timeout elapses."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            wait_object = camera.GetGrabStopWaitObject()
            result = wait_object.WaitEx(WAIT_EX_NEGATIVE_TIMEOUT_MS, False)
            self.assertEqual(result, pylon.waitex_timeout)

    def test_wait_ex_signaled(self):
        """WaitEx returns waitex_signaled when the object is signaled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            wait_object = camera.GetGrabStopWaitObject()
            camera.StopGrabbing()
            result = wait_object.WaitEx(SIGNAL_WAIT_TIMEOUT_MS, False)
            self.assertEqual(result, pylon.waitex_signaled)

    def test_wait_ex_alertable_timeout(self):
        """WaitEx with alertable=True returns timeout or alerted."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            wait_object = camera.GetGrabStopWaitObject()
            result = wait_object.WaitEx(WAIT_EX_NEGATIVE_TIMEOUT_MS, True)
            self.assertIn(result, (pylon.waitex_timeout, pylon.waitex_alerted))

    # ------------------------------------------------------------------
    # WaitObject.Sleep (static)
    # ------------------------------------------------------------------

    def test_sleep(self):
        """Sleep suspends the calling thread for approximately the given time."""
        start = time.monotonic()
        pylon.WaitObject.Sleep(SLEEP_DURATION_MS)
        elapsed_ms = (time.monotonic() - start) * 1000
        self.assertGreaterEqual(elapsed_ms, SLEEP_DURATION_MS * SLEEP_MIN_RATIO)
        self.assertLess(elapsed_ms, SLEEP_DURATION_MS + SLEEP_MAX_OVERHEAD_MS)

    # ------------------------------------------------------------------
    # WaitEx result constants
    # ------------------------------------------------------------------

    def test_waitex_constants_exist(self):
        """The waitex result constants are available in the pylon module."""
        self.assertIsNotNone(pylon.waitex_timeout)
        self.assertIsNotNone(pylon.waitex_signaled)
        self.assertIsNotNone(pylon.waitex_abandoned)
        self.assertIsNotNone(pylon.waitex_alerted)

    def test_waitex_constants_are_distinct(self):
        """All waitex result constants have distinct values."""
        constants = [
            pylon.waitex_timeout,
            pylon.waitex_signaled,
            pylon.waitex_abandoned,
            pylon.waitex_alerted,
        ]
        self.assertEqual(len(constants), len(set(constants)))

    # ------------------------------------------------------------------
    # waitForever constant
    # ------------------------------------------------------------------

    def test_wait_forever_constant(self):
        """The waitForever constant is available in the pylon module."""
        self.assertIsNotNone(pylon.waitForever)


if __name__ == "__main__":
    unittest.main()