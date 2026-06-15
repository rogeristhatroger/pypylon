%rename(RegionParameter) Pylon::DataProcessing::CRegionParameter;

%ignore Pylon::DataProcessing::CRegionParameter::CRegionParameter(GENAPI_NAMESPACE::INodeMap*, const char*);
%ignore Pylon::DataProcessing::CRegionParameter::operator=(const Pylon::DataProcessing::CRegion& value);

%include <pylondataprocessing/RegionParameter.h>

ADD_PROP_GETSET(RegionParameter, Value)


