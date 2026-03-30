from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest


class FloatParameterTestSuite(PylonParameterTestCase):

    # ------------------------------------------------------------------
    # Construction / Attach / Release
    # ------------------------------------------------------------------

    def test_float_parameter_construction_default(self):
        """Default construction produces an invalid parameter."""
        p = pylon.FloatParameter()
        self.assertFalse(p.IsValid())

    def test_float_parameter_construction_from_inode(self):
        """Construction from a matching INode attaches and validates;
        a wrong node type yields an invalid parameter."""
        node = self.getINode("TestFloatRW")
        p = pylon.FloatParameter(node)
        self.assertTrue(p.IsValid())

        node_int = self.getINode("TestInt")
        p_bad = pylon.FloatParameter(node_int)
        self.assertFalse(p_bad.IsValid())

    def test_float_parameter_construction_from_ifloat(self):
        """Construction from a GenApi IFloat object attaches and validates."""
        ifloat = self.nodemap.GetNode("TestFloatRW")
        p = pylon.FloatParameter(ifloat)
        self.assertTrue(p.IsValid())

    def test_float_parameter_construction_from_nodemap_name(self):
        """Construction from nodemap + name attaches and validates."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(self.getINode("TestFloatRW")))
        self.assertFalse(p.Equals(self.getINode("TestFloatRO")))

    def test_float_parameter_construction_from_nonexistent_name(self):
        """Construction from nodemap + non-existent name produces an invalid parameter."""
        p = pylon.FloatParameter(self.nodemap, "TestEmpty")
        self.assertFalse(p.IsValid())

    def test_float_parameter_construction_copy(self):
        """Copy construction produces a valid, equal parameter."""
        p1 = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        p2 = pylon.FloatParameter(p1)
        self.assertTrue(p1.IsValid())
        self.assertTrue(p2.IsValid())
        self.assertTrue(p1.Equals(p2))

    def test_float_parameter_attach_from_inode(self):
        """Attach from INode sets validity and correct node."""
        node_a = self.getINode("TestFloatRW")
        node_b = self.getINode("TestFloatRO")

        p = pylon.FloatParameter()
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

    def test_float_parameter_attach_from_ifloat(self):
        """Attach from GenApi IFloat attaches correctly."""
        ifloat = self.nodemap.GetNode("TestFloatRW")
        p = pylon.FloatParameter()
        result = p.Attach(ifloat)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

    def test_float_parameter_attach_from_nodemap_name(self):
        """Attach from nodemap + name; non-existent name returns False."""
        p = pylon.FloatParameter()

        result = p.Attach(self.nodemap, "TestFloatRW")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "TestFloatRO")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "NonExistent")
        self.assertFalse(result)

    def test_float_parameter_release(self):
        """Release makes parameter invalid."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    # ------------------------------------------------------------------
    # Equals
    # ------------------------------------------------------------------

    def test_float_parameter_equals_parameter(self):
        """Equals between two FloatParameters."""
        node_a = self.nodemap.GetNode("TestFloatRW")
        node_b = self.nodemap.GetNode("TestFloatRO")

        p1 = pylon.FloatParameter(node_a)
        p2 = pylon.FloatParameter(node_a)
        p3 = pylon.FloatParameter(node_b)
        p_empty1 = pylon.FloatParameter()
        p_empty2 = pylon.FloatParameter()

        self.assertTrue(p_empty1.Equals(p_empty2))
        self.assertTrue(p1.Equals(p2))
        self.assertTrue(p2.Equals(p1))
        self.assertFalse(p1.Equals(p3))
        self.assertFalse(p3.Equals(p1))
        self.assertFalse(p1.Equals(p_empty1))
        self.assertFalse(p_empty1.Equals(p1))

    def test_float_parameter_equals_inode(self):
        """Equals against INode and None."""
        node_a = self.getINode("TestFloatRW")
        node_b = self.getINode("TestFloatRO")

        p_empty = pylon.FloatParameter()
        p = pylon.FloatParameter(node_a)

        self.assertTrue(p_empty.Equals(None))
        self.assertFalse(p_empty.Equals(node_a))
        self.assertTrue(p.Equals(node_a))
        self.assertFalse(p.Equals(node_b))
        self.assertFalse(p.Equals(None))

    def test_float_parameter_equals_ifloat(self):
        """Equals against a GenApi IFloat node."""
        ifloat_rw = self.nodemap.GetNode("TestFloatRW")
        ifloat_ro = self.nodemap.GetNode("TestFloatRO")

        p_empty = pylon.FloatParameter()
        p = pylon.FloatParameter(ifloat_rw)

        self.assertTrue(p.Equals(ifloat_rw))
        self.assertFalse(p.Equals(ifloat_ro))
        self.assertFalse(p_empty.Equals(ifloat_rw))

    # ------------------------------------------------------------------
    # IsValid / IsReadable / IsWritable / GetAccessMode
    # ------------------------------------------------------------------

    def test_float_parameter_is_valid(self):
        """IsValid reflects attachment state."""
        p = pylon.FloatParameter()
        self.assertFalse(p.IsValid())
        p.Attach(self.nodemap, "TestFloatRW")
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    def test_float_parameter_is_readable_writable(self):
        """IsReadable / IsWritable reflect the access mode."""
        p_ro = pylon.FloatParameter(self.nodemap, "TestFloatRO")
        self.assertTrue(p_ro.IsReadable())
        self.assertFalse(p_ro.IsWritable())

        p_wo = pylon.FloatParameter(self.nodemap, "TestFloatWO")
        self.assertFalse(p_wo.IsReadable())
        self.assertTrue(p_wo.IsWritable())

        p_rw = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        self.assertTrue(p_rw.IsReadable())
        self.assertTrue(p_rw.IsWritable())

        p_unattached = pylon.FloatParameter()
        self.assertFalse(p_unattached.IsReadable())
        self.assertFalse(p_unattached.IsWritable())

    def test_float_parameter_get_access_mode(self):
        """GetAccessMode returns the correct genicam constant."""
        self.assertEqual(genicam.RO, pylon.FloatParameter(self.nodemap, "TestFloatRO").GetAccessMode())
        self.assertEqual(genicam.WO, pylon.FloatParameter(self.nodemap, "TestFloatWO").GetAccessMode())
        self.assertEqual(genicam.RW, pylon.FloatParameter(self.nodemap, "TestFloatRW").GetAccessMode())
        self.assertEqual(genicam.NI, pylon.FloatParameter().GetAccessMode())

    # ------------------------------------------------------------------
    # Unattached – all value operations must raise
    # ------------------------------------------------------------------

    def test_float_parameter_unattached_raises(self):
        """All value/property access on unattached parameter raises."""
        p = pylon.FloatParameter()
        with self.assertRaises(Exception): p.SetValue(1000.0)
        with self.assertRaises(Exception): p.GetValue()
        with self.assertRaises(Exception): p.GetMin()
        with self.assertRaises(Exception): p.GetMax()
        with self.assertRaises(Exception): p.HasInc()
        with self.assertRaises(Exception): p.GetIncMode()
        with self.assertRaises(Exception): p.GetInc()
        with self.assertRaises(Exception): p.GetListOfValidValues()
        with self.assertRaises(Exception): p.GetRepresentation()
        with self.assertRaises(Exception): p.GetUnit()
        with self.assertRaises(Exception): p.GetDisplayNotation()
        with self.assertRaises(Exception): p.GetDisplayPrecision()
        with self.assertRaises(Exception): p.ImposeMin(1000.0)
        with self.assertRaises(Exception): p.ImposeMax(1020.0)

    def test_float_parameter_nonexistent_node_raises(self):
        """Parameter attached to a non-existent node raises on value access."""
        p = pylon.FloatParameter(self.nodemap, "TestEmpty")
        self.assertFalse(p.IsValid())
        with self.assertRaises(Exception): p.GetValue()
        with self.assertRaises(Exception): p.SetValue(1234.0)
        with self.assertRaises(Exception): p.GetInc()
        with self.assertRaises(Exception): p.ToString()
        self.assertEqual(1999.0, p.GetValueOrDefault(1999.0))
        self.assertFalse(p.TrySetValue(1234.0))

    # ------------------------------------------------------------------
    # Simple read
    # ------------------------------------------------------------------

    def test_float_parameter_simple_read(self):
        """GetValue, GetMin, GetMax, GetValueOrDefault, GetValuePercentOfRange."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")

        # TestFloatRW: Value=1250, Min=1000, Max=2000, Inc=2
        self.assertEqual(1250.0, p.GetValue())
        self.assertEqual(1250.0, p.GetValue(False))
        self.assertEqual(1250.0, p.GetValue(False, False))
        self.assertEqual(1000.0, p.GetMin())
        self.assertEqual(2000.0, p.GetMax())
        self.assertEqual(1250.0, p.GetValueOrDefault(9999.0))
        # (1250 - 1000) / (2000 - 1000) * 100 = 25 %
        self.assertEqual(25.0, p.GetValuePercentOfRange())

        # property shortcuts
        self.assertEqual(1250.0, p.Value)
        self.assertEqual(1000.0, p.Min)
        self.assertEqual(2000.0, p.Max)
        self.assertEqual(25.0,   p.ValuePercentOfRange)
        p.ValuePercentOfRange = 50.0
        self.assertEqual(1500.0, p.Value)

    def test_float_parameter_inc_mode_and_inc(self):
        """HasInc / GetIncMode / GetInc for node with and without increment."""
        p_rw = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        self.assertTrue(p_rw.HasInc())
        self.assertEqual(genicam.fixedIncrement, p_rw.GetIncMode())
        self.assertEqual(2.0, p_rw.GetInc())
        self.assertEqual(genicam.fixedIncrement, p_rw.IncMode)
        self.assertEqual(2.0, p_rw.Inc)

        # TestFloatRO has no Inc tag → HasInc returns False, GetInc raises
        p_ro = pylon.FloatParameter(self.nodemap, "TestFloatRO")
        self.assertFalse(p_ro.HasInc())
        with self.assertRaises(Exception): p_ro.GetInc()

    def test_float_parameter_list_of_valid_values(self):
        """GetListOfValidValues returns a tuple of doubles for a fixed-increment node."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")

        # fixedIncrement node → empty list (bounded=True, the default)
        vals = p.GetListOfValidValues()
        self.assertIsInstance(vals, tuple)
        self.assertEqual(0, len(vals))

        # bounded=False variant
        vals_unbounded = p.GetListOfValidValues(False)
        self.assertIsInstance(vals_unbounded, tuple)
        self.assertEqual(0, len(vals_unbounded))

        # property shortcut agrees
        vals_prop = p.ListOfValidValues
        self.assertIsInstance(vals_prop, tuple)
        self.assertEqual(len(vals), len(vals_prop))

        # all elements are floats when the tuple is non-empty
        for v in vals:
            self.assertIsInstance(v, float)

    def test_float_parameter_unit_and_representation(self):
        """GetUnit and GetRepresentation return expected values."""
        # TestFloat has unit="eggs"
        p = pylon.FloatParameter(self.nodemap, "TestFloat")
        self.assertEqual("eggs", p.GetUnit())
        self.assertEqual("eggs", p.Unit)

        # TestFloat2 (Converter) has Representation=Linear
        p2 = pylon.FloatParameter(self.nodemap, "TestFloat2")
        self.assertEqual(genicam.Linear, p2.GetRepresentation())
        self.assertEqual(genicam.Linear, p2.Representation)

    def test_float_parameter_display_notation_and_precision(self):
        """GetDisplayNotation and GetDisplayPrecision are callable."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        notation = p.GetDisplayNotation()
        self.assertIn(notation, (genicam.fnAutomatic, genicam.fnFixed, genicam.fnScientific))
        self.assertEqual(notation, p.DisplayNotation)
        precision = p.GetDisplayPrecision()
        self.assertIsInstance(precision, int)
        self.assertEqual(precision, p.DisplayPrecision)

    # ------------------------------------------------------------------
    # Simple write
    # ------------------------------------------------------------------

    def test_float_parameter_simple_write(self):
        """SetValue / GetValue round-trip."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        p.SetValue(1000.0)
        self.assertEqual(1000.0, p.GetValue())
        p.SetValue(1001.0, False)
        self.assertEqual(1001.0, p.GetValue())

    def test_float_parameter_simple_write_prop(self):
        """Property Value round-trip for RW parameter."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        p.Value = 1000.0
        self.assertEqual(1000.0, p.Value)
        p.Value = 1001.0
        self.assertEqual(1001.0, p.Value)

    def test_float_parameter_write_ro_raises(self):
        """SetValue on a read-only parameter raises."""
        p_ro = pylon.FloatParameter(self.nodemap, "TestFloatRO")
        with self.assertRaises(Exception):
            p_ro.SetValue(1000.0)
        self.assertEqual(1234.5, p_ro.GetValue())

    def test_float_parameter_set_to_maximum(self):
        """SetToMaximum / TrySetToMaximum."""
        p_rw = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        max_val = p_rw.GetMax()

        p_rw.SetToMaximum()
        self.assertEqual(max_val, p_rw.GetValue())

        p_rw.SetValue(1002.0)
        self.assertTrue(p_rw.TrySetToMaximum())
        self.assertEqual(max_val, p_rw.GetValue())

        # TrySetToMaximum on RO returns False, value unchanged
        p_ro = pylon.FloatParameter(self.nodemap, "TestFloatRO")
        self.assertFalse(p_ro.TrySetToMaximum())
        self.assertEqual(1234.5, p_ro.GetValue())

    def test_float_parameter_set_to_minimum(self):
        """SetToMinimum / TrySetToMinimum."""
        p_rw = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        min_val = p_rw.GetMin()

        p_rw.SetToMinimum()
        self.assertEqual(min_val, p_rw.GetValue())

        p_rw.SetValue(1003.0)
        self.assertTrue(p_rw.TrySetToMinimum())
        self.assertEqual(min_val, p_rw.GetValue())

        # TrySetToMinimum on RO returns False, value unchanged
        p_ro = pylon.FloatParameter(self.nodemap, "TestFloatRO")
        self.assertFalse(p_ro.TrySetToMinimum())
        self.assertEqual(1234.5, p_ro.GetValue())

    def test_float_parameter_set_value_percent_of_range(self):
        """SetValuePercentOfRange and TrySetValuePercentOfRange."""
        p_rw = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        min_val = p_rw.GetMin()   # 1000
        max_val = p_rw.GetMax()   # 2000

        # 50 % → 1500
        p_rw.SetValuePercentOfRange(50.0)
        self.assertEqual(min_val + (max_val - min_val) * 0.5, p_rw.GetValue())

        # TrySetValuePercentOfRange on writable → True, correct value
        p_rw.SetValue(1004.0)
        self.assertTrue(p_rw.TrySetValuePercentOfRange(42.0))
        self.assertEqual(1420.0, p_rw.GetValue())

        # TrySetValuePercentOfRange on RO → False, value unchanged
        p_ro = pylon.FloatParameter(self.nodemap, "TestFloatRO")
        self.assertFalse(p_ro.TrySetValuePercentOfRange(42.0))
        self.assertEqual(1234.5, p_ro.GetValue())

        # Out-of-range percent is clipped: >100 → max, <0 → min
        p_rw.SetValuePercentOfRange(300.0)
        self.assertEqual(max_val, p_rw.GetValue())
        p_rw.SetValuePercentOfRange(-50.0)
        self.assertEqual(min_val, p_rw.GetValue())

    # ------------------------------------------------------------------
    # Out-of-range writes
    # ------------------------------------------------------------------

    def test_float_parameter_write_out_of_range_raises(self):
        """SetValue with out-of-range value raises; value stays unchanged."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        old_val = p.GetValue()
        min_val = p.GetMin()   # 1000
        max_val = p.GetMax()   # 2000

        with self.assertRaises(Exception): p.SetValue(min_val - 1.0)
        self.assertEqual(old_val, p.GetValue())

        with self.assertRaises(Exception): p.SetValue(max_val + 1.0)
        self.assertEqual(old_val, p.GetValue())

        with self.assertRaises(Exception): p.SetValue(min_val - 1.0, pylon.FloatValueCorrection_None)
        self.assertEqual(old_val, p.GetValue())

        with self.assertRaises(Exception): p.SetValue(max_val + 1.0, pylon.FloatValueCorrection_None)
        self.assertEqual(old_val, p.GetValue())

    def test_float_parameter_write_with_clip_correction(self):
        """SetValue with FloatValueCorrection_ClipToRange clips to min/max."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        min_val = p.GetMin()   # 1000
        max_val = p.GetMax()   # 2000

        p.SetValue(min_val - 1.0, pylon.FloatValueCorrection_ClipToRange)
        self.assertEqual(min_val, p.GetValue())

        p.SetValue(max_val + 1.0, pylon.FloatValueCorrection_ClipToRange)
        self.assertEqual(max_val, p.GetValue())

    # ------------------------------------------------------------------
    # TrySetValue
    # ------------------------------------------------------------------

    def test_float_parameter_try_set_value_rw(self):
        """TrySetValue(value) returns True and sets the value on writable parameter."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")

        self.assertTrue(p.TrySetValue(1001.0))
        self.assertEqual(1001.0, p.GetValue())

        self.assertTrue(p.TrySetValue(1002.0, pylon.FloatValueCorrection_None))
        self.assertEqual(1002.0, p.GetValue())

        self.assertTrue(p.TrySetValue(1003.0, pylon.FloatValueCorrection_ClipToRange))
        self.assertEqual(1003.0, p.GetValue())

    def test_float_parameter_try_set_value_out_of_range(self):
        """TrySetValue with value below min raises; with ClipToRange clips."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        p.SetValue(1003.0)

        # Below min without correction → raises, value unchanged
        with self.assertRaises(Exception): p.TrySetValue(999.0)
        self.assertEqual(1003.0, p.GetValue())

        with self.assertRaises(Exception): p.TrySetValue(999.0, pylon.FloatValueCorrection_None)
        self.assertEqual(1003.0, p.GetValue())

        # With clip correction → succeeds, clipped to min/max
        self.assertTrue(p.TrySetValue(999.0, pylon.FloatValueCorrection_ClipToRange))
        self.assertEqual(1000.0, p.GetValue())

        self.assertTrue(p.TrySetValue(2999.0, pylon.FloatValueCorrection_ClipToRange))
        self.assertEqual(2000.0, p.GetValue())

    def test_float_parameter_try_set_value_ro_returns_false(self):
        """TrySetValue on a read-only parameter returns False without raising."""
        p_ro = pylon.FloatParameter(self.nodemap, "TestFloatRO")
        self.assertFalse(p_ro.TrySetValue(1010.0))
        self.assertEqual(1234.5, p_ro.GetValue())

        self.assertFalse(p_ro.TrySetValue(1010.0, pylon.FloatValueCorrection_ClipToRange))
        self.assertEqual(1234.5, p_ro.GetValue())

    # ------------------------------------------------------------------
    # GetValueOrDefault
    # ------------------------------------------------------------------

    def test_float_parameter_get_value_or_default_readable(self):
        """GetValueOrDefault returns the actual value for a readable parameter."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        self.assertEqual(p.GetValue(), p.GetValueOrDefault(9999.0))

    def test_float_parameter_get_value_or_default_wo(self):
        """GetValueOrDefault returns the default for a write-only parameter."""
        p_wo = pylon.FloatParameter(self.nodemap, "TestFloatWO")
        self.assertFalse(p_wo.IsReadable())
        self.assertTrue(p_wo.IsWritable())
        self.assertEqual(1400.5, p_wo.GetValueOrDefault(1400.5))

    # ------------------------------------------------------------------
    # ImposeMin / ImposeMax
    # ------------------------------------------------------------------

    def test_float_parameter_impose_min_max(self):
        """ImposeMin / ImposeMax narrow the effective range."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        orig_min = p.GetMin()   # 1000
        orig_max = p.GetMax()   # 2000

        p.ImposeMin(orig_min + 1.0)
        p.ImposeMax(orig_max - 1.0)
        self.assertEqual(orig_min + 1.0, p.GetMin())
        self.assertEqual(orig_max - 1.0, p.GetMax())

        # Restore
        p.ImposeMin(orig_min)
        p.ImposeMax(orig_max)
        self.assertEqual(orig_min, p.GetMin())
        self.assertEqual(orig_max, p.GetMax())

    # ------------------------------------------------------------------
    # ToString / FromString
    # ------------------------------------------------------------------

    def test_float_parameter_to_string(self):
        """ToString returns the current value as a string."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        p.SetValue(1250.0)
        self.assertIsInstance(p.ToString(), str)

    def test_float_parameter_to_string_unattached_raises(self):
        """ToString on unattached parameter raises."""
        p = pylon.FloatParameter()
        with self.assertRaises(Exception): p.ToString()

    def test_float_parameter_from_string(self):
        """FromString parses and sets the value."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")

        p.FromString("1003")
        self.assertEqual(1003.0, p.GetValue())

        p.FromString("1023.23")
        self.assertAlmostEqual(1023.23, p.GetValue(), places=10)

        p.FromString("1004.2E0")
        self.assertAlmostEqual(1004.2, p.GetValue(), places=10)

        # Invalid string raises
        with self.assertRaises(Exception): p.FromString("abc1003")

    def test_float_parameter_from_string_ro_raises(self):
        """FromString on RO parameter raises; WO does not raise."""
        p_ro = pylon.FloatParameter(self.nodemap, "TestFloatRO")
        with self.assertRaises(Exception): p_ro.FromString("1234")

        p_wo = pylon.FloatParameter(self.nodemap, "TestFloatWO")
        p_wo.FromString("1234")   # must not raise

    # ------------------------------------------------------------------
    # ToStringOrDefault / __str__
    # ------------------------------------------------------------------

    def test_float_parameter_to_string_or_default(self):
        """ToStringOrDefault returns value string or default."""
        p_unattached = pylon.FloatParameter()
        self.assertEqual("default", p_unattached.ToStringOrDefault("default"))

        p_ro = pylon.FloatParameter(self.nodemap, "TestFloatRO")
        self.assertNotEqual("default", p_ro.ToStringOrDefault("default"))

        p_wo = pylon.FloatParameter(self.nodemap, "TestFloatWO")
        self.assertEqual("default", p_wo.ToStringOrDefault("default"))

    def test_float_parameter_str(self):
        """__str__ returns value, '<not found>', or '<not readable>'."""
        self.assertEqual("<not found>",    str(pylon.FloatParameter()))
        self.assertEqual("<not readable>", str(pylon.FloatParameter(self.nodemap, "TestFloatWO")))
        p_ro = pylon.FloatParameter(self.nodemap, "TestFloatRO")
        self.assertNotEqual("<not found>",    str(p_ro))
        self.assertNotEqual("<not readable>", str(p_ro))

    # ------------------------------------------------------------------
    # GetNode / IsValueCacheValid
    # ------------------------------------------------------------------

    def test_float_parameter_get_node(self):
        """GetNode returns the attached node; unattached raises."""
        node = self.getINode("TestFloatRW")
        p = pylon.FloatParameter(node)
        self.assertEqual(node.GetName(), p.GetNode().GetName())
        self.assertEqual(node.GetName(), p.Node.GetName())

        p.Release()
        with self.assertRaises(Exception): p.GetNode()

    def test_float_parameter_is_value_cache_valid(self):
        """IsValueCacheValid is callable on an attached parameter."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        self.assertIsInstance(p.IsValueCacheValid(), bool)

    # ------------------------------------------------------------------
    # GetAlternativeIntegerRepresentation
    # ------------------------------------------------------------------

    def test_float_parameter_get_alternative_integer_representation_with_alias(self):
        """GetAlternativeIntegerRepresentation returns a valid IntegerParameter when an alias exists."""
        # TestFloat2 (Converter) has pAlias → TestInt2
        p_float = pylon.FloatParameter(self.nodemap, "TestFloat2")
        self.assertTrue(p_float.IsValid())

        int_param = p_float.GetAlternativeIntegerRepresentation()

        self.assertIsInstance(int_param, pylon.IntegerParameter)
        self.assertTrue(int_param.IsValid())
        self.assertEqual("TestInt2", int_param.GetNode().GetName())
        self.assertEqual(1234, int_param.GetValue())

    def test_float_parameter_get_alternative_integer_representation_without_alias(self):
        """GetAlternativeIntegerRepresentation returns an invalid IntegerParameter when no alias exists."""
        # TestFloat has no pAlias
        p_float = pylon.FloatParameter(self.nodemap, "TestFloat")
        self.assertTrue(p_float.IsValid())

        int_param = p_float.GetAlternativeIntegerRepresentation()

        self.assertIsInstance(int_param, pylon.IntegerParameter)
        self.assertFalse(int_param.IsValid())

    # ------------------------------------------------------------------
    # ValuePercentOfRange property
    # ------------------------------------------------------------------

    def test_float_parameter_value_percent_of_range_property(self):
        """ValuePercentOfRange property matches GetValuePercentOfRange()."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        self.assertEqual(p.GetValuePercentOfRange(), p.ValuePercentOfRange)

    # ------------------------------------------------------------------
    # Compatibility with genicam
    # ------------------------------------------------------------------

    def test_genicam_compatibility(self):
        """Parameter can be used wherever genicam interfaces are expected."""
        p = pylon.FloatParameter(self.nodemap, "TestFloatRW")
        self.assertIsInstance(p, genicam.IFloat)
        self.assertIsInstance(p, genicam.IValue)
        self.assertTrue(genicam.IsReadable(p))
        self.assertTrue(genicam.IsWritable(p))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
