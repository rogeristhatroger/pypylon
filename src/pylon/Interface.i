%rename (Interface) Pylon::IInterface;
%nodefaultdtor Pylon::IInterface;
%extend Pylon::IInterface
{
    PROP_GET(InterfaceInfo)

%pythoncode %{
    class NodeMapContext:
        def __init__(self, iface):
            self.iface = iface

        def __enter__(self):
            self.iface.Open()
            return self.iface.GetNodeMap()

        def __exit__(self, type, value, traceback):
            self.iface.Close()

    NodeMap = property(NodeMapContext)
%}

}

%typemap(out) GENAPI_NAMESPACE::INodeMap* Pylon::IInterface::GetNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::INodeMapWrapper($1, Pylon::NodeMapType_Interface),
        $descriptor(Pylon::INodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%include <pylon/Interface.h>;
