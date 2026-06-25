%rename(ImageParameter) Pylon::DataProcessing::CImageParameter;

%ignore Pylon::DataProcessing::CImageParameter::CImageParameter(GENAPI_NAMESPACE::INodeMap*, const char*);
%ignore Pylon::DataProcessing::CImageParameter::operator=(const Pylon::CPylonImage& value);

%include <pylondataprocessing/ImageParameter.h>

ADD_PROP_GETSET(ImageParameter, Value)


