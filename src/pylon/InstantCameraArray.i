%rename(InstantCameraArray) Pylon::CInstantCameraArray;

%pythonprepend Pylon::CInstantCameraArray::operator[]( size_t index) %{
    if index >= self.GetSize():
        raise IndexError
%}
%ignore Pylon::CInstantCameraArray::operator[]( size_t index) const;
%rename(__getitem__) Pylon::CInstantCameraArray::operator[]( size_t index);

%extend Pylon::CInstantCameraArray {
%pythoncode %{
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.DestroyDevice()
        return False

    def __iter__(self):
        for i in range(self.GetSize()):
            yield self[i]
%}
};

%include <pylon/InstantCameraArray.h>;