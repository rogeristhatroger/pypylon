%rename (StringParameter) Pylon::CStringParameter;
#define GenICam GENICAM_NAMESPACE
%rename(_IStringEx) Pylon::IStringEx;
%ignore Pylon::CStringParameter::CStringParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CStringParameter::operator()();
%ignore Pylon::CStringParameter::operator*();
%ignore Pylon::CStringParameter::operator=(const GenICam::gcstring& value);
%include "pylon_kwarg_normalize.i"
PYLON_KWARG_NORMALIZE_BEGIN
%include <pylon/StringParameter.h>
PYLON_KWARG_NORMALIZE_END

ADD_PROP_GETSET(StringParameter, Value)
ADD_PROP_GET(StringParameter, MaxLength)
ADD_PROP_GET(StringParameter, Length)
