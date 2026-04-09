#!/usr/bin/env python3
"""\
Demonstrate the measurement feature to get statistics about recipe execution.

No camera is used in this sample. A blank test image is created
programmatically and fed to a recipe containing a Stamp Demo vTool via
TriggerUpdate(). The recipe measurement API (StartMeasurement /
StopMeasurement) records per-vTool timing data and produces a CSV report.
"""
import os
import sys
from pypylon import pylon
from pypylon import pylondataprocessing

COUNT_OF_UPDATES = 10

exit_code = 0
try:
    with pylondataprocessing.Recipe() as recipe:
        # Load the recipe file.
        this_dir = os.path.dirname(__file__)
        recipe_file = os.path.join(this_dir, "measurement.precipe")
        recipe.Load(recipe_file)

        # Start the recipe measurement.
        recipe.StartMeasurement()

        # Start the processing.
        recipe.Start()

        # Prepare a blank test image and trigger updates.
        input_image = pylon.PylonImage.Create(
            pylon.PixelType_Mono8, 640, 480
        )
        image_variant = pylondataprocessing.Variant(input_image)

        for i in range(COUNT_OF_UPDATES):
            recipe.TriggerUpdate(
                {"Image": image_variant},
                5000,
                pylon.TimeoutHandling_ThrowException,
            )

        # Stop the processing.
        recipe.Stop()

        # Stop measurement and get the CSV report.
        csv_report = recipe.StopMeasurement()
        print(csv_report)

        # Write the report to disk.
        # You can use the timing analyzer that can found in the pylon software
        # suite data processing samples installation to analyze the measurement.
        report_path = os.path.join(this_dir, "MeasurementReport.csv")
        with open(report_path, "w", encoding="utf-8") as report_file:
            report_file.write(csv_report)
        print(f"Report written to {report_path}")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
