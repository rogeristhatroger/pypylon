%rename (BooleanParameter) Pylon::CBooleanParameter;
#define GenICam GENICAM_NAMESPACE
%rename(_IBooleanEx) Pylon::IBooleanEx;
%ignore Pylon::CBooleanParameter::CBooleanParameter(GENAPI_NAMESPACE::INodeMap &,char const *);
%ignore Pylon::CBooleanParameter::operator()();
%ignore Pylon::CBooleanParameter::operator*();
%ignore Pylon::CBooleanParameter::operator=( bool value );
%include "pylon_kwarg_normalize.i"
PYLON_KWARG_NORMALIZE_BEGIN
%include <pylon/BooleanParameter.h>
PYLON_KWARG_NORMALIZE_END

ADD_PROP_GETSET(BooleanParameter, Value)

%extend Pylon::CBooleanParameter {
    %pythoncode %{
        def __str__(self):
            if not self.IsValid():
                result = "<not found>"
            elif not self.IsReadable():
                result = "<not readable>"
            else:
                result = str(True) if self.GetValue() else str(False)
            return result
    %}
}

