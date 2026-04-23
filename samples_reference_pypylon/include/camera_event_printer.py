"""Camera event handler that prints a message for each event method call."""

from pypylon import pylon
from pypylon import genicam


class CameraEventPrinter(pylon.CameraEventHandler):
    """Log every camera event together with the name of the event data node."""

    def OnCameraEvent(self, camera, user_provided_id, parameter):
        print("OnCameraEvent event for device", camera.DeviceInfo.ModelName)
        print("User provided ID:", user_provided_id)
        print("Event data name:", parameter.GetInfoOrDefault(pylon.ParameterInfo_Name, "<unknown>"))
        print("Event data value:", str(parameter))