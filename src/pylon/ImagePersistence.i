%rename (ImagePersistence) Pylon::CImagePersistence;
%rename (ImagePersistenceOptions) Pylon::CImagePersistenceOptions;
%ignore Pylon::CImagePersistence::Save(EImageFileFormat, const Pylon::String_t&, const void*, size_t, EPixelType, uint32_t, uint32_t, size_t, EImageOrientation, CImagePersistenceOptions*);
%ignore Pylon::CImagePersistence::LoadFromMemory(const void*, size_t, IReusableImage&);

%extend Pylon::CImagePersistence {
%pythoncode %{
    @staticmethod
    @needs_numpy
    def SaveArray(image_file_format, filename, array, pixel_type, options=None):
        """Save a NumPy array as an image file.

        A convenience wrapper around :meth:`Save` that accepts a NumPy array
        directly instead of a :class:`PylonImage` or grab result.  Internally
        a :class:`PylonImage` is created and the array is attached to it
        before calling :meth:`Save`.

        Parameters
        ----------
        image_file_format : EImageFileFormat
            Target file format (e.g. ``pylon.ImageFileFormat_Png``).
        filename : str
            Destination file path.
        array : numpy.ndarray
            Image data.  Must be a 2-D array ``(height, width)`` for
            single-channel formats or a 3-D array ``(height, width, channels)``
            for multi-channel formats.  Must be C-contiguous.
        pixel_type : EPixelType
            Pixel type that describes the layout of *array*
            (e.g. ``pylon.PixelType_Mono8``, ``pylon.PixelType_RGB8packed``).
        options : ImagePersistenceOptions, optional
            Save options (e.g. JPEG quality).  When omitted the default
            quality (90) is used.

        Examples
        --------
        >>> import numpy as np
        >>> array = np.zeros((480, 640), dtype=np.uint8)
        >>> pylon.ImagePersistence.SaveArray(
        ...     pylon.ImageFileFormat_Png, "output.png", array, pylon.PixelType_Mono8
        ... )
        """
        with PylonImage() as image:
            image.AttachArray(array, pixel_type)
            if options is None:
                ImagePersistence.Save(image_file_format, filename, image)
            else:
                ImagePersistence.Save(image_file_format, filename, image, options)
%}
}

%include <pylon/ImagePersistence.h>;

ADD_PROP_GETSET(ImagePersistenceOptions, Quality)

