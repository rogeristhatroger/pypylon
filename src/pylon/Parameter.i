%rename (Parameter) Pylon::CParameter;
#define GenICam GENICAM_NAMESPACE
%rename(_IValueEx) Pylon::IValueEx;
%ignore Pylon::CParameter::CParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CParameter::Attach(GENAPI_NAMESPACE::INodeMap &,char const *);

%pythonprepend Pylon::CParameter::FromString %{
    # Normalize ValueStr to canonical form only for BooleanParameter nodes
    from pypylon.genicam import intfIBoolean as _intfIBoolean
    if self.IsValid() and self.Node.GetPrincipalInterfaceType() == _intfIBoolean:
        value = ValueStr.strip().lower()
        if value == "true":
            return _pylon.Parameter_FromString(self, "true", Verify)
        elif value == "false":
            return _pylon.Parameter_FromString(self, "false", Verify)
    return _pylon.Parameter_FromString(self, ValueStr.strip(), Verify)
%}


%include "pylon_kwarg_normalize.i"
PYLON_KWARG_NORMALIZE_BEGIN
%include <pylon/Parameter.h>
PYLON_KWARG_NORMALIZE_END

ADD_PROP_GET(Parameter, AccessMode)
ADD_PROP_GET(Parameter, Node)



%extend Pylon::CParameter {
    std::string GetValueOrDefault(const std::string& defaultValue) {
        try {
            if (!$self->IsReadable()) return defaultValue;
            return std::string($self->ToString().c_str());
        } catch (...) {
            return defaultValue;
        }
    }

    %pythoncode %{
        def __str__(self):
            if not self.IsValid():
                result = "<not found>"
            elif not self.IsReadable():
                result = "<not readable>"
            else:
                result = self.ToString();
            return result
    %}
}
