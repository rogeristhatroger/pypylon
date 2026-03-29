%rename (InstantCamera) Pylon::CInstantCamera;

%ignore IInstantCameraExtensions;
%ignore GetExtensionInterface;
%ignore CGrabResultDataFactory;
%ignore CreateDeviceSpecificGrabResultData;
%ignore CreateGrabResultData;
%ignore CInstantCameraParams_Params;
%ignore Basler_InstantCameraParams;

namespace Basler_InstantCameraParams
{
   class CInstantCameraParams_Params
   {
   };
}
namespace Pylon
{
   using namespace Basler_InstantCameraParams;
}

#define AutoLock GENAPI_NAMESPACE::AutoLock
#define CLock GENAPI_NAMESPACE::CLock

%rename(ConfigurationEventHandler) Pylon::CConfigurationEventHandler;
%rename(ImageEventHandler) Pylon::CImageEventHandler;
%rename(CameraEventHandler) Pylon::CCameraEventHandler;
%rename(StartGrabbingMax) StartGrabbing( size_t maxImages, EGrabStrategy strategy = GrabStrategy_OneByOne, EGrabLoop grabLoopType = GrabLoop_ProvidedByUser);

namespace Pylon {
     class CConfigurationEventHandler;
     class CImageEventHandler;
     class CCameraEventHandler;
};

%pythoncode %{
    FirstFound = True
    Unambiguous = False
%}

%extend Pylon::CInstantCamera {




    PROP_GET(QueuedBufferCount)
    PROP_GETSET(CameraContext)
    PROP_GET(DeviceInfo)

    PROP_GET(NodeMap)
    PROP_GET(TLNodeMap)
    PROP_GET(StreamGrabberNodeMap)
    PROP_GET(EventGrabberNodeMap)
    PROP_GET(InstantCameraNodeMap)
%pythoncode %{
    StreamGrabber = property(lambda self: self.GetStreamGrabberNodeMap() if self.IsOpen() else None)
    EventGrabber = property(lambda self: self.GetEventGrabberNodeMap() if self.IsOpen() else None)
    TransportLayer = property(lambda self: self.GetTLNodeMap())

    @staticmethod
    def _device_info_from_dict(d):
        di = DeviceInfo()
        di.update(d)
        return di

    def __getattr__(self, attribute):
        if attribute in ( "thisown","this") or attribute.startswith("__"):
            return object.__getattr__(self, attribute)
        else:
            return _LookupParameter(self.GetInstantCameraNodeMap(), self.GetNodeMap() if self.IsPylonDeviceAttached() else None, attribute)

    def __setattr__(self, attribute, val):
        if attribute in ( "thisown","this") or attribute.startswith("__"):
            object.__setattr__(self, attribute, val)
        else:
            warnings.warn(f"Setting a feature value by direct assignment is deprecated. Use <nodemap>.{attribute}.Value = {val}", DeprecationWarning, stacklevel=2)
            self.GetNodeMap().GetNode(attribute).SetValue(val)

    def __dir__(self):
        l = dir(type(self))
        l.extend(self.__dict__.keys())
        try:
            nodes = self.GetInstantCameraNodeMap().GetNodes()
            features = filter(lambda n: n.GetNode().IsFeature(), nodes)
            l.extend(x.GetNode().GetName() for x in features)
        except:
            pass
        try:
            if self.IsPylonDeviceAttached():
                nodes = self.GetNodeMap().GetNodes()
                features = filter(lambda n: n.GetNode().IsFeature(), nodes)
                l.extend(x.GetNode().GetName() for x in features)
        except:
            pass
        return sorted(set(l))

    def __enter__(self):
        if self.IsPylonDeviceAttached():
            self.Open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.DestroyDevice() #automatically closes the camera and releases the device
        return False
%}
}

