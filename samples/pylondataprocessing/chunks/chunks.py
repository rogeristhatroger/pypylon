#!/usr/bin/env python3
"""\
Receive chunks and events from the Camera vTool via BuildersRecipe (no license required).

A recipe with a Camera vTool is loaded using BuildersRecipe. Event and chunk
output pins are configured programmatically. The sample enables available
chunk features on the camera device and turns on Exposure End event
notification. For each grabbed image, chunk data (Timestamp, ExposureTime,
LineStatusAll) and event data (EoxTimestamp, FrameID) are printed.

Note: The pylon camera emulator does not support chunks or events. On devices
without chunk/event support, the corresponding outputs will contain errors.

This sample is designed to work with SFNC 2.x cameras that support chunk and event
features. You can change that by adapting the names of the corresponding camera
parameters, e.g., EventExposureEndTimestamp or ChunkExposureTime.
"""
import os
import sys
from pypylon import pylon
from pypylon import pylondataprocessing

COUNT_OF_IMAGES_TO_GRAB = 3

exit_code = 0
try:
    # This object is used for collecting the output data.
    # It must be created before the recipe so that it outlives it.
    result_collector = pylondataprocessing.GenericOutputObserver()

    # Create a recipe representing a design created using
    # the pylon Viewer Workbench.
    with pylondataprocessing.BuildersRecipe() as recipe:
        # Load the recipe file.
        this_dir = os.path.dirname(__file__)
        recipe_file = os.path.join(this_dir, "chunks.precipe")
        recipe.Load(recipe_file)

        # Add event output pins for end of exposure events.
        # The syntax for an event configuration entry is as follows:
        # <MyPinName>.Type=<MyPinType>.EventName=<CameraEvent>.ValueName=<CameraEventValue>
        # More detailed information about the event configuration can be found here:
        # https://docs.baslerweb.com/camera-vtool#accessing-camera-events
        event_configurations = [
            "EoxTimestamp.Type=Integer.EventName=ExposureEnd.ValueName=EventExposureEndTimestamp",
            "FrameID.Type=Integer.EventName=ExposureEnd.ValueName=EventExposureEndFrameID",
        ]
        for event_index, config in enumerate(event_configurations):
            recipe.GetParameter("MyCamera/@vTool/EventPinAdd").Execute()
            recipe.GetParameter(
                "MyCamera/@vTool/EventPinSelector"
            ).Value = event_index
            recipe.GetParameter(
                "MyCamera/@vTool/EventPinConfiguration"
            ).Value = config
            print(f"Configured event output '{config}'")

        # Enable output of Timestamp, Exposure Time, and Line Status All chunks.
        # The syntax for a chunk configuration entry is as follows:
        # <MyPinName>.Type=<MyPinType>.ValueName=<ChunkName>
        # More detailed information about the chunk configuration can be found here:
        # https://docs.baslerweb.com/camera-vtool#accessing-chunk-data
        chunk_configurations = [
            "ExposureTime.Type=Float.ValueName=ChunkExposureTime",
            "Timestamp.Type=Integer.ValueName=ChunkTimestamp",
            "LineStatusAll.Type=Integer.ValueName=ChunkLineStatusAll",
        ]
        for chunk_index, config in enumerate(chunk_configurations):
            recipe.GetParameter("MyCamera/@vTool/ChunkPinAdd").Execute()
            recipe.GetParameter(
                "MyCamera/@vTool/ChunkPinSelector"
            ).Value = chunk_index
            recipe.GetParameter(
                "MyCamera/@vTool/ChunkPinConfiguration"
            ).Value = config
            print(f"Configured chunk output '{config}'")

        # Allocate the required resources. This includes the camera device.
        recipe.PreAllocateResources()

        # Configure camera after allocation.

        # This sample is designed to work with SFNC 2.x cameras that support
        # chunk and event features
        # You can change that by adapting the names of the corresponding camera
        # parameters, e.g., EventExposureEndTimestamp or ChunkExposureTime.
        chunk_selector = recipe.GetParameter(
            "MyCamera/@CameraDevice/ChunkSelector"
        )
        event_selector = recipe.GetParameter(
            "MyCamera/@CameraDevice/EventSelector"
        )
        if not chunk_selector.IsValid():
            print("The camera doesn't support chunk features")
            sys.exit(0)
        if not event_selector.IsValid():
            print("The camera doesn't support event features")
            sys.exit(0)

        recipe.GetParameter(
            "MyCamera/@CameraDevice/ChunkModeActive"
        ).Value = True

        chunk_enable = recipe.GetParameter(
            "MyCamera/@CameraDevice/ChunkEnable"
        )
        print(chunk_selector.GetSettableValues())
        if chunk_selector.IsReadable():
            for name in chunk_selector.GetSettableValues():
                chunk_selector.Value = name
                chunk_enable.Value = True
                print(f"Enable chunk '{name}'")

        # Turn Exposure End event notification on.
        if (recipe.GetParameter(
                "MyCamera/@CameraDevice/EventSelector"
            ).TrySetValue("ExposureEnd")
                and recipe.GetParameter(
                    "MyCamera/@CameraDevice/EventNotification"
                ).TrySetValue("On")):
            print("Configured event notification for ExposureEnd event")


        # Add outputs and connections for chunk and event data.
        output_connections = [
            ("EoxTimestamp", pylondataprocessing.VariantDataType_Int64,
             "camera_to_eoxtimestamp", "MyCamera.EoxTimestamp"),
            ("FrameID", pylondataprocessing.VariantDataType_Int64,
             "camera_to_frameid", "MyCamera.FrameID"),
            ("ExposureTime", pylondataprocessing.VariantDataType_Float,
             "camera_to_exposuretime", "MyCamera.ExposureTime"),
            ("Timestamp", pylondataprocessing.VariantDataType_Int64,
             "camera_to_timestamp", "MyCamera.Timestamp"),
            ("LineStatusAll", pylondataprocessing.VariantDataType_Int64,
             "camera_to_linestatusall", "MyCamera.LineStatusAll"),
        ]
        for name, dtype, conn_name, source_pin in output_connections:
            recipe.AddOutput(name, dtype)
            recipe.AddConnection(
                conn_name, source_pin, f"<RecipeOutput>.{name}"
            )

        # For demonstration purposes only
        # Print available output names.
        print()
        print("Output names:")
        for name in recipe.GetOutputNames():
            print(f"  {name}")

        # Register the helper object for receiving all output data.
        recipe.RegisterAllOutputsObserver(
            result_collector, pylon.RegistrationMode_Append
        )

        # Start the processing.
        recipe.Start()

        for i in range(COUNT_OF_IMAGES_TO_GRAB):
            if result_collector.WaitObject.Wait(5000):
                result = result_collector.RetrieveResult()

                for key, variant in result.items():
                    print(f"  Output pin '{key}':")
                    if not variant.HasError():
                        if key == "Image":
                            image = variant.ToImage()
                            img = image.Array
                            print(f"SizeX: {image.Width}; SizeY: {image.Height}; "
                                  f"Gray value of first pixel: {img[0, 0]}")
                            pylon.DisplayImage(1, image)
                            image.Release()
                        else:
                            data = variant.ToData()
                            print(data)
                    else:
                        print(f"    Error: {variant.ErrorDescription}")
                print()
            else:
                raise RuntimeError("Result timeout.")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
