"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/WaitObjects.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import threading
import unittest


SIGNAL_WAIT_TIMEOUT_MS = 5000
NEGATIVE_WAIT_TIMEOUT_MS = 250
THREAD_WAIT_TIMEOUT_MS = 10000
THREAD_JOIN_TIMEOUT_S = 15
THREAD_CLEANUP_JOIN_TIMEOUT_S = 2


class WaitObjectsTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_default_construction(self):
        """Default-constructed WaitObjects container is empty."""
        container = pylon.WaitObjects()
        self.assertIsNotNone(container)

    # ------------------------------------------------------------------
    # Add / RemoveAll
    # ------------------------------------------------------------------

    def test_add_wait_object(self):
        """A WaitObject can be added to a WaitObjects container."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            wait_object = camera.GetGrabResultWaitObject()
            container = pylon.WaitObjects()
            container.Add(wait_object)
            # After adding a signaled wait object, WaitForAny should succeed
            self.assertTrue(container.WaitForAny(SIGNAL_WAIT_TIMEOUT_MS))

    def test_remove_all(self):
        """RemoveAll clears the container without error."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(wait_object)
            # RemoveAll should not raise
            container.RemoveAll()

    # ------------------------------------------------------------------
    # WaitForAll
    # ------------------------------------------------------------------

    def test_wait_for_all_timeout(self):
        """WaitForAll returns False when not all objects are signaled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_result_wait_object)
            container.Add(grab_stop_wait_object)
            # grab_stop is not signaled while grabbing, so WaitForAll should fail
            self.assertFalse(container.WaitForAll(NEGATIVE_WAIT_TIMEOUT_MS))

    def test_wait_for_all_signaled(self):
        """WaitForAll returns True when all objects are signaled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            camera.StopGrabbing()
            container = pylon.WaitObjects()
            container.Add(grab_stop_wait_object)
            # The grab stop wait object should be signaled after stopping
            self.assertTrue(container.WaitForAll(SIGNAL_WAIT_TIMEOUT_MS))

    # ------------------------------------------------------------------
    # WaitForAllEx
    # ------------------------------------------------------------------

    def test_wait_for_all_ex_timeout(self):
        """WaitForAllEx returns waitex_timeout when not all objects are signaled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_result_wait_object)
            container.Add(grab_stop_wait_object)
            self.assertEqual(
                pylon.waitex_timeout,
                container.WaitForAllEx(NEGATIVE_WAIT_TIMEOUT_MS, False),
            )

    def test_wait_for_all_ex_signaled(self):
        """WaitForAllEx returns waitex_signaled when all objects are signaled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            camera.StopGrabbing()
            container = pylon.WaitObjects()
            container.Add(grab_stop_wait_object)
            self.assertEqual(
                pylon.waitex_signaled,
                container.WaitForAllEx(SIGNAL_WAIT_TIMEOUT_MS, False),
            )

    def test_wait_for_all_ex_alertable(self):
        """WaitForAllEx with alertable=True returns timeout or alerted."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_stop_wait_object)
            result = container.WaitForAllEx(NEGATIVE_WAIT_TIMEOUT_MS, True)
            self.assertIn(result, (pylon.waitex_timeout, pylon.waitex_alerted))

    # ------------------------------------------------------------------
    # WaitForAny
    # ------------------------------------------------------------------

    def test_wait_for_any_timeout(self):
        """WaitForAny returns False when no object is signaled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_stop_wait_object)
            self.assertFalse(container.WaitForAny(NEGATIVE_WAIT_TIMEOUT_MS))

    def test_wait_for_any_signaled(self):
        """WaitForAny returns True when at least one object is signaled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_result_wait_object)
            container.Add(grab_stop_wait_object)
            # grab result wait object should be signaled when images are available
            self.assertTrue(container.WaitForAny(SIGNAL_WAIT_TIMEOUT_MS))

    # ------------------------------------------------------------------
    # WaitForAnyEx
    # ------------------------------------------------------------------

    def test_wait_for_any_ex_timeout(self):
        """WaitForAnyEx returns waitex_timeout when no object is signaled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_stop_wait_object)
            result = container.WaitForAnyEx(NEGATIVE_WAIT_TIMEOUT_MS, False)
            self.assertEqual(pylon.waitex_timeout, result)

    def test_wait_for_any_ex_signaled(self):
        """WaitForAnyEx returns waitex_signaled when an object is signaled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_result_wait_object)
            result = container.WaitForAnyEx(SIGNAL_WAIT_TIMEOUT_MS, False)
            self.assertEqual(pylon.waitex_signaled, result)

    def test_wait_for_any_ex_alertable(self):
        """WaitForAnyEx with alertable=True returns timeout or alerted."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_stop_wait_object)
            result = container.WaitForAnyEx(NEGATIVE_WAIT_TIMEOUT_MS, True)
            self.assertIn(result, (pylon.waitex_timeout, pylon.waitex_alerted))

    # ------------------------------------------------------------------
    # WaitForAny / WaitForAnyEx with pIndex parameter
    # ------------------------------------------------------------------

    def test_wait_for_any_with_none_index(self):
        """WaitForAny with pIndex=None returns plain bool."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_result_wait_object)
            result = container.WaitForAny(SIGNAL_WAIT_TIMEOUT_MS, None)
            # pIndex=None passes NULL - result is a plain bool
            self.assertIsInstance(result, bool)
            self.assertTrue(result)

    def test_wait_for_any_ex_with_none_index(self):
        """WaitForAnyEx with pIndex=None returns plain EWaitExResult."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_result_wait_object)
            result = container.WaitForAnyEx(SIGNAL_WAIT_TIMEOUT_MS, False, None)
            self.assertEqual(pylon.waitex_signaled, result)

    def test_wait_for_any_with_index(self):
        """WaitForAny with pIndex=True returns (bool, index) tuple."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_stop_wait_object)
            container.Add(grab_result_wait_object)
            result = container.WaitForAny(SIGNAL_WAIT_TIMEOUT_MS, True)
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            signaled, index = result
            self.assertTrue(signaled)
            self.assertEqual(1, index)

    def test_wait_for_any_ex_with_index(self):
        """WaitForAnyEx with pIndex=True returns (EWaitExResult, index) tuple."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_stop_wait_object)
            container.Add(grab_result_wait_object)
            result = container.WaitForAnyEx(SIGNAL_WAIT_TIMEOUT_MS, False, True)
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            wait_ex_result, index = result
            self.assertEqual(pylon.waitex_signaled, wait_ex_result)
            self.assertEqual(1, index)

    def test_wait_for_any_without_index_returns_plain_bool(self):
        """WaitForAny without pIndex argument returns a plain bool (backward compatibility)."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_result_wait_object)
            result = container.WaitForAny(SIGNAL_WAIT_TIMEOUT_MS)
            self.assertIsInstance(result, bool)
            self.assertTrue(result)

    def test_wait_for_any_ex_without_index_returns_plain_result(self):
        """WaitForAnyEx without pIndex argument returns a plain EWaitExResult (backward compatibility)."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_result_wait_object)
            result = container.WaitForAnyEx(SIGNAL_WAIT_TIMEOUT_MS, False)
            self.assertNotIsInstance(result, tuple)
            self.assertEqual(pylon.waitex_signaled, result)

    def test_wait_for_any_rejects_invalid_index_type(self):
        """WaitForAny raises TypeError when pIndex is not None or True."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_result_wait_object)
            with self.assertRaises(TypeError):
                container.WaitForAny(SIGNAL_WAIT_TIMEOUT_MS, 0)

    def test_wait_for_any_ex_rejects_invalid_index_type(self):
        """WaitForAnyEx raises TypeError when pIndex is not None or True."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_result_wait_object)
            with self.assertRaises(TypeError):
                container.WaitForAnyEx(SIGNAL_WAIT_TIMEOUT_MS, False, 0)

    # ------------------------------------------------------------------
    # Multiple objects in container
    # ------------------------------------------------------------------

    def test_multiple_wait_objects_wait_for_any(self):
        """WaitForAny succeeds when one of multiple objects is signaled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_result_wait_object = camera.GetGrabResultWaitObject()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_stop_wait_object)
            container.Add(grab_result_wait_object)
            # grab_result_wait_object should be signaled (images available), grab_stop_wait_object not
            self.assertTrue(container.WaitForAny(SIGNAL_WAIT_TIMEOUT_MS))

    def test_wait_for_all_after_stop(self):
        """WaitForAll succeeds after grab is stopped."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            camera.StopGrabbing()
            container = pylon.WaitObjects()
            container.Add(grab_stop_wait_object)
            self.assertTrue(container.WaitForAll(SIGNAL_WAIT_TIMEOUT_MS))

    # ------------------------------------------------------------------
    # Threaded waiting (mirrors C++ TestPylonWaitMany / TestPylonWaitAny)
    # ------------------------------------------------------------------

    def test_wait_for_all_from_thread(self):
        """WaitForAll can be used from a background thread."""
        thread = None
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_stop_wait_object)

            result_holder = [None]

            def wait_thread():
                result_holder[0] = container.WaitForAll(THREAD_WAIT_TIMEOUT_MS)

            thread = threading.Thread(target=wait_thread)
            self.addCleanup(
                lambda: thread.join(timeout=THREAD_CLEANUP_JOIN_TIMEOUT_S)
                if thread.is_alive() else None
            )
            thread.start()
            # Signal by stopping the grab
            camera.StopGrabbing()
            thread.join(timeout=THREAD_JOIN_TIMEOUT_S)
            if thread.is_alive():
                thread.join(timeout=THREAD_CLEANUP_JOIN_TIMEOUT_S)
            self.assertFalse(thread.is_alive())
            self.assertTrue(result_holder[0])

    def test_wait_for_any_from_thread(self):
        """WaitForAny can be used from a background thread."""
        thread = None
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing()
            grab_stop_wait_object = camera.GetGrabStopWaitObject()
            container = pylon.WaitObjects()
            container.Add(grab_stop_wait_object)

            result_holder = [None]

            def wait_thread():
                result_holder[0] = container.WaitForAny(THREAD_WAIT_TIMEOUT_MS)

            thread = threading.Thread(target=wait_thread)
            self.addCleanup(
                lambda: thread.join(timeout=THREAD_CLEANUP_JOIN_TIMEOUT_S)
                if thread.is_alive() else None
            )
            thread.start()
            # Signal by stopping the grab
            camera.StopGrabbing()
            thread.join(timeout=THREAD_JOIN_TIMEOUT_S)
            if thread.is_alive():
                thread.join(timeout=THREAD_CLEANUP_JOIN_TIMEOUT_S)
            self.assertFalse(thread.is_alive())
            self.assertTrue(result_holder[0])


if __name__ == "__main__":
    unittest.main()

