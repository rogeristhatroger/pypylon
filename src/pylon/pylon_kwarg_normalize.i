// pylon_kwarg_normalize.i
//
// SWIG %define macros to normalize pylon C*Parameter method parameter names
// to match the PascalCase names used by the underlying GenAPI interfaces.
//
// SWIG uses C++ parameter names as Python keyword-argument names.  The pylon
// headers use camelCase while GenAPI uses PascalCase, which breaks code that
// calls pylon wrappers with the same keyword arguments used for raw GenAPI
// objects.
//
// Using %define/%enddef (rather than separate %include files) guarantees the
// #define directives expand inline at the call site, in exactly the same
// preprocessor scope as the %include <pylon/XxxParameter.h> that follows.
//
// Usage – bracket every %include of a pylon Parameter header:
//
//   %include "pylon_kwarg_normalize.i"
//
//   PYLON_KWARG_NORMALIZE_BEGIN
//   %include <pylon/XxxParameter.h>
//   PYLON_KWARG_NORMALIZE_END
//
// Normalisation table (pylon camelCase -> GenAPI PascalCase):
//
//   verify      -> Verify      : GetValue, ToString, FromString, SetValue,
//                                SetIntValue, Execute, IsDone, Get, Set,
//                                GetLength, GetAddress, GetMaxLength,
//                                GetCurrentEntry, GetIntValue
//   ignoreCache -> IgnoreCache : GetValue, ToString, Get, GetCurrentEntry,
//                                GetIntValue
//   value       -> Value       : SetValue, TrySetValue, CanSetValue,
//                                ImposeMax, ImposeMin, operator=,
//                                GetEntryByNameAsParameter
//   valueStr    -> ValueStr    : FromString, IEnumeration::operator=
//   symbolic    -> Symbolic    : GetEntryByName
//   intValue    -> IntValue    : GetEntry
//   length      -> Length      : Get, Set  (ArrayParameter)
//
// Not normalised:
//   bounded     – already lowercase in GenAPI
//   symbolics   – argout parameter, invisible as kwarg
//   entries     – argout parameter, invisible as kwarg
//------------------------------------------------------------------------------

%define PYLON_KWARG_NORMALIZE_BEGIN
#define verify      Verify
#define ignoreCache IgnoreCache
#define value       Value
#define valueStr    ValueStr
#define symbolic    Symbolic
#define intValue    IntValue
#define length      Length
%enddef

%define PYLON_KWARG_NORMALIZE_END
#undef verify
#undef ignoreCache
#undef value
#undef valueStr
#undef symbolic
#undef intValue
#undef length
%enddef

