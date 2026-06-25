%rename(TlInfo) Pylon::CTlInfo;
%include <pylon/TlInfo.h>;

// CTlInfo-specific properties
ADD_PROP_GETSET(TlInfo, FileName)
ADD_PROP_GETSET(TlInfo, InfoID)
ADD_PROP_GETSET(TlInfo, ModelName)
ADD_PROP_GETSET(TlInfo, Version)
