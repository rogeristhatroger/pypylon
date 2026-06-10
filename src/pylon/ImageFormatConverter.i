%rename(ImageFormatConverter) Pylon::CImageFormatConverter;
%ignore CImageFormatConverterImpl;
%ignore CImageFormatConverterParams_Params;
%ignore Basler_ImageFormatConverterParams;
// CImageFormatConverter has a nested class (IOutputPixelFormatEnum) which
// is not supported by SWIG.
%ignore Pylon::CImageFormatConverter::IOutputPixelFormatEnum;

namespace Basler_ImageFormatConverterParams
{
   class CImageFormatConverterParams_Params
   {
   };
}
namespace Pylon
{
   using namespace Basler_ImageFormatConverterParams;
}

// added for backwards compatibility
%pythoncode %{
    InconvertibleEdgeHandling_Clip    = "Clip"
    InconvertibleEdgeHandling_Extend  = "Extend"
    InconvertibleEdgeHandling_SetZero = "SetZero"
    MonoConversionMethod_Gamma        = "Gamma"
    MonoConversionMethod_Truncate     = "Truncate"
    OutputBitAlignment_LsbAligned     = "LsbAligned"
    OutputBitAlignment_MsbAligned     = "MsbAligned"
    OutputOrientation_BottomUp        = "BottomUp"
    OutputOrientation_TopDown         = "TopDown"
    OutputOrientation_Unchanged       = "Unchanged"
%}


// Typemap to return a heap-allocated CPylonImage* with Python-owned lifetime.
// (Mirrors the same typemap in ImageDecompressor.i; defined here too because
// ImageFormatConverter.i is included before ImageDecompressor.i.)
%typemap(out) Pylon::CPylonImage*
    %{
        $result = SWIG_NewPointerObj($1, $descriptor(Pylon::CPylonImage*), SWIG_POINTER_OWN);
    %}

// Not all overloads of 'Convert' and 'ImageHasDestinationFormat' are usable. So we ignore all of them and
// redefine those that we want.
%extend Pylon::CImageFormatConverter {

    // Since '_Unpack' allocates a CPylonImage, it must not be called without
    // the GIL being held. Therefore we have to tell SWIG not to release the GIL
    // when calling it (%nothread).
    %nothread _Unpack;

    // Unpack any packed-format image into a CPylonImage.
    //
    // Accepts any image type (GrabResult, PylonDataComponent, PylonImage, …)
    // by taking the generic const IImage& interface.
    //
    // Throws Pylon::InvalidArgumentException when:
    //   * the source pixel type is not a packed format (IsPacked() == false), or
    //   * the packed format has no known unpacking target
    //     (GetPixelTypesForUnpacking() returns false).
    //
    // The returned CPylonImage is owned by the caller (Python GC manages it).
    static Pylon::CPylonImage* _Unpack(const Pylon::IImage& src)
    {
        const EPixelType pixelType = src.GetPixelType();

        // Validate: source must be a packed format
        if (!IsPacked(pixelType))
            throw INVALID_ARGUMENT_EXCEPTION(
                "Image pixel type is not packed, unable to unpack.");

        // Resolve the conversion types.
        // For Bayer packed formats GetPixelTypesForUnpacking returns a Mono
        // source-impose type so the converter treats the raw bits as Mono
        // (the geometry / metadata of the resulting CPylonImage still reflects
        // the original pixel type).
        EPixelType pixelTypeSourceImpose = PixelType_Undefined;
        EPixelType pixelTypeTarget       = PixelType_Undefined;
        if (!GetPixelTypesForUnpacking(pixelType, pixelTypeSourceImpose, pixelTypeTarget))
            throw INVALID_ARGUMENT_EXCEPTION(
                "Packed pixel format is not supported for unpacking.");

        CImageFormatConverter converter;
        converter.OutputPixelFormat  = pixelTypeTarget;
        converter.OutputBitAlignment = OutputBitAlignment_LsbAligned;

        Pylon::CPylonImage* pResult = new Pylon::CPylonImage();
        try
        {
            // Use the buffer-level Convert overload so we can pass
            // pixelTypeSourceImpose instead of the original pixelType.
            converter.Convert(
                *pResult,
                src.GetBuffer(),
                src.GetImageSize(),
                pixelTypeSourceImpose,
                src.GetWidth(),
                src.GetHeight(),
                src.GetPaddingX(),
                src.GetOrientation()
            );
        }
        catch (...)
        {
            delete pResult;
            throw;
        }

        return pResult;
    }

    // Repeat conversion from IImage.
    void Convert(IReusableImage& dst, const IImage& src)
    {
        $self->Convert(dst, src);
    }
    // Make sure CGrabResultPtr can be converted directly
    void Convert(IReusableImage& dst, const CGrabResultPtr& src)
    {
        $self->Convert(dst, src);
    }

    // Make sure IImage can be converted directly
    bool ImageHasDestinationFormat(const IImage& src)
    {
        return $self->ImageHasDestinationFormat(src);
    }

    // Make sure CGrabResultPtr can be converted directly
    bool ImageHasDestinationFormat(const CGrabResultPtr& src)
    {
        return $self->ImageHasDestinationFormat(src);
    }

    // Access nested class instance
    void SetOutputPixelFormat(EPixelType pxl_fmt)
    {
        $self->OutputPixelFormat.SetValue(pxl_fmt);
    }

    EPixelType GetOutputPixelFormat()
    {
        return $self->OutputPixelFormat.GetValue();
    }
    PROP_GETSET(OutputPixelFormat)

%pythoncode %{
    def __getattr__(self, attribute):
        if attribute in self.__dict__ or attribute in ( "thisown","this") or attribute.startswith("__"):
            return object.__getattr__(self, attribute)
        else:
            return _LookupInFixedParameterSet(self.GetNodeMap(), attribute)

    def __setattr__(self, attribute, val):
        if attribute == "OutputPixelFormat":
            self.SetOutputPixelFormat(val)
        elif attribute in self.__dict__ or attribute in ( "thisown","this") or attribute.startswith("__"):
            object.__setattr__(self, attribute, val)
        else:
            warnings.warn(f"Setting a feature value by direct assignment is deprecated. Use <nodemap>.{attribute}.Value = {val}", DeprecationWarning, stacklevel=2)
            self.GetNodeMap().GetNode(attribute).SetValue(val)

    def __dir__(self):
        l = dir(type(self))
        l.extend(self.__dict__.keys())
        nodes = []
        try:
            nodes = self.GetNodeMap().GetNodes()
            features = filter(lambda n: n.GetNode().IsFeature(), nodes)
            l.extend(x.GetNode().GetName() for x in features)
        except:
            pass
        return sorted(set(l))
%}
};

%ignore Pylon::CImageFormatConverter::Convert;
%ignore Pylon::CImageFormatConverter::ImageHasDestinationFormat;
%ignore Pylon::CImageFormatConverter::OutputPixelFormat;

// Method-qualified typemap: wrap the returned INodeMap& in an INodeMapWrapper
// carrying NodeMapType_ImageFormatConverter.
%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CImageFormatConverter::GetNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::INodeMapWrapper($1, Pylon::NodeMapType_ImageFormatConverter),
        $descriptor(Pylon::INodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%include <pylon/ImageFormatConverter.h>;
