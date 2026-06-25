
"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/InstantCameraArray.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


def _attach_emulated_devices(camera_array, device_filter):
    """Attach one emulated device to every slot in *camera_array*."""
    tl_factory = pylon.TlFactory.GetInstance()
    devices = tl_factory.EnumerateDevices(device_filter)
    for index, camera in enumerate(camera_array):
        camera.Attach(tl_factory.CreateDevice(devices[index]))


class InstantCameraArrayTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_default_construction_produces_size_zero_array(self):
        """Default constructor creates an array with size 0."""
        camera_array = pylon.InstantCameraArray()
        self.assertEqual(camera_array.GetSize(), 0)

    def test_sized_construction_produces_correct_size(self):
        """Constructor with numberOfCameras creates an array of that size."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        self.assertEqual(camera_array.GetSize(), self.num_devices)

    def test_default_construction_state_flags_all_false(self):
        """Default-constructed array reports all state flags as False."""
        camera_array = pylon.InstantCameraArray()
        self.assertFalse(camera_array.IsOpen())
        self.assertFalse(camera_array.IsGrabbing())
        self.assertFalse(camera_array.IsPylonDeviceAttached())
        self.assertFalse(camera_array.IsCameraDeviceRemoved())

    # ------------------------------------------------------------------
    # Initialize / GetSize
    # ------------------------------------------------------------------

    def test_initialize_changes_array_size(self):
        """Initialize() replaces the array with the requested number of cameras."""
        camera_array = pylon.InstantCameraArray()
        camera_array.Initialize(self.num_devices)
        self.assertEqual(camera_array.GetSize(), self.num_devices)

    def test_initialize_to_zero_empties_array(self):
        """Initialize(0) shrinks the array back to size 0."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        camera_array.Initialize(0)
        self.assertEqual(camera_array.GetSize(), 0)

    def test_reinitialize_replaces_cameras_and_sets_context(self):
        """Re-initializing an array that already had cameras resets camera contexts."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        camera_array.Initialize(self.num_devices)
        for index, camera in enumerate(camera_array):
            self.assertEqual(camera.GetCameraContext(), index)

    # ------------------------------------------------------------------
    # Index access / __getitem__ / __iter__
    # ------------------------------------------------------------------

    def test_getitem_returns_camera_at_index(self):
        """camera_array[i] returns the InstantCamera at position i."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        for index in range(self.num_devices):
            camera = camera_array[index]
            self.assertEqual(camera.GetCameraContext(), index)

    def test_getitem_out_of_range_raises_index_error(self):
        """camera_array[size] raises IndexError."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        with self.assertRaises(IndexError):
            _ = camera_array[self.num_devices]

    def test_iter_visits_every_camera_once(self):
        """Iterating over the array yields exactly GetSize() cameras."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        contexts = [camera.GetCameraContext() for camera in camera_array]
        self.assertEqual(contexts, list(range(self.num_devices)))

    def test_iter_over_empty_array_yields_nothing(self):
        """Iterating over a size-0 array yields no items."""
        camera_array = pylon.InstantCameraArray()
        self.assertEqual(list(camera_array), [])

    # ------------------------------------------------------------------
    # IsPylonDeviceAttached
    # ------------------------------------------------------------------

    def test_is_pylon_device_attached_false_before_attach(self):
        """IsPylonDeviceAttached() returns False when no device is attached."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        self.assertFalse(camera_array.IsPylonDeviceAttached())

    def test_is_pylon_device_attached_true_after_attach(self):
        """IsPylonDeviceAttached() returns True when all slots have a device."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)
        self.assertTrue(camera_array.IsPylonDeviceAttached())
        camera_array.DestroyDevice()

    def test_is_pylon_device_attached_false_for_size_zero_array(self):
        """IsPylonDeviceAttached() returns False for a size-0 array."""
        camera_array = pylon.InstantCameraArray()
        self.assertFalse(camera_array.IsPylonDeviceAttached())

    # ------------------------------------------------------------------
    # Open / IsOpen / Close
    # ------------------------------------------------------------------

    def test_open_and_close(self):
        """Open() makes IsOpen() True; Close() makes IsOpen() False."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)

        self.assertFalse(camera_array.IsOpen())
        camera_array.Open()
        self.assertTrue(camera_array.IsOpen())
        camera_array.Close()
        self.assertFalse(camera_array.IsOpen())
        camera_array.DestroyDevice()

    def test_is_open_false_for_size_zero_array(self):
        """IsOpen() returns False for a size-0 array."""
        camera_array = pylon.InstantCameraArray()
        self.assertFalse(camera_array.IsOpen())

    # ------------------------------------------------------------------
    # DestroyDevice
    # ------------------------------------------------------------------

    def test_destroy_device_detaches_all_devices(self):
        """DestroyDevice() leaves IsPylonDeviceAttached() False while preserving array size."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)
        camera_array.Open()

        camera_array.DestroyDevice()

        self.assertEqual(camera_array.GetSize(), self.num_devices)
        self.assertFalse(camera_array.IsPylonDeviceAttached())
        self.assertFalse(camera_array.IsOpen())

    def test_destroy_device_stops_grabbing(self):
        """DestroyDevice() stops an ongoing grab."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)
        camera_array.StartGrabbing()
        self.assertTrue(camera_array.IsGrabbing())

        camera_array.DestroyDevice()

        self.assertFalse(camera_array.IsGrabbing())

    # ------------------------------------------------------------------
    # DetachDevice
    # ------------------------------------------------------------------

    def test_detach_device_transfers_ownership_and_clears_attachment(self):
        """DetachDevice() clears attachment state without destroying the device."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)

        camera_array.DetachDevice()

        self.assertEqual(camera_array.GetSize(), self.num_devices)
        self.assertFalse(camera_array.IsPylonDeviceAttached())

    def test_detach_device_stops_grabbing(self):
        """DetachDevice() stops an ongoing grab."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)
        camera_array.StartGrabbing()
        self.assertTrue(camera_array.IsGrabbing())

        camera_array.DetachDevice()

        self.assertFalse(camera_array.IsGrabbing())

    # ------------------------------------------------------------------
    # StartGrabbing / IsGrabbing / StopGrabbing / RetrieveResult
    # ------------------------------------------------------------------

    def test_start_and_stop_grabbing(self):
        """StartGrabbing() sets IsGrabbing() True; StopGrabbing() sets it False."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)

        camera_array.StartGrabbing()
        self.assertTrue(camera_array.IsGrabbing())

        camera_array.StopGrabbing()
        self.assertFalse(camera_array.IsGrabbing())
        camera_array.DestroyDevice()

    def test_retrieve_result_returns_true_and_valid_grab_result(self):
        """RetrieveResult() returns True and a successful grab result while grabbing."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)
        camera_array.StartGrabbing()

        grab_result = camera_array.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        self.assertTrue(grab_result.GrabSucceeded())
        grab_result.Release()
        camera_array.StopGrabbing()
        camera_array.DestroyDevice()

    def test_retrieve_result_returns_false_when_not_grabbing(self):
        """RetrieveResult() returns False immediately when grabbing is not active."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)

        grab_result = camera_array.RetrieveResult(0, pylon.TimeoutHandling_Return)

        self.assertFalse(grab_result.IsValid())
        grab_result.Release()
        camera_array.DestroyDevice()

    def test_retrieve_result_camera_context_identifies_source_camera(self):
        """GetCameraContext() on the grab result identifies which camera produced it."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)
        camera_array.StartGrabbing()

        observed_contexts = set()
        for _ in range(self.num_devices * 3):
            grab_result = camera_array.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grab_result.GrabSucceeded():
                observed_contexts.add(grab_result.GetCameraContext())

        self.assertEqual(observed_contexts, set(range(self.num_devices)))
        camera_array.StopGrabbing()
        camera_array.DestroyDevice()

    def test_retrieve_result_and_check_image(self):
        """GetCameraContext() on the grab result identifies which camera produced it."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)
        camera_array.StartGrabbing()

        observed_contexts = set()
        for _ in range(self.num_devices * 3):
            grab_result = camera_array.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            self.assertTrue(grab_result.IsValid() and grab_result.GrabSucceeded())
            if grab_result.GrabSucceeded():
                img = grab_result.GetArray()
                first_line = img[0]
                previous = int(first_line[0])
                for pixel in first_line[1:]:
                    self.assertEqual(int(pixel), (previous + 1) % 256)
                    previous = int(pixel)
                grab_result.Release()

        camera_array.StopGrabbing()
        camera_array.DestroyDevice()

    def test_start_grabbing_with_latest_image_only_strategy(self):
        """StartGrabbing accepts GrabStrategy_LatestImageOnly."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)

        camera_array.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        self.assertTrue(camera_array.IsGrabbing())
        camera_array.StopGrabbing()
        camera_array.DestroyDevice()

    # ------------------------------------------------------------------
    # Context manager (__enter__ / __exit__)
    # ------------------------------------------------------------------

    def test_context_manager_calls_destroy_device_on_exit(self):
        """The with-statement context manager calls DestroyDevice() on exit."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)
        self.assertTrue(camera_array.IsPylonDeviceAttached())

        with camera_array:
            self.assertTrue(camera_array.IsPylonDeviceAttached())

        self.assertFalse(camera_array.IsPylonDeviceAttached())

    def test_context_manager_calls_destroy_device_on_exception(self):
        """The context manager calls DestroyDevice() even when an exception is raised."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)

        try:
            with camera_array:
                raise RuntimeError("simulated error")
        except RuntimeError:
            pass

        self.assertFalse(camera_array.IsPylonDeviceAttached())

    # ------------------------------------------------------------------
    # IsCameraDeviceRemoved
    # ------------------------------------------------------------------

    def test_is_camera_device_removed_false_on_open_emulated_cameras(self):
        """IsCameraDeviceRemoved() returns False for open emulated cameras."""
        camera_array = pylon.InstantCameraArray(self.num_devices)
        _attach_emulated_devices(camera_array, self.device_filter)
        camera_array.Open()

        self.assertFalse(camera_array.IsCameraDeviceRemoved())

        camera_array.Close()
        camera_array.DestroyDevice()


if __name__ == "__main__":
    unittest.main()
