%ignore CSimpleMutex;
%ignore TlMap;
%ignore ImplicitTlRefs;

%nodefaultctor Pylon::CTlFactory;
%rename(TlFactory) Pylon::CTlFactory;

%extend Pylon::CTlFactory
{
%pythoncode %{
    class TransportLayerContext:
        """Context manager for a transport layer created by TlFactory.

        Ensures ReleaseTl() is called when the context is exited, even if
        an exception occurs.

        Usage::

            with TlFactory.GetInstance().TransportLayer("BaslerGigE") as tl:
                devices = tl.EnumerateDevices()

            # or with a CTlInfo object:
            tls = TlFactory.GetInstance().EnumerateTls()
            with TlFactory.GetInstance().TransportLayer(tls[0]) as tl:
                devices = tl.EnumerateDevices()
        """
        def __init__(self, factory, tl_info):
            self._factory = factory
            self._tl_info = tl_info
            self._tl = None

        def __enter__(self):
            self._tl = self._factory.CreateTl(self._tl_info)
            return self._tl

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self._tl is not None:
                self._factory.ReleaseTl(self._tl)
                self._tl = None
            return False

    def TransportLayer(self, tl_info):
        """Return a context manager that creates and releases a transport layer.

        :param tl_info: A :class:`TlInfo` object or a device-class string
                        (e.g. ``"BaslerGigE"``).
        :returns: A context manager whose ``__enter__`` returns the
                  :class:`TransportLayer` object.
        """
        return self.TransportLayerContext(self, tl_info)
%}
}

////////////////////////////////////////////////////////////////////////////////
//
// TlInfoList output
//

%typemap(in, numinputs=0, noblock=1) Pylon::TlInfoList_t & {
  $1 = new Pylon::TlInfoList_t();
}

%typemap(argout) Pylon::TlInfoList_t & {
  Py_DECREF($result);
  PyObject *tpl = PyTuple_New($1->size());
  for (unsigned int i = 0; i < $1->size(); i++) {
    CTlInfo *ti = new CTlInfo((*$1)[i]);
    PyObject *item = SWIG_NewPointerObj(
        SWIG_as_voidptr(ti),
        SWIGTYPE_p_Pylon__CTlInfo,
        SWIG_POINTER_OWN
        );
    PyTuple_SetItem(tpl, i, item);
  }
  $result = tpl;
  delete $1;
}


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

// This out-typemap tries to downcast the TL to the specific implementation.
// Currently the only TL with an extended interface is GigE.
%typemap(out) Pylon::ITransportLayer*
%{
    if (0 == $1)
    {
        // CreateTl returns null when no matching TL is found – expose as None.
        $result = Py_None;
        Py_INCREF(Py_None);
    }
    else
    {
        swig_type_info *outtype = $descriptor(Pylon::IGigETransportLayer*);
        void *outptr = dynamic_cast<Pylon::IGigETransportLayer*>($1);
        if (!outptr)
        {
            outptr = $1;
            outtype = $descriptor(Pylon::ITransportLayer*);
        };
        // Must not own TL object, since calling delete on it is forbidden
        // by the pylon API. The user has to call tl.Release().
        $result = SWIG_NewPointerObj(outptr, outtype, 0);
    };
%}


%include <pylon/TlFactory.h>;

// now that the local typemaps are no longer needed, clear them.

%typemap(in) Pylon::TlInfoList_t&;
%typemap(argout) Pylon::TlInfoList_t&;
%typemap(out) Pylon::ITransportLayer*;
