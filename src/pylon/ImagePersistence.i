%rename (ImagePersistence) Pylon::CImagePersistence;
%rename (ImagePersistenceOptions) Pylon::CImagePersistenceOptions;
%ignore Pylon::CImagePersistence::Save(EImageFileFormat, const Pylon::String_t&, const void*, size_t, EPixelType, uint32_t, uint32_t, size_t, EImageOrientation, CImagePersistenceOptions*);
%ignore Pylon::CImagePersistence::LoadFromMemory(const void*, size_t, IReusableImage&);

%include <pylon/ImagePersistence.h>;

ADD_PROP_GETSET(ImagePersistenceOptions, Quality)