"""\
This unit test checks the Recipe API of pylondataprocessing.

It loads a recipe, registers output/update/event observers, starts processing
and verifies the results delivered through the different observer interfaces.
A Basler Camera Emulation device is required (configured via PYLON_CAMEMU).
"""
import os
num = 1
if int(os.environ.get("PYLON_CAMEMU", 0)) < num:
    os.environ["PYLON_CAMEMU"] = "%d" % num
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import pylon
import unittest


class TWaitObject:
    """Minimal wait object backed by a GenericOutputObserver (test workaround)."""

    def __init__(self):
        self._result_collector = pylondataprocessing.GenericOutputObserver()

    def Wait(self, timeout):
        """Wait until signaled or the timeout (in ms) elapses."""
        return self._result_collector.GetWaitObject().Wait(timeout)

    def Signal(self):
        """Signal the wait object by pushing an empty result."""
        self._result_collector.OutputDataPush(pylondataprocessing.Recipe(), {}, pylondataprocessing.Update(), 0)

    def Reset(self):
        """Reset the wait object to the non-signaled state."""
        self._result_collector.Clear()


class TOutputObserver(pylondataprocessing.OutputObserver):
    """Output observer that records the last pushed result."""

    def __init__(self):
        pylondataprocessing.OutputObserver.__init__(self)
        self.Recipe = None
        self.Value = None
        self.Update = None
        self.UserProvidedID = None

    def OutputDataPush(self, recipe, value, update, user_provided_id):
        # The recipe can only be used in this call, e.g. to get the RecipeContext.
        self.Recipe = recipe
        # Value is converted from CVariantContainer to a dictionary and can be used anywhere.
        self.Value = value
        # The update is only valid in this call, so create a copy to move it elsewhere.
        self.Update = pylondataprocessing.Update(update)
        self.UserProvidedID = user_provided_id


class TUpdateObserver(pylondataprocessing.UpdateObserver):
    """Update observer that records the last completed update and signals a wait object."""

    def __init__(self):
        pylondataprocessing.UpdateObserver.__init__(self)
        self.Recipe = None
        self.Update = None
        self.UserProvidedID = None
        self.WaitObject = TWaitObject()

    def UpdateDone(self, recipe, update, user_provided_id):
        # The recipe can only be used in this call, e.g. to get the RecipeContext.
        self.Recipe = recipe
        # The update is only valid in this call, so create a copy to move it elsewhere.
        self.Update = pylondataprocessing.Update(update)
        self.UserProvidedID = user_provided_id
        self.WaitObject.Signal()


class TEventObserver(pylondataprocessing.EventObserver):
    """Event observer that records signaled events and signals a wait object."""

    def __init__(self):
        pylondataprocessing.EventObserver.__init__(self)
        self.Recipe = None
        self.Events = None
        self.WaitObject = TWaitObject()

    def OnEventSignaled(self, recipe, events):
        # The recipe can only be used in this call, e.g. to get the RecipeContext.
        self.Recipe = recipe
        # Events is converted to a list and can be used anywhere.
        self.Events = events
        self.WaitObject.Signal()
        return True  # superfluous in C++ API, has been removed in data processing version 2.0/pylon 7.5


class RecipeTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Full processing flow
    # ------------------------------------------------------------------

    def test_flow(self):
        """A loaded recipe delivers results to registered observers and supports triggered updates."""
        this_dir = os.path.dirname(__file__)
        recipe_filename = os.path.join(this_dir, 'recipe_test.precipe')

        # create observer objects
        result_collector = pylondataprocessing.GenericOutputObserver()
        event_observer = TEventObserver()

        # create
        with pylondataprocessing.Recipe() as recipe:
            self.assertFalse(recipe.IsLoaded())
            self.assertFalse(recipe.IsStarted())
            self.assertFalse(recipe.HasInput("Image"))
            self.assertFalse(recipe.HasOutput("Image"))
            #
            # register event observer
            recipe.RegisterEventObserver(event_observer)
            #
            # recipe context
            recipe.SetRecipeContext(85)
            self.assertEqual(recipe.GetRecipeContext(), 85)
            self.assertEqual(recipe.RecipeContext, 85)
            #
            # load
            recipe.Load(recipe_filename)
            self.assertTrue(recipe.IsLoaded())
            self.assertFalse(recipe.IsStarted())
            self.assertTrue(recipe.HasInput("Image"))
            self.assertTrue(recipe.HasOutput("Image"))
            self.assertEqual(recipe.GetInputType("Image"), pylondataprocessing.VariantDataType_PylonImage)
            self.assertEqual(recipe.GetOutputType("Image"), pylondataprocessing.VariantDataType_PylonImage)
            #
            # parameters
            self.assertTrue(recipe.ContainsParameter("ImageLoading/@vTool/SourcePath"))
            self.assertFalse(recipe.ContainsParameter("ImageLoading/@vTool/TestNotThere"))
            all_parameter_names = recipe.GetAllParameterNames()
            self.assertTrue("ImageLoading/@vTool/SourcePath" in all_parameter_names)
            recipe.GetParameter("ImageLoading/@vTool/SourcePath").SetValue(this_dir)
            self.assertIsInstance(recipe.GetParameter("ImageLoading/@vTool/SourcePath"), pylon.StringParameter)
            #
            # check get output names
            output_names = recipe.GetOutputNames()
            self.assertEqual(len(output_names), 5)
            self.assertIs(type(output_names), tuple)
            #
            # preallocate
            recipe.PreAllocateResources()
            #
            # register output sink
            recipe.RegisterAllOutputsObserver(result_collector, pylon.RegistrationMode_Append, 85)
            #
            # unregister output sink
            self.assertTrue(recipe.UnregisterOutputObserver(result_collector, 85))
            self.assertFalse(recipe.UnregisterOutputObserver(result_collector, 85))
            #
            # register output sink v2
            recipe.RegisterOutputObserver(
                ["Image", "ImageLoader", "ImagePath", "RunCount"], result_collector, pylon.RegistrationMode_Append, 85)
            # start
            recipe.Start()
            self.assertTrue(recipe.IsLoaded())
            self.assertTrue(recipe.IsStarted())
            #
            # result 1
            self.assertTrue(result_collector.GetWaitObject().Wait(5000))
            full_result_1 = result_collector.RetrieveFullResult()
            self.assertTrue(full_result_1.Update.IsValid())
            self.assertEqual(full_result_1.UserProvidedID, 85)
            self.assertTrue(full_result_1.Container["Image"].ToImage().IsValid())
            self.assertTrue(full_result_1.Container["ImageLoader"].ToImage().IsValid())
            self.assertEqual(full_result_1.Container["ImagePath"].DataType, pylondataprocessing.VariantDataType_String)
            self.assertTrue(full_result_1.Container["RunCount"].ToInt64(), 1)
            #
            # result 2
            self.assertTrue(result_collector.GetWaitObject().Wait(5000))
            full_result_2 = result_collector.RetrieveFullResult()
            self.assertTrue(full_result_1.Update < full_result_2.Update)
            self.assertTrue(full_result_1.Update != full_result_2.Update)
            self.assertTrue(full_result_2.Update.IsValid())
            self.assertEqual(full_result_2.UserProvidedID, 85)
            self.assertTrue(full_result_2.Container["Image"].ToImage().IsValid())
            self.assertTrue(full_result_2.Container["ImageLoader"].ToImage().IsValid())
            self.assertEqual(full_result_2.Container["ImagePath"].DataType, pylondataprocessing.VariantDataType_String)
            self.assertTrue(full_result_2.Container["RunCount"].ToInt64(), 1)
            #
            # result 3
            self.assertTrue(result_collector.GetWaitObject().Wait(5000))
            result = result_collector.RetrieveResult()
            self.assertTrue(result["Image"].ToImage().IsValid())
            self.assertTrue(result["ImageLoader"].ToImage().IsValid())
            self.assertEqual(result["ImagePath"].DataType, pylondataprocessing.VariantDataType_String)
            self.assertTrue(result["RunCount"].ToInt64(), 1)
            #
            # loader vTool stopped, it is configured to trigger updates for 3 images
            self.assertFalse(result_collector.GetWaitObject().Wait(100))
            self.assertTrue(recipe.CanTriggerUpdate())
            #
            # unregister output sink
            self.assertTrue(recipe.UnregisterOutputObserver(result_collector, 85))
            #
            # TriggerUpdateAsync
            output_observer = TOutputObserver()
            update_observer = TUpdateObserver()
            recipe.RegisterOutputObserver(["ImageConverter2"], output_observer, pylon.RegistrationMode_Append, 83)
            recipe.RegisterOutputObserver(["ImageConverter2"], result_collector, pylon.RegistrationMode_Append, 83)
            async_update = recipe.TriggerUpdateAsync({"Image": result["Image"]}, update_observer, 47)
            self.assertTrue(result_collector.GetWaitObject().Wait(5000))
            self.assertTrue(update_observer.WaitObject.Wait(5000))  # the update may finish later, depends on the recipe
            self.assertTrue(recipe.UnregisterOutputObserver(result_collector, 83))
            self.assertTrue(recipe.UnregisterOutputObserver(output_observer, 83))
            self.assertEqual(update_observer.UserProvidedID, 47)
            self.assertEqual(output_observer.UserProvidedID, 83)
            self.assertTrue(async_update == update_observer.Update)
            self.assertTrue(async_update == output_observer.Update)
            self.assertTrue(output_observer.Value["ImageConverter2"].ToImage().IsValid())
            #
            # TriggerUpdate
            output_observer = TOutputObserver()
            update_observer = TUpdateObserver()
            recipe.RegisterOutputObserver(["ImageConverter2"], output_observer, pylon.RegistrationMode_Append, 83)
            sync_update = recipe.TriggerUpdate(
                {"Image": result["Image"]}, 1000, pylon.TimeoutHandling_ThrowException, update_observer, 48)
            self.assertTrue(update_observer.WaitObject.Wait(5000))  # the update may finish later, depends on the recipe
            self.assertEqual(update_observer.UserProvidedID, 48)
            self.assertEqual(output_observer.UserProvidedID, 83)
            self.assertTrue(sync_update == update_observer.Update)
            self.assertTrue(sync_update == output_observer.Update)
            self.assertTrue(output_observer.Value["ImageConverter2"].ToImage().IsValid())
            #
            # stop
            recipe.Stop()
            self.assertTrue(recipe.IsLoaded())
            self.assertFalse(recipe.IsStarted())
            recipe.Stop(100)
            #
            # deallocate
            recipe.DeallocateResources()
            #
            # unload
            recipe.Unload()
            self.assertFalse(recipe.IsLoaded())
            self.assertFalse(recipe.IsStarted())
            self.assertFalse(recipe.HasInput("Image"))
            self.assertFalse(recipe.HasOutput("Image"))
            #
            # unregister event observer, info: this is done by __exit__ too
            recipe.UnregisterEventObserver()

    # ------------------------------------------------------------------
    # Loading from binary
    # ------------------------------------------------------------------

    def test_load_from_binary(self):
        """LoadFromBinary loads a recipe from in-memory file content."""
        this_dir = os.path.dirname(__file__)
        recipe_filename = os.path.join(this_dir, 'recipe_test.precipe')
        with open(recipe_filename, mode='rb') as file:
            file_content = file.read()
        with pylondataprocessing.Recipe() as recipe:
            recipe.LoadFromBinary(file_content)
            self.assertTrue(recipe.IsLoaded())
            recipe.Unload()
            self.assertFalse(recipe.IsLoaded())
            recipe.LoadFromBinary(file_content, this_dir)
            self.assertTrue(recipe.IsLoaded())
            recipe.Unload()
            self.assertFalse(recipe.IsLoaded())

    # ------------------------------------------------------------------
    # Event observer
    # ------------------------------------------------------------------

    def test_event_observer(self):
        """A registered event observer receives start/stop and error events."""
        this_dir = os.path.dirname(__file__)
        recipe_filename = os.path.join(this_dir, 'recipe_eventobserver_test.precipe')
        with pylondataprocessing.Recipe() as recipe:
            event_observer = TEventObserver()
            recipe.RegisterEventObserver(event_observer)
            recipe.Load(recipe_filename)
            recipe.Start()
            self.assertTrue(recipe.ContainsParameter("Camera/@CameraDevice/FirePnPCallback"))
            # Trigger a camera vTool error.
            recipe.GetParameter("Camera/@CameraDevice/FirePnPCallback").Execute()
            self.assertTrue(event_observer.WaitObject.Wait(500))
            self.assertEqual(len(event_observer.Events), 1)
            self.assertEqual(event_observer.Events[0].EventType, 1)
            self.assertEqual(event_observer.Events[0].EventSourceName, "Camera")
            event_observer.WaitObject.Reset()
            recipe.Stop()
            self.assertTrue(event_observer.WaitObject.Wait(500))
            self.assertEqual(len(event_observer.Events), 1)
            self.assertEqual(event_observer.Events[0].EventType, 2)
            self.assertEqual(event_observer.Events[0].EventSourceName, "Camera")
            self.assertTrue(event_observer.WaitObject.Wait(500))

if __name__ == "__main__":
    unittest.main()
