%rename (PortParameter) Pylon::CPortParameter;
#define GenICam GENICAM_NAMESPACE
%rename(_IPortEx) Pylon::IPortEx;
%ignore Pylon::CPortParameter::CPortParameter(GENAPI_NAMESPACE::INodeMap &,char const *);

// The raw C++ Read/Write signatures have void* as the FIRST argument:
//   Read (void *pBuffer, int64_t Address, int64_t Length)
//   Write(const void *pBuffer, int64_t Address, int64_t Length)
// This ordering is not compatible with the genicam buffer typemaps (which
// expect pBuffer/Length to be adjacent at the END of the argument list).
// Suppress the raw overrides; the %extend below provides Python-friendly
// replacements with Address first, matching the genicam IPort Python API.
%ignore Pylon::CPortParameter::Read;
%ignore Pylon::CPortParameter::Write;

// ---------------------------------------------------------------------------
// Buffer typemaps for the %extend Read / Write below.
//
// These are the same patterns as genicam.i uses for IPort, but defined here
// because %import (used for genicam in pylon.i) does not propagate typemaps
// into the importing module.
//
// Read  – (void *pBuffer, int64_t Length):
//   'in'     : allocate a buffer of Length bytes for C++ to write into
//   'argout' : wrap the filled buffer as a Python bytes object and append to result
//   'freearg': free the allocated buffer
// ---------------------------------------------------------------------------
%typemap(in) (void *pBuffer, int64_t Length)
{
    $2 = PyLong_AsLongLong($input);
    if (PyErr_Occurred()) SWIG_fail;
    if (($2 < 0) || ($2 > INT_MAX)) {
        PyErr_SetString(PyExc_ValueError,
                        "CPortParameter.Read: Length must be in [0, INT_MAX]");
        SWIG_fail;
    }
    $1 = (void*) new char[(size_t)$2 + 1];
}

%typemap(argout) (void *pBuffer, int64_t Length)
{
    PyObject *o = PyBytes_FromStringAndSize((const char*)$1, (Py_ssize_t)$2);
    $result = SWIG_AppendOutput($result, o);
}

%typemap(freearg) (void *pBuffer, int64_t Length)
{
    delete[] (char*)$1;
}

// Write – (const void *pBuffer, int64_t Length):
//   'in' : accept bytes or bytearray; extract buffer pointer and length
// ---------------------------------------------------------------------------
%typemap(in) (const void *pBuffer, int64_t Length)
{
    Py_ssize_t _len = 0;
    const char *_buf = nullptr;
    if (PyBytes_Check($input)) {
        _len = PyBytes_GET_SIZE($input);
        _buf = PyBytes_AS_STRING($input);
    } else if (PyByteArray_Check($input)) {
        _len = PyByteArray_GET_SIZE($input);
        _buf = PyByteArray_AS_STRING($input);
    } else {
        PyErr_SetString(PyExc_TypeError,
                        "CPortParameter.Write: expected bytes or bytearray");
        SWIG_fail;
    }
    $1 = (const void*) _buf;
    $2 = (int64_t) _len;
}

%include "PortParameter.h";

// ---------------------------------------------------------------------------
// Python-friendly overloads that reorder parameters so that the typemaps above
// match (pBuffer/Length come last, adjacent):
//
//   p.Read(address, length)  -> bytes
//   p.Write(address, data)   where data is bytes or bytearray
// ---------------------------------------------------------------------------
%extend Pylon::CPortParameter {
    void Read(int64_t Address, void *pBuffer, int64_t Length)
    {
        $self->Read(pBuffer, Address, Length);
    }
    void Write(int64_t Address, const void *pBuffer, int64_t Length)
    {
        $self->Write(pBuffer, Address, Length);
    }
};

ADD_PROP_GET(PortParameter, Node);
ADD_PROP_GET(PortParameter, ChunkID);
