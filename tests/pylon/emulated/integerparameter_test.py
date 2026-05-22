from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest

class IntegerParameterTestSuite(PylonParameterTestCase):

    # ------------------------------------------------------------------
    # Construction / Attach / Release
    # ------------------------------------------------------------------

    def test_integer_parameter_construction_default(self):
        """Default construction produces an invalid parameter."""
        p = pylon.IntegerParameter()
        self.assertFalse(p.IsValid())

    def test_integer_parameter_construction_from_inode(self):
        """Construction from INode attaches and validates."""
        node = self.getINode("TestInt")
        p = pylon.IntegerParameter(node)
        self.assertTrue(p.IsValid())
        node = self.getINode("TestBoolRO")
        p = pylon.IntegerParameter(node)
        self.assertFalse(p.IsValid())

    def test_integer_parameter_construction_from_nodemap_name(self):
        """Construction from nodemap + name attaches and validates."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        self.assertTrue(p.IsValid())

    def test_integer_parameter_construction_copy(self):
        """Copy construction produces a valid, equal parameter."""
        p1 = pylon.IntegerParameter(self.nodemap, "TestInt")
        p2 = pylon.IntegerParameter(p1)
        self.assertTrue(p1.IsValid())
        self.assertTrue(p2.IsValid())
        self.assertTrue(p1.Equals(p2))

    def test_integer_parameter_attach_from_inode(self):
        """Attach from INode sets validity and correct node."""
        node_a = self.getINode("TestInt")
        node_b = self.getINode("TestIntRO")

        p = pylon.IntegerParameter()
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

    def test_integer_parameter_attach_from_nodemap_name(self):
        """Attach from nodemap + name; non-existent name returns False."""
        p = pylon.IntegerParameter()

        result = p.Attach(self.nodemap, "TestInt")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "TestIntRO")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "NonExistent")
        self.assertFalse(result)

    def test_integer_parameter_release(self):
        """Release makes parameter invalid."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    def test_integer_parameter_genicam_integer(self):
        """Can work with GenICam IInteger type."""
        integer = self.nodemap.GetNode("TestInt") #returns GenApi::IInteger python equivalent
        p = pylon.IntegerParameter(integer)
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())
        p.Attach(integer)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(integer))

    # ------------------------------------------------------------------
    # Equals
    # ------------------------------------------------------------------

    def test_integer_parameter_equals_parameter(self):
        """Equals between two IntegerParameters."""
        node_a = self.nodemap.GetNode("TestInt")
        node_b = self.nodemap.GetNode("TestIntRO")

        p1 = pylon.IntegerParameter(node_a)
        p2 = pylon.IntegerParameter(node_a)
        p3 = pylon.IntegerParameter(node_b)
        p_empty1 = pylon.IntegerParameter()
        p_empty2 = pylon.IntegerParameter()

        self.assertTrue(p_empty1.Equals(p_empty2))
        self.assertTrue(p1.Equals(p2))
        self.assertTrue(p2.Equals(p1))
        self.assertFalse(p1.Equals(p3))
        self.assertFalse(p1.Equals(p_empty1))
        self.assertFalse(p_empty1.Equals(p1))

    def test_integer_parameter_equals_inode(self):
        """Equals against INode and None."""
        node_a = self.getINode("TestInt")
        node_b = self.getINode("TestIntRO")

        p_empty = pylon.IntegerParameter()
        p = pylon.IntegerParameter(node_a)

        self.assertTrue(p_empty.Equals(None))
        self.assertFalse(p_empty.Equals(node_a))
        self.assertTrue(p.Equals(node_a))
        self.assertFalse(p.Equals(node_b))
        self.assertFalse(p.Equals(None))

    # ------------------------------------------------------------------
    # Unattached – all value operations must raise
    # ------------------------------------------------------------------

    def test_integer_parameter_unattached_raises(self):
        """All value/property access on unattached parameter raises."""
        p = pylon.IntegerParameter()
        with self.assertRaises(Exception): p.SetValue(1000)
        with self.assertRaises(Exception): p.GetValue()
        with self.assertRaises(Exception): p.GetMin()
        with self.assertRaises(Exception): p.GetMax()
        with self.assertRaises(Exception): p.GetIncMode()
        with self.assertRaises(Exception): p.GetInc()
        with self.assertRaises(Exception): p.GetListOfValidValues()
        with self.assertRaises(Exception): p.GetRepresentation()
        with self.assertRaises(Exception): p.GetUnit()
        with self.assertRaises(Exception): p.ImposeMin(1000)
        with self.assertRaises(Exception): p.ImposeMax(1020)

    # ------------------------------------------------------------------
    # Simple Read
    # ------------------------------------------------------------------

    def test_integer_parameter_simple_read(self):
        """Read initial value, min, max, inc and GetValueOrDefault."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")

        self.assertEqual(1500, p.GetValue())
        self.assertEqual(1500, p.GetValue(True))
        self.assertEqual(1500, p.GetValue(True, True))
        self.assertEqual(1000, p.GetMin())
        self.assertEqual(2000, p.GetMax())
        self.assertEqual(4,    p.GetInc())
        self.assertEqual(1500, p.Value)
        self.assertEqual(1000, p.Min)
        self.assertEqual(2000, p.Max)
        self.assertEqual(4,    p.Inc)
        self.assertEqual(genicam.fixedIncrement, p.GetIncMode())
        self.assertEqual(genicam.fixedIncrement, p.IncMode)
        self.assertEqual(1500, p.GetValueOrDefault(1))

    def test_integer_parameter_unit_and_representation(self):
        """GetUnit and GetRepresentation are callable on attached parameter."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        unit = p.GetUnit()
        self.assertIsInstance(unit, str)
        self.assertEqual("eggs", unit)
        self.assertEqual("eggs", p.Unit)
        rep = p.GetRepresentation()
        self.assertEqual(rep, genicam.PureNumber)
        self.assertEqual(p.Representation, genicam.PureNumber)

    def test_integer_parameter_list_of_valid_values(self):
        """GetListOfValidValues returns a sequence for a fixed-increment node."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        vals = p.GetListOfValidValues()
        self.assertIsInstance(vals, tuple)
        self.assertEqual(len(vals), 0)
        vals2 = p.ListOfValidValues
        self.assertIsInstance(vals2, tuple)
        self.assertEqual(len(vals2), 0)

    # ------------------------------------------------------------------
    # Simple Write
    # ------------------------------------------------------------------

    def test_integer_parameter_simple_write(self):
        """SetValue / GetValue round-trip for RW parameter."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        old_val = p.GetValue()
        min_val = p.GetMin()
        max_val = p.GetMax()

        p.SetValue(min_val, True)
        self.assertEqual(min_val, p.GetValue())

        p.SetValue(max_val)
        self.assertEqual(max_val, p.GetValue())

        p.SetValue(old_val)
        self.assertEqual(old_val, p.GetValue())

    def test_integer_parameter_simple_write_prop(self):
        """Property Value round-trip for RW parameter."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        old_val = p.Value
        min_val = p.Min
        max_val = p.Max

        p.Value = min_val
        self.assertEqual(min_val, p.Value)

        p.Value = max_val
        self.assertEqual(max_val, p.Value)

        p.Value = old_val
        self.assertEqual(old_val, p.Value)

    def test_integer_parameter_write_out_of_range_raises(self):
        """SetValue with out-of-range value raises OutOfRangeException."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        old_val = p.GetValue()

        with self.assertRaises(Exception):
            p.SetValue(p.GetMin() - 1)
        self.assertEqual(old_val, p.GetValue())

        with self.assertRaises(Exception):
            p.SetValue(p.GetMax() + 1)
        self.assertEqual(old_val, p.GetValue())

    # ------------------------------------------------------------------
    # GetValueOrDefault
    # ------------------------------------------------------------------

    def test_integer_parameter_get_value_or_default_write_only(self):
        """GetValueOrDefault returns default when parameter is write-only."""
        p = pylon.IntegerParameter(self.nodemap, "TestIntWO")
        self.assertTrue(p.IsWritable())
        self.assertFalse(p.IsReadable())
        self.assertEqual(1400, p.GetValueOrDefault(1400))

    def test_integer_parameter_get_value_or_default_unattached(self):
        """GetValueOrDefault returns default for unattached parameter."""
        p = pylon.IntegerParameter()
        self.assertEqual(1999, p.GetValueOrDefault(1999))

    # ------------------------------------------------------------------
    # ImposeMin / ImposeMax
    # ------------------------------------------------------------------

    def test_integer_parameter_impose_min_max(self):
        """ImposeMin/ImposeMax narrow the reported range."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        orig_min = p.GetMin()
        orig_max = p.GetMax()
        inc = p.GetInc()

        imposed_min = orig_min + inc
        imposed_max = orig_max - inc

        p.ImposeMin(imposed_min)
        p.ImposeMax(imposed_max)
        self.assertEqual(imposed_min, p.GetMin())
        self.assertEqual(imposed_max, p.GetMax())

        # Restore
        p.ImposeMin(orig_min)
        p.ImposeMax(orig_max)
        self.assertEqual(orig_min, p.GetMin())
        self.assertEqual(orig_max, p.GetMax())

    # ------------------------------------------------------------------
    # TrySetValue
    # ------------------------------------------------------------------

    def test_integer_parameter_try_set_value(self):
        """TrySetValue returns True for RW, False for RO."""
        p_rw = pylon.IntegerParameter(self.nodemap, "TestInt")
        p_ro = pylon.IntegerParameter(self.nodemap, "TestIntRO")

        self.assertTrue(p_rw.TrySetValue(1140))
        self.assertEqual(1140, p_rw.GetValue())

        self.assertFalse(p_ro.TrySetValue(1140))

    def test_integer_parameter_try_set_value_with_correction_none(self):
        """TrySetValue with IntegerValueCorrection_None on RW/RO."""
        p_rw = pylon.IntegerParameter(self.nodemap, "TestInt")
        p_ro = pylon.IntegerParameter(self.nodemap, "TestIntRO")

        self.assertTrue(p_rw.TrySetValue(1140, pylon.IntegerValueCorrection_None))
        self.assertEqual(1140, p_rw.GetValue())

        self.assertFalse(p_ro.TrySetValue(1140, pylon.IntegerValueCorrection_None))

    def test_integer_parameter_try_set_value_with_correction_nearest(self):
        """TrySetValue with IntegerValueCorrection_Nearest on RW/RO."""
        p_rw = pylon.IntegerParameter(self.nodemap, "TestInt")
        p_ro = pylon.IntegerParameter(self.nodemap, "TestIntRO")

        self.assertTrue(p_rw.TrySetValue(1139, pylon.IntegerValueCorrection_Nearest))
        self.assertEqual(1140, p_rw.GetValue())

        self.assertFalse(p_ro.TrySetValue(1140, pylon.IntegerValueCorrection_Nearest))

    # ------------------------------------------------------------------
    # SetValue with EIntegerValueCorrection
    # ------------------------------------------------------------------

    def test_integer_parameter_set_value_correction_nearest_inc3(self):
        """SetValue nearest correction rounds to nearest valid increment (inc=3)."""
        p = pylon.IntegerParameter(self.nodemap, "TestIntCorrectionInc3")

        p.SetValue(14, pylon.IntegerValueCorrection_Nearest)
        self.assertEqual(13, p.GetValue())

        p.SetValue(15, pylon.IntegerValueCorrection_Nearest)
        self.assertEqual(16, p.GetValue())

    def test_integer_parameter_set_value_correction_nearest_inc10(self):
        """SetValue nearest correction rounds to nearest valid increment (inc=10)."""
        p = pylon.IntegerParameter(self.nodemap, "TestIntCorrectionInc10")

        p.SetValue(14, pylon.IntegerValueCorrection_Nearest)
        self.assertEqual(10, p.GetValue())

        p.SetValue(15, pylon.IntegerValueCorrection_Nearest)
        self.assertEqual(20, p.GetValue())

        p.SetValue(16, pylon.IntegerValueCorrection_Nearest)
        self.assertEqual(20, p.GetValue())

    def test_integer_parameter_set_value_correction_up(self):
        """SetValue up correction rounds up to nearest valid increment (inc=3)."""
        p = pylon.IntegerParameter(self.nodemap, "TestIntCorrectionInc3")

        p.SetValue(14, pylon.IntegerValueCorrection_Up)
        self.assertEqual(16, p.GetValue())

        p.SetValue(15, pylon.IntegerValueCorrection_Up)
        self.assertEqual(16, p.GetValue())

        p.SetValue(16, pylon.IntegerValueCorrection_Up)
        self.assertEqual(16, p.GetValue())

    def test_integer_parameter_set_value_correction_none_out_of_range_raises(self):
        """SetValue with IntegerValueCorrection_None raises on out-of-range value."""
        p = pylon.IntegerParameter(self.nodemap, "TestIntCorrectionInc1")
        with self.assertRaises(Exception):
            p.SetValue(p.GetMin() - 1, pylon.IntegerValueCorrection_None)
        # In-range value must not raise
        p.SetValue(p.GetMin() + 1, pylon.IntegerValueCorrection_None)

    def test_integer_parameter_set_value_correction_nearest_clamps_to_range(self):
        """SetValue nearest correction clamps to min/max."""
        p = pylon.IntegerParameter(self.nodemap, "TestIntCorrectionInc1")
        min_val = p.GetMin()
        max_val = p.GetMax()

        p.SetValue(min_val - 10, pylon.IntegerValueCorrection_Nearest)
        self.assertEqual(min_val, p.GetValue())

        p.SetValue(max_val + 10, pylon.IntegerValueCorrection_Up)
        self.assertEqual(max_val, p.GetValue())

    # ------------------------------------------------------------------
    # Negative range correction
    # ------------------------------------------------------------------

    def test_integer_parameter_negative_range_correction_nearest(self):
        """Nearest correction works correctly for negative range (inc=10)."""
        p = pylon.IntegerParameter(self.nodemap, "TestNegIntCorrectionInc10")

        p.SetValue(-14, pylon.IntegerValueCorrection_Nearest)
        self.assertEqual(-10, p.GetValue())

        p.SetValue(-15, pylon.IntegerValueCorrection_Nearest)
        self.assertEqual(-10, p.GetValue())

        p.SetValue(-16, pylon.IntegerValueCorrection_Nearest)
        self.assertEqual(-20, p.GetValue())

    def test_integer_parameter_negative_range_correction_up(self):
        """Up correction works correctly for negative range (inc=10)."""
        p = pylon.IntegerParameter(self.nodemap, "TestNegIntCorrectionInc10")

        p.SetValue(-14, pylon.IntegerValueCorrection_Up)
        self.assertEqual(-10, p.GetValue())

        p.SetValue(-15, pylon.IntegerValueCorrection_Up)
        self.assertEqual(-10, p.GetValue())

        p.SetValue(-16, pylon.IntegerValueCorrection_Up)
        self.assertEqual(-10, p.GetValue())

    # ------------------------------------------------------------------
    # Around-zero correction
    # ------------------------------------------------------------------

    def test_integer_parameter_around_zero_correction_nearest(self):
        """Nearest correction around zero (min=-95, max=95, inc=10)."""
        p = pylon.IntegerParameter(self.nodemap, "TestArounZeroIntCorrectionInc10")

        p.SetValue(0, pylon.IntegerValueCorrection_Nearest)
        self.assertEqual(5, p.GetValue())

        p.SetValue(1, pylon.IntegerValueCorrection_Nearest)
        self.assertEqual(5, p.GetValue())

        p.SetValue(-1, pylon.IntegerValueCorrection_Nearest)
        self.assertEqual(-5, p.GetValue())

    def test_integer_parameter_around_zero_correction_up(self):
        """Up correction around zero."""
        p = pylon.IntegerParameter(self.nodemap, "TestArounZeroIntCorrectionInc10")

        p.SetValue(-5, pylon.IntegerValueCorrection_Up)
        self.assertEqual(-5, p.GetValue())

        p.SetValue(-1, pylon.IntegerValueCorrection_Up)
        self.assertEqual(5, p.GetValue())

        p.SetValue(1, pylon.IntegerValueCorrection_Up)
        self.assertEqual(5, p.GetValue())

    # ------------------------------------------------------------------
    # GetValuePercentOfRange / SetValuePercentOfRange
    # ------------------------------------------------------------------

    def test_integer_parameter_get_value_percent_of_range(self):
        """GetValuePercentOfRange returns correct percentage."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        # Initial value is 1500, range 1000-2000 → 50%
        self.assertAlmostEqual(50.0, p.GetValuePercentOfRange())

        p.SetToMinimum()
        self.assertAlmostEqual(0.0, p.GetValuePercentOfRange())

        p.SetToMaximum()
        self.assertAlmostEqual(100.0, p.GetValuePercentOfRange())

    def test_integer_parameter_get_value_percent_of_range_prop(self):
        """Property ValuePercentOfRange returns correct percentage."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        # Initial value is 1500, range 1000-2000 → 50%
        self.assertAlmostEqual(50.0, p.ValuePercentOfRange)

        p.ValuePercentOfRange = 0.0
        self.assertAlmostEqual(0.0, p.ValuePercentOfRange)

        p.SetToMaximum()
        self.assertAlmostEqual(100.0, p.ValuePercentOfRange)

    def test_integer_parameter_get_value_percent_of_range_equal_min_max(self):
        """GetValuePercentOfRange returns 100 when min == max."""
        p = pylon.IntegerParameter(self.nodemap, "TestPercentOfRangeInt")
        self.assertAlmostEqual(100.0, p.GetValuePercentOfRange())

    def test_integer_parameter_set_value_percent_of_range(self):
        """SetValuePercentOfRange sets value at expected quantised position."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        min_val = p.GetMin()
        max_val = p.GetMax()

        p.SetValuePercentOfRange(-10)
        self.assertEqual(min_val, p.GetValue())

        p.SetValuePercentOfRange(0)
        self.assertEqual(min_val, p.GetValue())

        p.SetValuePercentOfRange(50)
        self.assertEqual(int(min_val + (max_val - min_val) * 0.5), p.GetValue())

        p.SetValuePercentOfRange(100)
        self.assertEqual(max_val, p.GetValue())

        p.SetValuePercentOfRange(110)
        self.assertEqual(max_val, p.GetValue())

    def test_integer_parameter_try_set_value_percent_of_range(self):
        """TrySetValuePercentOfRange returns True for RW, False for RO."""
        p_rw = pylon.IntegerParameter(self.nodemap, "TestInt")
        p_ro = pylon.IntegerParameter(self.nodemap, "TestIntRO")

        self.assertTrue(p_rw.TrySetValuePercentOfRange(10))
        self.assertFalse(p_ro.TrySetValuePercentOfRange(10))

    # ------------------------------------------------------------------
    # SetToMaximum / SetToMinimum / TrySetToMaximum / TrySetToMinimum
    # ------------------------------------------------------------------

    def test_integer_parameter_set_to_maximum(self):
        """SetToMaximum sets value to GetMax()."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        p.SetToMaximum()
        self.assertEqual(p.GetMax(), p.GetValue())

    def test_integer_parameter_set_to_minimum(self):
        """SetToMinimum sets value to GetMin()."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        p.SetToMinimum()
        self.assertEqual(p.GetMin(), p.GetValue())

    def test_integer_parameter_try_set_to_maximum(self):
        """TrySetToMaximum returns True for RW, False for RO."""
        p_rw = pylon.IntegerParameter(self.nodemap, "TestInt")
        p_ro = pylon.IntegerParameter(self.nodemap, "TestIntRO")

        self.assertTrue(p_rw.TrySetToMaximum())
        self.assertEqual(p_rw.GetMax(), p_rw.GetValue())

        self.assertFalse(p_ro.TrySetToMaximum())

    def test_integer_parameter_try_set_to_minimum(self):
        """TrySetToMinimum returns True for RW, False for RO."""
        p_rw = pylon.IntegerParameter(self.nodemap, "TestInt")
        p_ro = pylon.IntegerParameter(self.nodemap, "TestIntRO")

        self.assertTrue(p_rw.TrySetToMinimum())
        self.assertEqual(p_rw.GetMin(), p_rw.GetValue())

        self.assertFalse(p_ro.TrySetToMinimum())

    # ------------------------------------------------------------------
    # ToString / FromString / ToStringOrDefault
    # ------------------------------------------------------------------

    def test_integer_parameter_to_string(self):
        """ToString returns correct string representation."""
        p_rw = pylon.IntegerParameter(self.nodemap, "TestInt")
        p_rw.SetValue(1500)
        self.assertEqual("1500", p_rw.ToString())

        p_unattached = pylon.IntegerParameter()
        with self.assertRaises(Exception):
            p_unattached.ToString()

    def test_integer_parameter_to_string_or_default(self):
        """ToStringOrDefault returns value string or default when not readable."""
        p_rw = pylon.IntegerParameter(self.nodemap, "TestInt")
        p_rw.SetValue(1500)
        self.assertEqual("1500", p_rw.ToStringOrDefault("default"))

        p_wo = pylon.IntegerParameter(self.nodemap, "TestIntWO")
        self.assertEqual("default", p_wo.ToStringOrDefault("default"))

        p_unattached = pylon.IntegerParameter()
        self.assertEqual("default", p_unattached.ToStringOrDefault("default"))

    def test_integer_parameter_from_string(self):
        """FromString parses and sets valid values; raises on invalid input."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")

        p.FromString("1100")
        self.assertEqual(1100, p.GetValue())

        # Float string truncates to integer
        p.FromString("1100.2")
        self.assertEqual(1100, p.GetValue())

        # Out of range
        with self.assertRaises(Exception):
            p.FromString("4000")
        self.assertEqual(1100, p.GetValue())

        # Non-numeric
        with self.assertRaises(Exception):
            p.FromString("sdgsdgsdg")
        self.assertEqual(1100, p.GetValue())

        # Read-only raises
        p_ro = pylon.IntegerParameter(self.nodemap, "TestIntRO")
        with self.assertRaises(Exception):
            p_ro.FromString("1200")
        self.assertEqual(1500, p_ro.GetValue())

        # Write-only does not raise
        p_wo = pylon.IntegerParameter(self.nodemap, "TestIntWO")
        p_wo.FromString("1200")

    # ------------------------------------------------------------------
    # IsReadable / IsWritable / GetAccessMode
    # ------------------------------------------------------------------

    def test_integer_parameter_access_modes(self):
        """Access mode helpers and GetAccessMode return correct values."""
        p_ro = pylon.IntegerParameter(self.nodemap, "TestIntRO")
        p_wo = pylon.IntegerParameter(self.nodemap, "TestIntWO")
        p_rw = pylon.IntegerParameter(self.nodemap, "TestInt")
        p_unattached = pylon.IntegerParameter()

        self.assertTrue(p_ro.IsReadable())
        self.assertFalse(p_ro.IsWritable())
        self.assertEqual(genicam.RO, p_ro.GetAccessMode())

        self.assertFalse(p_wo.IsReadable())
        self.assertTrue(p_wo.IsWritable())
        self.assertEqual(genicam.WO, p_wo.GetAccessMode())

        self.assertTrue(p_rw.IsReadable())
        self.assertTrue(p_rw.IsWritable())
        self.assertEqual(genicam.RW, p_rw.GetAccessMode())

        self.assertFalse(p_unattached.IsReadable())
        self.assertFalse(p_unattached.IsWritable())
        self.assertEqual(genicam.NI, p_unattached.GetAccessMode())

    # ------------------------------------------------------------------
    # GetInfo / GetInfoOrDefault
    # ------------------------------------------------------------------

    def test_integer_parameter_get_info_or_default_unattached(self):
        """GetInfoOrDefault returns defaults for unattached parameter."""
        p = pylon.IntegerParameter()
        self.assertEqual("A", p.GetInfoOrDefault(pylon.ParameterInfo_Name, "A"))
        self.assertEqual("B", p.GetInfoOrDefault(pylon.ParameterInfo_DisplayName, "B"))
        self.assertEqual("C", p.GetInfoOrDefault(pylon.ParameterInfo_ToolTip, "C"))
        self.assertEqual("D", p.GetInfoOrDefault(pylon.ParameterInfo_Description, "D"))

    def test_integer_parameter_get_info_unattached_raises(self):
        """GetInfo raises for each info kind when unattached."""
        p = pylon.IntegerParameter()
        for kind in (pylon.ParameterInfo_Name, pylon.ParameterInfo_DisplayName,
                     pylon.ParameterInfo_ToolTip, pylon.ParameterInfo_Description):
            with self.assertRaises(Exception):
                p.GetInfo(kind)

    def test_integer_parameter_get_info_attached(self):
        """GetInfo returns node name for attached parameter."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        self.assertEqual("TestInt", p.GetInfo(pylon.ParameterInfo_Name))
        self.assertEqual("TestInt", p.GetInfoOrDefault(pylon.ParameterInfo_Name, "default"))

    # ------------------------------------------------------------------
    # IsValid / IsValueCacheValid / GetNode
    # ------------------------------------------------------------------

    def test_integer_parameter_is_valid(self):
        """IsValid reflects attach/release lifecycle."""
        p = pylon.IntegerParameter()
        self.assertFalse(p.IsValid())

        p.Attach(self.nodemap, "TestInt")
        self.assertTrue(p.IsValid())

        p.Release()
        self.assertFalse(p.IsValid())

    def test_integer_parameter_is_value_cache_valid(self):
        """IsValueCacheValid is callable and returns a bool."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        self.assertIsInstance(p.IsValueCacheValid(), bool)

    def test_integer_parameter_get_node(self):
        """GetNode returns attached node; raises when unattached."""
        node = self.getINode("TestInt")
        p = pylon.IntegerParameter(node)
        self.assertEqual("TestInt", p.GetNode().GetName())

        p.Release()
        with self.assertRaises(Exception):
            p.GetNode()

    def test_parameter_str(self):
        """Test CParameter __str__."""
        p_unattached = pylon.IntegerParameter()
        self.assertEqual(str(p_unattached), "<not found>")
        p_wo = pylon.IntegerParameter(self.nodemap, "TestIntWO")
        self.assertEqual(str(p_wo), "<not readable>")
        p_ro = pylon.IntegerParameter(self.nodemap, "TestIntRO")
        self.assertEqual(str(p_ro), "1500")

    # ------------------------------------------------------------------
    # Compatibility with genicam
    # ------------------------------------------------------------------

    def test_genicam_compatibility(self):
        """Parameter can be used wherever genicam interfaces are expected."""
        p = pylon.IntegerParameter(self.nodemap, "TestInt")
        self.assertIsInstance(p, genicam.IInteger)
        self.assertIsInstance(p, genicam.IValue)
        self.assertTrue(genicam.IsReadable(p))
        self.assertTrue(genicam.IsWritable(p))

if __name__ == "__main__":
    unittest.main()
