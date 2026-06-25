from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest

class BooleanParameterTestSuite(PylonParameterTestCase):

    # ------------------------------------------------------------------
    # Construction / Attach / Release
    # ------------------------------------------------------------------

    def test_boolean_parameter_construction_default(self):
        """Default construction produces an invalid parameter."""
        p = pylon.BooleanParameter()
        self.assertFalse(p.IsValid())

    def test_boolean_parameter_construction_from_inode(self):
        """Construction from a matching INode attaches and validates;
        a wrong node type yields an invalid parameter."""
        node = self.getINode("TestBoolRW")
        p = pylon.BooleanParameter(node)
        self.assertTrue(p.IsValid())

        node_int = self.getINode("TestInt")
        p_bad = pylon.BooleanParameter(node_int)
        self.assertFalse(p_bad.IsValid())

    def test_boolean_parameter_construction_from_iboolean(self):
        """Construction from a GenApi IBoolean object attaches and validates."""
        iboolean = self.nodemap.GetNode("TestBoolRW")
        p = pylon.BooleanParameter(iboolean)
        self.assertTrue(p.IsValid())

    def test_boolean_parameter_construction_from_nodemap_name(self):
        """Construction from nodemap + name attaches and validates."""
        p = pylon.BooleanParameter(self.nodemap, "TestBoolRW")
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(self.getINode("TestBoolRW")))
        self.assertFalse(p.Equals(self.getINode("TestBoolRO")))

    def test_boolean_parameter_construction_from_nonexistent_name(self):
        """Construction from nodemap + non-existent name produces an invalid parameter."""
        p = pylon.BooleanParameter(self.nodemap, "TestBoolNotFound")
        self.assertFalse(p.IsValid())

    def test_boolean_parameter_construction_copy(self):
        """Copy construction produces a valid, equal parameter."""
        p1 = pylon.BooleanParameter(self.nodemap, "TestBoolRW")
        p2 = pylon.BooleanParameter(p1)
        self.assertTrue(p1.IsValid())
        self.assertTrue(p2.IsValid())
        self.assertTrue(p1.Equals(p2))

    def test_boolean_parameter_attach_from_inode(self):
        """Attach from INode sets validity and correct node."""
        node_a = self.getINode("TestBoolRW")
        node_b = self.getINode("TestBoolRO")

        p = pylon.BooleanParameter()
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

    def test_boolean_parameter_attach_from_iboolean(self):
        """Attach from GenApi IBoolean attaches correctly."""
        iboolean = self.nodemap.GetNode("TestBoolRW")
        p = pylon.BooleanParameter()
        result = p.Attach(iboolean)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

    def test_boolean_parameter_attach_from_nodemap_name(self):
        """Attach from nodemap + name; non-existent name returns False."""
        p = pylon.BooleanParameter()

        result = p.Attach(self.nodemap, "TestBoolRW")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "TestBoolRO")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "NonExistent")
        self.assertFalse(result)

    def test_boolean_parameter_release(self):
        """Release makes parameter invalid."""
        p = pylon.BooleanParameter(self.nodemap, "TestBoolRW")
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    # ------------------------------------------------------------------
    # Equals
    # ------------------------------------------------------------------

    def test_boolean_parameter_equals_parameter(self):
        """Equals between two BooleanParameters."""
        node_a = self.nodemap.GetNode("TestBoolRW")
        node_b = self.nodemap.GetNode("TestBoolRO")

        p1 = pylon.BooleanParameter(node_a)
        p2 = pylon.BooleanParameter(node_a)
        p3 = pylon.BooleanParameter(node_b)
        p_empty1 = pylon.BooleanParameter()
        p_empty2 = pylon.BooleanParameter()

        self.assertTrue(p_empty1.Equals(p_empty2))
        self.assertTrue(p1.Equals(p2))
        self.assertTrue(p2.Equals(p1))
        self.assertFalse(p1.Equals(p3))
        self.assertFalse(p3.Equals(p1))
        self.assertFalse(p1.Equals(p_empty1))
        self.assertFalse(p_empty1.Equals(p1))

    def test_boolean_parameter_equals_inode(self):
        """Equals against INode and None."""
        node_a = self.getINode("TestBoolRW")
        node_b = self.getINode("TestBoolRO")

        p_empty = pylon.BooleanParameter()
        p = pylon.BooleanParameter(node_a)

        self.assertTrue(p_empty.Equals(None))
        self.assertFalse(p_empty.Equals(node_a))
        self.assertTrue(p.Equals(node_a))
        self.assertFalse(p.Equals(node_b))
        self.assertFalse(p.Equals(None))

    def test_boolean_parameter_equals_iboolean(self):
        """Equals against a GenApi IBoolean node."""
        iboolean_rw = self.nodemap.GetNode("TestBoolRW")
        iboolean_ro = self.nodemap.GetNode("TestBoolRO")

        p_empty = pylon.BooleanParameter()
        p = pylon.BooleanParameter(iboolean_rw)

        self.assertTrue(p.Equals(iboolean_rw))
        self.assertFalse(p.Equals(iboolean_ro))
        self.assertFalse(p_empty.Equals(iboolean_rw))

    # ------------------------------------------------------------------
    # IsValid / IsReadable / IsWritable / GetAccessMode
    # ------------------------------------------------------------------

    def test_boolean_parameter_is_valid(self):
        """IsValid reflects attachment state."""
        p = pylon.BooleanParameter()
        self.assertFalse(p.IsValid())
        p.Attach(self.nodemap, "TestBoolRW")
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    def test_boolean_parameter_is_readable_writable(self):
        """IsReadable / IsWritable reflect the access mode."""
        p_ro = pylon.BooleanParameter(self.nodemap, "TestBoolRO")
        self.assertTrue(p_ro.IsReadable())
        self.assertFalse(p_ro.IsWritable())

        p_wo = pylon.BooleanParameter(self.nodemap, "TestBoolWO")
        self.assertFalse(p_wo.IsReadable())
        self.assertTrue(p_wo.IsWritable())

        p_rw = pylon.BooleanParameter(self.nodemap, "TestBoolRW")
        self.assertTrue(p_rw.IsReadable())
        self.assertTrue(p_rw.IsWritable())

        p_unattached = pylon.BooleanParameter()
        self.assertFalse(p_unattached.IsReadable())
        self.assertFalse(p_unattached.IsWritable())

    def test_boolean_parameter_get_access_mode(self):
        """GetAccessMode returns the correct genicam constant."""
        self.assertEqual(genicam.RO, pylon.BooleanParameter(self.nodemap, "TestBoolRO").GetAccessMode())
        self.assertEqual(genicam.WO, pylon.BooleanParameter(self.nodemap, "TestBoolWO").GetAccessMode())
        self.assertEqual(genicam.RW, pylon.BooleanParameter(self.nodemap, "TestBoolRW").GetAccessMode())
        self.assertEqual(genicam.NI, pylon.BooleanParameter().GetAccessMode())

    # ------------------------------------------------------------------
    # Unattached – all value operations must raise
    # ------------------------------------------------------------------

    def test_boolean_parameter_unattached_raises(self):
        """All value access on unattached parameter raises."""
        p = pylon.BooleanParameter()
        with self.assertRaises(Exception): p.SetValue(True)
        with self.assertRaises(Exception): p.GetValue()

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def test_boolean_parameter_read(self):
        """GetValue returns the correct initial value.
        TestBoolRO has Value=1 (True), TestBoolRW has Value=0 (False)."""
        p_ro = pylon.BooleanParameter(self.nodemap, "TestBoolRO")
        self.assertIs(True, p_ro.GetValue())
        self.assertIs(True, p_ro.GetValue(False))
        self.assertIs(True, p_ro.GetValue(False, False))
        # Value property shortcut
        self.assertIs(True, p_ro.Value)

        p_rw = pylon.BooleanParameter(self.nodemap, "TestBoolRW")
        self.assertIs(False, p_rw.GetValue())

    def test_boolean_parameter_read_only_raises_on_write(self):
        """SetValue on a read-only parameter raises; value stays unchanged."""
        p_ro = pylon.BooleanParameter(self.nodemap, "TestBoolRO")
        with self.assertRaises(Exception):
            p_ro.SetValue(True)
        # Value remains True
        self.assertIs(True, p_ro.GetValue())

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def test_boolean_parameter_write(self):
        """SetValue / GetValue round-trip for RW parameter."""
        p_rw = pylon.BooleanParameter(self.nodemap, "TestBoolRW")
        initial = p_rw.GetValue()   # False

        # Invert the value
        p_rw.SetValue(not initial)
        self.assertEqual(not initial, p_rw.GetValue())

        # Invert back
        p_rw.SetValue(initial)
        self.assertEqual(initial, p_rw.GetValue())

    def test_boolean_parameter_write_prop(self):
        """Property Value round-trip for RW parameter."""
        p_rw = pylon.BooleanParameter(self.nodemap, "TestBoolRW")
        initial = p_rw.Value   # False

        # Invert the value
        p_rw.Value = not initial
        self.assertEqual(not initial, p_rw.Value)

        # Invert back
        p_rw.Value = initial
        self.assertEqual(initial, p_rw.Value)

    # ------------------------------------------------------------------
    # TrySetValue
    # ------------------------------------------------------------------

    def test_boolean_parameter_try_set_value_rw(self):
        """TrySetValue returns True and sets the value on writable parameter."""
        p_rw = pylon.BooleanParameter(self.nodemap, "TestBoolRW")

        self.assertTrue(p_rw.TrySetValue(True))
        self.assertTrue(p_rw.TrySetValue(False))
        self.assertIs(False, p_rw.GetValue())

    def test_boolean_parameter_try_set_value_ro_returns_false(self):
        """TrySetValue on a read-only parameter returns False without raising;
        value stays unchanged."""
        p_ro = pylon.BooleanParameter(self.nodemap, "TestBoolRO")
        self.assertFalse(p_ro.TrySetValue(True))
        self.assertFalse(p_ro.TrySetValue(False))
        # Value must remain unchanged
        self.assertIs(True, p_ro.GetValue())

    # ------------------------------------------------------------------
    # GetValueOrDefault
    # ------------------------------------------------------------------

    def test_boolean_parameter_get_value_or_default_wo(self):
        """GetValueOrDefault returns the default value for a write-only parameter."""
        p_wo = pylon.BooleanParameter(self.nodemap, "TestBoolWO")
        self.assertFalse(p_wo.IsReadable())
        self.assertTrue(p_wo.IsWritable())
        self.assertIs(True, p_wo.GetValueOrDefault(True))

    def test_boolean_parameter_get_value_or_default_rw(self):
        """GetValueOrDefault returns the actual value for a readable parameter."""
        p_rw = pylon.BooleanParameter(self.nodemap, "TestBoolRW")
        # TestBoolRW initial value is False; default True must not be returned
        self.assertIs(False, p_rw.GetValueOrDefault(True))

    # ------------------------------------------------------------------
    # ToString / FromString
    # ------------------------------------------------------------------

    def test_boolean_parameter_to_string(self):
        """ToString returns '0' for False and '1' for True."""
        p_rw = pylon.BooleanParameter(self.nodemap, "TestBoolRW")

        p_rw.SetValue(False)
        self.assertEqual("0", p_rw.ToString())

        p_rw.SetValue(True)
        self.assertEqual("1", p_rw.ToString())

        p_rw.SetValue(False, False)
        self.assertEqual("0", p_rw.ToString())

    def test_boolean_parameter_to_string_wo_raises(self):
        """ToString on a write-only parameter raises."""
        p_wo = pylon.BooleanParameter(self.nodemap, "TestBoolWO")
        with self.assertRaises(Exception):
            p_wo.ToString()

    def test_boolean_parameter_to_string_not_found_raises(self):
        """ToString on a parameter attached to a non-existent node raises."""
        p = pylon.BooleanParameter(self.nodemap, "TestBoolNotFound")
        self.assertFalse(p.IsValid())
        with self.assertRaises(Exception):
            p.ToString()

    def test_boolean_parameter_to_string_unattached_raises(self):
        """ToString on unattached parameter raises."""
        p = pylon.BooleanParameter()
        with self.assertRaises(Exception):
            p.ToString()

    def test_boolean_parameter_from_string(self):
        """FromString parses 'true'/'false' (and as prefixes) and sets the value."""
        p_rw = pylon.BooleanParameter(self.nodemap, "TestBoolRW")

        # Valid: exact strings
        p_rw.FromString("true")
        self.assertIs(True, p_rw.GetValue())

        p_rw.FromString("false")
        self.assertIs(False, p_rw.GetValue())

        # Valid: true/false as prefix of longer string
        p_rw.FromString("true1")
        self.assertIs(True, p_rw.GetValue())

        p_rw.FromString("false2")
        self.assertIs(False, p_rw.GetValue())

        # Invalid string raises
        with self.assertRaises(Exception):
            p_rw.FromString("Test")

        p_rw.SetValue(True )
        self.assertIs(True, p_rw.GetValue())

        p_rw.SetValue(False)
        self.assertIs(False, p_rw.GetValue())

    def test_boolean_parameter_from_string_ro_raises(self):
        """FromString on RO parameter raises; value unchanged."""
        p_ro = pylon.BooleanParameter(self.nodemap, "TestBoolRO")
        with self.assertRaises(Exception):
            p_ro.FromString("false")
        # Value must remain True
        self.assertIs(True, p_ro.GetValue())

    def test_boolean_parameter_from_string_wo_does_not_raise(self):
        """FromString on WO parameter does not raise."""
        p_wo = pylon.BooleanParameter(self.nodemap, "TestBoolWO")
        p_wo.FromString("true")  # must not raise


    def test_boolean_parameter_from_string_case_insensitive(self):
        """FromString is case-insensitive for all recognised aliases."""
        p_rw = pylon.BooleanParameter(self.nodemap, "TestBoolRW")

        for truthy in ("TRUE", "True"):
            p_rw.FromString(truthy)
            self.assertIs(True, p_rw.GetValue(), msg=f"Expected True for '{truthy}'")

        for falsy in ("FALSE", "False"):
            p_rw.FromString(falsy)
            self.assertIs(False, p_rw.GetValue(), msg=f"Expected False for '{falsy}'")

    def test_boolean_parameter_from_string_whitespace_stripped(self):
        """FromString strips leading/trailing whitespace before matching."""
        p_rw = pylon.BooleanParameter(self.nodemap, "TestBoolRW")

        for truthy in ("  true  ", "True  "):
            p_rw.FromString(truthy)
            self.assertIs(True, p_rw.GetValue(), msg=f"Expected True for {truthy!r}")

        for falsy in ("  false  ", "  False"):
            p_rw.FromString(falsy)
            self.assertIs(False, p_rw.GetValue(), msg=f"Expected False for {falsy!r}")

    def test_boolean_parameter_from_string_with_verify_false(self):
        """FromString accepts an explicit Verify=False second argument."""
        p_rw = pylon.BooleanParameter(self.nodemap, "TestBoolRW")

        p_rw.FromString("true", False)
        self.assertIs(True, p_rw.GetValue())

        p_rw.FromString("false", False)
        self.assertIs(False, p_rw.GetValue())


    def test_boolean_parameter_from_string_unattached_raises(self):
        """FromString on an unattached BooleanParameter raises."""
        p = pylon.BooleanParameter()
        self.assertFalse(p.IsValid())
        with self.assertRaises(Exception):
            p.FromString("true")

    def test_boolean_parameter_from_string_normalization_not_applied_to_non_boolean(self):
        """The boolean alias normalization in FromString must not affect
        non-boolean parameters (e.g. IntegerParameter)."""
        p_int = pylon.IntegerParameter(self.nodemap, "TestInt2")
        self.assertTrue(p_int.IsValid())

        # "1" must be forwarded as-is to the C++ integer layer and succeed
        p_int.FromString("1")
        self.assertEqual(1, p_int.GetValue())

        # "true" / "on" are not valid integer strings and must raise
        with self.assertRaises(Exception):
            p_int.FromString("true")

    # ------------------------------------------------------------------
    # ToStringOrDefault / __str__
    # ------------------------------------------------------------------

    def test_boolean_parameter_to_string_or_default(self):
        """ToStringOrDefault returns the value string or the default."""
        p_unattached = pylon.BooleanParameter()
        self.assertEqual("default", p_unattached.ToStringOrDefault("default"))

        p_ro = pylon.BooleanParameter(self.nodemap, "TestBoolRO")
        self.assertEqual("1", p_ro.ToStringOrDefault("default"))

        p_wo = pylon.BooleanParameter(self.nodemap, "TestBoolWO")
        self.assertEqual("default", p_wo.ToStringOrDefault("default"))

    def test_boolean_parameter_str(self):
        """__str__ returns 'False'/'True', '<not found>', or '<not readable>'."""
        self.assertEqual("<not found>",    str(pylon.BooleanParameter()))
        self.assertEqual("<not readable>", str(pylon.BooleanParameter(self.nodemap, "TestBoolWO")))

        p_rw = pylon.BooleanParameter(self.nodemap, "TestBoolRW")
        p_rw.SetValue(False)
        self.assertEqual("False", str(p_rw))
        p_rw.SetValue(True)
        self.assertEqual("True", str(p_rw))

    # ------------------------------------------------------------------
    # GetNode / IsValueCacheValid
    # ------------------------------------------------------------------

    def test_boolean_parameter_get_node(self):
        """GetNode returns the attached node; unattached raises."""
        node = self.getINode("TestBoolRW")
        p = pylon.BooleanParameter(node)
        self.assertEqual(node.GetName(), p.GetNode().GetName())
        self.assertEqual(node.GetName(), p.Node.GetName())
        self.assertIsInstance(p.GetNode(), genicam.INode)

        p.Release()
        with self.assertRaises(Exception):
            p.GetNode()

    def test_boolean_parameter_is_value_cache_valid(self):
        """IsValueCacheValid is callable on an attached parameter."""
        p = pylon.BooleanParameter(self.nodemap, "TestBoolRW")
        self.assertIsInstance(p.IsValueCacheValid(), bool)

    # ------------------------------------------------------------------
    # Compatibility with genicam
    # ------------------------------------------------------------------

    def test_genicam_compatibility(self):
        """Parameter can be used wherever genicam interfaces are expected."""
        p = pylon.BooleanParameter(self.nodemap, "TestBoolRW")
        self.assertIsInstance(p, genicam.IBoolean)
        self.assertIsInstance(p, genicam.IValue)
        self.assertTrue(genicam.IsReadable(p))
        self.assertTrue(genicam.IsWritable(p))

    def test_python_representation_to_boolean_parameter(self):
        """BooleanParameter interoperates predictably with common Python value representations."""
        p = pylon.BooleanParameter(self.nodemap, "TestBoolRW")

        # --- Native bools (current happy path) ---
        p.Value = True
        self.assertIs(p.GetValue(), True)
        self.assertIs(p.Value, True)

        p.Value = False
        self.assertIs(p.GetValue(), False)
        self.assertIs(p.Value, False)

        # --- Rejected numeric representations (contract: only bool accepted) ---
        with self.assertRaises(Exception):
            p.Value = 1
        with self.assertRaises(Exception):
            p.Value = 0

        # --- String representations should not be silently accepted via Value assignment ---
        # (String parsing belongs to FromString, tested elsewhere.)
        for invalid in ("true", "false", "1", "0", " yes ", ""):
            with self.assertRaises(Exception):
                p.Value = invalid

        # --- Non-boolean Python objects should raise ---
        for invalid in (None, [], {}, object()):
            with self.assertRaises(Exception):
                p.Value = invalid


if __name__ == "__main__":
    unittest.main()
