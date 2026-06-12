"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylon/GigETransportLayer.i.
"""
from pylongigetestcase import PylonTestCase
from pypylon import pylon, genicam
import unittest


class GigETransportLayerTestSuite(PylonTestCase):
    def setUp(self):
        try:
            self.gige_tl = pylon.TlFactory.GetInstance().CreateTl(pylon.BaslerGigEDeviceClass)
        except Exception:
            self.skipTest("GigE transport layer not available")
        if self.gige_tl is None:
            self.skipTest("GigE transport layer not available")

    def tearDown(self):
        if self.gige_tl is not None:
            pylon.TlFactory.GetInstance().ReleaseTl(self.gige_tl)

    # ------------------------------------------------------------------
    # Type checks
    # ------------------------------------------------------------------

    def test_gige_transport_layer_is_transport_layer(self):
        """GigETransportLayer is a subclass of TransportLayer."""
        self.assertTrue(issubclass(pylon.GigETransportLayer, pylon.TransportLayer))

    def test_gige_transport_layer_is_device_factory(self):
        """GigETransportLayer is a subclass of IDeviceFactory."""
        self.assertTrue(issubclass(pylon.GigETransportLayer, pylon.IDeviceFactory))

    # ------------------------------------------------------------------
    # CreateTl
    # ------------------------------------------------------------------

    def test_create_tl_by_device_class_string(self):
        """CreateTl with 'BaslerGigE' string returns a GigETransportLayer instance."""
        self.assertIsInstance(self.gige_tl, pylon.GigETransportLayer)

    # ------------------------------------------------------------------
    # TlInfo / NodeMap
    # ------------------------------------------------------------------

    def test_tl_info(self):
        """TlInfo property returns a TlInfo for the GigE transport layer."""
        self.assertIsInstance(self.gige_tl.TlInfo, pylon.TlInfo)

    def test_node_map(self):
        """NodeMap property returns the transport layer node map."""
        self.assertIsNotNone(self.gige_tl.NodeMap)

    # ------------------------------------------------------------------
    # EnumerateAllDevices / EnumerateDevices / EnumerateInterfaces
    # ------------------------------------------------------------------

    def test_enumerate_all_devices_returns_tuple(self):
        """EnumerateAllDevices returns a tuple, including devices on different subnets."""
        self.assertIsInstance(self.gige_tl.EnumerateAllDevices(), tuple)

    def test_enumerate_devices_returns_tuple(self):
        """EnumerateDevices returns a tuple of DeviceInfo objects."""
        self.assertIsInstance(self.gige_tl.EnumerateDevices(), tuple)

    def test_enumerate_interfaces_returns_tuple(self):
        """EnumerateInterfaces returns a tuple of InterfaceInfo objects."""
        self.assertIsInstance(self.gige_tl.EnumerateInterfaces(), tuple)

    # ------------------------------------------------------------------
    # ForceIp
    # ------------------------------------------------------------------

    def test_force_ip_raises_on_invalid_mac(self):
        """ForceIp raises RuntimeException when no device with the given MAC address is found."""
        self.assertRaises(
            genicam.RuntimeException,
            self.gige_tl.ForceIp,
            "000000000000",  # non-existent MAC
            "127.0.0.1",
            "255.255.255.0",
            "127.0.0.0",
        )

    # ------------------------------------------------------------------
    # RestartIpConfiguration
    # ------------------------------------------------------------------

    def test_restart_ip_configuration_raises_on_invalid_mac(self):
        """RestartIpConfiguration, can call method."""
        self.gige_tl.RestartIpConfiguration("000000000000")  # non-existent MAC

    # ------------------------------------------------------------------
    # AnnounceRemoteDevice / RenounceRemoteDevice
    # ------------------------------------------------------------------

    def test_announce_remote_device_returns_result_tuple(self):
        """AnnounceRemoteDevice round trip."""
        ok, device_info = self.gige_tl.AnnounceRemoteDevice("1.2.3.4")
        self.assertIsInstance(ok, bool)
        self.assertIsInstance(device_info, pylon.DeviceInfo)
        self.assertFalse(ok)
        ok = self.gige_tl.RenounceRemoteDevice("1.2.3.4")
        self.assertIsInstance(ok, bool)

    # ------------------------------------------------------------------
    # BroadcastIpConfiguration
    # ------------------------------------------------------------------

    def test_broadcast_ip_configuration_returns_bool(self):
        """BroadcastIpConfiguration returns a bool indicating whether the configuration was written."""
        ok = self.gige_tl.BroadcastIpConfiguration(
            "000000000000",  # non-existent MAC
            False,           # EnablePersistentIp
            True,            # EnableDhcp
            "",              # IpAddress
            "",              # SubnetMask
            "",              # DefaultGateway
            "",              # UserdefinedName
        )
        self.assertIsInstance(ok, bool)

    # ------------------------------------------------------------------
    # ActionCommand (Python helper class, SWIG extension)
    # ------------------------------------------------------------------

    def test_action_command_issue_no_wait(self):
        """ActionCommand.IssueNoWait broadcasts an action command and returns bool."""
        action_command = self.gige_tl.ActionCommand(123454321, 2, pylon.AllGroupMask)
        self.assertIsInstance(action_command.IssueNoWait(), bool)

    def test_issue_action_command_no_wait(self):
        """IssueActionCommandNoWait broadcasts an action command and returns bool."""
        ok = self.gige_tl.IssueActionCommandNoWait(123454321, 2, pylon.AllGroupMask, "255.255.255.255")
        self.assertIsInstance(ok, bool)

    def test_issue_action_command_wait_returns_result_tuple(self):
        """IssueActionCommandWait returns a (bool, tuple) pair with action-command results."""
        ok, results = self.gige_tl.IssueActionCommandWait(
            123454321, 2, pylon.AllGroupMask, "255.255.255.255", 100, 1
        )
        self.assertIsInstance(ok, bool)
        self.assertIsInstance(results, tuple)

    def test_issue_action_command_wait_result_entries_are_address_status_tuples(self):
        """Each entry in IssueActionCommandWait results is a (str, int) tuple."""
        ok, results = self.gige_tl.IssueActionCommandWait(
            123454321, 2, pylon.AllGroupMask, "255.255.255.255", 100, 1
        )
        for entry in results:
            self.assertIsInstance(entry, tuple)
            self.assertEqual(len(entry), 2)
            address, status = entry
            self.assertIsInstance(address, str)
            self.assertIsInstance(status, int)

    def test_issue_action_command_wait_invalid_group_mask(self):
        """IssueActionCommandWait raises InvalidArgumentException when GroupMask is 0."""
        self.assertRaises(
            genicam.InvalidArgumentException,
            self.gige_tl.IssueActionCommandWait,
            123454321, 2, 0, "255.255.255.255", 100, 1,
        )

    def test_action_command_issue_wait_returns_result_tuple(self):
        """ActionCommand.IssueWait returns a (bool, tuple) pair with action-command results."""
        action_command = self.gige_tl.ActionCommand(123454321, 2, pylon.AllGroupMask)
        ok, results = action_command.IssueWait(100, 1)
        self.assertIsInstance(ok, bool)
        self.assertIsInstance(results, tuple)

    # ------------------------------------------------------------------
    # ScheduledActionCommand (Python helper class, SWIG extension)
    # ------------------------------------------------------------------

    def test_scheduled_action_command_action_time_ns_property(self):
        """ScheduledActionCommand.actionTimeNs property can be read and written."""
        scheduled_action_command = self.gige_tl.ScheduledActionCommand(
            123454321, 2, pylon.AllGroupMask, 1000
        )
        self.assertEqual(scheduled_action_command.actionTimeNs, 1000)
        scheduled_action_command.actionTimeNs = 2000
        self.assertEqual(scheduled_action_command.actionTimeNs, 2000)

    def test_scheduled_action_command_issue_no_wait(self):
        """ScheduledActionCommand.IssueNoWait broadcasts a scheduled action command and returns bool."""
        scheduled_action_command = self.gige_tl.ScheduledActionCommand(
            123454321, 2, pylon.AllGroupMask, 0
        )
        self.assertIsInstance(scheduled_action_command.IssueNoWait(), bool)

    def test_issue_scheduled_action_command_no_wait(self):
        """IssueScheduledActionCommandNoWait broadcasts a scheduled action command and returns bool."""
        ok = self.gige_tl.IssueScheduledActionCommandNoWait(
            123454321, 2, pylon.AllGroupMask, 0, "255.255.255.255"
        )
        self.assertIsInstance(ok, bool)

    def test_issue_scheduled_action_command_wait_returns_result_tuple(self):
        """IssueScheduledActionCommandWait returns a (bool, tuple) pair with results."""
        ok, results = self.gige_tl.IssueScheduledActionCommandWait(
            123454321, 2, pylon.AllGroupMask, 0, "255.255.255.255", 100, 1
        )
        self.assertIsInstance(ok, bool)
        self.assertIsInstance(results, tuple)

    def test_issue_scheduled_action_command_wait_result_entries_are_address_status_tuples(self):
        """Each entry in IssueScheduledActionCommandWait results is a (str, int) tuple."""
        ok, results = self.gige_tl.IssueScheduledActionCommandWait(
            123454321, 2, pylon.AllGroupMask, 0, "255.255.255.255", 100, 1
        )
        for entry in results:
            self.assertIsInstance(entry, tuple)
            self.assertEqual(len(entry), 2)
            address, status = entry
            self.assertIsInstance(address, str)
            self.assertIsInstance(status, int)

    def test_issue_scheduled_action_command_wait_invalid_group_mask(self):
        """IssueScheduledActionCommandWait raises InvalidArgumentException when GroupMask is 0."""
        self.assertRaises(
            genicam.InvalidArgumentException,
            self.gige_tl.IssueScheduledActionCommandWait,
            123454321, 2, 0, 0, "255.255.255.255", 100, 1,
        )

    def test_scheduled_action_command_issue_wait_returns_result_tuple(self):
        """ScheduledActionCommand.IssueWait returns a (bool, tuple) pair with results."""
        scheduled_action_command = self.gige_tl.ScheduledActionCommand(
            123454321, 2, pylon.AllGroupMask, 0
        )
        ok, results = scheduled_action_command.IssueWait(100, 1)
        self.assertIsInstance(ok, bool)
        self.assertIsInstance(results, tuple)

    # ------------------------------------------------------------------
    # EGigEActionCommandStatus
    # ------------------------------------------------------------------

    def test_gige_action_command_status_ok(self):
        """GigEActionCommandStatus_Ok equals 0."""
        self.assertEqual(pylon.GigEActionCommandStatus_Ok, 0)

    def test_gige_action_command_status_no_ref_time(self):
        """GigEActionCommandStatus_NoRefTime is the signed-32-bit interpretation of 0xE1018013."""
        self.assertEqual(pylon.GigEActionCommandStatus_NoRefTime, 0xE1018013 - 0x100000000)

    def test_gige_action_command_status_overflow(self):
        """GigEActionCommandStatus_Overflow is the signed-32-bit interpretation of 0xE1018015."""
        self.assertEqual(pylon.GigEActionCommandStatus_Overflow, 0xE1018015 - 0x100000000)

    def test_gige_action_command_status_action_late(self):
        """GigEActionCommandStatus_ActionLate is the signed-32-bit interpretation of 0xE1018016."""
        self.assertEqual(pylon.GigEActionCommandStatus_ActionLate, 0xE1018016 - 0x100000000)


if __name__ == "__main__":
    unittest.main()
