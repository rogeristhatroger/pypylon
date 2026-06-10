// ---------------------------------------------------------------------------
// PlaceholderParameter.i
//
// SWIG binding for Pylon::CPlaceholderParameter.
//
// The Python layer adds:
//   - SetValue / GetValue for every value type used by the standard Pylon
//     parameter classes.  All raise LogicalErrorException with a message
//     that includes the stored path.
//   - Every Try* and *OrDefault method from all standard parameter types.
//     Try*          -> always returns False (never raises)
//     *OrDefault    -> always returns the supplied default (never raises)
// ---------------------------------------------------------------------------

%rename(PlaceholderParameter) Pylon::CPlaceholderParameter;
%ignore Pylon::CPlaceholderParameter::operator=;

%include "PlaceholderParameter.h"

// Properties present in CParameter (base)
ADD_PROP_GET(PlaceholderParameter, Node)
ADD_PROP_GET(PlaceholderParameter, AccessMode)
ADD_PROP_GET(PlaceholderParameter, Path)

// Standard value-type properties (Integer / Float)
ADD_PROP_GET(PlaceholderParameter, Min)
ADD_PROP_GET(PlaceholderParameter, Max)
ADD_PROP_GET(PlaceholderParameter, IncMode)
ADD_PROP_GET(PlaceholderParameter, Inc)
ADD_PROP_GET(PlaceholderParameter, ListOfValidValues)
ADD_PROP_GET(PlaceholderParameter, Representation)
ADD_PROP_GET(PlaceholderParameter, Unit)
ADD_PROP_GET(PlaceholderParameter, FloatAlias)
ADD_PROP_GET(PlaceholderParameter, DisplayNotation)
ADD_PROP_GET(PlaceholderParameter, DisplayPrecision)

// String properties
ADD_PROP_GET(PlaceholderParameter, MaxLength)
ADD_PROP_GET(PlaceholderParameter, Length)

// Enum properties
ADD_PROP_GET(PlaceholderParameter, Symbolic)
ADD_PROP_GET(PlaceholderParameter, Symbolics)
ADD_PROP_GET(PlaceholderParameter, Entries)
ADD_PROP_GETSET(PlaceholderParameter, IntValue)

// EnumEntry properties
ADD_PROP_GET(PlaceholderParameter, NumericValue)

// Category / Register / Port properties
ADD_PROP_GET(PlaceholderParameter, Features)
ADD_PROP_GET(PlaceholderParameter, Address)
ADD_PROP_GET(PlaceholderParameter, ChunkID)

// Read/write compound properties
ADD_PROP_GETSET(PlaceholderParameter, Value)
ADD_PROP_GETSET(PlaceholderParameter, ValuePercentOfRange)

