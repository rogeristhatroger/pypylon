%typemap(in) (const uint8_t* pBuffer, int64_t length)
{
    Py_ssize_t len;
    char *buf;
    if (PyBytes_AsStringAndSize($input, &buf, &len) < 0) {
        PyErr_Clear();
        PyErr_SetString(PyExc_TypeError, "Set() requires a bytes object");
        SWIG_fail;
    }
    $1 = reinterpret_cast<uint8_t*>(buf);
    $2 = static_cast<int64_t>(len);
}
%typemap(typecheck, precedence=SWIG_TYPECHECK_CHAR) (const uint8_t* pBuffer, int64_t length)
{
    $1 = PyBytes_Check($input) ? 1 : 0;
}

// Get( uint8_t* pBuffer, int64_t length, bool verify = false, bool ignoreCache = false )
//
// Matches IRegister behaviour: caller passes length integer; returns bytes.
//
%typemap(in) (uint8_t* pBuffer, int64_t length)
{
    $2 = PyLong_AsLongLong($input);
    if (PyErr_Occurred()) SWIG_fail;
    if (($2 < 0) || ($2 > INT_MAX)) {
        PyErr_SetString(PyExc_ValueError, "Invalid Length: 0 >= Length <= INT_MAX");
        SWIG_fail;
    }
    $1 = reinterpret_cast<uint8_t*>(new char[(int)$2 + 1]);
}
%typemap(argout) (uint8_t* pBuffer, int64_t length)
{
    PyObject* o = PyBytes_FromStringAndSize(reinterpret_cast<const char*>($1), (int)$2);
    $result = SWIG_AppendOutput($result, o);
}
%typemap(freearg) (uint8_t* pBuffer, int64_t length)
{
    delete[] (char*)$1;
}
%typemap(typecheck, precedence=SWIG_TYPECHECK_CHAR) (uint8_t* pBuffer, int64_t length)
{
    $1 = (PyLong_Check($input) || PyInt_Check($input)) ? 1 : 0;
}

%rename (ArrayParameter) Pylon::CArrayParameter;
#define GenICam GENICAM_NAMESPACE
%ignore Pylon::IRegisterEx;
%ignore Pylon::CArrayParameter::CArrayParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%include <pylon/ArrayParameter.h>;

ADD_PROP_GET(ArrayParameter, Length)
ADD_PROP_GET(ArrayParameter, Address)

%pythoncode %{
    def _ArrayParameter_GetAll(self):
        return self.Get(self.GetLength())
    ArrayParameter.GetAll = _ArrayParameter_GetAll
%}
