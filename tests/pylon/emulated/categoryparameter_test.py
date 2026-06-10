"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/CategoryParameter.i.
"""
from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest

# Category nodes defined in the test nodemap
CATEGORY_ROOT = "Root"
CATEGORY_NESTED = "NestedCategory"

# Root contains: NestedCategory, TestFloat, TestInt  (3 direct features)
ROOT_FEATURE_COUNT = 3
# NestedCategory contains: TestEnumerationRW  (1 direct feature)
NESTED_FEATURE_COUNT = 1


class CategoryParameterTestSuite(PylonParameterTestCase):

    # Helper: obtain ICategory via nodemap auto-downcast
    def _get_icategory(self, name):
        return self.nodemap.GetNode(name)

    # ------------------------------------------------------------------
    # Construction / Attach / Release
    # ------------------------------------------------------------------

    def test_category_parameter_construction_default(self):
        """Default construction produces an invalid parameter."""
        p = pylon.CategoryParameter()
        self.assertFalse(p.IsValid())

    def test_category_parameter_construction_from_inode_matching(self):
        """Construction from a matching INode (category) attaches and validates."""
        node = self.getINode(CATEGORY_ROOT)
        p = pylon.CategoryParameter(node)
        self.assertTrue(p.IsValid())

    def test_category_parameter_construction_from_inode_wrong_type(self):
        """Construction from a non-category INode yields an invalid parameter."""
        node_int = self.getINode("TestInt")
        p = pylon.CategoryParameter(node_int)
        self.assertFalse(p.IsValid())

    def test_category_parameter_construction_from_icategory(self):
        """Construction from a GenApi ICategory object attaches and validates."""
        icategory = self._get_icategory(CATEGORY_ROOT)
        self.assertIsInstance(icategory, genicam.ICategory)
        p = pylon.CategoryParameter(icategory)
        self.assertTrue(p.IsValid())

    def test_category_parameter_construction_from_nodemap_name(self):
        """Construction from nodemap + name attaches and validates."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(self.getINode(CATEGORY_ROOT)))
        self.assertFalse(p.Equals(self.getINode(CATEGORY_NESTED)))

    def test_category_parameter_construction_from_nonexistent_name(self):
        """Construction from nodemap + non-existent name produces an invalid parameter."""
        p = pylon.CategoryParameter(self.nodemap, "CategoryDoesNotExist")
        self.assertFalse(p.IsValid())

    def test_category_parameter_construction_copy(self):
        """Copy construction produces a valid, equal parameter."""
        p1 = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        p2 = pylon.CategoryParameter(p1)
        self.assertTrue(p1.IsValid())
        self.assertTrue(p2.IsValid())
        self.assertTrue(p1.Equals(p2))

    def test_category_parameter_attach_from_inode(self):
        """Attach from INode sets validity and the correct node."""
        node_root = self.getINode(CATEGORY_ROOT)
        node_nested = self.getINode(CATEGORY_NESTED)

        p = pylon.CategoryParameter()
        self.assertFalse(p.IsValid())

        result = p.Attach(node_root)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(node_root))
        self.assertFalse(p.Equals(node_nested))

        result = p.Attach(node_nested)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(node_nested))
        self.assertFalse(p.Equals(node_root))

    def test_category_parameter_attach_from_icategory(self):
        """Attach from GenApi ICategory attaches correctly."""
        icategory = self._get_icategory(CATEGORY_ROOT)
        p = pylon.CategoryParameter()
        result = p.Attach(icategory)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

    def test_category_parameter_attach_from_nodemap_name(self):
        """Attach from nodemap + name; non-existent name returns False."""
        p = pylon.CategoryParameter()

        result = p.Attach(self.nodemap, CATEGORY_ROOT)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, CATEGORY_NESTED)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "CategoryDoesNotExist")
        self.assertFalse(result)

    def test_category_parameter_release(self):
        """Release makes parameter invalid."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    # ------------------------------------------------------------------
    # Equals
    # ------------------------------------------------------------------

    def test_category_parameter_equals_parameter(self):
        """Equals between two CategoryParameters."""
        node_root = self.nodemap.GetNode(CATEGORY_ROOT)
        node_nested = self.nodemap.GetNode(CATEGORY_NESTED)

        p1 = pylon.CategoryParameter(node_root)
        p2 = pylon.CategoryParameter(node_root)
        p3 = pylon.CategoryParameter(node_nested)
        p_empty1 = pylon.CategoryParameter()
        p_empty2 = pylon.CategoryParameter()

        self.assertTrue(p_empty1.Equals(p_empty2))
        self.assertTrue(p1.Equals(p2))
        self.assertTrue(p2.Equals(p1))
        self.assertFalse(p1.Equals(p3))
        self.assertFalse(p3.Equals(p1))
        self.assertFalse(p1.Equals(p_empty1))
        self.assertFalse(p_empty1.Equals(p1))

    def test_category_parameter_equals_inode(self):
        """Equals against INode and None."""
        node_root = self.getINode(CATEGORY_ROOT)
        node_nested = self.getINode(CATEGORY_NESTED)

        p_empty = pylon.CategoryParameter()
        p = pylon.CategoryParameter(node_root)

        self.assertTrue(p_empty.Equals(None))
        self.assertFalse(p_empty.Equals(node_root))
        self.assertTrue(p.Equals(node_root))
        self.assertFalse(p.Equals(node_nested))
        self.assertFalse(p.Equals(None))

    def test_category_parameter_equals_icategory(self):
        """Equals against a GenApi ICategory object."""
        icategory_root = self._get_icategory(CATEGORY_ROOT)
        icategory_nested = self._get_icategory(CATEGORY_NESTED)

        p_empty = pylon.CategoryParameter()
        p = pylon.CategoryParameter(icategory_root)

        self.assertTrue(p.Equals(icategory_root))
        self.assertFalse(p.Equals(icategory_nested))
        self.assertFalse(p_empty.Equals(icategory_root))

    # ------------------------------------------------------------------
    # IsValid / IsReadable / IsWritable / GetAccessMode
    # ------------------------------------------------------------------

    def test_category_parameter_is_valid(self):
        """IsValid reflects attachment state."""
        p = pylon.CategoryParameter()
        self.assertFalse(p.IsValid())
        p.Attach(self.nodemap, CATEGORY_ROOT)
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    def test_category_parameter_is_readable_writable(self):
        """Category nodes are readable but not directly writable."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        self.assertTrue(p.IsReadable())
        self.assertFalse(p.IsWritable())

    def test_category_parameter_is_readable_writable_unattached(self):
        """An unattached parameter reports not readable and not writable."""
        p = pylon.CategoryParameter()
        self.assertFalse(p.IsReadable())
        self.assertFalse(p.IsWritable())

    def test_category_parameter_get_access_mode_unattached(self):
        """GetAccessMode returns genicam.NI when unattached."""
        self.assertEqual(genicam.NI, pylon.CategoryParameter().GetAccessMode())

    # ------------------------------------------------------------------
    # Unattached – value operations must raise
    # ------------------------------------------------------------------

    def test_category_parameter_unattached_get_features_raises(self):
        """GetFeatures on an unattached parameter raises."""
        p = pylon.CategoryParameter()
        with self.assertRaises(Exception):
            p.GetFeatures()

    # ------------------------------------------------------------------
    # ICategory.GetFeatures
    # ------------------------------------------------------------------

    def test_category_parameter_get_features_root(self):
        """GetFeatures on Root returns a tuple with the expected number of features."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        features = p.GetFeatures()
        self.assertIsInstance(features, tuple)
        self.assertEqual(ROOT_FEATURE_COUNT, len(features))

    def test_category_parameter_get_features_nested(self):
        """GetFeatures on NestedCategory returns the single sub-feature."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_NESTED)
        features = p.GetFeatures()
        self.assertIsInstance(features, tuple)
        self.assertEqual(NESTED_FEATURE_COUNT, len(features))

    def test_category_parameter_get_features_returns_parameters(self):
        """Each feature returned by GetFeatures is a pylon Parameter subtype."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        for feature in p.GetFeatures():
            self.assertIsInstance(feature, pylon.Parameter)

    def test_category_parameter_get_features_nested_contains_enum(self):
        """NestedCategory's single feature is TestEnumerationRW (an EnumParameter)."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_NESTED)
        features = p.GetFeatures()
        self.assertEqual(1, len(features))
        self.assertIsInstance(features[0], pylon.EnumParameter)

    def test_category_parameter_get_features_root_contains_nested_category(self):
        """Root's features include NestedCategory wrapped as a CategoryParameter."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        features = p.GetFeatures()
        category_features = [f for f in features if isinstance(f, pylon.CategoryParameter)]
        self.assertEqual(1, len(category_features))
        self.assertTrue(category_features[0].Equals(self.getINode(CATEGORY_NESTED)))

    # ------------------------------------------------------------------
    # Features property
    # ------------------------------------------------------------------

    def test_category_parameter_features_property_equals_get_features(self):
        """Features property returns the same result as GetFeatures()."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        self.assertEqual(len(p.GetFeatures()), len(p.Features))
        for f_method, f_prop in zip(p.GetFeatures(), p.Features):
            self.assertEqual(f_method.GetNode().GetName(), f_prop.GetNode().GetName())

    def test_category_parameter_features_property_is_tuple(self):
        """Features property returns a tuple of pylon Parameter objects."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        features = p.Features
        self.assertIsInstance(features, tuple)
        self.assertGreater(len(features), 0)
        for f in features:
            self.assertIsInstance(f, pylon.Parameter)

    def test_category_parameter_features_property_nested(self):
        """Features property on NestedCategory equals GetFeatures()."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_NESTED)
        self.assertEqual(len(p.GetFeatures()), len(p.Features))
        self.assertIsInstance(p.Features, tuple)

    # ------------------------------------------------------------------
    # ToString / ToStringOrDefault / __str__
    # ------------------------------------------------------------------

    def test_category_parameter_to_string_unattached_raises(self):
        """ToString on an unattached parameter raises."""
        with self.assertRaises(Exception):
            pylon.CategoryParameter().ToString()

    def test_category_parameter_to_string(self):
        """ToString on an unattached parameter raises."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        self.assertEqual(p.ToString(), CATEGORY_ROOT)
        self.assertEqual(str(p), CATEGORY_ROOT)

    def test_category_parameter_to_string_or_default(self):
        """ToStringOrDefault returns the default when unattached."""
        p_unattached = pylon.CategoryParameter()
        self.assertEqual("default", p_unattached.ToStringOrDefault("default"))

    def test_category_parameter_str_unattached(self):
        """__str__ returns '<not found>' when unattached."""
        self.assertEqual("<not found>", str(pylon.CategoryParameter()))

    # ------------------------------------------------------------------
    # GetNode / IsValueCacheValid
    # ------------------------------------------------------------------

    def test_category_parameter_get_node(self):
        """GetNode returns the attached node; unattached raises."""
        node = self.getINode(CATEGORY_ROOT)
        p = pylon.CategoryParameter(node)
        self.assertEqual(node.GetName(), p.GetNode().GetName())
        self.assertEqual(node.GetName(), p.Node.GetName())

        p.Release()
        with self.assertRaises(Exception):
            p.GetNode()

    def test_category_parameter_is_value_cache_valid(self):
        """IsValueCacheValid is callable on an attached parameter."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        self.assertIsInstance(p.IsValueCacheValid(), bool)

    # ------------------------------------------------------------------
    # GetInfo / GetInfoOrDefault
    # ------------------------------------------------------------------

    def test_category_parameter_get_info_name(self):
        """GetInfo with ParameterInfo_Name returns the node name."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        self.assertEqual(CATEGORY_ROOT, p.GetInfo(pylon.ParameterInfo_Name))

    def test_category_parameter_get_info_or_default_unattached(self):
        """GetInfoOrDefault returns the default when unattached."""
        p = pylon.CategoryParameter()
        self.assertEqual("fallback", p.GetInfoOrDefault(pylon.ParameterInfo_Name, "fallback"))

    # ------------------------------------------------------------------
    # Compatibility with genicam
    # ------------------------------------------------------------------

    def test_genicam_compatibility(self):
        """CategoryParameter can be used wherever genicam interfaces are expected."""
        p = pylon.CategoryParameter(self.nodemap, CATEGORY_ROOT)
        self.assertIsInstance(p, genicam.ICategory)
        self.assertIsInstance(p, genicam.IValue)

if __name__ == "__main__":
    unittest.main()

