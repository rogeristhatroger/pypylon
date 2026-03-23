%rename (BooleanParameter) Pylon::CBooleanParameter;
#define GenICam GENICAM_NAMESPACE
%ignore Pylon::IBooleanEx;
%ignore Pylon::CBooleanParameter::CBooleanParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CBooleanParameter::operator()();
%ignore Pylon::CBooleanParameter::operator*();
%ignore Pylon::CBooleanParameter::operator=( bool value );
%include <pylon/BooleanParameter.h>;

ADD_PROP_GETSET(BooleanParameter, Value)
