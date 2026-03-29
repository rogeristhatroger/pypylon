%nodefaultdtor Pylon::IProperties;
%ignore CInfoImpl;

%extend Pylon::CInfoBase {
%pythoncode %{
    def keys(self):
        """Return all available property names."""
        return [str(n) for n in self.GetPropertyNames()]

    def values(self):
        """Return all available property values."""
        return [self[k] for k in self.keys()]

    def items(self):
        """Return all (name, value) pairs."""
        return [(k, self[k]) for k in self.keys()]

    def __getitem__(self, key):
        ok, value = self.GetPropertyValue(key)
        if not ok:
            raise KeyError(key)
        return str(value)

    def __setitem__(self, key, value):
        self.SetPropertyValue(key, value)

    def __iter__(self):
        return iter(self.keys())

    def __contains__(self, key):
        return self.GetPropertyAvailable(key)

    def to_dict(self):
        """Convert all properties to a plain Python dict."""
        return dict(self.items())

    def update(self, d):
        """Set properties from a dict."""
        for key, value in d.items():
            self.SetPropertyValue(key, value)
%}
}

%include <pylon/Info.h>;

// CInfoBase properties (inherited by all Info subclasses)
ADD_PROP_GETSET(CInfoBase, FriendlyName)
ADD_PROP_GETSET(CInfoBase, FullName)
ADD_PROP_GETSET(CInfoBase, VendorName)
ADD_PROP_GETSET(CInfoBase, DeviceClass)
ADD_PROP_GETSET(CInfoBase, TLType)
