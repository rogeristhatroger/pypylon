from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest

class StringParameterTestSuite(PylonParameterTestCase):

    # ------------------------------------------------------------------
    # Construction / Attach / Release
    # ------------------------------------------------------------------

    def test_string_parameter_construction_default(self):
        """Default construction produces an invalid parameter."""
        p = pylon.StringParameter()
        self.assertFalse(p.IsValid())

    def test_string_parameter_construction_from_inode(self):
        """Construction from a matching INode attaches and validates;
        a wrong node type yields an invalid parameter."""
        node = self.getINode("TestStringRW")
        p = pylon.StringParameter(node)
        self.assertTrue(p.IsValid())

        # Wrong node type → invalid
        node_int = self.getINode("TestInt")
        p_bad = pylon.StringParameter(node_int)
        self.assertFalse(p_bad.IsValid())

    def test_string_parameter_construction_from_istring(self):
        """Construction from a GenApi IString object attaches and validates."""
        istring = self.nodemap.GetNode("TestStringRW")  # returns IString
        p = pylon.StringParameter(istring)
        self.assertTrue(p.IsValid())

    def test_string_parameter_construction_from_nodemap_name(self):
        """Construction from nodemap + name attaches and validates."""
        p = pylon.StringParameter(self.nodemap, "TestStringRW")
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(self.getINode("TestStringRW")))
        self.assertFalse(p.Equals(self.getINode("TestStringRO")))

    def test_string_parameter_construction_from_nonexistent_name(self):
        """Construction from nodemap + non-existent name produces an invalid parameter."""
        p = pylon.StringParameter(self.nodemap, "TestStringEmpty")
        self.assertFalse(p.IsValid())

    def test_string_parameter_construction_copy(self):
        """Copy construction produces a valid, equal parameter."""
        p1 = pylon.StringParameter(self.nodemap, "TestStringRW")
        p2 = pylon.StringParameter(p1)
        self.assertTrue(p1.IsValid())
        self.assertTrue(p2.IsValid())
        self.assertTrue(p1.Equals(p2))

    def test_string_parameter_attach_from_inode(self):
        """Attach from INode sets validity and correct node."""
        node_a = self.getINode("TestStringRW")
        node_b = self.getINode("TestStringRO")

        p = pylon.StringParameter()
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

    def test_string_parameter_attach_from_istring(self):
        """Attach from GenApi IString attaches correctly."""
        istring_rw = self.nodemap.GetNode("TestStringRW")
        p = pylon.StringParameter()
        result = p.Attach(istring_rw)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

    def test_string_parameter_attach_from_nodemap_name(self):
        """Attach from nodemap + name; non-existent name returns False."""
        p = pylon.StringParameter()

        result = p.Attach(self.nodemap, "TestStringRW")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "TestStringRO")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "NonExistent")
        self.assertFalse(result)

    def test_string_parameter_release(self):
        """Release makes parameter invalid."""
        p = pylon.StringParameter(self.nodemap, "TestStringRW")
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    # ------------------------------------------------------------------
    # Equals
    # ------------------------------------------------------------------

    def test_string_parameter_equals_parameter(self):
        """Equals between two StringParameters."""
        node_a = self.nodemap.GetNode("TestStringRW")
        node_b = self.nodemap.GetNode("TestStringRO")

        p1 = pylon.StringParameter(node_a)
        p2 = pylon.StringParameter(node_a)
        p3 = pylon.StringParameter(node_b)
        p_empty1 = pylon.StringParameter()
        p_empty2 = pylon.StringParameter()

        # Both empty → equal
        self.assertTrue(p_empty1.Equals(p_empty2))

        # Same node → equal
        self.assertTrue(p1.Equals(p2))
        self.assertTrue(p2.Equals(p1))

        # Different nodes → not equal
        self.assertFalse(p1.Equals(p3))
        self.assertFalse(p3.Equals(p1))

        # Attached vs empty → not equal
        self.assertFalse(p1.Equals(p_empty1))
        self.assertFalse(p_empty1.Equals(p1))

    def test_string_parameter_equals_inode(self):
        """Equals against INode and None."""
        node_a = self.getINode("TestStringRW")
        node_b = self.getINode("TestStringRO")

        p_empty = pylon.StringParameter()
        p = pylon.StringParameter(node_a)

        self.assertTrue(p_empty.Equals(None))
        self.assertFalse(p_empty.Equals(node_a))
        self.assertTrue(p.Equals(node_a))
        self.assertFalse(p.Equals(node_b))
        self.assertFalse(p.Equals(None))

    def test_string_parameter_equals_istring(self):
        """Equals against a GenApi IString node."""
        istring_rw = self.nodemap.GetNode("TestStringRW")
        istring_ro = self.nodemap.GetNode("TestStringRO")

        p_empty = pylon.StringParameter()
        p = pylon.StringParameter(istring_rw)

        self.assertTrue(p.Equals(istring_rw))
        self.assertFalse(p.Equals(istring_ro))
        self.assertFalse(p_empty.Equals(istring_rw))

    # ------------------------------------------------------------------
    # IsValid / IsReadable / IsWritable / GetAccessMode
    # ------------------------------------------------------------------

    def test_string_parameter_is_valid(self):
        """IsValid reflects attachment state."""
        p = pylon.StringParameter()
        self.assertFalse(p.IsValid())

        p.Attach(self.nodemap, "TestStringRW")
        self.assertTrue(p.IsValid())

        p.Release()
        self.assertFalse(p.IsValid())

    def test_string_parameter_is_readable_writable(self):
        """IsReadable / IsWritable reflect the access mode."""
        p_ro = pylon.StringParameter(self.nodemap, "TestStringRO")
        self.assertTrue(p_ro.IsReadable())
        self.assertFalse(p_ro.IsWritable())

        p_wo = pylon.StringParameter(self.nodemap, "TestStringWO")
        self.assertFalse(p_wo.IsReadable())
        self.assertTrue(p_wo.IsWritable())

        p_rw = pylon.StringParameter(self.nodemap, "TestStringRW")
        self.assertTrue(p_rw.IsReadable())
        self.assertTrue(p_rw.IsWritable())

        p_unattached = pylon.StringParameter()
        self.assertFalse(p_unattached.IsReadable())
        self.assertFalse(p_unattached.IsWritable())

    def test_string_parameter_get_access_mode(self):
        """GetAccessMode returns the correct genicam constant."""
        p_ro = pylon.StringParameter(self.nodemap, "TestStringRO")
        p_wo = pylon.StringParameter(self.nodemap, "TestStringWO")
        p_rw = pylon.StringParameter(self.nodemap, "TestStringRW")
        p_unattached = pylon.StringParameter()

        self.assertEqual(p_ro.GetAccessMode(), genicam.RO)
        self.assertEqual(p_wo.GetAccessMode(), genicam.WO)
        self.assertEqual(p_rw.GetAccessMode(), genicam.RW)
        self.assertEqual(p_unattached.GetAccessMode(), genicam.NI)

    # ------------------------------------------------------------------
    # Unattached – all value operations must raise
    # ------------------------------------------------------------------

    def test_string_parameter_unattached_raises(self):
        """All value/property access on unattached parameter raises."""
        p = pylon.StringParameter()
        with self.assertRaises(Exception):
            p.SetValue("dont care")
        with self.assertRaises(Exception):
            p.GetValue()
        with self.assertRaises(Exception):
            p.GetMaxLength()

    def test_string_parameter_nonexistent_node_raises(self):
        """Parameter attached to a non-existent node raises on value access."""
        p = pylon.StringParameter(self.nodemap, "TestStringEmpty")
        self.assertFalse(p.IsValid())
        self.assertFalse(p.IsReadable())
        self.assertFalse(p.IsWritable())
        with self.assertRaises(Exception):
            p.GetValue()
        with self.assertRaises(Exception):
            p.SetValue("")
        with self.assertRaises(Exception):
            p.SetValue("test")
        with self.assertRaises(Exception):
            p.ToString()

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def test_string_parameter_read(self):
        """GetValue returns the correct initial value for the RO node."""
        p = pylon.StringParameter(self.nodemap, "TestStringRO")
        value = p.GetValue()
        self.assertEqual("TestStringValueRO", value)

        # ignoreCache variants
        self.assertEqual("TestStringValueRO", p.GetValue(False))
        self.assertEqual("TestStringValueRO", p.GetValue(False, False))

    def test_string_parameter_read_only_raises_on_write(self):
        """SetValue on a read-only parameter raises an AccessException."""
        p = pylon.StringParameter(self.nodemap, "TestStringRO")
        with self.assertRaises(Exception):
            p.SetValue("")
        with self.assertRaises(Exception):
            p.SetValue("Test")
        # Value must remain unchanged
        self.assertEqual("TestStringValueRO", p.GetValue())

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def test_string_parameter_write(self):
        """SetValue / GetValue round-trip for RW parameter."""
        p = pylon.StringParameter(self.nodemap, "TestStringRW")
        initial = p.GetValue()

        p.SetValue("test")
        after = p.GetValue()
        self.assertNotEqual(initial, after)
        self.assertEqual("test", after)

        p.SetValue("test2", False)
        after = p.GetValue()
        self.assertNotEqual(initial, after)
        self.assertEqual("test2", after)

    def test_string_parameter_write_prop(self):
        """Property Value round-trip for RW parameter."""
        p = pylon.StringParameter(self.nodemap, "TestStringRW")
        initial = p.Value

        p.Value = "test"
        after = p.Value
        self.assertNotEqual(initial, after)
        self.assertEqual("test", after)

        p.Value = "test2"
        after = p.Value
        self.assertNotEqual(initial, after)
        self.assertEqual("test2", after)

    def test_string_parameter_write_empty_string(self):
        """SetValue accepts an empty string."""
        p = pylon.StringParameter(self.nodemap, "TestStringRW")
        p.SetValue("")
        self.assertEqual("", p.GetValue())

    # ------------------------------------------------------------------
    # ToString / FromString
    # ------------------------------------------------------------------

    def test_string_parameter_to_string(self):
        """ToString returns the string representation of the current value."""
        p = pylon.StringParameter(self.nodemap, "TestStringRO")
        self.assertEqual("TestStringValueRO", p.ToString())

        p_rw = pylon.StringParameter(self.nodemap, "TestStringRW")
        p_rw.SetValue("hello")
        self.assertEqual("hello", p_rw.ToString())

    def test_string_parameter_to_string_unattached_raises(self):
        """ToString on unattached parameter raises."""
        p = pylon.StringParameter()
        with self.assertRaises(Exception):
            p.ToString()

    def test_string_parameter_from_string(self):
        """FromString sets the value; RO parameter raises."""
        p_rw = pylon.StringParameter(self.nodemap, "TestStringRW")

        # Empty value
        p_rw.FromString("")
        self.assertEqual("", p_rw.GetValue())

        # Valid value 1
        p_rw.FromString("value1")
        self.assertEqual("value1", p_rw.GetValue())

        # Valid value 2
        p_rw.FromString("value2")
        self.assertEqual("value2", p_rw.GetValue())

        # RO parameter raises
        p_ro = pylon.StringParameter(self.nodemap, "TestStringRO")
        with self.assertRaises(Exception):
            p_ro.FromString("value1")
        # Value must remain unchanged
        self.assertEqual("TestStringValueRO", p_ro.GetValue())

        # WO parameter does not raise
        p_wo = pylon.StringParameter(self.nodemap, "TestStringWO")
        p_wo.FromString("value1")  # must not raise

    def test_string_parameter_from_string_unattached_raises(self):
        """FromString on unattached parameter raises."""
        p = pylon.StringParameter()
        with self.assertRaises(Exception):
            p.FromString("1234")

    # ------------------------------------------------------------------
    # TrySetValue
    # ------------------------------------------------------------------

    def test_string_parameter_try_set_value_rw(self):
        """TrySetValue succeeds on a writable parameter and returns True."""
        p = pylon.StringParameter(self.nodemap, "TestStringRW")

        # Empty string
        self.assertTrue(p.TrySetValue(""))
        self.assertEqual("", p.GetValue())

        # Non-empty values
        self.assertTrue(p.TrySetValue("value1"))
        self.assertEqual("value1", p.GetValue())

        self.assertTrue(p.TrySetValue("value2"))
        self.assertEqual("value2", p.GetValue())
        self.assertEqual("value2", p.GetValue(True))
        self.assertEqual("value2", p.GetValue(True, True))

    def test_string_parameter_try_set_value_ro_returns_false(self):
        """TrySetValue on a read-only parameter returns False without raising."""
        p_ro = pylon.StringParameter(self.nodemap, "TestStringRO")
        result = p_ro.TrySetValue("value1")
        self.assertFalse(result)
        # Value must remain unchanged
        self.assertEqual("TestStringValueRO", p_ro.GetValue())

    def test_string_parameter_try_set_value_wo_returns_true(self):
        """TrySetValue on a write-only parameter returns True without raising."""
        p_wo = pylon.StringParameter(self.nodemap, "TestStringWO")
        result = p_wo.TrySetValue("value1")
        self.assertTrue(result)

    # ------------------------------------------------------------------
    # GetValueOrDefault
    # ------------------------------------------------------------------

    def test_string_parameter_get_value_or_default_readable(self):
        """GetValueOrDefault returns the actual value for a readable parameter."""
        p_rw = pylon.StringParameter(self.nodemap, "TestStringRW")
        self.assertTrue(p_rw.IsReadable())
        actual = p_rw.GetValue()
        result = p_rw.GetValueOrDefault("defaultValue")
        self.assertEqual(actual, result)
        self.assertNotEqual("defaultValue", result)

    def test_string_parameter_get_value_or_default_not_readable(self):
        """GetValueOrDefault returns the default for a non-readable (WO) parameter."""
        p_wo = pylon.StringParameter(self.nodemap, "TestStringWO")
        self.assertFalse(p_wo.IsReadable())
        self.assertTrue(p_wo.IsWritable())
        result = p_wo.GetValueOrDefault("defaultValue")
        self.assertEqual("defaultValue", result)

    # ------------------------------------------------------------------
    # GetMaxLength
    # ------------------------------------------------------------------

    def test_string_parameter_get_max_length(self):
        """GetMaxLength is callable on an attached parameter and returns an integer."""
        p = pylon.StringParameter(self.nodemap, "TestStringRW")
        max_len = p.GetMaxLength()
        self.assertIsInstance(max_len, int)
        # Property shortcut
        self.assertEqual(max_len, p.MaxLength)
        self.assertEqual(p.GetMaxLength(), p.GetMaxLength(False))

    def test_string_parameter_get_max_length_unattached_raises(self):
        """GetMaxLength on unattached parameter raises."""
        p = pylon.StringParameter()
        with self.assertRaises(Exception):
            p.GetMaxLength()

    # ------------------------------------------------------------------
    # Value property shortcut
    # ------------------------------------------------------------------

    def test_string_parameter_value_property(self):
        """The .Value property returns the same as GetValue()."""
        p = pylon.StringParameter(self.nodemap, "TestStringRO")
        self.assertEqual(p.GetValue(), p.Value)

    # ------------------------------------------------------------------
    # GetNode
    # ------------------------------------------------------------------

    def test_string_parameter_get_node(self):
        """GetNode returns the attached node; unattached raises."""
        node = self.getINode("TestStringRW")
        p = pylon.StringParameter(node)
        self.assertEqual(p.GetNode().GetName(), node.GetName())
        self.assertEqual(p.Node.GetName(), node.GetName())

        p.Release()
        with self.assertRaises(Exception):
            p.GetNode()

    # ------------------------------------------------------------------
    # IsValueCacheValid
    # ------------------------------------------------------------------

    def test_string_parameter_is_value_cache_valid(self):
        """IsValueCacheValid is callable on an attached parameter."""
        p = pylon.StringParameter(self.nodemap, "TestStringRW")
        cache_valid = p.IsValueCacheValid()
        self.assertIsInstance(cache_valid, bool)

    # ------------------------------------------------------------------
    # ToStringOrDefault / __str__
    # ------------------------------------------------------------------

    def test_string_parameter_to_string_or_default(self):
        """ToStringOrDefault returns actual value or default depending on readability."""
        p_unattached = pylon.StringParameter()
        self.assertEqual("default", p_unattached.ToStringOrDefault("default"))

        p_ro = pylon.StringParameter(self.nodemap, "TestStringRO")
        self.assertEqual("TestStringValueRO", p_ro.ToStringOrDefault("default"))

        p_wo = pylon.StringParameter(self.nodemap, "TestStringWO")
        self.assertEqual("default", p_wo.ToStringOrDefault("default"))

    def test_string_parameter_str(self):
        """__str__ returns the value string, '<not found>', or '<not readable>'."""
        p_unattached = pylon.StringParameter()
        self.assertEqual("<not found>", str(p_unattached))

        p_wo = pylon.StringParameter(self.nodemap, "TestStringWO")
        self.assertEqual("<not readable>", str(p_wo))

        p_ro = pylon.StringParameter(self.nodemap, "TestStringRO")
        self.assertEqual("TestStringValueRO", str(p_ro))

    # ------------------------------------------------------------------
    # Compatibility with genicam
    # ------------------------------------------------------------------

    def test_genicam_compatibility(self):
        """Parameter can be used wherever genicam interfaces are expected."""
        p = pylon.StringParameter(self.nodemap, "TestStringRW")
        self.assertIsInstance(p, genicam.IString)
        self.assertIsInstance(p, genicam.IValue)
        self.assertTrue(genicam.IsReadable(p))
        self.assertTrue(genicam.IsWritable(p))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
