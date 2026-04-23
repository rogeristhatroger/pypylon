"""Configuration event handler that prints a message for each event method call."""

from pypylon import pylon


class ConfigurationEventPrinter(pylon.ConfigurationEventHandler):
    """Log every InstantCamera lifecycle event."""

    def OnAttach(self, camera):
        print("OnAttach event")

    def OnAttached(self, camera):
        print("OnAttached event for device", camera.DeviceInfo.ModelName)

    def OnOpen(self, camera):
        print("OnOpen event for device", camera.DeviceInfo.ModelName)

    def OnOpened(self, camera):
        print("OnOpened event for device", camera.DeviceInfo.ModelName)

    def OnGrabStart(self, camera):
        print("OnGrabStart event for device", camera.DeviceInfo.ModelName)

    def OnGrabStarted(self, camera):
        print("OnGrabStarted event for device", camera.DeviceInfo.ModelName)

    def OnGrabStop(self, camera):
        print("OnGrabStop event for device", camera.DeviceInfo.ModelName)

    def OnGrabStopped(self, camera):
        print("OnGrabStopped event for device", camera.DeviceInfo.ModelName)

    def OnClose(self, camera):
        print("OnClose event for device", camera.DeviceInfo.ModelName)

    def OnClosed(self, camera):
        print("OnClosed event for device", camera.DeviceInfo.ModelName)

    def OnDestroy(self, camera):
        print("OnDestroy event for device", camera.DeviceInfo.ModelName)

    def OnDestroyed(self, camera):
        print("OnDestroyed event")

    def OnDetach(self, camera):
        print("OnDetach event for device", camera.DeviceInfo.ModelName)

    def OnDetached(self, camera):
        print("OnDetached event for device", camera.DeviceInfo.ModelName)

    def OnGrabError(self, camera, error_message):
        print("OnGrabError event for device", camera.DeviceInfo.ModelName)
        print("Error Message:", error_message)

    def OnCameraDeviceRemoved(self, camera):
        print("OnCameraDeviceRemoved event for device", camera.DeviceInfo.ModelName)
