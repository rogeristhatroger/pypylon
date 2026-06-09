%rename (BooleanParameter) Pylon::CBooleanParameter;
#define GenICam GENICAM_NAMESPACE
%rename(_IBooleanEx) Pylon::IBooleanEx;
%ignore Pylon::CBooleanParameter::CBooleanParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CBooleanParameter::operator()();
%ignore Pylon::CBooleanParameter::operator*();
%ignore Pylon::CBooleanParameter::operator=( bool value );
%include "pylon_kwarg_normalize.i"
PYLON_KWARG_NORMALIZE_BEGIN
%include <pylon/BooleanParameter.h>
PYLON_KWARG_NORMALIZE_END

ADD_PROP_GETSET(BooleanParameter, Value)
