%ignore WaitObjectsImpl;

// ---------------------------------------------------------------------------
// pIndex typemaps for WaitForAny / WaitForAnyEx
//
// The C++ signature uses  unsigned int *pIndex = NULL  as an optional output
// parameter. The typemaps below make it usable from Python while keeping
// backward compatibility:
//
//   container.WaitForAny(timeout)            -> bool          (no index)
//   container.WaitForAny(timeout, None)      -> bool          (no index)
//   container.WaitForAny(timeout, True)      -> (bool, int)   (with index)
//
// The same pattern applies to WaitForAnyEx.
// ---------------------------------------------------------------------------

// --- typecheck (overload resolution) ---
%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER) unsigned int *pIndex {
    $1 = ($input == Py_None || $input == Py_True);
}

// --- in ---
%typemap(in) unsigned int *pIndex (unsigned int temp_index = 0) {
    if ($input == Py_None) {
        $1 = NULL;
    } else if ($input == Py_True) {
        temp_index = 0;
        $1 = &temp_index;
    } else {
        SWIG_exception_fail(SWIG_TypeError,
            "pIndex must be None (no index output) or True (return index)");
    }
}

// --- argout: append index to result when pIndex was not NULL ---
%typemap(argout) unsigned int *pIndex {
    if ($1 != NULL) {
        PyObject *orig = $result;
        $result = PyTuple_New(2);
        if (!$result) SWIG_fail;
        PyTuple_SET_ITEM($result, 0, orig);
        PyTuple_SET_ITEM($result, 1, PyLong_FromUnsignedLong(*$1));
    }
}

%include <pylon/WaitObjects.h>;