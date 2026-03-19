from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest


class CommandParameterTestSuite(PylonParameterTestCase):

    # ------------------------------------------------------------------
    # Construction / Attach / Release
    # ------------------------------------------------------------------

    def test_command_parameter_construction_default(self):
        """Default construction produces an invalid parameter."""
        p = pylon.CommandParameter()
        self.assertFalse(p.IsValid())

    def test_command_parameter_construction_from_inode(self):
        """Construction from INode attaches and validates."""
        node = self.getINode("TestCommand")
        p = pylon.CommandParameter(node)
        self.assertTrue(p.IsValid())

    def test_command_parameter_construction_from_nodemap_name(self):
        """Construction from nodemap + name attaches and validates."""
        p = pylon.CommandParameter(self.nodemap, "TestCommand")
        self.assertTrue(p.IsValid())

    def test_command_parameter_construction_copy(self):
        """Copy construction produces a valid, equal parameter."""
        p1 = pylon.CommandParameter(self.nodemap, "TestCommand")
        p2 = pylon.CommandParameter(p1)
        self.assertTrue(p1.IsValid())
        self.assertTrue(p2.IsValid())
        self.assertTrue(p1.Equals(p2))

    def test_command_parameter_attach_from_inode(self):
        """Attach from INode sets validity and correct node."""
        node_a = self.getINode("TestCommand")
        node_b = self.getINode("DeviceReset")

        p = pylon.CommandParameter()
        self.assertFalse(p.IsValid())

        result = p.Attach(node_a)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(node_a))
        self.assertFalse(p.Equals(node_b))

        result = p.Attach(node_b)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(node_b))
        self.assertFalse(p.Equals(node_a))

    def test_command_parameter_attach_from_nodemap_name(self):
        """Attach from nodemap + name; non-existent name returns False."""
        p = pylon.CommandParameter()

        result = p.Attach(self.nodemap, "TestCommand")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "DeviceReset")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "NonExistent")
        self.assertFalse(result)

    def test_command_parameter_release(self):
        """Release makes parameter invalid."""
        p = pylon.CommandParameter(self.nodemap, "TestCommand")
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    def test_integer_parameter_genicam_Command(self):
        """Can work with GenICam ICommand type."""
        command = self.nodemap.GetNode("TestCommand") #returns GenApi::ICommand python equivalent
        p = pylon.CommandParameter(command)
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())
        p.Attach(command)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(command))


    # ------------------------------------------------------------------
    # Equals
    # ------------------------------------------------------------------

    def test_command_parameter_equals_parameter(self):
        """Equals between two CommandParameters."""
        node_a = self.nodemap.GetNode("TestCommand")
        node_b = self.nodemap.GetNode("DeviceReset")

        p1 = pylon.CommandParameter(node_a)
        p2 = pylon.CommandParameter(node_a)
        p3 = pylon.CommandParameter(node_b)
        p_empty1 = pylon.CommandParameter()
        p_empty2 = pylon.CommandParameter()

        self.assertTrue(p_empty1.Equals(p_empty2))
        self.assertTrue(p1.Equals(p2))
        self.assertTrue(p2.Equals(p1))
        self.assertFalse(p1.Equals(p3))
        self.assertFalse(p1.Equals(p_empty1))
        self.assertFalse(p_empty1.Equals(p1))

    def test_command_parameter_equals_inode(self):
        """Equals against INode and None."""
        node_a = self.getINode("TestCommand")
        node_b = self.getINode("DeviceReset")

        p_empty = pylon.CommandParameter()
        p = pylon.CommandParameter(node_a)

        self.assertTrue(p_empty.Equals(None))
        self.assertFalse(p_empty.Equals(node_a))
        self.assertTrue(p.Equals(node_a))
        self.assertFalse(p.Equals(node_b))
        self.assertFalse(p.Equals(None))

    # ------------------------------------------------------------------
    # IsValid
    # ------------------------------------------------------------------

    def test_command_parameter_is_valid(self):
        """IsValid reflects attach/release lifecycle."""
        p = pylon.CommandParameter()
        self.assertFalse(p.IsValid())

        p.Attach(self.nodemap, "TestCommand")
        self.assertTrue(p.IsValid())

        p.Release()
        self.assertFalse(p.IsValid())

    # ------------------------------------------------------------------
    # Unattached – Execute, IsDone must raise
    # ------------------------------------------------------------------

    def test_command_parameter_unattached_raises(self):
        """Execute and IsDone raise on unattached parameter."""
        p = pylon.CommandParameter()
        with self.assertRaises(Exception):
            p.Execute()
        with self.assertRaises(Exception):
            p.IsDone()

    # ------------------------------------------------------------------
    # Execute / IsDone / TryExecute
    # ------------------------------------------------------------------

    def test_command_parameter_execute(self):
        """Execute on RW command sets CommandInt to the CommandValue (4711)."""
        command_int = pylon.IntegerParameter(self.nodemap, "CommandInt")
        p = pylon.CommandParameter(self.nodemap, "TestCommand")

        command_int.SetValue(23)
        self.assertEqual(23, command_int.GetValue())

        p.Execute()
        self.assertEqual(4711, command_int.GetValue())

    def test_command_parameter_execute_ro_raises(self):
        """Execute on read-only command raises AccessException."""
        p = pylon.CommandParameter(self.nodemap, "TestCommandRO")
        with self.assertRaises(Exception):
            p.Execute()

    def test_command_parameter_execute_wo(self):
        """Execute on write-only command does not raise."""
        p = pylon.CommandParameter(self.nodemap, "TestCommandWO")
        p.Execute()  # must not raise

    def test_command_parameter_try_execute_rw(self):
        """TryExecute returns True for RW command."""
        p = pylon.CommandParameter(self.nodemap, "TestCommand")
        self.assertTrue(p.TryExecute())

    def test_command_parameter_try_execute_wo(self):
        """TryExecute returns True for write-only command."""
        p = pylon.CommandParameter(self.nodemap, "TestCommandWO")
        self.assertTrue(p.TryExecute())

    def test_command_parameter_try_execute_ro(self):
        """TryExecute returns False for read-only command."""
        p = pylon.CommandParameter(self.nodemap, "TestCommandRO")
        self.assertFalse(p.TryExecute())

    def test_command_parameter_is_done(self):
        """IsDone is callable after Execute on RW and RO commands."""
        p_rw = pylon.CommandParameter(self.nodemap, "TestCommand")
        p_rw.Execute()
        result = p_rw.IsDone()
        self.assertIsInstance(result, bool)

        p_ro = pylon.CommandParameter(self.nodemap, "TestCommandRO")
        result = p_ro.IsDone()  # must not raise, even for RO
        self.assertIsInstance(result, bool)

        p_wo = pylon.CommandParameter(self.nodemap, "TestCommandWO")
        p_wo.Execute()
        result = p_wo.IsDone()
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    # ------------------------------------------------------------------
    # Access modes
    # ------------------------------------------------------------------

    def test_command_parameter_access_modes(self):
        """IsReadable, IsWritable, GetAccessMode return correct values."""
        p_rw = pylon.CommandParameter(self.nodemap, "TestCommand")
        p_wo = pylon.CommandParameter(self.nodemap, "TestCommandWO")
        p_ro = pylon.CommandParameter(self.nodemap, "TestCommandRO")
        p_unattached = pylon.CommandParameter()

        # TestCommand is RW (readable = IsDone, writable = Execute)
        self.assertEqual(genicam.RW, p_rw.GetAccessMode())

        # TestCommandWO is write-only
        self.assertFalse(p_wo.IsReadable())
        self.assertTrue(p_wo.IsWritable())
        self.assertEqual(genicam.WO, p_wo.GetAccessMode())

        # TestCommandRO is read-only
        self.assertTrue(p_ro.IsReadable())
        self.assertFalse(p_ro.IsWritable())
        self.assertEqual(genicam.RO, p_ro.GetAccessMode())

        # Unattached is NI
        self.assertFalse(p_unattached.IsReadable())
        self.assertFalse(p_unattached.IsWritable())
        self.assertEqual(genicam.NI, p_unattached.GetAccessMode())

    # ------------------------------------------------------------------
    # ToString / FromString / ToStringOrDefault
    # ------------------------------------------------------------------

    def test_command_parameter_to_string(self):
        """ToString is callable on attached RW command."""
        p = pylon.CommandParameter(self.nodemap, "TestCommand")
        result = p.ToString()
        self.assertIsInstance(result, str)

    def test_command_parameter_to_string_unattached_raises(self):
        """ToString raises on unattached parameter."""
        p = pylon.CommandParameter()
        with self.assertRaises(Exception):
            p.ToString()

    def test_command_parameter_from_string_invalid_raises(self):
        """FromString with non-'1' string raises InvalidArgumentException."""
        p = pylon.CommandParameter(self.nodemap, "TestCommand")
        with self.assertRaises(Exception):
            p.FromString("")
        with self.assertRaises(Exception):
            p.FromString("test")

    def test_command_parameter_from_string_executes(self):
        """FromString('1') executes the command (sets CommandInt to 4711)."""
        command_int = pylon.IntegerParameter(self.nodemap, "CommandInt")
        p = pylon.CommandParameter(self.nodemap, "TestCommand")

        command_int.SetValue(23)
        self.assertEqual(23, command_int.GetValue())

        p.FromString("1")
        self.assertEqual(4711, command_int.GetValue())

    def test_command_parameter_to_string_or_default(self):
        """ToStringOrDefault returns value for RW, default for WO/unattached."""
        p_rw = pylon.CommandParameter(self.nodemap, "TestCommand")
        result = p_rw.ToStringOrDefault("default")
        self.assertIsInstance(result, str)
        self.assertNotEqual("default", result)

        p_wo = pylon.CommandParameter(self.nodemap, "TestCommandWO")
        self.assertEqual("default", p_wo.ToStringOrDefault("default"))

        p_unattached = pylon.CommandParameter()
        self.assertEqual("default", p_unattached.ToStringOrDefault("default"))

    # ------------------------------------------------------------------
    # GetNode / IsValueCacheValid
    # ------------------------------------------------------------------

    def test_command_parameter_get_node(self):
        """GetNode returns attached node; raises when unattached."""
        node = self.getINode("TestCommand")
        p = pylon.CommandParameter(node)
        self.assertEqual("TestCommand", p.GetNode().GetName())

        p.Release()
        with self.assertRaises(Exception):
            p.GetNode()

    def test_command_parameter_is_value_cache_valid(self):
        """IsValueCacheValid is callable and returns a bool."""
        p = pylon.CommandParameter(self.nodemap, "TestCommand")
        self.assertIsInstance(p.IsValueCacheValid(), bool)

    # ------------------------------------------------------------------
    # GetInfo / GetInfoOrDefault
    # ------------------------------------------------------------------

    def test_command_parameter_get_info_or_default_unattached(self):
        """GetInfoOrDefault returns defaults for unattached parameter."""
        p = pylon.CommandParameter()
        self.assertEqual("A", p.GetInfoOrDefault(pylon.ParameterInfo_Name, "A"))
        self.assertEqual("B", p.GetInfoOrDefault(pylon.ParameterInfo_DisplayName, "B"))
        self.assertEqual("C", p.GetInfoOrDefault(pylon.ParameterInfo_ToolTip, "C"))
        self.assertEqual("D", p.GetInfoOrDefault(pylon.ParameterInfo_Description, "D"))

    def test_command_parameter_get_info_unattached_raises(self):
        """GetInfo raises for each info kind when unattached."""
        p = pylon.CommandParameter()
        for kind in (pylon.ParameterInfo_Name, pylon.ParameterInfo_DisplayName,
                     pylon.ParameterInfo_ToolTip, pylon.ParameterInfo_Description):
            with self.assertRaises(Exception):
                p.GetInfo(kind)

    def test_command_parameter_get_info_attached(self):
        """GetInfo returns node name for attached parameter."""
        p = pylon.CommandParameter(self.nodemap, "TestCommand")
        self.assertEqual("TestCommand", p.GetInfo(pylon.ParameterInfo_Name))
        self.assertEqual("TestCommand", p.GetInfoOrDefault(pylon.ParameterInfo_Name, "default"))

    def test_parameter_str(self):
        """Test CParameter __str__."""
        p_unattached = pylon.CommandParameter()
        self.assertEqual(str(p_unattached), "<not found>")
        p_wo = pylon.CommandParameter(self.nodemap, "TestCommandWO")
        self.assertEqual(str(p_wo), "<not readable>")
        p_ro = pylon.CommandParameter(self.nodemap, "TestCommandRO")
        self.assertEqual(str(p_ro), "0")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
