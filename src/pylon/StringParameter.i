%rename (StringParameter) Pylon::CStringParameter;
#define GenICam GENICAM_NAMESPACE
%ignore Pylon::IStringEx;
%ignore Pylon::CStringParameter::CStringParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CStringParameter::operator()();
%ignore Pylon::CStringParameter::operator*();
%ignore Pylon::CStringParameter::operator=(const GenICam::gcstring& value);
%include <pylon/StringParameter.h>;

ADD_PROP_GETSET(StringParameter, Value)
ADD_PROP_GET(StringParameter, MaxLength)