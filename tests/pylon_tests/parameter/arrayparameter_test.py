from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest


# ---------------------------------------------------------------------------
# A minimal in-process port backed by a plain bytearray.
# ---------------------------------------------------------------------------
class _TestPort(genicam.CPortImpl):
    def __init__(self, size=256):
        genicam.CPortImpl.__init__(self)
        self._mem = bytearray(size)

    def Read(self, address, length):
        return bytes(self._mem[address:address + length])

    def Write(self, address, data):
        n = len(data)
        self._mem[address:address + n] = data

    def GetAccessMode(self):
        return genicam.RW

class ArrayParameterTestSuite(PylonParameterTestCase):

    def setUp(self):
        super().setUp()
        # Connect the test port to the 'Device' port node so that the
        # Register nodes (RegisterA, RegisterB) become accessible.
        self._port = _TestPort()
        self.nodemapref._Connect(self._port, "Device")

    # ------------------------------------------------------------------
    # Construction / Attach / Release
    # ------------------------------------------------------------------

    def test_array_parameter_construction_default(self):
        """Default construction produces an invalid parameter."""
        p = pylon.ArrayParameter()
        self.assertFalse(p.IsValid())

    def test_array_parameter_construction_from_inode(self):
        """Construction from INode: register node → valid, non-register → invalid."""
        node_reg = self.getINode("RegisterA")
        p = pylon.ArrayParameter(node_reg)
        self.assertTrue(p.IsValid())

        node_other = self.getINode("TestInt")
        p2 = pylon.ArrayParameter(node_other)
        self.assertFalse(p2.IsValid())

    def test_array_parameter_construction_from_iregister(self):
        """Construction from IRegister (obtained via GetNode) attaches and validates."""
        reg = self.nodemap.GetNode("RegisterA")
        p = pylon.ArrayParameter(reg)
        self.assertTrue(p.IsValid())

    def test_array_parameter_construction_from_nodemap_name(self):
        """Construction from nodemap + name attaches and validates."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        self.assertTrue(p.IsValid())

        p2 = pylon.ArrayParameter(self.nodemap, "RegisterB")
        self.assertTrue(p2.IsValid())

        # Non-register node → invalid
        p3 = pylon.ArrayParameter(self.nodemap, "TestInt")
        self.assertFalse(p3.IsValid())

    def test_array_parameter_construction_copy(self):
        """Copy construction produces a valid, equal parameter."""
        p1 = pylon.ArrayParameter(self.nodemap, "RegisterA")
        p2 = pylon.ArrayParameter(p1)
        self.assertTrue(p1.IsValid())
        self.assertTrue(p2.IsValid())
        self.assertTrue(p1.Equals(p2))

    def test_array_parameter_attach_from_inode(self):
        """Attach from INode sets validity and correct node."""
        node_a = self.getINode("RegisterA")
        node_b = self.getINode("RegisterB")

        p = pylon.ArrayParameter()
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

    def test_array_parameter_attach_from_iregister(self):
        """Attach from IRegister (obtained via GetNode) attaches correctly."""
        reg_a = self.nodemap.GetNode("RegisterA")
        reg_b = self.nodemap.GetNode("RegisterB")

        p = pylon.ArrayParameter()
        result = p.Attach(reg_a)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(reg_a))
        self.assertFalse(p.Equals(reg_b))

    def test_array_parameter_attach_from_nodemap_name(self):
        """Attach from nodemap + name; non-existent name returns False."""
        p = pylon.ArrayParameter()

        result = p.Attach(self.nodemap, "RegisterA")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "RegisterB")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "NonExistent")
        self.assertFalse(result)

    def test_array_parameter_release(self):
        """Release makes parameter invalid."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    # ------------------------------------------------------------------
    # Equals
    # ------------------------------------------------------------------

    def test_array_parameter_equals_parameter(self):
        """Equals between two ArrayParameters."""
        node_a = self.nodemap.GetNode("RegisterA")
        node_b = self.nodemap.GetNode("RegisterB")

        p1 = pylon.ArrayParameter(node_a)
        p2 = pylon.ArrayParameter(node_a)
        p3 = pylon.ArrayParameter(node_b)
        p_empty1 = pylon.ArrayParameter()
        p_empty2 = pylon.ArrayParameter()

        self.assertTrue(p_empty1.Equals(p_empty2))
        self.assertTrue(p1.Equals(p2))
        self.assertTrue(p2.Equals(p1))
        self.assertFalse(p1.Equals(p3))
        self.assertFalse(p1.Equals(p_empty1))
        self.assertFalse(p_empty1.Equals(p1))

    def test_array_parameter_equals_inode(self):
        """Equals against INode and None."""
        node_a = self.getINode("RegisterA")
        node_b = self.getINode("RegisterB")

        p_empty = pylon.ArrayParameter()
        p = pylon.ArrayParameter(node_a)

        self.assertTrue(p_empty.Equals(None))
        self.assertFalse(p_empty.Equals(node_a))
        self.assertTrue(p.Equals(node_a))
        self.assertFalse(p.Equals(node_b))
        self.assertFalse(p.Equals(None))

    def test_array_parameter_equals_iregister(self):
        """Equals against IRegister (obtained via GetNode)."""
        reg_a = self.nodemap.GetNode("RegisterA")
        reg_b = self.nodemap.GetNode("RegisterB")

        p_empty = pylon.ArrayParameter()
        p = pylon.ArrayParameter(reg_a)

        self.assertFalse(p_empty.Equals(reg_a))
        self.assertTrue(p.Equals(reg_a))
        self.assertFalse(p.Equals(reg_b))

    # ------------------------------------------------------------------
    # Unattached – all value/register operations must raise
    # ------------------------------------------------------------------

    def test_array_parameter_unattached_raises(self):
        """All register/value access on unattached parameter raises."""
        p = pylon.ArrayParameter()
        with self.assertRaises(Exception): p.Set(b'\x00\x00')
        with self.assertRaises(Exception): p.Get(2)
        with self.assertRaises(Exception): p.GetLength()
        with self.assertRaises(Exception): p.GetAddress()
        with self.assertRaises(Exception): p.ToString()
        with self.assertRaises(Exception): p.FromString("0xabcd")
        with self.assertRaises(Exception): p.IsValueCacheValid()

    # ------------------------------------------------------------------
    # GetLength / GetAddress
    # ------------------------------------------------------------------

    def test_array_parameter_get_length(self):
        """GetLength returns the register length defined in the XML."""
        p_a = pylon.ArrayParameter(self.nodemap, "RegisterA")  # Length=4
        p_b = pylon.ArrayParameter(self.nodemap, "RegisterB")  # Length=2

        self.assertEqual(4, p_a.GetLength())
        self.assertEqual(2, p_b.GetLength())

    def test_array_parameter_get_length_property(self):
        """Length property equals GetLength()."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        self.assertEqual(p.GetLength(), p.Length)

    def test_array_parameter_get_address(self):
        """GetAddress returns the register address defined in the XML."""
        p_a = pylon.ArrayParameter(self.nodemap, "RegisterA")  # Address=0x80
        p_b = pylon.ArrayParameter(self.nodemap, "RegisterB")  # Address=0x90

        self.assertEqual(0x80, p_a.GetAddress())
        self.assertEqual(0x90, p_b.GetAddress())

    def test_array_parameter_get_address_property(self):
        """Address property equals GetAddress()."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        self.assertEqual(p.GetAddress(), p.Address)

    # # ------------------------------------------------------------------
    # # Set / Get round-trip
    # # ------------------------------------------------------------------

    def test_array_parameter_set_get_bytes(self):
        """Set bytes then Get returns identical data (RegisterA, length 4)."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        length = p.GetLength()
        length1 = p.GetLength(False)
        self.assertEqual(length, length1)

        data_a = bytes([0x41, 0x42, 0x43, 0x44])
        p.Set(data_a)
        result = p.Get(length)
        self.assertIsInstance(result, bytes)
        self.assertEqual(data_a, result)

        data_b = bytes([0xDE, 0xAD, 0xBE, 0xEF])
        p.Set(data_b)
        result = p.Get(length, False)
        self.assertEqual(data_b, result)

    def test_array_parameter_set_bytearray_get(self):
        """Set accepts bytearray; Get returns matching bytes."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        length = p.GetLength()

        data = bytes([0x11, 0x22, 0x33, 0x44])
        p.Set(data)
        result = p.Get(length)
        self.assertEqual(bytes(data), result)

        data = bytes([0x12, 0x23, 0x34, 0x45])
        p.Set(data, False)
        result = p.Get(length, False)
        self.assertEqual(bytes(data), result)
        result = p.Get(length, False, False)
        self.assertEqual(bytes(data), result)

    def test_array_parameter_set_get_register_b(self):
        """Set/Get round-trip on RegisterB (2 bytes)."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterB")
        length = p.GetLength()

        data_a = bytes([0x43, 0x44])
        p.Set(data_a)
        self.assertEqual(data_a, p.Get(length))

        data_b = bytes([0x67, 0x68])
        p.Set(data_b)
        self.assertEqual(data_b, p.Get(length))

    def test_array_parameter_set_invalid_type_raises(self):
        """Set raises when passed something other than bytes/bytearray."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        with self.assertRaises(Exception):
            p.Set("not bytes")
        with self.assertRaises(Exception):
            p.Set(12345)

    def test_array_parameter_set_verify_false(self):
        """Set with verify=False does not raise and data is stored."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        data = bytes([0x10, 0x20, 0x30, 0x40])
        p.Set(data, False)
        self.assertEqual(data, p.Get(p.GetLength()))

    def test_array_parameter_get_with_verify_and_ignore_cache_flags(self):
        """Get with explicit verify and ignoreCache flags works correctly."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        length = p.GetLength()
        data = bytes([0xAA, 0xBB, 0xCC, 0xDD])
        p.Set(data)

        self.assertEqual(data, p.Get(length, False, False))
        self.assertEqual(data, p.Get(length, False, True))

    def test_array_parameter_set_visible_in_port_memory(self):
        """Data written via Set is visible directly in the backing port memory."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        addr = p.GetAddress()    # 0x80
        addr1 = p.GetAddress(False)    # 0x80
        length = p.GetLength()   # 4
        self.assertEqual(addr, addr1)

        data = bytes([0x01, 0x02, 0x03, 0x04])
        p.Set(data)

        raw = bytes(self._port._mem[addr:addr + length])
        self.assertEqual(data, raw)

    def test_array_parameter_get_reads_from_port_memory(self):
        """Data written directly into port memory is visible via Get."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        addr = p.GetAddress()
        length = p.GetLength()

        expected = bytes([0xCA, 0xFE, 0xBA, 0xBE])
        self._port._mem[addr:addr + length] = expected

        self.assertEqual(expected, p.Get(length))

    def test_array_parameter_two_parameters_same_register(self):
        """Two parameters attached to the same register see each other's writes."""
        p1 = pylon.ArrayParameter(self.nodemap, "RegisterB")
        p2 = pylon.ArrayParameter(self.nodemap, "RegisterB")
        length = p1.GetLength()

        data_a = bytes([0xAB, 0xCD])
        p1.Set(data_a)
        self.assertEqual(data_a, p2.Get(length))

        data_b = bytes([0xEF, 0x34])
        p2.Set(data_b)
        self.assertEqual(data_b, p1.Get(length))

    # ------------------------------------------------------------------
    # ToString / FromString
    # ------------------------------------------------------------------

    def test_array_parameter_to_string_from_string(self):
        """FromString sets value; ToString returns the same hex string."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterB")  # 2-byte register

        p.FromString("0xabcd")
        s = p.ToString()
        self.assertIsInstance(s, str)
        self.assertEqual("0xabcd", s.lower())

        p.FromString("0xef34")
        self.assertEqual("0xef34", p.ToString().lower())

    def test_array_parameter_to_string_unattached_raises(self):
        """ToString on unattached parameter raises."""
        p = pylon.ArrayParameter()
        with self.assertRaises(Exception):
            p.ToString()

    def test_array_parameter_from_string_unattached_raises(self):
        """FromString on unattached parameter raises."""
        p = pylon.ArrayParameter()
        with self.assertRaises(Exception):
            p.FromString("0xabcd")

    # ------------------------------------------------------------------
    # IsValueCacheValid
    # ------------------------------------------------------------------

    def test_array_parameter_is_value_cache_valid(self):
        """IsValueCacheValid is callable and returns a bool."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        self.assertIsInstance(p.IsValueCacheValid(), bool)

    # ------------------------------------------------------------------
    # GetNode
    # ------------------------------------------------------------------

    def test_array_parameter_get_node(self):
        """GetNode returns the attached node; raises when unattached."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        self.assertEqual("RegisterA", p.GetNode().GetName())

        p.Release()
        with self.assertRaises(Exception):
            p.GetNode()

    # ------------------------------------------------------------------
    # IsValid lifecycle
    # ------------------------------------------------------------------

    def test_array_parameter_is_valid_lifecycle(self):
        """IsValid reflects attach/release lifecycle."""
        p = pylon.ArrayParameter()
        self.assertFalse(p.IsValid())

        p.Attach(self.nodemap, "RegisterA")
        self.assertTrue(p.IsValid())

        p.Release()
        self.assertFalse(p.IsValid())

    # ------------------------------------------------------------------
    # IsReadable / IsWritable / GetAccessMode
    # ------------------------------------------------------------------

    def test_array_parameter_access_mode(self):
        """GetAccessMode and IsReadable/IsWritable return correct values."""
        p_rw = pylon.ArrayParameter(self.nodemap, "RegisterA")  # AccessMode=RW
        p_unattached = pylon.ArrayParameter()

        self.assertTrue(p_rw.IsReadable())
        self.assertTrue(p_rw.IsWritable())
        self.assertEqual(genicam.RW, p_rw.GetAccessMode())

        self.assertFalse(p_unattached.IsReadable())
        self.assertFalse(p_unattached.IsWritable())
        self.assertEqual(genicam.NI, p_unattached.GetAccessMode())

    # ------------------------------------------------------------------
    # GetInfo / GetInfoOrDefault
    # ------------------------------------------------------------------

    def test_array_parameter_get_info_or_default_unattached(self):
        """GetInfoOrDefault returns the supplied default for unattached parameter."""
        p = pylon.ArrayParameter()
        self.assertEqual("A", p.GetInfoOrDefault(pylon.ParameterInfo_Name, "A"))
        self.assertEqual("B", p.GetInfoOrDefault(pylon.ParameterInfo_DisplayName, "B"))
        self.assertEqual("C", p.GetInfoOrDefault(pylon.ParameterInfo_ToolTip, "C"))
        self.assertEqual("D", p.GetInfoOrDefault(pylon.ParameterInfo_Description, "D"))

    def test_array_parameter_get_info_unattached_raises(self):
        """GetInfo raises for every info kind when unattached."""
        p = pylon.ArrayParameter()
        for kind in (pylon.ParameterInfo_Name, pylon.ParameterInfo_DisplayName,
                     pylon.ParameterInfo_ToolTip, pylon.ParameterInfo_Description):
            with self.assertRaises(Exception):
                p.GetInfo(kind)

    def test_array_parameter_get_info_attached(self):
        """GetInfo returns the node name for an attached parameter."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        self.assertEqual("RegisterA", p.GetInfo(pylon.ParameterInfo_Name))
        self.assertEqual("RegisterA", p.GetInfoOrDefault(pylon.ParameterInfo_Name, "default"))

    # ------------------------------------------------------------------
    # __str__
    # ------------------------------------------------------------------

    def test_array_parameter_str_unattached(self):
        """str() on unattached parameter returns '<not found>'."""
        p = pylon.ArrayParameter()
        self.assertEqual("<not found>", str(p))

    def test_array_parameter_str_attached(self):
        """str() on an attached, readable parameter returns a non-empty hex string."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        s = str(p)
        self.assertIsInstance(s, str)
        self.assertGreater(len(s), 0)
        self.assertNotEqual("<not found>", s)
        self.assertNotEqual("<not readable>", s)

    # ------------------------------------------------------------------
    # Compatibility with genicam
    # ------------------------------------------------------------------
    def test_genicam_compatibility(self):
        """Parameter can be used wherever genicam interfaces are expected."""
        p = pylon.ArrayParameter(self.nodemap, "RegisterA")
        self.assertIsInstance(p, genicam.IRegister)
        self.assertIsInstance(p, genicam.IValue)
        self.assertTrue(genicam.IsReadable(p))
        self.assertTrue(genicam.IsWritable(p))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
