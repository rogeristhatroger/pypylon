"""Image event handler that prints a message for each event method call."""

from pypylon import pylon


class ImageEventPrinter(pylon.ImageEventHandler):
    """Log grabbed and skipped image events for an InstantCamera."""

    def OnImagesSkipped(self, camera, count_of_skipped_images):
        print("OnImagesSkipped event for device", camera.DeviceInfo.ModelName)
        print(count_of_skipped_images, "images have been skipped.")
        print()

    def OnImageGrabbed(self, camera, grab_result):
        print("OnImageGrabbed event for device", camera.DeviceInfo.ModelName)

        if grab_result.GrabSucceeded():
            print("SizeX:", grab_result.Width)
            print("SizeY:", grab_result.Height)
            image = grab_result.Array
            print("Gray values of first row:", image[0])
            print()
        else:
            print(
                "Error:",
                f"{grab_result.ErrorCode:#x}",
                grab_result.ErrorDescription
            )
