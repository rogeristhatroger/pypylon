#!/usr/bin/env python3
"""\
Demonstrate the Camera vTool with parameterization and live test-image toggling
(no license required).

A recipe is loaded and used to enumerate device properties, list available
parameters before and after resource allocation, and grab images. The sample
toggles the test image pattern every 10 frames to demonstrate live parameter
changes during acquisition.
"""
import os
import sys

# For the sake of demonstration, enable two emulated camera devices.
PYLON_CAMEMU = 2
os.environ["PYLON_CAMEMU"] = str(PYLON_CAMEMU)

from pypylon import pylon
from pypylon import pylondataprocessing

COUNT_OF_IMAGES_TO_GRAB = 100

exit_code = 0
try:
    # This object is used for collecting the output data.
    result_collector = pylondataprocessing.GenericOutputObserver()

    # Create a recipe representing a design created using
    # the pylon Viewer Workbench.
    with pylondataprocessing.Recipe() as recipe:
        # Load the recipe file.
        this_dir = os.path.dirname(__file__)
        recipe_file = os.path.join(this_dir, "camera.precipe")
        recipe.Load(recipe_file)

        # List the DeviceInfo properties used for camera selection.
        # Basler recommends using DeviceClass and UserDefinedName to
        # identify a camera.
        # The UserDefinedName is taken from the DeviceUserID parameter
        # that you can set in the pylon Viewer's Features pane.
        # Note: USB cameras must be disconnected and reconnected or reset
        # to provide the new DeviceUserID (USB standard restriction).
        print("Properties used for selecting a camera device")
        device_property_selector = recipe.GetParameter(
            "MyCamera/@vTool/DevicePropertySelector"
        )
        if device_property_selector.IsWritable():
            device_key = recipe.GetParameter("MyCamera/@vTool/DevicePropertyKey")
            device_value = recipe.GetParameter("MyCamera/@vTool/DevicePropertyValue")
            for i in range(device_property_selector.Min, device_property_selector.Max + 1):
                device_property_selector.SetValue(i)
                print(f"  {device_key.GetValue()}={device_value.GetValue()}")
        else:
            print("The first camera device found is used.")

        # For demonstration purposes only
        # Print available parameters.
        print()
        print("Parameter names before allocating resources:")
        for name in recipe.GetAllParameterNames():
            print(f"  {name}")

        # Allocate the required resources. This includes the camera device.
        recipe.PreAllocateResources()

        # For demonstration purposes only
        print()
        print("Selected camera device:")
        param = recipe.GetParameter("MyCamera/@vTool/SelectedDeviceModelName")
        print("  ModelName=" + param.GetValueOrDefault("N/A"))
        param = recipe.GetParameter("MyCamera/@vTool/SelectedDeviceSerialNumber")
        print("  SerialNumber=" + param.GetValueOrDefault("N/A"))
        param = recipe.GetParameter("MyCamera/@vTool/SelectedDeviceVendorName")
        print("  VendorName=" + param.GetValueOrDefault("N/A"))
        param = recipe.GetParameter("MyCamera/@vTool/SelectedDeviceUserDefinedName")
        print("  UserDefinedName=" + param.GetValueOrDefault("N/A"))
        # Parameter path format: <vToolName>/<scope>/<parameterName>
        # MyCamera is the name of the vTool. Available scopes:
        #   @vTool              - vTool parameters
        #   @CameraInstance     - CInstantCamera parameters
        #   @DeviceTransportLayer - transport layer parameters
        #   @CameraDevice       - camera device parameters
        #   @StreamGrabber0     - stream grabber parameters

        # For demonstration purposes only
        # Print available parameters after allocating resources.
        # Now we can access the camera parameters.
        print()
        print("Parameter names after allocating resources:")
        for name in recipe.GetAllParameterNames():
            print(f"  {name}")

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

        # Start the processing. The recipe is triggered internally
        # by the camera vTool for each image.
        recipe.Start()

        test_image_1 = True
        test_image_selector = recipe.GetParameter(
            "MyCamera/@CameraDevice/TestImageSelector"
            "|MyCamera/@CameraDevice/TestPattern"
        )
        for i in range(COUNT_OF_IMAGES_TO_GRAB):
            if result_collector.WaitObject.Wait(5000):
                # Get the recipe-dependent dictionary; key is the pin
                # name, value is a variant object.
                result = result_collector.RetrieveResult()

                image_variant = result["Image"]
                if not image_variant.HasError():
                    image = image_variant.ToImage()
                    img = image.Array
                    print(f"SizeX: {image.Width}; SizeY: {image.Height}; "
                        f"Gray value of first pixel: {img[0, 0]}")
                    image.Release()
                else:
                    print("An error occurred in processing:",
                          image_variant.ErrorDescription)

                # Now let's change a parameter every 10 images
                # while grabbing is active.
                if (i + 1) % 10 == 0:
                    test_image_1 = not test_image_1
                    test_image_selector.SetValue(
                        "Testimage1" if test_image_1 else "Testimage2"
                    )
            else:
                raise RuntimeError("Result timeout")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