%pythonprepend Pylon::CInstantCamera::CInstantCamera %{
    # InstantCamera(firstFound: bool)
    if len(args) == 1 and isinstance(args[0], bool):
        _pylon.InstantCamera_swiginit(self, _pylon.new_InstantCamera())
        tlf = TlFactory.GetInstance()
        if args[0] == FirstFound:
            self.Attach(tlf.CreateFirstDevice())
        else:
            self.Attach(tlf.CreateDevice(DeviceInfo()))
        return
    # InstantCamera(di: DeviceInfo | dict, firstFound: bool)
    if len(args) == 2 and isinstance(args[1], bool):
        di_arg = args[0]
        first_found = args[1]
        if isinstance(di_arg, dict):
            di_arg = InstantCamera._device_info_from_dict(di_arg)
        _pylon.InstantCamera_swiginit(self, _pylon.new_InstantCamera())
        tlf = TlFactory.GetInstance()
        if first_found == FirstFound:
            self.Attach(tlf.CreateFirstDevice(di_arg))
        else:
            self.Attach(tlf.CreateDevice(di_arg))
        return
%}

%pythonprepend Pylon::CInstantCamera::Attach %{
    # Attach(firstFound: bool)
    if len(args) == 1 and isinstance(args[0], bool):
        tlf = TlFactory.GetInstance()
        if args[0] == FirstFound:
            _pylon.InstantCamera_Attach(self, tlf.CreateFirstDevice())
        else:
            _pylon.InstantCamera_Attach(self, tlf.CreateDevice(DeviceInfo()))
        return
    # Attach(di: DeviceInfo | dict, firstFound: bool)
    if len(args) == 2 and isinstance(args[1], bool):
        di_arg = args[0]
        first_found = args[1]
        if isinstance(di_arg, dict):
            di_arg = InstantCamera._device_info_from_dict(di_arg)
        tlf = TlFactory.GetInstance()
        if first_found == FirstFound:
            _pylon.InstantCamera_Attach(self, tlf.CreateFirstDevice(di_arg))
        else:
            _pylon.InstantCamera_Attach(self, tlf.CreateDevice(di_arg))
        return
%}

%pythonprepend Pylon::CInstantCamera::RegisterConfiguration %{
    if cleanupProcedure == Cleanup_Delete:
        pConfigurator.__disown__()
    elif cleanupProcedure == Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}
%pythonprepend Pylon::CInstantCamera::RegisterImageEventHandler %{
    if cleanupProcedure == Cleanup_Delete:
        pImageEventHandler.__disown__()
    elif cleanupProcedure == Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}
%pythonprepend Pylon::CInstantCamera::RegisterCameraEventHandler %{
    assert(len(args) > 4)
    if args[4] == Cleanup_Delete:
        args[0].__disown__()
    elif args[4] == Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}

// These enums used to be part of InstantCamera.h in pylon <= 6.3.0.18933.
// Now they are placed in seperate headers.
#if  PYLON_VERSION_MAJOR > 6 || \
    (PYLON_VERSION_MAJOR == 6 && PYLON_VERSION_MINOR > 3) || \
    (PYLON_VERSION_MAJOR == 6 && PYLON_VERSION_MINOR == 3 && PYLON_VERSION_SUBMINOR > 0) || \
    (PYLON_VERSION_MAJOR == 6 && PYLON_VERSION_MINOR == 3 && PYLON_VERSION_SUBMINOR == 0 && PYLON_VERSION_BUILD > 18933)
%include <pylon/ECleanup.h>;
%include <pylon/ERegistrationMode.h>;
%include <pylon/ETimeoutHandling.h>;
#endif

// Per-method typemaps for nodemap getters – each wraps the returned
// GenApi::INodeMap& in an INodeMapWrapper carrying the correct ENodeMapType.
// These must appear before %include <pylon/InstantCamera.h> so SWIG uses them
// instead of the generic INodeMap& typemap defined in pylon.i.

%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CInstantCamera::GetNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::INodeMapWrapper($1, Pylon::NodeMapType_Camera),
        $descriptor(Pylon::INodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CInstantCamera::GetTLNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::INodeMapWrapper($1, Pylon::NodeMapType_DeviceTransportLayer),
        $descriptor(Pylon::INodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CInstantCamera::GetStreamGrabberNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::INodeMapWrapper($1, Pylon::NodeMapType_StreamGrabber),
        $descriptor(Pylon::INodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CInstantCamera::GetEventGrabberNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::INodeMapWrapper($1, Pylon::NodeMapType_EventGrabber),
        $descriptor(Pylon::INodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CInstantCamera::GetInstantCameraNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::INodeMapWrapper($1, Pylon::NodeMapType_InstantCamera),
        $descriptor(Pylon::INodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%include <pylon/InstantCamera.h>;

