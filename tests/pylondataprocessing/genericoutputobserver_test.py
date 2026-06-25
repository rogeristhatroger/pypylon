"""\
This unit test checks the GenericOutputObserver bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class GenericOutputObserverTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_init(self):
        """A fresh observer has no results and exposes its container as a dict."""
        result = pylondataprocessing.GenericOutputObserverResult()
        self.assertEqual(result.Update, pylondataprocessing.Update())
        self.assertEqual(result.UserProvidedID, 0)
        self.assertIs(type(result.Container), dict)
        self.assertIs(type(result.GetContainer()), dict)  # do not use

        observer = pylondataprocessing.GenericOutputObserver()
        self.assertFalse(observer.GetWaitObject().Wait(0))
        self.assertEqual(observer.GetNumResults(), 0)
        self.assertIs(type(observer.RetrieveFullResult().Container), dict)
        self.assertIs(type(observer.RetrieveResult()), dict)
        self.assertEqual(len(observer.RetrieveFullResult().Container), 0)
        self.assertEqual(len(observer.RetrieveResult()), 0)
        observer.Clear()

    # ------------------------------------------------------------------
    # Pushing results
    # ------------------------------------------------------------------

    def test_push(self):
        """OutputDataPush queues results that can be retrieved and cleared."""
        input_data = {"Image": pylondataprocessing.Variant(pylondataprocessing.VariantDataType_PylonImage)}
        observer = pylondataprocessing.GenericOutputObserver()
        recipe = pylondataprocessing.Recipe()
        recipe.SetRecipeContext(17)
        observer.OutputDataPush(recipe, input_data, pylondataprocessing.Update(), 892)
        self.assertTrue(observer.GetWaitObject().Wait(0))
        self.assertEqual(observer.GetNumResults(), 1)
        full_result = observer.RetrieveFullResult()
        self.assertFalse(observer.GetWaitObject().Wait(0))
        self.assertEqual(observer.GetNumResults(), 0)
        self.assertIs(type(full_result.Container), dict)
        self.assertEqual(len(full_result.Container), 1)
        self.assertEqual(full_result.UserProvidedID, 892)
        self.assertFalse(full_result.Update.IsValid())
        self.assertEqual(full_result.RecipeContext, 17)
        observer.OutputDataPush(pylondataprocessing.Recipe(), input_data, pylondataprocessing.Update(), 892)
        self.assertTrue(observer.GetWaitObject().Wait(0))
        self.assertEqual(observer.GetNumResults(), 1)
        plain_result = observer.RetrieveResult()
        self.assertFalse(observer.GetWaitObject().Wait(0))
        self.assertEqual(observer.GetNumResults(), 0)
        self.assertEqual(plain_result, input_data)
        observer.OutputDataPush(pylondataprocessing.Recipe(), input_data, pylondataprocessing.Update(), 892)
        self.assertTrue(observer.GetWaitObject().Wait(0))
        self.assertTrue(observer.WaitObject.Wait(0))
        self.assertEqual(observer.GetNumResults(), 1)
        self.assertEqual(observer.NumResults, 1)
        observer.Clear()
        self.assertFalse(observer.GetWaitObject().Wait(0))
        self.assertEqual(observer.GetNumResults(), 0)


if __name__ == "__main__":
    unittest.main()
