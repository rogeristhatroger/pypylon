%rename (EnumEntryParameter) Pylon::CEnumEntryParameter;
#define GenICam GENICAM_NAMESPACE
%rename(_IEnumEntryEx) Pylon::IEnumEntryEx;
%ignore Pylon::CEnumEntryParameter::CEnumEntryParameter(GENAPI_NAMESPACE::INodeMap &,char const *);

%include "EnumEntryParameter.h";

ADD_PROP_GET(EnumEntryParameter, Symbolic)
ADD_PROP_GET(EnumEntryParameter, Value) //Hint: avoid to use an enums (Int)Value, any IntValue is device specific
ADD_PROP_GET(EnumEntryParameter, NumericValue)