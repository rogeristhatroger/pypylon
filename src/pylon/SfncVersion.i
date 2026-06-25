#define Sfnc_VersionUndefined Sfnc_VersionUndefined = Pylon::VersionInfo
// SWIG does not understand the C++ "direct initialization" syntax (Type var(args)) for global/namespace-scope variables.
// It interprets the parentheses as a function parameter list, so SWIG thinks this declares a function
// Sfnc_VersionUndefined taking three int arguments and returning VersionInfo — not a const VersionInfo object.
// Work around this by using the preprocessor to replace the variable declarations with something that SWIG can understand.
#define Sfnc_1_2_1 Sfnc_1_2_1 = Pylon::VersionInfo
#define Sfnc_1_3_0 Sfnc_1_3_0 = Pylon::VersionInfo
#define Sfnc_1_4_0 Sfnc_1_4_0 = Pylon::VersionInfo
#define Sfnc_1_5_0 Sfnc_1_5_0 = Pylon::VersionInfo
#define Sfnc_1_5_1 Sfnc_1_5_1 = Pylon::VersionInfo
#define Sfnc_2_0_0 Sfnc_2_0_0 = Pylon::VersionInfo
#define Sfnc_2_1_0 Sfnc_2_1_0 = Pylon::VersionInfo
#define Sfnc_2_2_0 Sfnc_2_2_0 = Pylon::VersionInfo
#define Sfnc_2_3_0 Sfnc_2_3_0 = Pylon::VersionInfo
#define Sfnc_2_4_0 Sfnc_2_4_0 = Pylon::VersionInfo
#define Sfnc_2_5_0 Sfnc_2_5_0 = Pylon::VersionInfo

%include <pylon/SfncVersion.h>
