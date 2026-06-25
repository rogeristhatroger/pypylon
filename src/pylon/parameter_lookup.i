%pythoncode %{
def _LookupParameter(nodemap_wrapper1, nodemap_wrapper2, name):
    """Lookup a genicam parameter by name and return it wrapped in the corresponding Pylon *Parameter type."""

    # GetNode always returns a parameter and does not throw
    parameter = nodemap_wrapper1.GetNode(name)
    if not parameter.IsValid() and nodemap_wrapper2 is not None:
        parameter = nodemap_wrapper2.GetNode(name)
    return parameter

def _LookupInFixedParameterSet(nodemap_wrapper, name):
    """Lookup a genicam parameter for objects providing a nodemap."""
    # GetNode always returns a parameter and does not throw
    parameter = nodemap_wrapper.GetNode(name)
    if not parameter.IsValid():
        nodemap_type_name = nodemap_wrapper.GetNodeMapTypeString()
        raise pypylon.genicam.LogicalErrorException(
            f"Parameter '{name}' not found in nodemap of type {nodemap_type_name}."
        )
    return parameter
%}