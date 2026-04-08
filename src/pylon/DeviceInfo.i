%rename(DeviceInfo) Pylon::CDeviceInfo;

%include <pylon/PylonVersionNumber.h>

%ignore DeviceIdxKey;
%include <pylon/DeviceInfo.h>;

// Read-write properties (public getter + public setter)
ADD_PROP_GETSET(DeviceInfo, SerialNumber)
ADD_PROP_GETSET(DeviceInfo, UserDefinedName)
ADD_PROP_GETSET(DeviceInfo, ModelName)
ADD_PROP_GETSET(DeviceInfo, DeviceVersion)
ADD_PROP_GETSET(DeviceInfo, DeviceFactory)
ADD_PROP_GETSET(DeviceInfo, XMLSource)
ADD_PROP_GETSET(DeviceInfo, InterfaceID)
ADD_PROP_GETSET(DeviceInfo, Address)
ADD_PROP_GETSET(DeviceInfo, IpAddress)
ADD_PROP_GETSET(DeviceInfo, SubnetAddress)
ADD_PROP_GETSET(DeviceInfo, DefaultGateway)
ADD_PROP_GETSET(DeviceInfo, SubnetMask)
ADD_PROP_GETSET(DeviceInfo, PortNr)
ADD_PROP_GETSET(DeviceInfo, MacAddress)
ADD_PROP_GETSET(DeviceInfo, Interface)
ADD_PROP_GETSET(DeviceInfo, IpConfigOptions)
ADD_PROP_GETSET(DeviceInfo, IpConfigCurrent)
ADD_PROP_GETSET(DeviceInfo, PortID)
ADD_PROP_GETSET(DeviceInfo, DeviceID)
ADD_PROP_GETSET(DeviceInfo, InitialBaudRate)
ADD_PROP_GETSET(DeviceInfo, DeviceXMLFileOverride)
ADD_PROP_GETSET(DeviceInfo, DeviceSpecificString)
ADD_PROP_GETSET(DeviceInfo, PortSpecificString)

// Read-only properties (public getter, private setter)
ADD_PROP_GET(DeviceInfo, DeviceGUID)
ADD_PROP_GET(DeviceInfo, ManufacturerInfo)
ADD_PROP_GET(DeviceInfo, ProductId)
ADD_PROP_GET(DeviceInfo, VendorId)
ADD_PROP_GET(DeviceInfo, DriverKeyName)
ADD_PROP_GET(DeviceInfo, UsbDriverType)
ADD_PROP_GET(DeviceInfo, TransferMode)

%pythoncode %{
    CDeviceInfo = DeviceInfo
%}