%extend Pylon::CPlaceholderParameter {

    // ------------------------------------------------------------------
    // Helper used by every raising getter/setter.
    // Raises pylon.LogicalErrorException with the stored path.
    // ------------------------------------------------------------------
    %pythoncode %{
        def _raise_not_available(self, action="access"):
            from pypylon import pylon
            path = self.GetPath()
            msg = (
                f"PlaceholderParameter: Cannot {action} '{path}'. "
                f"The parameter is not available."
            )
            raise pylon.LogicalErrorException(msg)
    %}

    // ------------------------------------------------------------------
    // Integer / Float range properties
    // ------------------------------------------------------------------
    %pythoncode %{
        def GetMin(self, *args, **kwargs):
            """GetMin always raises — the parameter is not available."""
            self._raise_not_available("get Min value of")

        def GetMax(self, *args, **kwargs):
            """GetMax always raises — the parameter is not available."""
            self._raise_not_available("get Max value of")

        def GetIncMode(self, *args, **kwargs):
            """GetIncMode always raises — the parameter is not available."""
            self._raise_not_available("get IncMode of")

        def GetInc(self, *args, **kwargs):
            """GetInc always raises — the parameter is not available."""
            self._raise_not_available("get Inc value of")

        def GetListOfValidValues(self, *args, **kwargs):
            """GetListOfValidValues always raises — the parameter is not available."""
            self._raise_not_available("get ListOfValidValues of")

        def GetRepresentation(self, *args, **kwargs):
            """GetRepresentation always raises — the parameter is not available."""
            self._raise_not_available("get Representation of")

        def GetUnit(self, *args, **kwargs):
            """GetUnit always raises — the parameter is not available."""
            self._raise_not_available("get Unit of")

        def GetFloatAlias(self, *args, **kwargs):
            """GetFloatAlias always raises — the parameter is not available."""
            self._raise_not_available("get FloatAlias of")

        def GetDisplayNotation(self, *args, **kwargs):
            """GetDisplayNotation always raises — the parameter is not available."""
            self._raise_not_available("get DisplayNotation of")

        def GetDisplayPrecision(self, *args, **kwargs):
            """GetDisplayPrecision always raises — the parameter is not available."""
            self._raise_not_available("get DisplayPrecision of")
    %}

    // ------------------------------------------------------------------
    // String properties
    // ------------------------------------------------------------------
    %pythoncode %{
        def GetMaxLength(self, *args, **kwargs):
            """GetMaxLength always raises — the parameter is not available."""
            self._raise_not_available("get MaxLength of")

        def GetLength(self, *args, **kwargs):
            """GetLength always raises — the parameter is not available."""
            self._raise_not_available("get Length of")
    %}

    // ------------------------------------------------------------------
    // Enum properties
    // ------------------------------------------------------------------
    %pythoncode %{
        def GetSymbolic(self, *args, **kwargs):
            """GetSymbolic always raises — the parameter is not available."""
            self._raise_not_available("get Symbolic of")

        def GetSymbolics(self, *args, **kwargs):
            """GetSymbolics always raises — the parameter is not available."""
            self._raise_not_available("get Symbolics of")

        def GetEntries(self, *args, **kwargs):
            """GetEntries always raises — the parameter is not available."""
            self._raise_not_available("get Entries of")

        def GetIntValue(self, *args, **kwargs):
            """GetIntValue always raises — the parameter is not available."""
            self._raise_not_available("get IntValue of")

        def SetIntValue(self, value, *args, **kwargs):
            """SetIntValue always raises — the parameter is not available."""
            self._raise_not_available("set IntValue of")
    %}

    // ------------------------------------------------------------------
    // EnumEntry properties
    // ------------------------------------------------------------------
    %pythoncode %{
        def GetNumericValue(self, *args, **kwargs):
            """GetNumericValue always raises — the parameter is not available."""
            self._raise_not_available("get NumericValue of")
    %}

    // ------------------------------------------------------------------
    // Category / Register / Port properties
    // ------------------------------------------------------------------
    %pythoncode %{
        def GetFeatures(self, *args, **kwargs):
            """GetFeatures always raises — the parameter is not available."""
            self._raise_not_available("get Features of")

        def GetAddress(self, *args, **kwargs):
            """GetAddress always raises — the parameter is not available."""
            self._raise_not_available("get Address of")

        def GetChunkID(self, *args, **kwargs):
            """GetChunkID always raises — the parameter is not available."""
            self._raise_not_available("get ChunkID of")
    %}

    // ------------------------------------------------------------------
    // Value / ValuePercentOfRange (GETSET)
    // ------------------------------------------------------------------
    %pythoncode %{
        def GetValue(self, *args, **kwargs):
            """GetValue always raises — the parameter is not available."""
            self._raise_not_available("get value of")

        def SetValue(self, value, *args, **kwargs):
            """SetValue always raises — the parameter is not available."""
            self._raise_not_available("set value of")

        def GetValuePercentOfRange(self, *args, **kwargs):
            """GetValuePercentOfRange always raises — the parameter is not available."""
            self._raise_not_available("get ValuePercentOfRange of")

        def SetValuePercentOfRange(self, value, *args, **kwargs):
            """SetValuePercentOfRange always raises — the parameter is not available."""
            self._raise_not_available("set ValuePercentOfRange of")
    %}

    // ------------------------------------------------------------------
    // Execute
    // ------------------------------------------------------------------
    %pythoncode %{
        def Execute(self, *args, **kwargs):
            """Execute always raises — the parameter is not available."""
            self._raise_not_available("execute")
    %}

    // ------------------------------------------------------------------
    // Try* — always False, never raise
    // ------------------------------------------------------------------
    %pythoncode %{
        def TrySetValue(self, *args, **kwargs):
            """TrySetValue always returns False — the parameter is not available."""
            return False

        def TryExecute(self):
            """TryExecute always returns False — the parameter is not available."""
            return False

        def TrySetValuePercentOfRange(self, percentOfRange):
            """TrySetValuePercentOfRange always returns False — the parameter is not available."""
            return False

        def TrySetToMaximum(self):
            """TrySetToMaximum always returns False — the parameter is not available."""
            return False

        def TrySetToMinimum(self):
            """TrySetToMinimum always returns False — the parameter is not available."""
            return False
    %}

    // ------------------------------------------------------------------
    // *OrDefault — always return supplied default, never raise
    // ------------------------------------------------------------------
    %pythoncode %{
        def GetValueOrDefault(self, defaultValue):
            """GetValueOrDefault always returns defaultValue — the parameter is not available."""
            return defaultValue

        def CanSetValue(self, value):
            """CanSetValue always returns False — the parameter is not available."""
            return False
    %}
}
