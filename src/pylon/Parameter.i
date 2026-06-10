%rename (Parameter) Pylon::CParameter;
#define GenICam GENICAM_NAMESPACE
%rename(_IValueEx) Pylon::IValueEx;
%ignore Pylon::CParameter::CParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CParameter::Attach(GENAPI_NAMESPACE::INodeMap &,char const *);
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