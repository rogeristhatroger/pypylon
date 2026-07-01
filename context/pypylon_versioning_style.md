# pypylon Versioning

pypylon uses pep 440 date based versioning, e.g. 26.6 (https://packaging.python.org/en/latest/specifications/version-specifiers/ )
This is the version of pypylon.
Usually it contains the pylon C++ module versions for pylon C++ SDK and pylon Data Processing C++ SDK of the same release month, e.g.,
there may have been no corresponding pylon software suite release, but extensions and fixes are released for pypylon.
The change log contains:

the installer version of the pylon software suite version used for building.
the module version of pylon C++ SDK
the module version of pylon Data Processing C++ SDK
the GenICam GenApi version is not mentioned separately, as it is included in the pylon C++ SDK version.
If the pylon software suite start with non-zero patch version in its initial release, pypylon starts with a patch version of 0 that is omitted though.
The pypylon patch version is incremented to 1 or higher if subsequent pypylon releases are made in the same month.