%rename (Parameter) Pylon::CParameter;
#define GenICam GENICAM_NAMESPACE
%ignore Pylon::IValueEx;
%ignore Pylon::CParameter::CParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CParameter::Attach(GENAPI_NAMESPACE::INodeMap &,char const *);
%include <pylon/Parameter.h>;

ADD_PROP_GET(Parameter, AccessMode)
ADD_PROP_GET(Parameter, Node)

%extend Pylon::CParameter {
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