%ignore IsValidRGB;
%ignore IsValidBGR;
%ignore PixelSize;
%ignore PixelType;

// ---------------------------------------------------------------------------
// Pylon::EPixelType typemaps
//
// Eight EPixelType enumerators set PIXEL_CUSTOMTYPE (0x80000000), so their
// 32-bit bit pattern has the MSB set (e.g. PixelType_YUV420planar =
// 0x820C0040). sizeof(EPixelType) is 4 on MSVC but 8 on GCC/Clang (LP64
// Linux), and SWIG's default enum handling routes values through a signed
// int. That narrowing-plus-sign-extension breaks the round-trip on Linux:
// PlaneCount(PixelType_YUV420planar) returns 1 instead of 3.
//
// Fix, in three parts:
//   1. `in` typemap reads a long long, and normalizes any legacy negative
//      32-bit encoding (e.g. -2113142720) back to its unsigned bit pattern
//      before casting to EPixelType. PixelType_Undefined (-1) is left alone
//      so it still sign-extends to the full enum width naturally.
//   2. `out` typemap emits values through `unsigned int -> long long`,
//      giving the canonical positive 32-bit bit pattern on every platform.
//      PixelType_Undefined is special-cased to keep its documented value of
//      -1.
//   3. `%init` block re-registers the 8 PIXEL_CUSTOMTYPE constants via the
//      same `unsigned int -> long long` path, because SWIG 4.3's Python
//      backend hard-codes enum-constant emission to SWIG_From_int and
//      neither %typemap(constcode) nor %apply long retargets it.
//

%typemap(in, fragment=SWIG_AsVal_frag(long long)) Pylon::EPixelType {
    long long _epx_tmp;
    int _epx_res = SWIG_AsVal_long_SS_long($input, &_epx_tmp);
    if (!SWIG_IsOK(_epx_res)) {
        SWIG_exception_fail(
            SWIG_ArgError(_epx_res),
            "in method '$symname', argument $argnum of type 'Pylon::EPixelType'"
        );
    }
    // Re-interpret legacy negative 32-bit encodings of MSB-set enumerators
    // as unsigned bit patterns. -1 (PixelType_Undefined) is excluded so it
    // sign-extends naturally to match the enum on every platform.
    if (_epx_tmp >= INT_MIN && _epx_tmp < 0 && _epx_tmp != -1) {
        $1 = static_cast<Pylon::EPixelType>(
            static_cast<unsigned int>(static_cast<int>(_epx_tmp))
        );
    } else {
        $1 = static_cast<Pylon::EPixelType>(_epx_tmp);
    }
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_INTEGER,
         fragment=SWIG_AsVal_frag(long long)) Pylon::EPixelType {
    long long _epx_val;
    $1 = SWIG_IsOK(SWIG_AsVal_long_SS_long($input, &_epx_val)) ? 1 : 0;
}

%typemap(out, fragment=SWIG_From_frag(long long)) Pylon::EPixelType {
    if ($1 == Pylon::PixelType_Undefined) {
        $result = SWIG_From_int(-1);
    } else {
        $result = SWIG_From_long_SS_long(
            static_cast<long long>(static_cast<unsigned int>($1))
        );
    }
}

%include<pylon/PixelType.h>;

// Overwrite the 8 PIXEL_CUSTOMTYPE (MSB-set) enumerators SWIG emitted via
// SWIG_From_int so the module-level Python constants agree with the `out`
// typemap above. All other EPixelType values have the MSB clear and are
// left as SWIG emits them.
%init %{
    #define PYPYLON_OVERRIDE_EPT(name)                                         \
        SWIG_Python_SetConstant(                                               \
            d,                                                                 \
            #name,                                                             \
            SWIG_From_long_SS_long(                                            \
                static_cast<long long>(                                        \
                    static_cast<unsigned int>(Pylon::name)                     \
                )                                                              \
            )                                                                  \
        )

    PYPYLON_OVERRIDE_EPT(PixelType_Mono1packed);
    PYPYLON_OVERRIDE_EPT(PixelType_Mono2packed);
    PYPYLON_OVERRIDE_EPT(PixelType_Mono4packed);
    PYPYLON_OVERRIDE_EPT(PixelType_YUV444planar);
    PYPYLON_OVERRIDE_EPT(PixelType_YUV422planar);
    PYPYLON_OVERRIDE_EPT(PixelType_YUV420planar);
    PYPYLON_OVERRIDE_EPT(PixelType_Double);
    PYPYLON_OVERRIDE_EPT(PixelType_Error8);

    #undef PYPYLON_OVERRIDE_EPT
%}
