////////////////////////////////////////////////////////////////////////////////
//
// DeviceInfoList output
//

%typemap(in, numinputs=0, noblock=1) Pylon::DeviceInfoList_t & {
  $1 = new DeviceInfoList_t();
}

%typemap(argout) Pylon::DeviceInfoList_t & {
  Py_DECREF($result);
  PyObject *tpl = PyTuple_New($1->size());
  for (unsigned int i = 0; i < $1->size(); i++) {
    CDeviceInfo *di = new CDeviceInfo((*$1)[i]);
    PyObject *item = SWIG_NewPointerObj(
        SWIG_as_voidptr(di),
        SWIGTYPE_p_Pylon__CDeviceInfo,
        SWIG_POINTER_OWN
        );
    PyTuple_SetItem(tpl, i, item);
  }
  $result = tpl;
  delete $1;
}

// ensure the above typemap will not be applied to const references
%typemap(argout, noblock=1) const Pylon::DeviceInfoList_t & {}

////////////////////////////////////////////////////////////////////////////////
//
// DeviceInfoList intput
//
// needed for EnumerateDevices(
//     DeviceInfoList_t& list,
//     const DeviceInfoList_t& filter,
//     bool addToList = false
//     );
//

// Type check to make overloading work
%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER)
const Pylon::DeviceInfoList_t&
{
    // We need a list
    $1 = PyList_Check($input) ? 1 : 0;
}

// Convert a python list of wrapped DeviceInfos (or dicts) to a DeviceInfoList_t.
// Each element may be either a CDeviceInfo object or a dict of {str: str}
// property name/value pairs applied via SetPropertyValue().
%typemap(in, numinputs=1, noblock=1)
const Pylon::DeviceInfoList_t&
(Pylon::DeviceInfoList_t di_list)
{
    if (PyList_Check($input))
    {
        Py_ssize_t size = PyList_Size($input);
        for (Py_ssize_t i = 0; i < size; i++)
        {
            // python object – either a wrapped CDeviceInfo or a dict
            PyObject *o = PyList_GetItem($input, i);
            void *w = 0;
            if (SWIG_IsOK(SWIG_ConvertPtr(o, &w, SWIGTYPE_p_Pylon__CDeviceInfo, 0)))
            {
                di_list.push_back(*reinterpret_cast<Pylon::CDeviceInfo*>(w));
            }
            else if (PyDict_Check(o))
            {
                Pylon::CDeviceInfo di;
                PyObject *key, *value;
                Py_ssize_t pos = 0;
                while (PyDict_Next(o, &pos, &key, &value))
                {
                    if (!PyUnicode_Check(key) || !PyUnicode_Check(value))
                    {
                        PyErr_SetString(
                            PyExc_TypeError,
                            "dict filter entries must be {str: str}"
                            );
                        SWIG_fail;
                    }
                    PyObject *k_bytes = PyUnicode_AsUTF8String(key);
                    PyObject *v_bytes = PyUnicode_AsUTF8String(value);
                    if (!k_bytes || !v_bytes) { Py_XDECREF(k_bytes); Py_XDECREF(v_bytes); SWIG_fail; }
                    Pylon::String_t k(PyBytes_AsString(k_bytes));
                    Pylon::String_t v(PyBytes_AsString(v_bytes));
                    Py_DECREF(k_bytes);
                    Py_DECREF(v_bytes);
                    di.SetPropertyValue(k, v);
                }
                di_list.push_back(di);
            }
            else
            {
                PyErr_SetString(
                    PyExc_TypeError,
                    "filter list must contain DeviceInfo objects or dicts"
                    );
                SWIG_fail;
            }
        }
        $1 = &di_list;
    }
    else
    {
        PyErr_SetString(PyExc_TypeError,"not a list");
        SWIG_fail;
    }
}

////////////////////////////////////////////////////////////////////////////////
//
// AccessModeSet input typemap
//
// Allows passing an EDeviceAccessMode integer (e.g. pylon.DeviceAccessMode_Control,
// pylon.DeviceAccessMode_Exclusive) wherever an AccessModeSet is expected.
//

%typemap(in) Pylon::AccessModeSet
{
    if (PyLong_Check($input))
    {
        $1 = Pylon::AccessModeSet(
            static_cast<Pylon::EDeviceAccessMode>(PyLong_AsLong($input))
        );
    }
    else
    {
        PyErr_SetString(PyExc_TypeError,
            "AccessModeSet argument must be an integer (e.g. pylon.DeviceAccessMode_Control or pylon.DeviceAccessMode_Exclusive)");
        SWIG_fail;
    }
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_INTEGER) Pylon::AccessModeSet
{
    $1 = PyLong_Check($input) ? 1 : 0;
}

////////////////////////////////////////////////////////////////////////////////
//
// EDeviceAccessiblityInfo output typemap
//
// The three-argument C++ overload IsDeviceAccessible(di, mode, *info) is
// ignored by SWIG to avoid overload ambiguity with the two-argument variant.
// A dedicated IsDeviceAccessibleInfo(di, mode) Python method is injected via
// %extend on IDeviceFactory to expose the accessibility detail.
//

%typemap(in, numinputs=0, noblock=1)
Pylon::EDeviceAccessiblityInfo* pAccessibilityInfo
(Pylon::EDeviceAccessiblityInfo tmp = Pylon::Accessibility_Unknown)
{
    $1 = &tmp;
}

%typemap(argout) Pylon::EDeviceAccessiblityInfo* pAccessibilityInfo
{
    PyObject *pair = PyTuple_New(2);
    PyTuple_SetItem(pair, 0, $result);
    PyTuple_SetItem(pair, 1, PyLong_FromLong((long)(*$1)));
    $result = pair;
}

// Rename the three-arg overload to a distinct Python name so it does not
// collide with the two-arg overload.  The renamed method is exposed as
// _IsDeviceAccessibleInfo (private); a %pythoncode wrapper below re-exposes
// it as IsDeviceAccessibleInfo with mode defaulting to DeviceAccessMode_Control.
%rename(_IsDeviceAccessibleInfo)
    Pylon::IDeviceFactory::IsDeviceAccessible(
        const CDeviceInfo&, AccessModeSet, EDeviceAccessiblityInfo*
    );

%extend Pylon::IDeviceFactory {
%pythoncode %{
    def IsDeviceAccessibleInfo(self, device_info, mode=None):
        """Return (accessible, accessibility_info) tuple.

        mode defaults to DeviceAccessMode_Control when omitted.
        """
        import pypylon.pylon as _pylon
        if mode is None:
            mode = _pylon.DeviceAccessMode_Control
        return self._IsDeviceAccessibleInfo(device_info, mode)
%}
}

%rename(DeviceAccessMode_Control)   Pylon::Control;
%rename(DeviceAccessMode_Stream)    Pylon::Stream;
%rename(DeviceAccessMode_Event)     Pylon::Event;
%rename(DeviceAccessMode_Exclusive) Pylon::Exclusive;

%rename(set2) Pylon::AccessModeSet::set( size_t ); //warning removal
%ignore Pylon::AccessModeSet;
%include <pylon/DeviceAccessMode.h>;
%include <pylon/DeviceFactory.h>;
