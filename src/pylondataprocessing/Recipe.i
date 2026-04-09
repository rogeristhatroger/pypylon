%rename(Recipe) Pylon::DataProcessing::CRecipe;
%rename(OutputObserver) Pylon::DataProcessing::IOutputObserver;

%ignore GetParameters;
%ignore GetInputTypeName;
%ignore GetOutputTypeName;
%ignore UnregisterOutputObserver;
%ignore RegisterOutputObserver;
%ignore TriggerUpdate;
%ignore TriggerUpdateAsync;

%ignore GetOutputNames;
%rename(GetOutputNames) GetOutputNames2;
%rename(UnregisterOutputObserver) UnregisterOutputObserver2;
%rename(RegisterOutputObserver) RegisterOutputObserver2;
%rename(TriggerUpdate) TriggerUpdate2;
%rename(TriggerUpdateAsync) TriggerUpdateAsync2;

#define CLock GENAPI_NAMESPACE::CLock

%typemap(typecheck,precedence=SWIG_TYPECHECK_CHAR)  (const void* pBuffer, size_t bufferSize)
   %{
       $1 = (PyBytes_Check($input) || PyByteArray_Check($input)) ? 1 : 0;
   %}

%typemap(in) (const void* pBuffer, size_t bufferSize)
    %{
        if (PyBytes_Check($input)) {
            $1 = PyBytes_AsString($input);
            $2 = PyBytes_Size($input);
        } else if (PyByteArray_Check($input)) {
            $1 = PyByteArray_AsString($input);
            $2 = PyByteArray_Size($input);
        } else {
            PyErr_SetString(
              PyExc_TypeError,
              "Invalid type of buffer (bytes and bytearray are supported)!."
            );
            SWIG_fail;
        }
    %}

%include <pylondataprocessing/Recipe.h>;

%extend Pylon::DataProcessing::CRecipe {
%pythoncode %{
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Unload()
        return False

    def GetParameter(self, fullname):
        """Get a recipe parameter by its full name.

        If the parameter node is not found in the live recipe nodemap and the
        full name refers to a Camera vTool sub-nodemap (/@CameraDevice/,
        /@DeviceTransportLayer/ or /@StreamGrabber), the method falls back to
        the static parameter tables from pypylon.pylon and returns an
        unattached parameter object of the correct type.  This mirrors the
        behaviour of _LookupParameter in the pylon module.
        """
        import pypylon.genicam as _genicam
        import pypylon.pylon as _pylon

        # Map of nodemap-identifier substrings to their static parameter dict
        _NODEMAP_LOOKUP = {
            "/@CameraDevice/": _pylon._CAMERA_PARAMETERS,
            "/@DeviceTransportLayer/": _pylon._TRANSPORT_LAYER_PARAMETERS,
        }

        try:
            return self._GetParameter(fullname)
        except _genicam.LogicalErrorException:
            # Parameter not found in the live nodemap – try static fallback.
            param_name = fullname.rsplit("/", 1)[-1]
            param_dict = None

            for marker, d in _NODEMAP_LOOKUP.items():
                if marker in fullname:
                    param_dict = d
                    break

            # /@StreamGrabber matches /@StreamGrabber0, /@StreamGrabber1 …
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

    void GetOutputNames2(StringList_t& result) const
    {
        $self->GetOutputNames(result);
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

    void RegisterOutputObserver2(const StringList_t& outputFullNames, IOutputObserver* pObserver, ERegistrationMode mode, intptr_t userProvidedId = 0)
    {
        $self->RegisterOutputObserver(outputFullNames, pObserver, mode, userProvidedId);
    }
    
    bool UnregisterOutputObserver2(IOutputObserver* pObserver, intptr_t userProvidedId = 0)
    {
        bool result = $self->UnregisterOutputObserver(pObserver, userProvidedId);
        return result;
    }
    
    Pylon::DataProcessing::CUpdate TriggerUpdateAsync2(Pylon::DataProcessing::CVariantContainer inputCollection, Pylon::DataProcessing::IUpdateObserver* pObserver = nullptr, intptr_t userProvidedId = 0)
    {
        Pylon::DataProcessing::CUpdate result = self->TriggerUpdateAsync(inputCollection, pObserver, userProvidedId);
        return result;
    }
    
    Pylon::DataProcessing::CUpdate TriggerUpdate2(Pylon::DataProcessing::CVariantContainer inputCollection, unsigned int timeoutMs, Pylon::ETimeoutHandling timeoutHandling = Pylon::TimeoutHandling_ThrowException, Pylon::DataProcessing::IUpdateObserver* pObserver = nullptr, intptr_t userProvidedId = 0)
    {
        Pylon::DataProcessing::CUpdate result = self->TriggerUpdate(inputCollection, timeoutMs, timeoutHandling, pObserver, userProvidedId);
        return result;
    }
}
