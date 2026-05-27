// ImageMixin.i
//
// Module-level Python helper functions shared by PylonDataComponent,
// PylonImage and GrabResultPtr to avoid code duplication.

%pythoncode %{
from contextlib import contextmanager
import sys

def _image_get_image_format(self, pt=None):
    """Common GetImageFormat implementation used by PylonDataComponent, PylonImage and GrabResultPtr."""
    if pt is None:
        pt = self.GetPixelType()
    if IsPacked(pt):
        raise ValueError("Packed Formats are not supported with numpy interface")
    if pt in ( PixelType_Mono8, PixelType_BayerGR8, PixelType_BayerRG8, PixelType_BayerGB8, PixelType_BayerBG8, PixelType_Confidence8, PixelType_Coord3D_C8 ):
        shape = (self.GetHeight(), self.GetWidth())
        format = "B"
        dtype = _pylon_numpy.uint8
    elif pt in ( PixelType_Mono10, PixelType_BayerGR10, PixelType_BayerRG10, PixelType_BayerGB10, PixelType_BayerBG10 ):
        shape = (self.GetHeight(), self.GetWidth())
        format = "H"
        dtype = _pylon_numpy.uint16
    elif pt in ( PixelType_Mono12, PixelType_BayerGR12, PixelType_BayerRG12, PixelType_BayerGB12, PixelType_BayerBG12 ):
        shape = (self.GetHeight(), self.GetWidth())
        format = "H"
        dtype = _pylon_numpy.uint16
    elif pt in ( PixelType_Mono16, PixelType_BayerGR16, PixelType_BayerRG16, PixelType_BayerGB16, PixelType_BayerBG16, PixelType_Confidence16, PixelType_Coord3D_C16 ):
        shape = (self.GetHeight(), self.GetWidth())
        format = "H"
        dtype = _pylon_numpy.uint16
    elif pt in ( PixelType_RGB8packed, PixelType_BGR8packed ):
        shape = (self.GetHeight(), self.GetWidth(), 3)
        dtype = _pylon_numpy.uint8
        format = "B"
    elif pt in ( PixelType_RGB12packed, PixelType_BGR12packed, PixelType_RGB10packed, PixelType_BGR10packed ):
        shape = (self.GetHeight(), self.GetWidth(), 3)
        format = "H"
        dtype = _pylon_numpy.uint16
    elif pt in ( PixelType_YUV422_YUYV_Packed, PixelType_YUV422packed ):
        shape = (self.GetHeight(), self.GetWidth(), 2)
        dtype = _pylon_numpy.uint8
        format = "B"
    elif pt in ( PixelType_Coord3D_ABC32f, ):
        shape = (self.GetHeight(), self.GetWidth(), 3)
        dtype = _pylon_numpy.float32
        format = "f"
    elif pt in ( PixelType_Data32f, ):
        shape = (self.GetHeight(), self.GetWidth(), 1)
        dtype = _pylon_numpy.float32
        format = "f"
    elif pt in ( PixelType_BiColorRGBG8, PixelType_BiColorBGRG8 ):
        shape = (self.GetHeight(), self.GetWidth() * 2)
        format = "B"
        dtype = _pylon_numpy.uint8
    elif pt in ( PixelType_BiColorRGBG10, PixelType_BiColorBGRG10, PixelType_BiColorRGBG12, PixelType_BiColorBGRG12 ):
        shape = (self.GetHeight(), self.GetWidth() * 2)
        format = "H"
        dtype = _pylon_numpy.uint16
    else:
        raise ValueError("Pixel format currently not supported")

    return (shape, dtype, format)


def _image_get_array(self, raw, get_buffer_func, get_size_func, strides_func=None):
    """Common GetArray core implementation.

    Parameters
    ----------
    raw            : bool          – return raw byte buffer when True
    get_buffer_func: callable()    – returns the image/payload buffer
    get_size_func  : callable()    – returns the size for the raw case
    strides_func   : callable(dtype) or None
                                  – optional function that receives the numpy
                                    dtype and returns strides (or None for
                                    contiguous arrays).
    """
    if raw:
        shape = get_size_func()
        buf = get_buffer_func()
        return _pylon_numpy.ndarray(shape, dtype=_pylon_numpy.uint8, buffer=buf)

    pt = self.GetPixelType()
    if IsPacked(pt):
        unpacked = ImageFormatConverter._Unpack(self)
        shape, dtype, format = _image_get_image_format(unpacked)
        buf = unpacked.GetBuffer()
    else:
        shape, dtype, format = self.GetImageFormat(pt)
        buf = get_buffer_func()

    strides = strides_func(dtype) if strides_func is not None else None
    return _pylon_numpy.ndarray(shape, dtype=dtype, buffer=buf, strides=strides)


def _image_array_zero_copy_gen(self, memory_view_func, raw=False):
    """Generator backing GetArrayZeroCopy for all image-like classes.

    Callers should wrap this with @contextmanager + @needs_numpy and
    yield from it::

        @contextmanager
        @needs_numpy
        def GetArrayZeroCopy(self, raw=False):
            yield from _image_array_zero_copy_gen(self, self.GetMemoryView, raw)
    """
    # For packed formats we cannot zero-copy; unpack into a CPylonImage first
    # and hand back a regular array.
    pt = self.GetPixelType()
    if IsPacked(pt):
        yield ImageFormatConverter._Unpack(self).GetArray()
        return

    mv = memory_view_func()
    if not raw:
        shape, dtype, format = self.GetImageFormat()
        mv = mv.cast(format, shape)

    ar = _pylon_numpy.asarray(mv)

    # trace external references to array
    initial_refcount = sys.getrefcount(ar)

    # yield the array to the context code
    yield ar

    # detect if more refs than the one from the yield are held
    if sys.getrefcount(ar) > initial_refcount + 1:
        raise RuntimeError("Please remove any references to the array before leaving context manager scope!!!")

    # release the memory view
    mv.release()
%}

