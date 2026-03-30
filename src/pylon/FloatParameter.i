%typemap(out) GenApi::double_autovector_t {
    PyObject *o = PyTuple_New($1.size());
    for( unsigned int i = 0; i < $1.size(); i++){
        PyObject *o_item;
        o_item = PyFloat_FromDouble($1[i]);
        PyTuple_SetItem(o,i,o_item);
    }
    $result = SWIG_AppendOutput($result,o);
}

// GetAlternativeIntegerRepresentation(CIntegerParameter& parameter):
// The C++ API uses an output argument.  Wrap it as a return value so Python
// callers can write:   int_param = p.GetAlternativeIntegerRepresentation()
%typemap(in, numinputs=0) Pylon::CIntegerParameter& parameter
    (Pylon::CIntegerParameter tmp)
{
    $1 = &tmp;
}
%typemap(argout) Pylon::CIntegerParameter& parameter
{
    PyObject* obj = SWIG_NewPointerObj(
        new Pylon::CIntegerParameter(*$1),
        SWIGTYPE_p_Pylon__CIntegerParameter,
        SWIG_POINTER_OWN);
    $result = SWIG_AppendOutput($result, obj);
}

%rename (FloatParameter) Pylon::CFloatParameter;
#define GenICam GENICAM_NAMESPACE
%rename(_IFloatEx) Pylon::IFloatEx;
%ignore Pylon::CFloatParameter::CFloatParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CFloatParameter::operator()();
%ignore Pylon::CFloatParameter::operator*();
%ignore Pylon::CFloatParameter::operator=( double value );
%include <pylon/FloatParameter.h>;

ADD_PROP_GETSET(FloatParameter, Value)
ADD_PROP_GET(FloatParameter, Min)
ADD_PROP_GET(FloatParameter, Max)
ADD_PROP_GET(FloatParameter, IncMode)
ADD_PROP_GET(FloatParameter, Inc)
ADD_PROP_GET(FloatParameter, ListOfValidValues)
ADD_PROP_GET(FloatParameter, Representation)
ADD_PROP_GET(FloatParameter, DisplayNotation)
ADD_PROP_GET(FloatParameter, DisplayPrecision)
ADD_PROP_GET(FloatParameter, Unit)
ADD_PROP_GETSET(FloatParameter, ValuePercentOfRange)
