%rename(CameraEventHandler) Pylon::CCameraEventHandler;
%rename(InstantCamera) Pylon::CInstantCamera;

%feature("director") Pylon::CCameraEventHandler;

%typemap(directorin) Pylon::String_t const &nodeName{
    $input = PyUnicode_FromStringAndSize($1.c_str(),$1.length());
}

%typemap(directorin) GENAPI_NAMESPACE::INode* pNode {
    PYLON_NODE_TO_PARAMETER($1, $input)
}

%ignore Pylon::CCameraEventHandler::DebugGetEventHandlerRegistrationCount;
%include <pylon/CameraEventHandler.h>