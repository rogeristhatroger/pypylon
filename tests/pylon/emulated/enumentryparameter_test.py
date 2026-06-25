"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/EnumEntryParameter.i.
"""
from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest

# Enum entries defined in TestEnumeration* nodes
ENTRY_NAME_TIC = "EnumEntry_TestEnumerationRW_EntryTic"
ENTRY_NAME_TAC = "EnumEntry_TestEnumerationRW_EntryTac"
ENTRY_NAME_TOE = "EnumEntry_TestEnumerationRW_EntryToe"

# Expected symbolic / integer / numeric values for each entry
ENTRY_TIC_SYMBOLIC = "tic"
ENTRY_TIC_VALUE = 0
ENTRY_TIC_NUMERIC = 0.0

ENTRY_TAC_SYMBOLIC = "tac"
ENTRY_TAC_VALUE = 1
ENTRY_TAC_NUMERIC = 1.0

ENTRY_TOE_SYMBOLIC = "toe"
ENTRY_TOE_VALUE = 2
ENTRY_TOE_NUMERIC = 2.0


class EnumEntryParameterTestSuite(PylonParameterTestCase):

    # Helper: obtain IEnumEntry for an entry node via EnumParameter
    def _get_ienum_entry(self, symbolic):
        return pylon.EnumParameter(self.nodemap, "TestEnumerationRW").GetEntryByName(symbolic)

    # ------------------------------------------------------------------
    # Construction / Attach / Release
    # ------------------------------------------------------------------

    def test_enum_entry_parameter_construction_default(self):
        """Default construction produces an invalid parameter."""
        p = pylon.EnumEntryParameter()
        self.assertFalse(p.IsValid())

    def test_enum_entry_parameter_construction_from_inode_matching(self):
        """Construction from a matching INode (enum entry) attaches and validates."""
        node = self.getINode(ENTRY_NAME_TIC)
        p = pylon.EnumEntryParameter(node)
        self.assertTrue(p.IsValid())

    def test_enum_entry_parameter_construction_from_inode_wrong_type(self):
        """Construction from a non-enum-entry INode yields an invalid parameter."""
        node_int = self.getINode("TestInt")
        p = pylon.EnumEntryParameter(node_int)
        self.assertFalse(p.IsValid())

    def test_enum_entry_parameter_construction_from_ienumentry(self):
        """Construction from a GenApi IEnumEntry object attaches and validates."""
        ienum_entry = self._get_ienum_entry(ENTRY_TIC_SYMBOLIC)
        self.assertIsInstance(ienum_entry, genicam.IEnumEntry)
        p = pylon.EnumEntryParameter(ienum_entry)
        self.assertTrue(p.IsValid())

    def test_enum_entry_parameter_construction_from_nodemap_name(self):
        """Construction from nodemap + name attaches and validates."""
        p = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(self.getINode(ENTRY_NAME_TIC)))
        self.assertFalse(p.Equals(self.getINode(ENTRY_NAME_TAC)))

    def test_enum_entry_parameter_construction_from_nonexistent_name(self):
        """Construction from nodemap + non-existent name produces an invalid parameter."""
        p = pylon.EnumEntryParameter(self.nodemap, "EntryDoesNotExist")
        self.assertFalse(p.IsValid())

    def test_enum_entry_parameter_construction_copy(self):
        """Copy construction produces a valid, equal parameter."""
        p1 = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        p2 = pylon.EnumEntryParameter(p1)
        self.assertTrue(p1.IsValid())
        self.assertTrue(p2.IsValid())
        self.assertTrue(p1.Equals(p2))

    def test_enum_entry_parameter_attach_from_inode(self):
        """Attach from INode sets validity and correct node."""
        node_tic = self.getINode(ENTRY_NAME_TIC)
        node_tac = self.getINode(ENTRY_NAME_TAC)

        p = pylon.EnumEntryParameter()
        self.assertFalse(p.IsValid())

        result = p.Attach(node_tic)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(node_tic))
        self.assertFalse(p.Equals(node_tac))

        result = p.Attach(node_tac)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(node_tac))
        self.assertFalse(p.Equals(node_tic))

    def test_enum_entry_parameter_attach_from_ienumentry(self):
        """Attach from GenApi IEnumEntry attaches correctly."""
        ienum_entry = self._get_ienum_entry(ENTRY_TIC_SYMBOLIC)
        p = pylon.EnumEntryParameter()
        result = p.Attach(ienum_entry)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

    def test_enum_entry_parameter_attach_from_nodemap_name(self):
        """Attach from nodemap + name; non-existent name returns False."""
        p = pylon.EnumEntryParameter()

        result = p.Attach(self.nodemap, ENTRY_NAME_TIC)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, ENTRY_NAME_TAC)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "EntryDoesNotExist")
        self.assertFalse(result)

    def test_enum_entry_parameter_release(self):
        """Release makes parameter invalid."""
        p = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    # ------------------------------------------------------------------
    # Equals
    # ------------------------------------------------------------------

    def test_enum_entry_parameter_equals_parameter(self):
        """Equals between two EnumEntryParameters."""
        node_tic = self.nodemap.GetNode(ENTRY_NAME_TIC)
        node_tac = self.nodemap.GetNode(ENTRY_NAME_TAC)

        p1 = pylon.EnumEntryParameter(node_tic)
        p2 = pylon.EnumEntryParameter(node_tic)
        p3 = pylon.EnumEntryParameter(node_tac)
        p_empty1 = pylon.EnumEntryParameter()
        p_empty2 = pylon.EnumEntryParameter()

        self.assertTrue(p_empty1.Equals(p_empty2))
        self.assertTrue(p1.Equals(p2))
        self.assertTrue(p2.Equals(p1))
        self.assertFalse(p1.Equals(p3))
        self.assertFalse(p3.Equals(p1))
        self.assertFalse(p1.Equals(p_empty1))
        self.assertFalse(p_empty1.Equals(p1))

    def test_enum_entry_parameter_equals_inode(self):
        """Equals against INode and None."""
        node_tic = self.getINode(ENTRY_NAME_TIC)
        node_tac = self.getINode(ENTRY_NAME_TAC)

        p_empty = pylon.EnumEntryParameter()
        p = pylon.EnumEntryParameter(node_tic)

        self.assertTrue(p_empty.Equals(None))
        self.assertFalse(p_empty.Equals(node_tic))
        self.assertTrue(p.Equals(node_tic))
        self.assertFalse(p.Equals(node_tac))
        self.assertFalse(p.Equals(None))

    def test_enum_entry_parameter_equals_ienumentry(self):
        """Equals against a GenApi IEnumEntry object."""
        entry_tic = self._get_ienum_entry(ENTRY_TIC_SYMBOLIC)
        entry_tac = self._get_ienum_entry(ENTRY_TAC_SYMBOLIC)

        p_empty = pylon.EnumEntryParameter()
        p = pylon.EnumEntryParameter(entry_tic)

        self.assertTrue(p.Equals(entry_tic))
        self.assertFalse(p.Equals(entry_tac))
        self.assertFalse(p_empty.Equals(entry_tic))

    # ------------------------------------------------------------------
    # IsValid / IsReadable / IsWritable / GetAccessMode
    # ------------------------------------------------------------------

    def test_enum_entry_parameter_is_valid(self):
        """IsValid reflects attachment state."""
        p = pylon.EnumEntryParameter()
        self.assertFalse(p.IsValid())
        p.Attach(self.nodemap, ENTRY_NAME_TIC)
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    def test_enum_entry_parameter_is_readable_writable(self):
        """Enum entry nodes are readable but not writable."""
        p = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertTrue(p.IsReadable())
        self.assertFalse(p.IsWritable())

    def test_enum_entry_parameter_is_readable_writable_unattached(self):
        """An unattached parameter reports not readable and not writable."""
        p = pylon.EnumEntryParameter()
        self.assertFalse(p.IsReadable())
        self.assertFalse(p.IsWritable())

    def test_enum_entry_parameter_get_access_mode(self):
        """GetAccessMode returns genicam.RO for an enum entry node."""
        p = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.IsReadable())
        self.assertFalse(p.IsWritable())
        self.assertEqual(genicam.RO, p.GetAccessMode())

    def test_enum_entry_parameter_get_access_mode_unattached(self):
        """GetAccessMode returns genicam.NI when unattached."""
        self.assertEqual(genicam.NI, pylon.EnumEntryParameter().GetAccessMode())

    # ------------------------------------------------------------------
    # Unattached – all value operations must raise
    # ------------------------------------------------------------------

    def test_enum_entry_parameter_unattached_raises(self):
        """All value access on an unattached parameter raises."""
        p = pylon.EnumEntryParameter()
        with self.assertRaises(Exception): p.GetValue()
        with self.assertRaises(Exception): p.GetSymbolic()
        with self.assertRaises(Exception): p.GetNumericValue()
        with self.assertRaises(Exception): p.IsSelfClearing()

    # ------------------------------------------------------------------
    # IEnumEntry methods
    # ------------------------------------------------------------------

    def test_enum_entry_parameter_get_value(self):
        """GetValue returns the integer value of each entry."""
        self.assertEqual(ENTRY_TIC_VALUE, pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC).GetValue())
        self.assertEqual(ENTRY_TAC_VALUE, pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TAC).GetValue())
        self.assertEqual(ENTRY_TOE_VALUE, pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TOE).GetValue())

    def test_enum_entry_parameter_get_symbolic(self):
        """GetSymbolic returns the symbolic string of each entry."""
        self.assertEqual(ENTRY_TIC_SYMBOLIC, pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC).GetSymbolic())
        self.assertEqual(ENTRY_TAC_SYMBOLIC, pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TAC).GetSymbolic())
        self.assertEqual(ENTRY_TOE_SYMBOLIC, pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TOE).GetSymbolic())

    def test_enum_entry_parameter_get_numeric_value(self):
        """GetNumericValue returns the double-precision value of each entry."""
        self.assertAlmostEqual(ENTRY_TIC_NUMERIC, pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC).GetNumericValue())
        self.assertAlmostEqual(ENTRY_TAC_NUMERIC, pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TAC).GetNumericValue())
        self.assertAlmostEqual(ENTRY_TOE_NUMERIC, pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TOE).GetNumericValue())

    def test_enum_entry_parameter_is_self_clearing(self):
        """IsSelfClearing returns False for non-self-clearing test entries."""
        p = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertIsInstance(p.IsSelfClearing(), bool)
        self.assertFalse(p.IsSelfClearing())

    # ------------------------------------------------------------------
    # Properties: Symbolic, NumericValue, Value
    # ------------------------------------------------------------------

    def test_enum_entry_parameter_symbolic_property(self):
        """The Symbolic property returns the symbolic name of the entry."""
        p_tic = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertEqual(ENTRY_TIC_SYMBOLIC, p_tic.Symbolic)

        p_tac = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TAC)
        self.assertEqual(ENTRY_TAC_SYMBOLIC, p_tac.Symbolic)

    def test_enum_entry_parameter_numeric_value_property(self):
        """The NumericValue property returns the double-precision entry value."""
        p_tic = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertAlmostEqual(ENTRY_TIC_NUMERIC, p_tic.NumericValue)

        p_tac = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TAC)
        self.assertAlmostEqual(ENTRY_TAC_NUMERIC, p_tac.NumericValue)

    def test_enum_entry_parameter_value_property(self):
        """Value property returns the integer value, equal to GetValue()."""
        p_tic = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertEqual(ENTRY_TIC_VALUE, p_tic.Value)
        self.assertEqual(p_tic.GetValue(), p_tic.Value)

        p_tac = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TAC)
        self.assertEqual(ENTRY_TAC_VALUE, p_tac.Value)

        p_toe = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TOE)
        self.assertEqual(ENTRY_TOE_VALUE, p_toe.Value)

    # ------------------------------------------------------------------
    # ToString / ToStringOrDefault / __str__
    # ------------------------------------------------------------------

    def test_enum_entry_parameter_to_string(self):
        """ToString returns the symbolic name of the entry."""
        p = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertEqual(str(ENTRY_TIC_VALUE), p.ToString())

    def test_enum_entry_parameter_to_string_unattached_raises(self):
        """ToString on an unattached parameter raises."""
        with self.assertRaises(Exception):
            pylon.EnumEntryParameter().ToString()

    def test_enum_entry_parameter_to_string_or_default(self):
        """ToStringOrDefault returns the symbolic name or the default when unattached."""
        p_unattached = pylon.EnumEntryParameter()
        self.assertEqual("default", p_unattached.ToStringOrDefault("default"))

        p = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertEqual(str(ENTRY_TIC_VALUE), p.ToStringOrDefault("default"))

    def test_enum_entry_parameter_str(self):
        """__str__ returns the symbolic name or '<not found>'."""
        self.assertEqual("<not found>", str(pylon.EnumEntryParameter()))
        p = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertEqual(str(ENTRY_TIC_VALUE), str(p))

    # ------------------------------------------------------------------
    # GetNode / IsValueCacheValid
    # ------------------------------------------------------------------

    def test_enum_entry_parameter_get_node(self):
        """GetNode returns the attached node; unattached raises."""
        node = self.getINode(ENTRY_NAME_TIC)
        p = pylon.EnumEntryParameter(node)
        self.assertEqual(node.GetName(), p.GetNode().GetName())
        self.assertEqual(node.GetName(), p.Node.GetName())
        self.assertIsInstance(p.GetNode(), genicam.INode)

        p.Release()
        with self.assertRaises(Exception):
            p.GetNode()

    def test_enum_entry_parameter_is_value_cache_valid(self):
        """IsValueCacheValid is callable on an attached parameter."""
        p = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertIsInstance(p.IsValueCacheValid(), bool)

    # ------------------------------------------------------------------
    # GetInfo / GetInfoOrDefault
    # ------------------------------------------------------------------

    def test_enum_entry_parameter_get_info_name(self):
        """GetInfo with ParameterInfo_Name returns the node name."""
        p = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertEqual(ENTRY_NAME_TIC, p.GetInfo(pylon.ParameterInfo_Name))

    def test_enum_entry_parameter_get_info_or_default_unattached(self):
        """GetInfoOrDefault returns the default when unattached."""
        p = pylon.EnumEntryParameter()
        self.assertEqual("fallback", p.GetInfoOrDefault(pylon.ParameterInfo_Name, "fallback"))

    # ------------------------------------------------------------------
    # Compatibility with genicam
    # ------------------------------------------------------------------

    def test_genicam_compatibility(self):
        """EnumEntryParameter can be used wherever genicam interfaces are expected."""
        p = pylon.EnumEntryParameter(self.nodemap, ENTRY_NAME_TIC)
        self.assertIsInstance(p, genicam.IEnumEntry)
        self.assertIsInstance(p, genicam.IValue)
        self.assertTrue(genicam.IsReadable(p))

if __name__ == "__main__":
    unittest.main()

