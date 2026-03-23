%rename (CommandParameter) Pylon::CCommandParameter;
#define GenICam GENICAM_NAMESPACE
%ignore Pylon::ICommandEx;
%ignore Pylon::CCommandParameter::CCommandParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CCommandParameter::operator()();
%include <pylon/CommandParameter.h>;
