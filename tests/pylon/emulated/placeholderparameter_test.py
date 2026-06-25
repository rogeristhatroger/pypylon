"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylon/PlaceholderParameter.i.

PlaceholderParameter is a permanently-invalid sentinel that represents a named
parameter path not available in the current device or node map.
"""
from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest

PATH_A = "Camera.ExposureTime"
PATH_B = "Camera.Gain"
PATH_EMPTY = ""


class PlaceholderParameterTestSuite(PylonParameterTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_placeholder_construction_default(self):
        """Default construction produces an invalid parameter with an empty path."""
        p = pylon.PlaceholderParameter()
        self.assertFalse(p.IsValid())
        self.assertEqual("", p.GetPath())
        self.assertFalse(genicam.IsAvailable(p))
        self.assertFalse(genicam.IsImplemented(p))
        self.assertFalse(genicam.IsReadable(p))
        self.assertFalse(genicam.IsWritable(p))

    def test_placeholder_construction_from_string(self):
        """Construction with a path string stores the path and stays invalid."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertFalse(p.IsValid())
        self.assertEqual(PATH_A, p.GetPath())

    def test_placeholder_construction_copy(self):
        """Copy construction preserves the path and stays invalid."""
        p1 = pylon.PlaceholderParameter(PATH_A)
        p2 = pylon.PlaceholderParameter(p1)
        self.assertFalse(p2.IsValid())
        self.assertEqual(PATH_A, p2.GetPath())
        self.assertEqual(p1.GetPath(), p2.GetPath())

    # ------------------------------------------------------------------
    # Path property
    # ------------------------------------------------------------------

    def test_placeholder_path_property(self):
        """The Path property returns the same value as GetPath()."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertEqual(p.GetPath(), p.Path)

    def test_placeholder_path_empty(self):
        """Default-constructed PlaceholderParameter has an empty path."""
        p = pylon.PlaceholderParameter()
        self.assertEqual("", p.Path)

    # ------------------------------------------------------------------
    # IsValid — always False
    # ------------------------------------------------------------------

    def test_placeholder_is_valid_always_false(self):
        """IsValid is always False regardless of the path."""
        self.assertFalse(pylon.PlaceholderParameter().IsValid())
        self.assertFalse(pylon.PlaceholderParameter(PATH_A).IsValid())
        self.assertFalse(pylon.PlaceholderParameter(PATH_EMPTY).IsValid())

    # ------------------------------------------------------------------
    # IsReadable / IsWritable / GetAccessMode
    # ------------------------------------------------------------------

    def test_placeholder_is_readable_writable(self):
        """IsReadable and IsWritable are both False."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertFalse(p.IsReadable())
        self.assertFalse(p.IsWritable())

    def test_placeholder_get_access_mode(self):
        """GetAccessMode returns genicam.NI."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertEqual(genicam.NI, p.GetAccessMode())

    def test_placeholder_access_mode_property(self):
        """AccessMode property returns genicam.NI (does not raise)."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertEqual(genicam.NI, p.AccessMode)

    # ------------------------------------------------------------------
    # Min / Max / Inc / Symbolic — all raise
    # ------------------------------------------------------------------

    def test_placeholder_get_min_raises(self):
        """GetMin always raises with the path in the message."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetMin()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_min_property_raises(self):
        """Min property always raises with the path in the message."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            _ = p.Min
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_get_max_raises(self):
        """GetMax always raises with the path in the message."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetMax()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_max_property_raises(self):
        """Max property always raises with the path in the message."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            _ = p.Max
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_get_inc_raises(self):
        """GetInc always raises with the path in the message."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetInc()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_inc_property_raises(self):
        """Inc property always raises with the path in the message."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            _ = p.Inc
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_get_symbolic_raises(self):
        """GetSymbolic always raises with the path in the message."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetSymbolic()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_symbolic_property_raises(self):
        """Symbolic property always raises with the path in the message."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            _ = p.Symbolic
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_range_properties_error_messages_contain_path(self):
        """All range getter error messages contain the stored path."""
        p = pylon.PlaceholderParameter(PATH_B)
        for method in (p.GetMin, p.GetMax, p.GetInc, p.GetSymbolic):
            with self.assertRaises(pylon.LogicalErrorException) as ctx:
                method()
            self.assertIn(PATH_B, str(ctx.exception))

    # ------------------------------------------------------------------
    # Attach — always raises
    # ------------------------------------------------------------------

    def test_placeholder_attach_from_inode_raises(self):
        """Attach(INode) raises because the parameter cannot be attached."""
        node = self.getINode("TestInt")
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            p.Attach(node)

    def test_placeholder_attach_from_nodemap_raises(self):
        """Attach(nodemap, name) raises because the parameter cannot be attached."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            p.Attach(self.nodemap, "TestInt")

    def test_placeholder_still_invalid_after_failed_attach(self):
        """After a failed Attach the parameter is still invalid."""
        node = self.getINode("TestInt")
        p = pylon.PlaceholderParameter(PATH_A)
        try:
            p.Attach(node)
        except Exception:
            pass
        self.assertFalse(p.IsValid())
        self.assertEqual(PATH_A, p.GetPath())

    # ------------------------------------------------------------------
    # Release — no-op (already invalid)
    # ------------------------------------------------------------------

    def test_placeholder_release_no_op(self):
        """Release on a PlaceholderParameter leaves it invalid."""
        p = pylon.PlaceholderParameter(PATH_A)
        p.Release()
        self.assertFalse(p.IsValid())
        self.assertEqual(PATH_A, p.GetPath())

    # ------------------------------------------------------------------
    # SetValue / GetValue — raise LogicalErrorException
    # ------------------------------------------------------------------

    def test_placeholder_set_value_bool_raises(self):
        """SetValue(bool) raises with a message containing the path."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.SetValue(True)
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_set_value_int_raises(self):
        """SetValue(int) raises with a message containing the path."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.SetValue(42)
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_set_value_float_raises(self):
        """SetValue(float) raises with a message containing the path."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.SetValue(1.5)
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_set_value_string_raises(self):
        """SetValue(str) raises with a message containing the path."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.SetValue("Continuous")
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_get_value_raises(self):
        """GetValue raises with a message containing the path."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetValue()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_error_message_contains_path(self):
        """Error message from SetValue/GetValue always includes the stored path."""
        p = pylon.PlaceholderParameter(PATH_B)
        for call in (lambda: p.SetValue(0), lambda: p.GetValue()):
            with self.assertRaises(pylon.LogicalErrorException) as ctx:
                call()
            self.assertIn(PATH_B, str(ctx.exception))

    # ------------------------------------------------------------------
    # Value property — get and set both raise
    # ------------------------------------------------------------------

    def test_placeholder_value_getter_raises(self):
        """Reading the Value property raises with the path in the message."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            _ = p.Value
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_value_setter_raises(self):
        """Writing the Value property raises with the path in the message."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.Value = 42
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_value_setter_raises_for_all_types(self):
        """Writing the Value property raises for every Python value type."""
        p = pylon.PlaceholderParameter(PATH_A)
        for v in (True, 0, 1.5, "Off", b"bytes"):
            with self.assertRaises(pylon.LogicalErrorException):
                p.Value = v

    # ------------------------------------------------------------------
    # Execute — raises
    # ------------------------------------------------------------------

    def test_placeholder_execute_raises(self):
        """Execute always raises with the path in the message."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.Execute()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_execute_raises_for_path_b(self):
        """Execute error message contains the correct path for a different placeholder."""
        p = pylon.PlaceholderParameter(PATH_B)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.Execute()
        self.assertIn(PATH_B, str(ctx.exception))
        self.assertNotIn(PATH_A, str(ctx.exception))

    # ------------------------------------------------------------------
    # Try* methods — always return False, never raise
    # ------------------------------------------------------------------

    def test_placeholder_try_set_value_returns_false(self):
        """TrySetValue always returns False for any value type."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertFalse(p.TrySetValue(True))
        self.assertFalse(p.TrySetValue(42))
        self.assertFalse(p.TrySetValue(1.5))
        self.assertFalse(p.TrySetValue("Continuous"))

    def test_placeholder_try_execute_returns_false(self):
        """TryExecute always returns False."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertFalse(p.TryExecute())

    def test_placeholder_try_set_value_percent_of_range_returns_false(self):
        """TrySetValuePercentOfRange always returns False."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertFalse(p.TrySetValuePercentOfRange(50.0))

    def test_placeholder_try_set_to_maximum_returns_false(self):
        """TrySetToMaximum always returns False."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertFalse(p.TrySetToMaximum())

    def test_placeholder_try_set_to_minimum_returns_false(self):
        """TrySetToMinimum always returns False."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertFalse(p.TrySetToMinimum())

    def test_placeholder_try_methods_do_not_raise(self):
        """All Try* methods return False without raising any exception."""
        p = pylon.PlaceholderParameter(PATH_A)
        # Must not raise
        self.assertFalse(p.TrySetValue(True))
        self.assertFalse(p.TrySetValue(0))
        self.assertFalse(p.TrySetValue(0.0))
        self.assertFalse(p.TrySetValue("x"))
        self.assertFalse(p.TryExecute())
        self.assertFalse(p.TrySetValuePercentOfRange(0.0))
        self.assertFalse(p.TrySetToMaximum())
        self.assertFalse(p.TrySetToMinimum())

    # ------------------------------------------------------------------
    # *OrDefault methods — always return the supplied default, never raise
    # ------------------------------------------------------------------

    def test_placeholder_get_value_or_default_bool(self):
        """GetValueOrDefault(bool) returns the supplied default."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertEqual(True,  p.GetValueOrDefault(True))
        self.assertEqual(False, p.GetValueOrDefault(False))

    def test_placeholder_get_value_or_default_int(self):
        """GetValueOrDefault(int) returns the supplied default."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertEqual(99, p.GetValueOrDefault(99))

    def test_placeholder_get_value_or_default_float(self):
        """GetValueOrDefault(float) returns the supplied default."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertAlmostEqual(3.14, p.GetValueOrDefault(3.14))

    def test_placeholder_get_value_or_default_string(self):
        """GetValueOrDefault(str) returns the supplied default."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertEqual("Off", p.GetValueOrDefault("Off"))

    def test_placeholder_to_string_or_default(self):
        """ToStringOrDefault always returns the supplied default."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertEqual("default", p.ToStringOrDefault("default"))
        self.assertEqual("", p.ToStringOrDefault(""))

    def test_placeholder_get_info_or_default(self):
        """GetInfoOrDefault always returns the supplied default info."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertEqual("fallback", p.GetInfoOrDefault(pylon.ParameterInfo_Name, "fallback"))
        self.assertEqual("x",        p.GetInfoOrDefault(pylon.ParameterInfo_DisplayName, "x"))
        self.assertEqual("y",        p.GetInfoOrDefault(pylon.ParameterInfo_ToolTip, "y"))
        self.assertEqual("z",        p.GetInfoOrDefault(pylon.ParameterInfo_Description, "z"))

    def test_placeholder_or_default_methods_do_not_raise(self):
        """All *OrDefault methods return the default without raising."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertEqual(False,  p.GetValueOrDefault(False))
        self.assertEqual(0,      p.GetValueOrDefault(0))
        self.assertEqual(0.0,    p.GetValueOrDefault(0.0))
        self.assertEqual("",     p.GetValueOrDefault(""))
        self.assertEqual("def",  p.ToStringOrDefault("def"))
        self.assertEqual("def",  p.GetInfoOrDefault(pylon.ParameterInfo_Name, "def"))

    # ------------------------------------------------------------------
    # CanSetValue — always False
    # ------------------------------------------------------------------

    def test_placeholder_can_set_value_always_false(self):
        """CanSetValue always returns False."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertFalse(p.CanSetValue("Off"))
        self.assertFalse(p.CanSetValue(""))

    # ------------------------------------------------------------------
    # Genicam compatibility
    # ------------------------------------------------------------------

    def test_placeholder_is_parameter_instance(self):
        """PlaceholderParameter is a Parameter instance."""
        p = pylon.PlaceholderParameter(PATH_A)
        self.assertIsInstance(p, pylon.Parameter)
        self.assertIsInstance(p, genicam.IValue)

    # ------------------------------------------------------------------
    # Two placeholders with the same / different paths
    # ------------------------------------------------------------------

    def test_placeholder_different_paths_independent(self):
        """Two PlaceholderParameters with different paths are independent."""
        p1 = pylon.PlaceholderParameter(PATH_A)
        p2 = pylon.PlaceholderParameter(PATH_B)
        self.assertNotEqual(p1.GetPath(), p2.GetPath())
        self.assertFalse(p1.IsValid())
        self.assertFalse(p2.IsValid())

    def test_placeholder_error_message_distinct_per_path(self):
        """Error messages from two placeholders with different paths are distinct."""
        p1 = pylon.PlaceholderParameter(PATH_A)
        p2 = pylon.PlaceholderParameter(PATH_B)
        msg1 = msg2 = ""
        try:
            p1.SetValue(0)
        except Exception as e:
            msg1 = str(e)
        try:
            p2.SetValue(0)
        except Exception as e:
            msg2 = str(e)
        self.assertIn(PATH_A, msg1)
        self.assertIn(PATH_B, msg2)
        self.assertNotIn(PATH_B, msg1)
        self.assertNotIn(PATH_A, msg2)

    # ------------------------------------------------------------------
    # Integer / Float range properties and methods
    # ------------------------------------------------------------------

    def test_placeholder_get_inc_mode_raises(self):
        """GetIncMode always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetIncMode()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_inc_mode_property_raises(self):
        """IncMode property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.IncMode

    def test_placeholder_get_list_of_valid_values_raises(self):
        """GetListOfValidValues always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetListOfValidValues()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_list_of_valid_values_property_raises(self):
        """ListOfValidValues property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.ListOfValidValues

    def test_placeholder_get_representation_raises(self):
        """GetRepresentation always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetRepresentation()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_representation_property_raises(self):
        """Representation property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.Representation

    def test_placeholder_get_unit_raises(self):
        """GetUnit always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetUnit()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_unit_property_raises(self):
        """Unit property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.Unit

    def test_placeholder_get_float_alias_raises(self):
        """GetFloatAlias always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetFloatAlias()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_float_alias_property_raises(self):
        """FloatAlias property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.FloatAlias

    def test_placeholder_get_display_notation_raises(self):
        """GetDisplayNotation always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetDisplayNotation()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_display_notation_property_raises(self):
        """DisplayNotation property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.DisplayNotation

    def test_placeholder_get_display_precision_raises(self):
        """GetDisplayPrecision always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetDisplayPrecision()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_display_precision_property_raises(self):
        """DisplayPrecision property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.DisplayPrecision

    # ------------------------------------------------------------------
    # String properties and methods
    # ------------------------------------------------------------------

    def test_placeholder_get_max_length_raises(self):
        """GetMaxLength always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetMaxLength()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_max_length_property_raises(self):
        """MaxLength property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.MaxLength

    def test_placeholder_get_length_raises(self):
        """GetLength always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetLength()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_length_property_raises(self):
        """Length property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.Length

    # ------------------------------------------------------------------
    # Enum properties and methods
    # ------------------------------------------------------------------

    def test_placeholder_get_symbolics_raises(self):
        """GetSymbolics always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetSymbolics()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_symbolics_property_raises(self):
        """Symbolics property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.Symbolics

    def test_placeholder_get_entries_raises(self):
        """GetEntries always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetEntries()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_entries_property_raises(self):
        """Entries property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.Entries

    def test_placeholder_get_int_value_raises(self):
        """GetIntValue always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetIntValue()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_int_value_property_get_raises(self):
        """IntValue property getter always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.IntValue

    def test_placeholder_set_int_value_raises(self):
        """SetIntValue always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.SetIntValue(0)
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_int_value_property_set_raises(self):
        """IntValue property setter always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            p.IntValue = 0

    # ------------------------------------------------------------------
    # EnumEntry properties
    # ------------------------------------------------------------------

    def test_placeholder_get_numeric_value_raises(self):
        """GetNumericValue always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetNumericValue()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_numeric_value_property_raises(self):
        """NumericValue property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.NumericValue

    # ------------------------------------------------------------------
    # Category / Register / Port properties
    # ------------------------------------------------------------------

    def test_placeholder_get_features_raises(self):
        """GetFeatures always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetFeatures()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_features_property_raises(self):
        """Features property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.Features

    def test_placeholder_get_address_raises(self):
        """GetAddress always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetAddress()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_address_property_raises(self):
        """Address property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.Address

    def test_placeholder_get_chunk_id_raises(self):
        """GetChunkID always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetChunkID()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_chunk_id_property_raises(self):
        """ChunkID property always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.ChunkID

    # ------------------------------------------------------------------
    # ValuePercentOfRange (GETSET)
    # ------------------------------------------------------------------

    def test_placeholder_get_value_percent_of_range_raises(self):
        """GetValuePercentOfRange always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.GetValuePercentOfRange()
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_value_percent_of_range_property_get_raises(self):
        """ValuePercentOfRange property getter always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            _ = p.ValuePercentOfRange

    def test_placeholder_set_value_percent_of_range_raises(self):
        """SetValuePercentOfRange always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            p.SetValuePercentOfRange(50.0)
        self.assertIn(PATH_A, str(ctx.exception))

    def test_placeholder_value_percent_of_range_property_set_raises(self):
        """ValuePercentOfRange property setter always raises — the parameter is not available."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(pylon.LogicalErrorException):
            p.ValuePercentOfRange = 50.0

    # ------------------------------------------------------------------
    # Node property
    # ------------------------------------------------------------------

    def test_placeholder_node_property_raises(self):
        """Node property always raises — the parameter has no attached node."""
        p = pylon.PlaceholderParameter(PATH_A)
        with self.assertRaises(Exception):
            _ = p.Node


if __name__ == "__main__":
    unittest.main()

