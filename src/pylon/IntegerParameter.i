%typemap(out) GenApi::int64_autovector_t {
    PyObject *o = PyTuple_New($1.size());
    for( unsigned int i = 0; i < $1.size(); i++){
        PyObject *o_item;
        o_item = PyLong_FromLongLong($1[i]);
        PyTuple_SetItem(o,i,o_item);
    }
    $result = SWIG_AppendOutput($result,o);
}

%rename (IntegerParameter) Pylon::CIntegerParameter;
#define GenICam GENICAM_NAMESPACE
%rename(_IIntegerEx) Pylon::IIntegerEx;
%ignore Pylon::CIntegerParameter::CIntegerParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CIntegerParameter::operator()();
%ignore Pylon::CIntegerParameter::operator*();
%ignore Pylon::CIntegerParameter::operator=( int64_t value );
%include <pylon/IntegerParameter.h>;

ADD_PROP_GETSET(IntegerParameter, Value)
ADD_PROP_GET(IntegerParameter, Min)
ADD_PROP_GET(IntegerParameter, Max)
ADD_PROP_GET(IntegerParameter, IncMode)
ADD_PROP_GET(IntegerParameter, Inc)
ADD_PROP_GET(IntegerParameter, ListOfValidValues)
ADD_PROP_GET(IntegerParameter, Representation)
ADD_PROP_GET(IntegerParameter, Unit)
ADD_PROP_GETSET(IntegerParameter, ValuePercentOfRange)
