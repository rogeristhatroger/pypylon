%rename(InterfaceInfo) Pylon::CInterfaceInfo;
%include <pylon/InterfaceInfo.h>;

// CInterfaceInfo-specific properties
ADD_PROP_GETSET(InterfaceInfo, InterfaceID)
