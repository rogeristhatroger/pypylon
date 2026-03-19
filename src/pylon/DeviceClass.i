
#include <pylon/DeviceClass.h>
    namespace Pylon{
        %immutable;
        extern const char * const BaslerCamEmuDeviceClass;
        extern const char * const BaslerGigEDeviceClass;
        extern const char * const BaslerIpCamDeviceClass;
        extern const char * const BaslerCameraLinkDeviceClass;
        extern const char * const BaslerGenTlDeviceClassPrefix;
        extern const char * const BaslerGenTlGevDeviceClass;
        extern const char * const BaslerGenTlU3vDeviceClass;
        extern const char * const BaslerGenTlCxpDeviceClass;
        extern const char * const BaslerUsbDeviceClass;
        extern const char * const BaslerGenTlBlazeDeviceClass;
        extern const char * const BaslerGenTlStaDeviceClass;
        %mutable;
    }
%pythoncode %{
import sys as _sys

_DEVICECLASS_CONSTS = {
    "BaslerCamEmuDeviceClass",
    "BaslerGigEDeviceClass",
    "BaslerIpCamDeviceClass",
    "BaslerCameraLinkDeviceClass",
    "BaslerGenTlDeviceClassPrefix",
    "BaslerGenTlGevDeviceClass",
    "BaslerGenTlU3vDeviceClass",
    "BaslerGenTlCxpDeviceClass",
    "BaslerUsbDeviceClass",
    "BaslerGenTlBlazeDeviceClass",
    "BaslerGenTlStaDeviceClass",
}

_mod = _sys.modules[__name__]
_base = type(_mod)

class _PylonConstGuardModule(_base):
    def __setattr__(self, name, value):
        if name in _DEVICECLASS_CONSTS:
            raise AttributeError("module attribute '%s' is read-only" % name)
        return _base.__setattr__(self, name, value)

_mod.__class__ = _PylonConstGuardModule
%}