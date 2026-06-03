%rename(VersionInfo) Pylon::VersionInfo;

// add a macro for getters with camel-casing
%define ADD_PROP_GET_CAMEL(class, name)
    %pythoncode %{ class ## .name = property(class ## .get ## name) %}
%enddef

%ignore Pylon::VersionInfo::getVersionString;

%extend Pylon::VersionInfo {
  %pythoncode %{
    def __repr__(self):
        return f"<VersionInfo {self.getMajor()}.{self.getMinor()}.{self.getSubminor()}>"
  %}
};

%include <pylon/PylonVersionInfo.h>;

// remove the genicam define interferering here
#if defined(Build)
#undef Build
#endif
ADD_PROP_GET_CAMEL(VersionInfo, Build)
ADD_PROP_GET_CAMEL(VersionInfo, Major)
ADD_PROP_GET_CAMEL(VersionInfo, Minor)
ADD_PROP_GET_CAMEL(VersionInfo, Subminor)

