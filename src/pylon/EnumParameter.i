// ---------------------------------------------------------------------------
// Typemap: Python sequence-of-strings  →  const char** nullTerminatedList
//
// Accepts any Python iterable whose elements are str (or bytes).
// Builds a heap-allocated const char*[] whose last entry is NULL,
// passes it to the C++ method, then releases all memory in freearg.
// ---------------------------------------------------------------------------

// typecheck – needed so SWIG can select the right overload when both
// SetValue(const String_t&) and SetValue(const char**) are visible.
%typemap(typecheck, precedence=SWIG_TYPECHECK_STRING_ARRAY)
    const char** nullTerminatedList
{
    $1 = (PySequence_Check($input) && !PyUnicode_Check($input) && !PyBytes_Check($input)) ? 1 : 0;
}

// in – convert the Python sequence into a NULL-terminated char** array.
// Note: SWIG declares the local variable as char** (it strips top-level const
// from pointer-to-pointer types), so the typemap body must use char* / char**.
%typemap(in) const char** nullTerminatedList
(char** string_array = NULL, PyObject** encoded_items = NULL, Py_ssize_t alloc_size = 0)
{
    if (!PySequence_Check($input)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of strings for nullTerminatedList");
        SWIG_fail;
    }

    alloc_size = PySequence_Size($input);
    // +1 for the terminating NULL pointer
    string_array = new char*[alloc_size + 1];
    encoded_items = new PyObject*[alloc_size];
    for (Py_ssize_t k = 0; k < alloc_size; k++) encoded_items[k] = NULL;

    for (Py_ssize_t i = 0; i < alloc_size; i++) {
        PyObject* item = PySequence_GetItem($input, i);
        if (!item) {
            SWIG_fail;
        }

        if (PyUnicode_Check(item)) {
            // Encode to UTF-8 bytes; the new bytes object is stored so its
            // internal buffer stays valid for the duration of the C++ call.
            encoded_items[i] = PyUnicode_AsEncodedString(item, "utf-8", "strict");
            Py_DECREF(item);
            if (!encoded_items[i]) {
                SWIG_fail;
            }
            string_array[i] = PyBytes_AsString(encoded_items[i]);
        } else if (PyBytes_Check(item)) {
            encoded_items[i] = item;   // keep ref alive
            string_array[i] = PyBytes_AsString(item);
        } else {
            Py_DECREF(item);
            PyErr_SetString(PyExc_TypeError, "All elements of nullTerminatedList must be str or bytes");
            SWIG_fail;
        }

        if (!string_array[i]) {
            SWIG_fail;
        }
    }

    string_array[alloc_size] = NULL;   // NULL terminator
    $1 = (char**)string_array;
}

// freearg – release the temporary arrays and encoded byte objects.
%typemap(freearg) const char** nullTerminatedList
{
    if (encoded_items$argnum) {
        for (Py_ssize_t k = 0; k < alloc_size$argnum; k++) {
            Py_XDECREF(encoded_items$argnum[k]);
        }
        delete[] encoded_items$argnum;
    }
    delete[] string_array$argnum;
}

// ---------------------------------------------------------------------------

%rename (EnumParameter) Pylon::CEnumParameter;
#define GenICam GENICAM_NAMESPACE
%rename(_IEnumerationEx) Pylon::IEnumerationEx;
%ignore Pylon::CEnumParameter::Table_t;
%ignore Pylon::CEnumParameter::TableItem_t;
%ignore Pylon::CEnumParameter::CEnumParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CEnumParameter::operator()();
%ignore Pylon::CEnumParameter::operator*();
%ignore Pylon::CEnumParameter::operator=( const GenICam::gcstring& valueStr );

%include <pylon/EnumParameter.h>;

ADD_PROP_GETSET(EnumParameter, Value)
//ADD_PROP_GETSET(EnumParameter, IntValue) Hint: avoid to use IntValue, any IntValue is device specific -> not mapped

%extend Pylon::CEnumParameter {
    %nothread GetSettableValues;

    PyObject* GetSettableValues() {
        GENAPI_NAMESPACE::StringList_t symbolics;
        $self->GetSymbolics(symbolics);

        PyObject* result = PyList_New(0);
        if (!result) return NULL;

        for (GENAPI_NAMESPACE::StringList_t::iterator it = symbolics.begin();
             it != symbolics.end(); ++it)
        {
            if ($self->CanSetValue(it->c_str())) {
                PyObject* pyStr = PyUnicode_FromString(it->c_str());
                if (!pyStr) {
                    Py_DECREF(result);
                    return NULL;
                }
                if (PyList_Append(result, pyStr) < 0) {
                    Py_DECREF(pyStr);
                    Py_DECREF(result);
                    return NULL;
                }
                Py_DECREF(pyStr);
            }
        }
        return result;
    }
}
