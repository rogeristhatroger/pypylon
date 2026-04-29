// PylonDevice is a handle-type object.
// It carries no standalone functionality of its own, so all of its methods are ignored.
// The only exception is GetDeviceInfo, which is exposed as a Python property
// and allows users to retrieve information about the device the handle refers to.

%rename (PylonDevice) Pylon::IPylonDevice;

%ignore Pylon::IPylonDevice::Open;
%ignore Pylon::IPylonDevice::Close;
%ignore Pylon::IPylonDevice::IsOpen;
%ignore Pylon::IPylonDevice::AccessMode;
%ignore Pylon::IPylonDevice::GetNumStreamGrabberChannels;
%ignore Pylon::IPylonDevice::GetStreamGrabber;
%ignore Pylon::IPylonDevice::GetEventGrabber;
%ignore Pylon::IPylonDevice::GetNodeMap;
%ignore Pylon::IPylonDevice::GetTLNodeMap;
%ignore Pylon::IPylonDevice::CreateChunkParser;
%ignore Pylon::IPylonDevice::DestroyChunkParser;
%ignore Pylon::IPylonDevice::CreateEventAdapter;
%ignore Pylon::IPylonDevice::DestroyEventAdapter;
%ignore Pylon::IPylonDevice::CreateSelfReliantChunkParser;
%ignore Pylon::IPylonDevice::DestroySelfReliantChunkParser;
%ignore Pylon::IPylonDevice::RegisterRemovalCallback;
%ignore Pylon::IPylonDevice::DeregisterRemovalCallback;

%extend Pylon::IPylonDevice {
    const Pylon::CDeviceInfo& _GetDeviceInfo() const {
        return $self->GetDeviceInfo();
    }
%pythoncode %{
    @property
    def DeviceInfo(self):
        return self._GetDeviceInfo()
%}
}

%ignore Pylon::IDevice;
%include <pylon/Device.h>

%pythoncode %{
    IPylonDevice = PylonDevice
%}
