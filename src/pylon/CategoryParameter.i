%rename (CategoryParameter) Pylon::CCategoryParameter;
#define GenICam GENICAM_NAMESPACE
%rename(_ICategoryEx) Pylon::ICategoryEx;
%ignore Pylon::CCategoryParameter::CCategoryParameter(GENAPI_NAMESPACE::INodeMap &,char const *);

%include "CategoryParameter.h";

ADD_PROP_GET(CategoryParameter, Features)
