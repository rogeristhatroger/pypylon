from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest

# All enum entries in the TestEnumeration* nodes
ENUM_VALUES = ("tic", "tac", "toe")

class EnumParameterTestSuite(PylonParameterTestCase):

    # ------------------------------------------------------------------
    # Construction / Attach / Release
    # ------------------------------------------------------------------

    def test_enum_parameter_construction_default(self):
        """Default construction produces an invalid parameter."""
        p = pylon.EnumParameter()
        self.assertFalse(p.IsValid())

    def test_enum_parameter_construction_from_inode(self):
        """Construction from a matching INode attaches and validates;
        a wrong node type yields an invalid parameter."""
        node = self.getINode("TestEnumerationRW")
        p = pylon.EnumParameter(node)
        self.assertTrue(p.IsValid())

        node_int = self.getINode("TestInt")
        p_bad = pylon.EnumParameter(node_int)
        self.assertFalse(p_bad.IsValid())

    def test_enum_parameter_construction_from_ienumeration(self):
        """Construction from a GenApi IEnumeration object attaches and validates."""
        ienum = self.nodemap.GetNode("TestEnumerationRW")
        self.assertIsInstance(ienum, genicam.IEnumeration)
        p = pylon.EnumParameter(ienum)
        self.assertTrue(p.IsValid())

    def test_enum_parameter_construction_from_nodemap_name(self):
        """Construction from nodemap + name attaches and validates."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(self.getINode("TestEnumerationRW")))
        self.assertFalse(p.Equals(self.getINode("TestEnumerationRO")))

    def test_enum_parameter_construction_from_nonexistent_name(self):
        """Construction from nodemap + non-existent name produces an invalid parameter."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationEmpty")
        self.assertFalse(p.IsValid())

    def test_enum_parameter_construction_copy(self):
        """Copy construction produces a valid, equal parameter."""
        p1 = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p2 = pylon.EnumParameter(p1)
        self.assertTrue(p1.IsValid())
        self.assertTrue(p2.IsValid())
        self.assertTrue(p1.Equals(p2))

    def test_enum_parameter_attach_from_inode(self):
        """Attach from INode sets validity and correct node."""
        node_a = self.getINode("TestEnumerationRW")
        node_b = self.getINode("TestEnumerationRO")

        p = pylon.EnumParameter()
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

    def test_enum_parameter_attach_from_ienumeration(self):
        """Attach from GenApi IEnumeration attaches correctly."""
        ienum = self.nodemap.GetNode("TestEnumerationRW")
        p = pylon.EnumParameter()
        result = p.Attach(ienum)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

    def test_enum_parameter_attach_from_nodemap_name(self):
        """Attach from nodemap + name; non-existent name returns False."""
        p = pylon.EnumParameter()

        result = p.Attach(self.nodemap, "TestEnumerationRW")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "TestEnumerationRO")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "NonExistent")
        self.assertFalse(result)

    def test_enum_parameter_release(self):
        """Release makes parameter invalid."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    # ------------------------------------------------------------------
    # Equals
    # ------------------------------------------------------------------

    def test_enum_parameter_equals_parameter(self):
        """Equals between two EnumParameters."""
        node_a = self.nodemap.GetNode("TestEnumerationRW")
        node_b = self.nodemap.GetNode("TestEnumerationRO")

        p1 = pylon.EnumParameter(node_a)
        p2 = pylon.EnumParameter(node_a)
        p3 = pylon.EnumParameter(node_b)
        p_empty1 = pylon.EnumParameter()
        p_empty2 = pylon.EnumParameter()

        self.assertTrue(p_empty1.Equals(p_empty2))
        self.assertTrue(p1.Equals(p2))
        self.assertTrue(p2.Equals(p1))
        self.assertFalse(p1.Equals(p3))
        self.assertFalse(p3.Equals(p1))
        self.assertFalse(p1.Equals(p_empty1))
        self.assertFalse(p_empty1.Equals(p1))

    def test_enum_parameter_equals_inode(self):
        """Equals against INode and None."""
        node_a = self.getINode("TestEnumerationRW")
        node_b = self.getINode("TestEnumerationRO")

        p_empty = pylon.EnumParameter()
        p = pylon.EnumParameter(node_a)

        self.assertTrue(p_empty.Equals(None))
        self.assertFalse(p_empty.Equals(node_a))
        self.assertTrue(p.Equals(node_a))
        self.assertFalse(p.Equals(node_b))
        self.assertFalse(p.Equals(None))

    def test_enum_parameter_equals_ienumeration(self):
        """Equals against a GenApi IEnumeration node."""
        ienum_rw = self.nodemap.GetNode("TestEnumerationRW")
        ienum_ro = self.nodemap.GetNode("TestEnumerationRO")

        p_empty = pylon.EnumParameter()
        p = pylon.EnumParameter(ienum_rw)

        self.assertTrue(p.Equals(ienum_rw))
        self.assertFalse(p.Equals(ienum_ro))
        self.assertFalse(p_empty.Equals(ienum_rw))

    # ------------------------------------------------------------------
    # IsValid / IsReadable / IsWritable / GetAccessMode
    # ------------------------------------------------------------------

    def test_enum_parameter_is_valid(self):
        """IsValid reflects attachment state."""
        p = pylon.EnumParameter()
        self.assertFalse(p.IsValid())
        p.Attach(self.nodemap, "TestEnumerationRW")
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    def test_enum_parameter_is_readable_writable(self):
        """IsReadable / IsWritable reflect the access mode."""
        p_ro = pylon.EnumParameter(self.nodemap, "TestEnumerationRO")
        self.assertTrue(p_ro.IsReadable())
        self.assertFalse(p_ro.IsWritable())

        p_wo = pylon.EnumParameter(self.nodemap, "TestEnumerationWO")
        self.assertFalse(p_wo.IsReadable())
        self.assertTrue(p_wo.IsWritable())

        p_rw = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        self.assertTrue(p_rw.IsReadable())
        self.assertTrue(p_rw.IsWritable())

        p_unattached = pylon.EnumParameter()
        self.assertFalse(p_unattached.IsReadable())
        self.assertFalse(p_unattached.IsWritable())

    def test_enum_parameter_get_access_mode(self):
        """GetAccessMode returns the correct genicam constant."""
        self.assertEqual(genicam.RO, pylon.EnumParameter(self.nodemap, "TestEnumerationRO").GetAccessMode())
        self.assertEqual(genicam.WO, pylon.EnumParameter(self.nodemap, "TestEnumerationWO").GetAccessMode())
        self.assertEqual(genicam.RW, pylon.EnumParameter(self.nodemap, "TestEnumerationRW").GetAccessMode())
        self.assertEqual(genicam.NI, pylon.EnumParameter().GetAccessMode())

    # ------------------------------------------------------------------
    # Unattached – all value operations must raise
    # ------------------------------------------------------------------

    def test_enum_parameter_unattached_raises(self):
        """All value/property access on unattached parameter raises."""
        p = pylon.EnumParameter()
        with self.assertRaises(Exception): p.GetValue()
        with self.assertRaises(Exception): p.SetValue("tic")
        with self.assertRaises(Exception): p.GetIntValue()
        with self.assertRaises(Exception): p.SetIntValue(0)
        with self.assertRaises(Exception): p.GetSymbolics()
        with self.assertRaises(Exception): p.GetEntries()
        with self.assertRaises(Exception): p.GetEntryByName("tic")
        with self.assertRaises(Exception): p.GetEntry(0)
        with self.assertRaises(Exception): p.GetCurrentEntry()
        with self.assertRaises(Exception): p.GetEntryByNameAsParameter("tic")
        with self.assertRaises(Exception): p.GetCurrentEntryAsParameter()

    # ------------------------------------------------------------------
    # Nonexistent / NI node
    # ------------------------------------------------------------------

    def test_enum_parameter_nonexistent_node_raises(self):
        """Parameter attached to a non-existent node is invalid and raises on value access."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationEmpty")
        self.assertFalse(p.IsValid())
        with self.assertRaises(Exception): p.GetValue()
        with self.assertRaises(Exception): p.GetAllValues()
        with self.assertRaises(Exception): p.SetValue("tic")
        with self.assertRaises(Exception): p.ToString()
        self.assertFalse(p.CanSetValue("tic"))

    def test_enum_parameter_ni_node_get_all_values(self):
        """GetAllValues on a NI (Not Implemented) parameter returns the entries without raising."""
        p_ni = pylon.EnumParameter(self.nodemap, "TestEnumerationNI")
        all_vals = p_ni.GetAllValues()
        self.assertIsInstance(all_vals, tuple)
        self.assertEqual(set(all_vals), set(ENUM_VALUES))

    def test_enum_parameter_ni_node_set_value_raises(self):
        """SetValue on NI parameter raises for every entry."""
        p_ni = pylon.EnumParameter(self.nodemap, "TestEnumerationNI")
        for v in p_ni.GetAllValues():
            with self.assertRaises(Exception):
                p_ni.SetValue(v)

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def test_enum_parameter_read(self):
        """GetValue returns the correct initial value.
        TestEnumerationRW starts at 'tic' (int value 0)."""
        p_rw = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        self.assertEqual("tic", p_rw.GetValue())
        self.assertEqual("tic", p_rw.Value)

        # Read-only also readable
        p_ro = pylon.EnumParameter(self.nodemap, "TestEnumerationRO")
        self.assertIn(p_ro.GetValue(), ENUM_VALUES)

    def test_enum_parameter_read_only_raises_on_write(self):
        """SetValue on a read-only parameter raises; value stays unchanged."""
        p_ro = pylon.EnumParameter(self.nodemap, "TestEnumerationRO")
        initial = p_ro.GetValue()
        with self.assertRaises(Exception):
            p_ro.SetValue("tac")
        self.assertEqual(initial, p_ro.GetValue())

    # ------------------------------------------------------------------
    # GetAllValues / GetSettableValues / GetSymbolics / GetEntries
    # ------------------------------------------------------------------

    def test_enum_parameter_get_all_values(self):
        """GetAllValues returns a tuple containing all symbolic names."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        all_vals = p.GetAllValues()
        self.assertIsInstance(all_vals, tuple)
        self.assertEqual(set(all_vals), set(ENUM_VALUES))
        # Every value can be set and read back
        for v in all_vals:
            p.SetValue(v)
            self.assertEqual(v, p.GetValue())

    def test_enum_parameter_get_settable_values(self):
        """GetSettableValues returns a tuple of currently settable values."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        settable = p.GetSettableValues()
        self.assertIsInstance(settable, tuple)
        self.assertGreater(len(settable), 0)
        for v in settable:
            self.assertIn(v, ENUM_VALUES)

    def test_enum_parameter_get_symbolics(self):
        """GetSymbolics returns a tuple of symbolic names."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        syms = p.GetSymbolics()
        self.assertIsInstance(syms, tuple)
        self.assertEqual(set(syms), set(ENUM_VALUES))

    def test_enum_parameter_symbolics_property(self):
        """Symbolics property equals GetSymbolics()."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        self.assertEqual(p.GetSymbolics(), p.Symbolics)
        self.assertIsInstance(p.Symbolics, tuple)
        self.assertEqual(set(p.Symbolics), set(ENUM_VALUES))

    def test_enum_parameter_get_entries(self):
        """GetEntries returns a tuple of IEnumEntry objects."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        entries = p.GetEntries()
        self.assertIsInstance(entries, tuple)
        self.assertEqual(len(entries), len(ENUM_VALUES))
        for e in entries:
            self.assertIsInstance(e, pylon.EnumEntryParameter)

    def test_enum_parameter_entries_property(self):
        """Entries property equals GetEntries()."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        self.assertEqual(len(p.GetEntries()), len(p.Entries))
        self.assertIsInstance(p.Entries, tuple)
        for e in p.Entries:
            self.assertIsInstance(e, pylon.EnumEntryParameter)

    # ------------------------------------------------------------------
    # CanSetValue
    # ------------------------------------------------------------------

    def test_enum_parameter_can_set_value(self):
        """CanSetValue returns True for valid entries, False for invalid ones."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        for v in ENUM_VALUES:
            self.assertTrue(p.CanSetValue(v))
        self.assertFalse(p.CanSetValue("anyvalue"))
        self.assertFalse(p.CanSetValue(""))

        # Non-writable parameter: CanSetValue returns False
        p_empty = pylon.EnumParameter(self.nodemap, "TestEnumerationEmpty")
        self.assertFalse(p_empty.CanSetValue("tic"))

    # ------------------------------------------------------------------
    # SetValue (string)
    # ------------------------------------------------------------------

    def test_enum_parameter_set_value_string(self):
        """SetValue(str) sets the value; round-trip with GetValue."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        initial = p.GetValue()   # "tic"

        p.SetValue("tac")
        self.assertEqual("tac", p.GetValue())
        self.assertNotEqual(initial, p.GetValue())

    def test_enum_parameter_set_value_string_prop(self):
        """Property Value round-trip for RW parameter."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        initial = p.Value   # "tic"

        p.Value = "tac"
        self.assertEqual("tac", p.Value)
        self.assertNotEqual(initial, p.Value)

    def test_enum_parameter_set_value_invalid_string_raises(self):
        """SetValue with an invalid symbolic raises InvalidArgumentException."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        with self.assertRaises(Exception):
            p.SetValue("anyvalue")

    def test_enum_parameter_set_value_ro_raises(self):
        """SetValue on a read-only parameter raises."""
        p_ro = pylon.EnumParameter(self.nodemap, "TestEnumerationRO")
        with self.assertRaises(Exception):
            p_ro.SetValue("tac")

    # ------------------------------------------------------------------
    # SetValue (null-terminated list → Python list/tuple)
    # ------------------------------------------------------------------

    def test_enum_parameter_set_value_list_first_valid_wins(self):
        """SetValue(list) sets the first entry in the list that is valid."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        initial = p.GetValue()   # "tic"

        # First valid entry found at index 2
        p.SetValue(["anyvalue1", "anyvalue2", initial])
        self.assertEqual(initial, p.GetValue())

    def test_enum_parameter_set_value_list_no_valid_entry_raises(self):
        """SetValue(list) raises when no entry in the list is valid."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        with self.assertRaises(Exception):
            p.SetValue(["anyvalue1", "anyvalue2"])

    def test_enum_parameter_set_value_empty_list_raises(self):
        """SetValue([]) raises because no valid entry can be found."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        with self.assertRaises(Exception):
            p.SetValue([])

    def test_enum_parameter_set_value_list_ro_raises(self):
        """SetValue(list) on a read-only parameter raises."""
        p_ro = pylon.EnumParameter(self.nodemap, "TestEnumerationRO")
        with self.assertRaises(Exception):
            p_ro.SetValue(["anyvalue1", "tac"])

    def test_enum_parameter_set_value_list_accepts_tuple(self):
        """SetValue also accepts a tuple of strings."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p.SetValue(("anyvalue1", "tac", "anyvalue2"))
        self.assertEqual("tac", p.GetValue())

    # ------------------------------------------------------------------
    # TrySetValue (string)
    # ------------------------------------------------------------------

    def test_enum_parameter_try_set_value_string_rw(self):
        """TrySetValue(str) returns True and sets the value for a valid entry."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        self.assertTrue(p.TrySetValue("tac"))
        self.assertEqual("tac", p.GetValue())

    def test_enum_parameter_try_set_value_string_invalid_returns_false(self):
        """TrySetValue(str) returns False for an invalid entry; value unchanged."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p.SetValue("tic")
        self.assertFalse(p.TrySetValue("anyvalue1"))
        self.assertEqual("tic", p.GetValue())

    def test_enum_parameter_try_set_value_string_ro_returns_false(self):
        """TrySetValue(str) on a read-only parameter returns False; value unchanged."""
        p_ro = pylon.EnumParameter(self.nodemap, "TestEnumerationRO")
        initial = p_ro.GetValue()
        self.assertFalse(p_ro.TrySetValue("tac"))
        self.assertEqual(initial, p_ro.GetValue())

    # ------------------------------------------------------------------
    # TrySetValue (null-terminated list → Python list/tuple)
    # ------------------------------------------------------------------

    def test_enum_parameter_try_set_value_list_first_valid_wins(self):
        """TrySetValue(list) returns True and sets the first valid entry."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        initial = p.GetValue()  # "tic"
        p.SetValue("tac")

        self.assertTrue(p.TrySetValue(["anyvalue1", initial, "anyvalue2"]))
        self.assertEqual(initial, p.GetValue())

    def test_enum_parameter_try_set_value_list_no_valid_entry_raises(self):
        """TrySetValue(list) raises AccessException when no entry matches."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        with self.assertRaises(Exception):
            p.TrySetValue(["anyvalue1", "anyvalue2"])

    def test_enum_parameter_try_set_value_list_ro_returns_false(self):
        """TrySetValue(list) on a read-only parameter returns False; value unchanged."""
        p_ro = pylon.EnumParameter(self.nodemap, "TestEnumerationRO")
        initial = p_ro.GetValue()
        self.assertFalse(p_ro.TrySetValue(["anyvalue1", initial, "anyvalue2"]))
        self.assertEqual(initial, p_ro.GetValue())

    # ------------------------------------------------------------------
    # GetValueOrDefault
    # ------------------------------------------------------------------

    def test_enum_parameter_get_value_or_default_readable(self):
        """GetValueOrDefault returns the actual value for a readable parameter."""
        p_rw = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p_rw.SetValue("tic")
        self.assertEqual("tic", p_rw.GetValueOrDefault("default"))

    def test_enum_parameter_get_value_or_default_wo(self):
        """GetValueOrDefault returns the default for a write-only parameter."""
        p_wo = pylon.EnumParameter(self.nodemap, "TestEnumerationWO")
        self.assertFalse(p_wo.IsReadable())
        self.assertEqual("default", p_wo.GetValueOrDefault("default"))

    # ------------------------------------------------------------------
    # GetIntValue / SetIntValue
    # ------------------------------------------------------------------

    def test_enum_parameter_get_set_int_value(self):
        """GetIntValue returns the integer representation; SetIntValue sets by int."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p.SetValue("tic")
        self.assertIsInstance(p.GetIntValue(), int)
        self.assertEqual(0, p.GetIntValue())
        self.assertIsInstance(p.GetIntValue(False), int)
        self.assertEqual(0, p.GetIntValue(False, False))

        p.SetIntValue(1, True)
        self.assertEqual("tac", p.GetValue())
        self.assertEqual(1, p.GetIntValue())

        p.SetIntValue(2)
        self.assertEqual("toe", p.GetValue())

    def test_enum_parameter_int_value_property_get(self):
        """IntValue property returns the same value as GetIntValue()."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p.SetValue("tic")
        self.assertEqual(0, p.IntValue)
        self.assertEqual(p.GetIntValue(), p.IntValue)

        p.SetValue("tac")
        self.assertEqual(1, p.IntValue)

        p.SetValue("toe")
        self.assertEqual(2, p.IntValue)

    def test_enum_parameter_int_value_property_set(self):
        """Assigning IntValue property sets the enum value by integer."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p.IntValue = 0
        self.assertEqual("tic", p.GetValue())

        p.IntValue = 1
        self.assertEqual("tac", p.GetValue())

        p.IntValue = 2
        self.assertEqual("toe", p.GetValue())

    # ------------------------------------------------------------------
    # GetEntryByName / GetEntry / GetCurrentEntry
    # ------------------------------------------------------------------

    def test_enum_parameter_get_entry_by_name(self):
        """GetEntryByName returns an IEnumEntry for a valid symbolic name."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        entry = p.GetEntryByName("tic")
        self.assertIsInstance(entry, genicam.IEnumEntry)
        self.assertEqual("tic", entry.GetSymbolic())

    def test_enum_parameter_get_entry_by_int_value(self):
        """GetEntry(int) returns the IEnumEntry for the given integer value."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        entry = p.GetEntry(0)
        self.assertIsInstance(entry, genicam.IEnumEntry)
        self.assertEqual("tic", entry.GetSymbolic())

    def test_enum_parameter_get_current_entry(self):
        """GetCurrentEntry returns the IEnumEntry for the current value."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p.SetValue("tac")
        entry = p.GetCurrentEntry()
        self.assertIsInstance(entry, genicam.IEnumEntry)
        self.assertEqual("tac", entry.GetSymbolic())
        entry = p.GetCurrentEntry(False)
        self.assertIsInstance(entry, genicam.IEnumEntry)
        self.assertEqual("tac", entry.GetSymbolic())
        entry = p.GetCurrentEntry(False, False)
        self.assertIsInstance(entry, genicam.IEnumEntry)
        self.assertEqual("tac", entry.GetSymbolic())

    # ------------------------------------------------------------------
    # GetEntryByNameAsParameter / GetCurrentEntryAsParameter
    # ------------------------------------------------------------------

    def test_enum_parameter_get_entry_by_name_as_parameter(self):
        """GetEntryByNameAsParameter returns a CParameter wrapping the entry node."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p.SetValue("tic")

        ent_tic = p.GetEntryByNameAsParameter("tic")
        ent_tac = p.GetEntryByNameAsParameter("tac")

        self.assertIsInstance(ent_tic, pylon.Parameter)
        self.assertTrue(ent_tic.IsValid())
        self.assertFalse(ent_tic.Equals(ent_tac))

    def test_enum_parameter_get_current_entry_as_parameter(self):
        """GetCurrentEntryAsParameter returns a CParameter matching the current entry."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p.SetValue("tic")

        cur = p.GetCurrentEntryAsParameter()
        ent_tic = p.GetEntryByNameAsParameter("tic")
        ent_tac = p.GetEntryByNameAsParameter("tac")

        self.assertIsInstance(cur, pylon.Parameter)
        self.assertTrue(cur.Equals(ent_tic))
        self.assertFalse(cur.Equals(ent_tac))

    def test_enum_parameter_entry_as_parameter_unattached_raises(self):
        """GetEntryByNameAsParameter and GetCurrentEntryAsParameter raise when unattached."""
        p = pylon.EnumParameter()
        with self.assertRaises(Exception): p.GetEntryByNameAsParameter("tic")
        with self.assertRaises(Exception): p.GetCurrentEntryAsParameter()

    # ------------------------------------------------------------------
    # ToString / FromString
    # ------------------------------------------------------------------

    def test_enum_parameter_to_string(self):
        """ToString returns the current symbolic name."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p.SetValue("tic")
        self.assertEqual("tic", p.ToString())

    def test_enum_parameter_to_string_unattached_raises(self):
        """ToString on unattached parameter raises."""
        with self.assertRaises(Exception):
            pylon.EnumParameter().ToString()

    def test_enum_parameter_from_string_valid(self):
        """FromString sets the value for valid symbolic names."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p.FromString("tic")
        self.assertEqual("tic", p.GetValue())
        p.FromString("tac")
        self.assertEqual("tac", p.GetValue())

    def test_enum_parameter_from_string_invalid_raises(self):
        """FromString raises for non-existent or wrongly cased symbolics."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        with self.assertRaises(Exception): p.FromString("")
        with self.assertRaises(Exception): p.FromString("Tic")   # wrong case
        with self.assertRaises(Exception): p.FromString("test")

    def test_enum_parameter_from_string_ro_raises(self):
        """FromString on RO parameter raises; value unchanged."""
        p_ro = pylon.EnumParameter(self.nodemap, "TestEnumerationRO")
        initial = p_ro.GetValue()
        with self.assertRaises(Exception):
            p_ro.FromString("tac")
        self.assertNotEqual("tac", p_ro.GetValue())
        self.assertEqual(initial, p_ro.GetValue())

    def test_enum_parameter_from_string_wo_does_not_raise(self):
        """FromString on WO parameter does not raise."""
        p_wo = pylon.EnumParameter(self.nodemap, "TestEnumerationWO")
        p_wo.FromString("tac")   # must not raise

    # ------------------------------------------------------------------
    # ToStringOrDefault / __str__
    # ------------------------------------------------------------------

    def test_enum_parameter_to_string_or_default(self):
        """ToStringOrDefault returns value string or default."""
        p_unattached = pylon.EnumParameter()
        self.assertEqual("default", p_unattached.ToStringOrDefault("default"))

        p_rw = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p_rw.SetValue("tic")
        self.assertEqual("tic", p_rw.ToStringOrDefault("default"))

        p_wo = pylon.EnumParameter(self.nodemap, "TestEnumerationWO")
        self.assertEqual("default", p_wo.ToStringOrDefault("default"))

    def test_enum_parameter_str(self):
        """__str__ returns the symbolic name, '<not found>', or '<not readable>'."""
        self.assertEqual("<not found>",    str(pylon.EnumParameter()))
        self.assertEqual("<not readable>", str(pylon.EnumParameter(self.nodemap, "TestEnumerationWO")))
        p_rw = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        p_rw.SetValue("tic")
        self.assertEqual("tic", str(p_rw))

    # ------------------------------------------------------------------
    # GetNode / IsValueCacheValid
    # ------------------------------------------------------------------

    def test_enum_parameter_get_node(self):
        """GetNode returns the attached node; unattached raises."""
        node = self.getINode("TestEnumerationRW")
        p = pylon.EnumParameter(node)
        self.assertEqual(node.GetName(), p.GetNode().GetName())
        self.assertEqual(node.GetName(), p.Node.GetName())

        p.Release()
        with self.assertRaises(Exception): p.GetNode()

    def test_enum_parameter_is_value_cache_valid(self):
        """IsValueCacheValid is callable on an attached parameter."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        self.assertIsInstance(p.IsValueCacheValid(), bool)

    # ------------------------------------------------------------------
    # Compatibility with genicam
    # ------------------------------------------------------------------

    def test_genicam_compatibility(self):
        """Parameter can be used wherever genicam interfaces are expected."""
        p = pylon.EnumParameter(self.nodemap, "TestEnumerationRW")
        self.assertIsInstance(p, genicam.IEnumeration)
        self.assertIsInstance(p, genicam.IValue)
        self.assertTrue(genicam.IsReadable(p))
        self.assertTrue(genicam.IsWritable(p))


if __name__ == "__main__":
    unittest.main()
