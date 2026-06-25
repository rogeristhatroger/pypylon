"""\
This unit test checks the TransformationData type bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class TransformationDataTestSuite(PylonDataProcessingTestCase):

    def assert_all_zero(self, transformation_data):
        """Assert that every entry of the given transformation data is zero."""
        for row_index in range(transformation_data.RowCount):
            for column_index in range(transformation_data.ColumnCount):
                self.assertEqual(transformation_data.GetEntry(column_index, row_index), 0.0)

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_init(self):
        """TransformationData exposes column/row counts as methods and properties."""
        empty_data = pylondataprocessing.TransformationData()
        self.assertEqual(empty_data.GetColumnCount(), 0)
        self.assertEqual(empty_data.GetRowCount(), 0)
        self.assertEqual(empty_data.ColumnCount, 0)
        self.assertEqual(empty_data.RowCount, 0)
        self.assertEqual(empty_data.IsValid(), False)
        sized_data = pylondataprocessing.TransformationData(3, 2)
        self.assertEqual(sized_data.GetColumnCount(), 3)
        self.assertEqual(sized_data.GetRowCount(), 2)
        self.assertEqual(sized_data.ColumnCount, 3)
        self.assertEqual(sized_data.RowCount, 2)
        self.assertEqual(sized_data.IsValid(), True)
        self.assert_all_zero(sized_data)

    # ------------------------------------------------------------------
    # Reset / entry access
    # ------------------------------------------------------------------

    def test_reset_and_set(self):
        """Reset resizes the matrix and SetEntry/GetEntry access individual entries."""
        transformation_data = pylondataprocessing.TransformationData()
        transformation_data.Reset(3, 2)
        self.assertEqual(transformation_data.GetColumnCount(), 3)
        self.assertEqual(transformation_data.GetRowCount(), 2)
        self.assertEqual(transformation_data.ColumnCount, 3)
        self.assertEqual(transformation_data.RowCount, 2)
        self.assertEqual(transformation_data.IsValid(), True)
        self.assert_all_zero(transformation_data)
        transformation_data.SetEntry(0, 0, 1.2)
        self.assertEqual(transformation_data.GetEntry(0, 0), 1.2)
        transformation_data.Reset(4, 3)
        self.assertEqual(transformation_data.GetColumnCount(), 4)
        self.assertEqual(transformation_data.GetRowCount(), 3)
        self.assertEqual(transformation_data.ColumnCount, 4)
        self.assertEqual(transformation_data.RowCount, 3)
        self.assertEqual(transformation_data.IsValid(), True)
        self.assert_all_zero(transformation_data)
        test_value = 1.1
        for row_index in range(transformation_data.RowCount):
            for column_index in range(transformation_data.ColumnCount):
                transformation_data.SetEntry(column_index, row_index, test_value)
                test_value += 1.0
        self.assertEqual(test_value, 13.1)
        test_value = 1.1
        for row_index in range(transformation_data.RowCount):
            for column_index in range(transformation_data.ColumnCount):
                self.assertEqual(transformation_data.GetEntry(column_index, row_index), test_value)
                test_value += 1.0
        self.assertEqual(test_value, 13.1)

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def test_str(self):
        """str(TransformationData) renders rows separated by newlines."""
        transformation_data = pylondataprocessing.TransformationData(3, 2)
        test_value = 1.1
        for row_index in range(transformation_data.RowCount):
            for column_index in range(transformation_data.ColumnCount):
                transformation_data.SetEntry(column_index, row_index, test_value)
                test_value += 1.0
        self.assertEqual(test_value, 7.1)
        self.assertEqual(str(transformation_data), "1.1, 2.1, 3.1\n4.1, 5.1, 6.1")


if __name__ == "__main__":
    unittest.main()
