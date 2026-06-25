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

    // Writes the converted image directly into a caller-supplied raw memory
    // region identified by its address and byte count.
    //
    // This internal helper is called exclusively from ConvertToArray (Python
    // level), which passes result.ctypes.data (memory address as a Python int)
    // and result.nbytes. Using raw integers avoids the Python buffer protocol
    // (Py_buffer / PyObject_GetBuffer) which is not part of the stable ABI
    // before Python 3.11. SWIG releases the GIL for the duration of the
    // (CPU-intensive) conversion as usual.
    void _ConvertToBuffer(unsigned long long dst_ptr, size_t dst_size, const IImage& src)
    {
        $self->Convert(
            reinterpret_cast<void*>(static_cast<uintptr_t>(dst_ptr)),
            dst_size,
            src
        );
    }

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

    @needs_numpy
    def ConvertToArray(self, src, raw=False):
        """Convert src directly into a pre-allocated NumPy array without an extra copy.

        Unlike ``converter.Convert(src).Array``, this method avoids the
        additional buffer copy that occurs when retrieving the pixel data from
        the intermediate :class:`PylonImage`: a NumPy array with the correct
        shape and dtype is pre-allocated and the format converter writes the
        converted pixels directly into its memory.

        Packed output formats (e.g. ``PixelType_Mono10packed``) are not
        supported when ``raw=False`` because they have no unambiguous NumPy
        shape/dtype representation.  Use ``raw=True`` to obtain the raw bytes
        in that case.

        Parameters
        ----------
        src : GrabResult, PylonImage, PylonDataComponent, or any IImage
            The source image to convert.  All source types accepted by
            :meth:`Convert` are supported.
        raw : bool, optional
            When ``True``, return a flat ``uint8`` array of the raw converted
            bytes.  In this mode the array has no pixel-format-specific shape
            or dtype interpretation, and packed output formats are allowed.
            When ``False`` (default), the array shape and dtype reflect the
            ``OutputPixelFormat`` setting.

        Returns
        -------
        numpy.ndarray
            The converted image as a NumPy array.

        Raises
        ------
        ValueError
            If ``raw=False`` and ``OutputPixelFormat`` is a packed pixel
            format.  Packed formats have no unambiguous NumPy shape/dtype
            representation.  Either set ``OutputPixelFormat`` to a non-packed
            format (e.g. ``PixelType_Mono8``, ``PixelType_RGB8packed``) or
            pass ``raw=True`` to obtain the raw bytes.

        Examples
        --------
        >>> converter = pylon.ImageFormatConverter()
        >>> converter.OutputPixelFormat = pylon.PixelType_RGB8packed
        >>> array = converter.ConvertToArray(grab_result)
        """
        output_pixel_type = self.OutputPixelFormat

        if raw:
            buffer_size = self.GetBufferSizeForConversion(
                src.GetPixelType(), src.GetWidth(), src.GetHeight()
            )
            result = _pylon_numpy.empty(buffer_size, dtype=_pylon_numpy.uint8)
            self._ConvertToBuffer(result.ctypes.data, result.nbytes, src)
            return result

        if IsPacked(output_pixel_type):
            raise ValueError("Packed Formats are not supported with numpy interface")

        shape, dtype, _ = _image_get_image_format(src, pt=output_pixel_type)
        result = _pylon_numpy.empty(shape, dtype=dtype)
        self._ConvertToBuffer(result.ctypes.data, result.nbytes, src)
        return result
%}
};

%ignore Pylon::CImageFormatConverter::Convert;
%ignore Pylon::CImageFormatConverter::ImageHasDestinationFormat;
%ignore Pylon::CImageFormatConverter::OutputPixelFormat;

// Method-qualified typemap: wrap the returned INodeMap& in an NodeMapWrapper
// carrying NodeMapType_ImageFormatConverter.
%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CImageFormatConverter::GetNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::NodeMapWrapper($1, Pylon::NodeMapType_ImageFormatConverter),
        $descriptor(Pylon::NodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%include <pylon/ImageFormatConverter.h>;
