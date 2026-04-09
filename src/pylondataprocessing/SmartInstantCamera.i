%ignore RegisterSmartResultEventHandler;
%ignore DeregisterSmartResultEventHandler;
%ignore GetParameters;
%rename(RegisterSmartResultEventHandler) RegisterSmartResultEventHandler2;
%rename(DeregisterSmartResultEventHandler) DeregisterSmartResultEventHandler2;
%rename(StartGrabbingMax) StartGrabbing( bool startRecipe, size_t maxImages, EGrabStrategy strategy, EGrabLoop grabLoopType, EGrabLoop grabLoopTypeDataProcessing);
%ignore ResultWithUpdate;
%ignore CStickyEventHandler;
%ignore COutputObserver;
%ignore SmartResultEventHandlerData;

%include <pylondataprocessing/SmartInstantCamera.h>

////////////////////////////////////////////////////////////////////////////////
//
// Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr> output
//

%typemap(in,numinputs=0, noblock=1) Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr>& {
  $1 = new Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr>();
}

%typemap(argout, noblock=1) Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr>& {
  Py_DECREF($result);
  $result = SWIG_NewPointerObj(
    SWIG_as_voidptr($1),
    SWIGTYPE_p_Pylon__DataProcessing__SSmartInstantCameraResultTT_Pylon__CGrabResultPtr_t,
    SWIG_POINTER_OWN
    ); // Now $1 is owned by $result. Must not 'delete' it now!
}

// '%typemap(freearg)' must be empty!
%typemap(freearg, noblock=1) Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr>& {}

// ensure the above typemap will not be applied to const references
%typemap(in) const Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr>& = const SWIGTYPE &;
%typemap(argout, noblock=1) const Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr>& {};
%typemap(freearg, noblock=1) const Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr>& {};

%pythonprepend Pylon::CInstantCamera::RegisterSmartResultEventHandler2 %{
    if cleanupProcedure == pypylon.pylon.Cleanup_Delete:
        pSmartResultEventHandler.__disown__()
    elif cleanupProcedure == pypylon.pylon.Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}

%template(SmartInstantCamera) Pylon::DataProcessing::CSmartInstantCameraT< Pylon::CInstantCamera, Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr> >;


%extend Pylon::DataProcessing::CSmartInstantCameraT< Pylon::CInstantCamera, Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr> > {

    // This is used to get the typemapping of pSmartResultEventHandler right.
    virtual void RegisterSmartResultEventHandler2( Pylon::DataProcessing::CSmartResultEventHandlerT< Pylon::CInstantCamera, Pylon::DataProcessing::SSmartInstantCameraResultT< Pylon::CGrabResultPtr > >* pSmartResultEventHandler, ERegistrationMode mode, ECleanup cleanupProcedure )
    {
        ($self)->RegisterSmartResultEventHandler(pSmartResultEventHandler, mode, cleanupProcedure);
    }

    // This is used to get the typemapping of pSmartResultEventHandler right.
    virtual bool DeregisterSmartResultEventHandler2( Pylon::DataProcessing::CSmartResultEventHandlerT< Pylon::CInstantCamera, Pylon::DataProcessing::SSmartInstantCameraResultT< Pylon::CGrabResultPtr > >* pSmartResultEventHandler )
    {
        return ($self)->DeregisterSmartResultEventHandler(pSmartResultEventHandler);
    }

    void GetAllParameterNames(StringList_t& result)
    {
      result = $self->GetParameters().GetAllParameterNames();
    }

    bool ContainsParameter(const Pylon::String_t& fullname)
    {
      bool result = $self->GetParameters().Contains(fullname);
      return result;
    }

    %nothread _GetParameter;
    PyObject* _GetParameter(const Pylon::String_t& fullname)
    {
        Pylon::CParameter parameter = $self->GetParameters().Get(fullname);
		GenApi::INode* pNode = parameter.IsValid() ? parameter.GetNode() : nullptr;
        return _DataprocNodeToParameter(pNode);
    }

%pythoncode %{
    def GetParameter(self, fullname):
        """Get a SmartInstantCamera recipe parameter by its full name.

        Falls back to the static pylon parameter tables for /@CameraDevice/,
        /@DeviceTransportLayer/, and /@StreamGrabber* nodemap identifiers when
        the parameter is not found in the live nodemap.
        """
        import pypylon.genicam as _genicam
        import pypylon.pylon as _pylon

        _NODEMAP_LOOKUP = {
            "/@CameraDevice/": _pylon._CAMERA_PARAMETERS,
            "/@DeviceTransportLayer/": _pylon._TRANSPORT_LAYER_PARAMETERS,
        }

        try:
            return self._GetParameter(fullname)
        except _genicam.LogicalErrorException:
            param_name = fullname.rsplit("/", 1)[-1]
            param_dict = None

            for marker, d in _NODEMAP_LOOKUP.items():
                if marker in fullname:
                    param_dict = d
                    break

            if param_dict is None and "/@StreamGrabber" in fullname:
                param_dict = _pylon._STREAM_PARAMETERS

            if param_dict is not None:
                intf_type = param_dict.get(param_name)
                if intf_type is not None:
                    if intf_type == _genicam.intfIInteger:
                        return _pylon.IntegerParameter()
                    elif intf_type == _genicam.intfIBoolean:
                        return _pylon.BooleanParameter()
                    elif intf_type == _genicam.intfICommand:
                        return _pylon.CommandParameter()
                    elif intf_type == _genicam.intfIFloat:
                        return _pylon.FloatParameter()
                    elif intf_type == _genicam.intfIString:
                        return _pylon.StringParameter()
                    elif intf_type == _genicam.intfIRegister:
                        return _pylon.ArrayParameter()
                    elif intf_type == _genicam.intfIEnumeration:
                        return _pylon.EnumParameter()
                    else:
                        return _pylon.Parameter()

            raise
%}
};

