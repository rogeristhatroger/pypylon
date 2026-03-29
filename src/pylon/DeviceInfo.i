%rename(DeviceInfo) Pylon::CDeviceInfo;

%include <pylon/PylonVersionNumber.h>

#if PYLON_VERSION_MAJOR < 6

    // swig (3.0.12) cannot handle definitions like:
    // const char* const ManufacturerInfoKey("ManufacturerInfo");
    // Since there is no need for the string constants defined in DeviceInfo.h, we
    // simply rename them and then tell swig to ignore them

    #define ManufacturerInfoKey                 ManufacturerInfoKeyI=
    #define DeviceGUIDKey                       DeviceGUIDKeyI=
    #define VendorIdKey                         VendorIdKeyI=
    #define ProductIdKey                        ProductIdKeyI=
    #define DriverKeyNameKey                    DriverKeyNameKeyI=
    #define UsbDriverTypeKey                    UsbDriverTypeKeyI=
    #define UsbPortVersionBcdKey                UsbPortVersionBcdKeyI=
    #define SpeedSupportBitmaskKey              SpeedSupportBitmaskKeyI=
    #define TransferModeKey                     TransferModeKeyI=
    #define BconAdapterLibraryNameKey           BconAdapterLibraryNameKeyI=
    #define BconAdapterLibraryVersionKey        BconAdapterLibraryVersionKeyI=
    #define BconAdapterLibraryApiVersionKey     BconAdapterLibraryApiVersionKeyI=
    #define SupportedBconAdapterApiVersionKey   SupportedBconAdapterApiVersionKeyI=

    %ignore ManufacturerInfoKeyI;
    %ignore DeviceGUIDKeyI;
    %ignore VendorIdKeyI;
    %ignore ProductIdKeyI;
    %ignore DriverKeyNameKeyI;
    %ignore UsbDriverTypeKeyI;
    %ignore UsbPortVersionBcdKeyI;
    %ignore SpeedSupportBitmaskKeyI;
    %ignore TransferModeKeyI;
    %ignore BconAdapterLibraryNameKeyI;
    %ignore BconAdapterLibraryVersionKeyI;
    %ignore BconAdapterLibraryApiVersionKeyI;
    %ignore SupportedBconAdapterApiVersionKeyI;

#endif


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

