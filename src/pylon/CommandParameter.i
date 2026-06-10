%rename (CommandParameter) Pylon::CCommandParameter;
#define GenICam GENICAM_NAMESPACE
%rename(_ICommandEx) Pylon::ICommandEx;
%ignore Pylon::CCommandParameter::CCommandParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CCommandParameter::operator()();
%include "pylon_kwarg_normalize.i"
PYLON_KWARG_NORMALIZE_BEGIN
%include <pylon/CommandParameter.h>
PYLON_KWARG_NORMALIZE_END
