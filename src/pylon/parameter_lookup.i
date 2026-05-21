%pythoncode %{
def _LookupParameter(nodemap_wrapper1, nodemap_wrapper2, name):
    """Lookup a genicam parameter by name and return it wrapped in the corresponding Pylon *Parameter type."""

    node = nodemap_wrapper1.GetNode(name, False)
    nodemap_wrapper = nodemap_wrapper1
    if isinstance(node, Parameter) and not node.IsValid() and nodemap_wrapper2 is not None:
        node = nodemap_wrapper2.GetNode(name, False)
        nodemap_wrapper = nodemap_wrapper2
    if not (isinstance(node, Parameter) and not node.IsValid()): # check for node being null
        return node; #this is already converted to the correct Parameter type by the typemap for GetNode()

    nodemap_type = nodemap_wrapper.GetNodeMapType()
    # Node not found in the live nodemap – look it up in the static parameter
    # table for this nodemap type so we can return an empty (unattached)
    # parameter of the correct class.
    if nodemap_type == NodeMapType_ChunkData:
        param_dict = _CHUNK_DATA_PARAMETERS
    elif nodemap_type == NodeMapType_Camera:
        param_dict = _CAMERA_PARAMETERS
    elif nodemap_type == NodeMapType_StreamGrabber:
        param_dict = _STREAM_PARAMETERS
    elif nodemap_type == NodeMapType_DeviceTransportLayer:
        param_dict = _TRANSPORT_LAYER_PARAMETERS
    elif nodemap_type == NodeMapType_EventGrabber:
        param_dict = _EVENT_GRABBER_PARAMETERS
    elif nodemap_type == NodeMapType_Interface:
        param_dict = _INTERFACE_PARAMETERS
    else:
        param_dict = None

    if param_dict is not None:
        intf_type = param_dict.get(name)
        if intf_type is not None:
            if intf_type == pypylon.genicam.intfIInteger:
                return IntegerParameter()
            elif intf_type == pypylon.genicam.intfIBoolean:
                return BooleanParameter()
            elif intf_type == pypylon.genicam.intfICommand:
                return CommandParameter()
            elif intf_type == pypylon.genicam.intfIFloat:
                return FloatParameter()
            elif intf_type == pypylon.genicam.intfIString:
                return StringParameter()
            elif intf_type == pypylon.genicam.intfIRegister:
                return ArrayParameter()
            elif intf_type == pypylon.genicam.intfIEnumeration:
                return EnumParameter()
            else:
                return Parameter()

    nodemap_type_name = nodemap_wrapper.GetNodeMapTypeString()
    raise pypylon.genicam.LogicalErrorException(
        f"Parameter '{name}' not found in nodemap of type {nodemap_type_name}."
    )
%}