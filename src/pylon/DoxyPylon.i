
// File: index.xml

// File: class_pylon_1_1_access_mode_set.xml


%feature("docstring") Pylon::AccessModeSet "

Collection of access mode bits.  

Used for defining how a device is accessed.  

par: Low Level API:
    This set is used when a device is opened. The combination of different
    access modes specifies how the device is opened. Not all combinations may be
    allowed because the device implementations have certain restrictions.  
  

See also: The method of IDevice::Open() uses it to define a default value.  

See also: The global operator |( EDeviceAccessMode lhs, EDeviceAccessMode rhs )
    allows to combine two modes to a set.  

C++ includes: DeviceAccessMode.h
";

%feature("docstring") Pylon::AccessModeSet::AccessModeSet "

Default constructor creates an empty set.  
";

%feature("docstring") Pylon::AccessModeSet::AccessModeSet "

Converts an access mode into a set.  
";

%feature("docstring") Pylon::AccessModeSet::AccessModeSet "

Copy constructor.  
";

%feature("docstring") Pylon::AccessModeSet::AccessModeSet "
";

%feature("docstring") Pylon::AccessModeSet::~AccessModeSet "
";

// File: class_pylon_1_1_avi_writer_fatal_exception.xml


%feature("docstring") Pylon::AviWriterFatalException "

Exception thrown if a fatal error occurs (e.g. access violations, ...) when
accessing an AVI video file.  

C++ includes: AviWriter.h
";

%feature("docstring") Pylon::AviWriterFatalException::AviWriterFatalException "
";

%feature("docstring") Pylon::AviWriterFatalException::AviWriterFatalException "
";

%feature("docstring") Pylon::AviWriterFatalException::AviWriterFatalException "
";

// File: class_pylon_1_1_base___callback1_body.xml


%feature("docstring") Pylon::Base_Callback1Body "
";

%feature("docstring") Pylon::Base_Callback1Body::~Base_Callback1Body "

destructor  
";

%feature("docstring") Pylon::Base_Callback1Body::clone "

deep copy  
";

// File: class_pylon_1_1_c_acquire_continuous_configuration.xml


%feature("docstring") Pylon::CAcquireContinuousConfiguration "

Changes the configuration of the camera to free-running continuous acquisition.  

The `CAcquireContinuousConfiguration` is the default configuration of the
Instant Camera class. The CAcquireContinuousConfiguration is automatically
registered when an Instant Camera object is created.  

This instant camera configuration is provided as header-only file. The code can
be copied and modified for creating own configuration classes.  

C++ includes: AcquireContinuousConfiguration.h
";

%feature("docstring") Pylon::CAcquireContinuousConfiguration::~CAcquireContinuousConfiguration "

Destructor.  
";

%feature("docstring") Pylon::CAcquireContinuousConfiguration::OnOpened "

This method is called after the attached Pylon Device has been opened.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CAcquireContinuousConfiguration::ApplyConfiguration "

Apply acquire continuous configuration.  
";

// File: class_pylon_1_1_c_acquire_single_frame_configuration.xml


%feature("docstring") Pylon::CAcquireSingleFrameConfiguration "

An instant camera configuration for single frame acquisition, Use together with
CInstantCamera::GrabOne() only.  

The CAcquireSingleFrameConfiguration is provided as header-only file. The code
can be copied and modified for creating own configuration classes.  

note: Grabbing single images using Software Trigger
    (CSoftwareTriggerConfiguration) is recommended if you want to maximize frame
    rate. This is because the overhead per grabbed image is reduced compared to
    Single Frame Acquisition. The grabbing can be started using
    CInstantCamera::StartGrabbing(). Images are grabbed using the
    CInstantCamera::WaitForFrameTriggerReady(),
    CInstantCamera::ExecuteSoftwareTrigger() and
    CInstantCamera::RetrieveResult() methods instead of using
    CInstantCamera::GrabOne(). The grab can be stopped using
    CInstantCamera::StopGrabbing() when done.  

C++ includes: AcquireSingleFrameConfiguration.h
";

%feature("docstring") Pylon::CAcquireSingleFrameConfiguration::~CAcquireSingleFrameConfiguration "

Destructor.  
";

%feature("docstring") Pylon::CAcquireSingleFrameConfiguration::OnOpened "

This method is called after the attached Pylon Device has been opened.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CAcquireSingleFrameConfiguration::ApplyConfiguration "

Apply acquire single frame configuration.  
";

// File: class_pylon_1_1_callback1.xml


%feature("docstring") Pylon::Callback1 "
";

%feature("docstring") Pylon::Callback1::Callback1 "

constructor, taking lifetime control of body  
";

%feature("docstring") Pylon::Callback1::Callback1 "

copy constructor doing deep copy  
";

%feature("docstring") Pylon::Callback1::~Callback1 "

destructor, destroying body  
";

// File: class_pylon_1_1_c_array_parameter.xml


%feature("docstring") Pylon::CArrayParameter "

CArrayParameter class used to simplify access to GenApi parameters.  

C++ includes: ArrayParameter.h
";

%feature("docstring") Pylon::CArrayParameter::CArrayParameter "

Creates an empty CArrayParameter object. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::CArrayParameter "

Creates a CArrayParameter object and attaches it to a node, typically retrieved
for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to attach.  

post:  

    *   If the passed node does not match the parameter type, the parameter will
        be empty, see IsValid().  
    *   If the passed node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::CArrayParameter "

Creates a CArrayParameter object and attaches it to a node of a matching type.  

Parameters
----------
* `pRegister` :  
    The node to attach.  

post: The parameter object must not be used to access the node's functionality
    if the source of the attached `pRegister` has been destroyed. In this case,
    call Release() or attach a new node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::CArrayParameter "

Creates a CArrayParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::CArrayParameter "

Creates a CArrayParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `name` is NULL, the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::CArrayParameter "

Copies a CArrayParameter object.  

Parameters
----------
* `rhs` :  
    The object to copy. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::~CArrayParameter "

Destroys the CArrayParameter object. Does not access the attached node. \\error
Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `name` is NULL the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::Attach "

Attaches a node, typically retrieved for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::Attach "

Assigns a node of the same type to the parameter object.  

Parameters
----------
* `pRegister` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::Equals "

Returns true if the same nodes are attached or both parameters are empty.  

Parameters
----------
* `rhs` :  
    The object to compare to.  

Returns
-------
Returns true if the same nodes are attached or both parameters are empty.
\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pNode` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pRegister` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::Release "

Releases the attached node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CArrayParameter::IsValid "
";

%feature("docstring") Pylon::CArrayParameter::Set "
";

%feature("docstring") Pylon::CArrayParameter::Get "
";

%feature("docstring") Pylon::CArrayParameter::GetLength "
";

%feature("docstring") Pylon::CArrayParameter::GetAddress "
";

// File: class_pylon_1_1_c_avi_writer.xml


%feature("docstring") Pylon::CAviWriter "

Supports writing AVI files.  

C++ includes: AviWriter.h
";

%feature("docstring") Pylon::CAviWriter::CAviWriter "

Creates an AVI writer object.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CAviWriter::~CAviWriter "

Destroys the AVI writer object.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CAviWriter::Open "

Opens an AVI file for writing.  

If a file with the same `filename` already exists, it will be overwritten.  

Parameters
----------
* `filename` :  
    Name and path of the image.  
* `framesPerSecondPlayback` :  
    The frame rate of the AVI file when shown in a media player.  
* `pixelType` :  
    The pixel type of the image in the AVI file.  
* `width` :  
    The number of pixels in a row.  
* `height` :  
    The number of rows of the image.  
* `orientation` :  
    The vertical orientation of the image data in the AVI file.  
* `pCompressionOptions` :  
    Compression can be enabled by passing compression options. See
    SAviCompressionOptions.  

pre:  

    *   The AVI file is closed.  
    *   The pixelType is either PixelType_Mono8, PixelType_BGR8packed or
        PixelType_BGRA8packed  
    *   The `width` value must be > 0 and < _I32_MAX.  
    *   The `height` value must be > 0 and < _I32_MAX.  

\\error Throws an exception if the AVI file cannot be opened. Throws an
exception if the preconditions are not met.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CAviWriter::IsOpen "

Returns the open state of the AVI file.  

Returns
-------
Returns true if open.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CAviWriter::Close "

Closes the AVI file.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CAviWriter::Add "

Adds the image to the AVI file. Converts the image to the correct format if
required.  

The image is automatically converted to the format passed when opening the file
if needed. The image is also converted if the stride of the passed image is not
aligned to 4 byte. The image is also converted if the orientation of the passed
image does mot match the value passed when opening the AVI file.  

If more control over the conversion is required, the CImageFormatConverter class
can be used to convert other images with a CPylonBitmapImage object as target.
The CPylonBitmapImage object can then be added to the AVI file.  

Parameters
----------
* `image` :  
    The image to add, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  
* `keyFrameSelection` :  
    Can be used to control key frame selection for compressed images if needed.  

pre:  

    *   The file is open.  
    *   The image added is valid.  
    *   The pixel type of the image to add is a supported input format of the
        Pylon::CImageFormatConverter.  
    *   The width and height of the `image` match the values passed when opening
        the AVI file.  
    *   The total size of the AVI file must not exceed 2 GB. See
        CAviWriter::GetImageDataBytesWritten().  

\\error Throws an exception if the image cannot be added.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CAviWriter::Add "

Adds the image to the AVI file. Converts the image to the correct format if
required.  

See Add( const Image&) for more details.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the image.  
* `bufferSize` :  
    The size of the buffer in byte.  
* `pixelType` :  
    The pixel type of the image to save.  
* `width` :  
    The number of pixels in a row of the image to save.  
* `height` :  
    The number of rows of the image to save.  
* `paddingX` :  
    The number of extra data bytes at the end of each line.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  
* `keyFrameSelection` :  
    Can be used to control key frame selection for compressed images if needed.  

pre:  

    *   The file is open.  
    *   The image added is valid.  
    *   The pixel type of the image to add is a supported input format of the
        Pylon::CImageFormatConverter.  
    *   The width and height of the `image` match the values passed when opening
        the AVI file.  
    *   The total size of the AVI file must not exceed 2 GB. See
        CAviWriter::GetImageDataBytesWritten().  

\\error Throws an exception if the image cannot be added.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CAviWriter::CanAddWithoutConversion "

Can be used to check whether the given image is added to the AVI file without
prior conversion when Add() is called.  

Parameters
----------
* `pixelType` :  
    The pixel type of the image to save.  
* `width` :  
    The number of pixels in a row of the image to save.  
* `height` :  
    The number of rows of the image to save.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image data in the AVI file.  

Returns
-------
Returns true if the image is added to the AVI stream without prior conversion
when Add() is called. Returns false if the image is automatically converted when
Add() is called. Returns false if the image cannot be added at all. See the
preconditions of Add() for more information.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CAviWriter::CanAddWithoutConversion "

Can be used to check whether the given image is added to the AVI file without
prior conversion when Add() is called.  

Parameters
----------
* `image` :  
    The image to save, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

Returns
-------
Returns true if the image is added to the AVI stream without prior conversion
when Add() is called. Returns false if the image is automatically converted when
Add() is called. Returns false if the image cannot be added at all. See the
preconditions of Add() for more information.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CAviWriter::GetCountOfAddedImages "

Provides access to the number of images that have been added to the AVI file.  

Returns
-------
Returns the number of images that have been added to the AVI file. Returns 0 if
no AVI file has been written yet. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CAviWriter::GetImageDataBytesWritten "

Provides access to the number of image data bytes written to the AVI file.  

This value is updated with each call to AviWriter::Add().  

Depending on the used image format and codec, about 5 KB of header information
and padding bytes are written to the AVI file. Furthermore, 24 additional bytes
are needed per image for chunk header and index entry data.  

Returns
-------
Returns the number of image data bytes that have been written to the AVI file.
Returns 0 if no AVI File has been written yet. This size does not include the
sizes of the AVI file header and AVI file index.  

\\error Does not throw C++ exceptions.  
";

// File: class_pylon_1_1_c_basler_universal_camera_event_handler.xml


%feature("docstring") Pylon::CBaslerUniversalCameraEventHandler "

The camera event handler base class.  

C++ includes: BaslerUniversalCameraEventHandler.h
";

%feature("docstring") Pylon::CBaslerUniversalCameraEventHandler::OnCameraEvent "

This method is called when a camera event has been received.  

Only very short processing tasks should be performed by this method. Otherwise,
the event notification will block the processing of images.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `userProvidedId` :  
    The ID passed when registering for the event. It can be used to distinguish
    between different events.  
* `pNode` :  
    The node identified by node name when registering.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified. \\threading This method is called outside the lock of the
camera object, outside the lock of the node map, and inside the lock of the
camera event handler registry.  
";

%feature("docstring") Pylon::CBaslerUniversalCameraEventHandler::OnCameraEventHandlerRegistered "

This method is called when the camera event handler has been registered.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `nodeName` :  
    The name of the event data node updated on camera event, e.g.
    \"ExposureEndEventTimestamp\" for exposure end event.  
* `userProvidedId` :  
    This ID is passed as a parameter in
    CBaslerUniversalCameraEventHandler::OnCameraEvent and can be used to
    distinguish between different events.  

\\error Exceptions from this call will propagate through. \\threading This
method is called inside the lock of the camera event handler registry.  
";

%feature("docstring") Pylon::CBaslerUniversalCameraEventHandler::OnCameraEventHandlerDeregistered "

This method is called when the camera event handler has been deregistered.  

The camera event handler is automatically deregistered when the Instant Camera
object is destroyed.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `nodeName` :  
    The name of the event data node updated on camera event, e.g.
    \"ExposureEndEventTimestamp\" for exposure end event.  
* `userProvidedId` :  
    This ID is passed as a parameter in
    CBaslerUniversalCameraEventHandler::OnCameraEvent and can be used to
    distinguish between different events.  

\\error C++ exceptions from this call will be caught and ignored. \\threading
This method is called inside the lock of the camera event handler registry.  
";

%feature("docstring") Pylon::CBaslerUniversalCameraEventHandler::DestroyCameraEventHandler "

Destroys the camera event handler.  

\\error C++ exceptions from this call will be caught and ignored.  
";

%feature("docstring") Pylon::CBaslerUniversalCameraEventHandler::CBaslerUniversalCameraEventHandler "

Create.  
";

%feature("docstring") Pylon::CBaslerUniversalCameraEventHandler::CBaslerUniversalCameraEventHandler "

Copy.  
";

%feature("docstring") Pylon::CBaslerUniversalCameraEventHandler::~CBaslerUniversalCameraEventHandler "

Destruct.  
";

%feature("docstring") Pylon::CBaslerUniversalCameraEventHandler::DebugGetEventHandlerRegistrationCount "
";

// File: class_pylon_1_1_c_basler_universal_configuration_event_handler.xml


%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler "

The configuration event handler base class.  

C++ includes: BaslerUniversalConfigurationEventHandler.h
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnAttach "

This method is called before a Pylon Device (Pylon::IPylonDevice) is attached by
calling the Instant Camera object's Attach() method.  

This method can not be used for detecting that a camera device has been attached
to the PC. The camera's Attach() method must not be called from here or from
subsequent calls to avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnAttached "

This method is called after a Pylon Device (Pylon::IPylonDevice) has been
attached by calling the Instant Camera object's Attach() method.  

This method can not be used for detecting that a camera device has been attached
to the PC. The camera's Attach() method must not be called from here or from
subsequent calls to avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnDetach "

This method is called before the attached Pylon Device is detached from the
Instant Camera object.  

The camera's Detach() method must not be called from here or from subsequent
calls to avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnDetached "

This method is called after the attached Pylon Device has been detached from the
Instant Camera object.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnDestroy "

This method is called before the attached Pylon Device is destroyed.  

Camera DestroyDevice must not be called from here or from subsequent calls to
avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnDestroyed "

This method is called after the attached Pylon Device has been destroyed.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnOpen "

This method is called before the attached Pylon Device is opened.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnOpened "

This method is called after the attached Pylon Device has been opened.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnClose "

This method is called before the attached Pylon Device is closed.  

Camera Close must not be called from here or from subsequent calls to avoid
infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnClosed "

This method is called after the attached Pylon Device has been closed.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnGrabStart "

This method is called before a grab session is started.  

Camera StartGrabbing must not be called from here or from subsequent calls to
avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnGrabStarted "

This method is called after a grab session has been started.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnGrabStop "

This method is called before a grab session is stopped.  

Camera StopGrabbing must not be called from here or from subsequent calls to
avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnGrabStopped "

This method is called after a grab session has been stopped.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnGrabError "

This method is called when an exception has been triggered during grabbing.  

An exception has been triggered by a grab thread. The grab will be stopped after
this event call.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `errorMessage` :  
    The message of the exception that signaled an error during grabbing.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnCameraDeviceRemoved "

This method is called when a camera device removal from the PC has been
detected.  

The Pylon Device attached to the Instant Camera is not operable after this
event. After it is made sure that no access to the Pylon Device or any of its
node maps is made anymore the Pylon Device should be destroyed using
InstantCamera::DeviceDestroy(). The access to the Pylon Device can be protected
using the lock provided by GetLock(), e.g. when accessing parameters.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object from an
additional thread.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnConfigurationRegistered "

This method is called when the configuration event handler has been registered.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. \\threading This
method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::OnConfigurationDeregistered "

This method is called when the configuration event handler has been
deregistered.  

The configuration event handler is automatically deregistered when the Instant
Camera object is destroyed.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. \\threading
This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::DestroyConfiguration "

Destroys the configuration event handler.  

\\error C++ exceptions from this call will be caught and ignored.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::CBaslerUniversalConfigurationEventHandler "

Create.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::CBaslerUniversalConfigurationEventHandler "

Copy.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::~CBaslerUniversalConfigurationEventHandler "

Destruct.  
";

%feature("docstring") Pylon::CBaslerUniversalConfigurationEventHandler::DebugGetEventHandlerRegistrationCount "
";

// File: class_pylon_1_1_c_basler_universal_grab_result_data.xml


%feature("docstring") Pylon::CBaslerUniversalGrabResultData "

The Universal grab result data.  

C++ includes: BaslerUniversalGrabResultData.h
";

// File: class_pylon_1_1_c_basler_universal_image_event_handler.xml


%feature("docstring") Pylon::CBaslerUniversalImageEventHandler "

The image event handler base class.  

C++ includes: BaslerUniversalImageEventHandler.h
";

%feature("docstring") Pylon::CBaslerUniversalImageEventHandler::OnImagesSkipped "

This method is called when images have been skipped using the
GrabStrategy_LatestImageOnly strategy or the GrabStrategy_LatestImages strategy.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `countOfSkippedImages` :  
    The number of images skipped. This `countOfSkippedImages` does not include
    the number of images lost in the case of a buffer under run in the driver.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called outside the lock of the camera object but
inside the lock of the image event handler registry.  
";

%feature("docstring") Pylon::CBaslerUniversalImageEventHandler::OnImageGrabbed "

This method is called when an image has been grabbed.  

The grab result smart pointer passed does always reference a grab result data
object. The status of the grab needs to be checked before accessing the grab
result data. See CGrabResultData::GrabSucceeded(),
CGrabResultData::GetErrorCode() and CGrabResultData::GetErrorDescription() for
more information.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `grabResult` :  
    The grab result data.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called outside the lock of the camera object but
inside the lock of the image event handler registry.  
";

%feature("docstring") Pylon::CBaslerUniversalImageEventHandler::OnImageEventHandlerRegistered "

This method is called when the image event handler has been registered.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. \\threading This
method is called inside the lock of the image event handler registry.  
";

%feature("docstring") Pylon::CBaslerUniversalImageEventHandler::OnImageEventHandlerDeregistered "

This method is called when the image event handler has been deregistered.  

The image event handler is automatically deregistered when the Instant Camera
object is destroyed.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. \\threading
This method is called inside the lock of the image event handler registry.  
";

%feature("docstring") Pylon::CBaslerUniversalImageEventHandler::DestroyImageEventHandler "

Destroys the image event handler.  

\\error C++ exceptions from this call will be caught and ignored.  
";

%feature("docstring") Pylon::CBaslerUniversalImageEventHandler::CBaslerUniversalImageEventHandler "

Create.  
";

%feature("docstring") Pylon::CBaslerUniversalImageEventHandler::CBaslerUniversalImageEventHandler "

Copy.  
";

%feature("docstring") Pylon::CBaslerUniversalImageEventHandler::~CBaslerUniversalImageEventHandler "

Destruct.  
";

%feature("docstring") Pylon::CBaslerUniversalImageEventHandler::DebugGetEventHandlerRegistrationCount "
";

// File: class_pylon_1_1_c_basler_universal_instant_camera.xml


%feature("docstring") Pylon::CBaslerUniversalInstantCamera "

Extends the CInstantCamera by universal parameter interface classes combining
all interface types.  

C++ includes: BaslerUniversalInstantCamera.h
";

%feature("docstring") Pylon::CBaslerUniversalInstantCamera::CBaslerUniversalInstantCamera "

Creates an Instant Camera object with no attached Pylon device.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CBaslerUniversalInstantCamera::CBaslerUniversalInstantCamera "

Creates an Instant Camera object and calls Attach().  

See Attach() for more information.  

Parameters
----------
* `pDevice` :  
    The Pylon device to attach.  
* `cleanupProcedure` :  
    If cleanupProcedure equals Cleanup_Delete, the Pylon device is destroyed
    when the Instant Camera object is destroyed.  

\\error May throw an exception if the passed Pylon device is open. Does not
throw C++ exceptions if the passed Pylon device is closed or NULL.  
";

%feature("docstring") Pylon::CBaslerUniversalInstantCamera::~CBaslerUniversalInstantCamera "

Destroys an Instant Camera object.  

Calls Attach( NULL) for destroying or removing a Pylon device depending on the
passed cleanup procedure.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CBaslerUniversalInstantCamera::ChangeIpConfiguration "

Enables/disables use of persistent IP address and DHCP usage of the attached
Pylon Device.  

See Pylon::IPylonGigEDevice::ChangeIpConfiguration()  

pre:  

    *   A Pylon Device is attached.  
    *   The Pylon Device is open.  

\\error The Instant Camera object is still valid after error.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CBaslerUniversalInstantCamera::GetPersistentIpAddress "

Reads the persistent IP address from the attached Pylon Device.  

See Pylon::IPylonGigEDevice::GetPersistentIpAddress()  

pre:  

    *   A Pylon Device is attached.  
    *   The Pylon Device is open.  

    \\error The Instant Camera object is still valid after error.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CBaslerUniversalInstantCamera::SetPersistentIpAddress "

Writes a persistent IP address to the attached Pylon Device.  

See Pylon::IPylonGigEDevice::SetPersistentIpAddress()  

pre:  

    *   A Pylon Device is attached.  
    *   The Pylon Device is open.  

    \\error The Instant Camera object is still valid after error.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

// File: class_pylon_1_1_c_basler_universal_instant_camera_array.xml


%feature("docstring") Pylon::CBaslerUniversalInstantCameraArray "

Universal instant camera array.  

\\threading The CBaslerUniversalInstantCameraArray class is not thread-safe.  

C++ includes: BaslerUniversalInstantCameraArray.h
";

%feature("docstring") Pylon::CBaslerUniversalInstantCameraArray::CBaslerUniversalInstantCameraArray "

Creates an Instant Camera Array of size 0.  

Initialize() can be used to adjust the size of the array.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CBaslerUniversalInstantCameraArray::CBaslerUniversalInstantCameraArray "

Creates an Instant Camera Array.  

Calls Initialize() to adjust the size of the array.  

Parameters
----------
* `numberOfCameras` :  
    The number of cameras the array shall hold. Can be 0.  

The index operator can be used to access the individual cameras for attaching a
Pylon Device or for configuration.  

Example:  

\\error Does not throw C++ exceptions, except when memory allocation fails.  
";

// File: struct_pylon_1_1_c_basler_universal_instant_camera_traits.xml


%feature("docstring") Pylon::CBaslerUniversalInstantCameraTraits "

Lists all the types used by the universal instant camera class.  

C++ includes: BaslerUniversalInstantCamera.h
";

%feature("docstring") Pylon::CBaslerUniversalInstantCameraTraits::HasSpecificDeviceClass "

Can be used to check whether the DeviceClass() can be used for enumeration.  
";

%feature("docstring") Pylon::CBaslerUniversalInstantCameraTraits::DeviceClass "

The name of this device class. Use this one for enumeration.  
";

// File: class_pylon_1_1_c_boolean_parameter.xml


%feature("docstring") Pylon::CBooleanParameter "

CBooleanParameter class used to simplify access to GenApi parameters.  

C++ includes: BooleanParameter.h
";

%feature("docstring") Pylon::CBooleanParameter::CBooleanParameter "

Creates an empty CBooleanParameter object. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::CBooleanParameter "

Creates a CBooleanParameter object and attaches it to a node, typically
retrieved for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to attach.  

post:  

    *   If the passed node does not match the parameter type, the parameter will
        be empty, see IsValid().  
    *   If the passed node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::CBooleanParameter "

Creates a CBooleanParameter object and attaches it to a node of a matching type.  

Parameters
----------
* `pBoolean` :  
    The node to attach.  

post: The parameter object must not be used to access the node's functionality
    if the source of the attached `pBoolean` has been destroyed. In this case,
    call Release() or attach a new node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::CBooleanParameter "

Creates a CBooleanParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::CBooleanParameter "

Creates a CBooleanParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `name` is NULL, the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::CBooleanParameter "

Copies a CBooleanParameter object.  

Parameters
----------
* `rhs` :  
    The object to copy. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::~CBooleanParameter "

Destroys the CBooleanParameter object. Does not access the attached node.
\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `name` is NULL the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::Attach "

Attaches a node, typically retrieved for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::Attach "

Assigns a node of the same type to the parameter object.  

Parameters
----------
* `pBoolean` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::Equals "

Returns true if the same nodes are attached or both parameters are empty.  

Parameters
----------
* `rhs` :  
    The object to compare to.  

Returns
-------
Returns true if the same nodes are attached or both parameters are empty.
\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pNode` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pBoolean` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::Release "

Releases the attached node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CBooleanParameter::IsValid "
";

%feature("docstring") Pylon::CBooleanParameter::SetValue "
";

%feature("docstring") Pylon::CBooleanParameter::GetValue "
";

%feature("docstring") Pylon::CBooleanParameter::TrySetValue "
";

%feature("docstring") Pylon::CBooleanParameter::GetValueOrDefault "
";

// File: class_pylon_1_1_c_chunk_parser_1_1_c_buffer.xml

// File: class_pylon_1_1_c_camera_event_handler.xml


%feature("docstring") Pylon::CCameraEventHandler "

The camera event handler base class.  

C++ includes: CameraEventHandler.h
";

%feature("docstring") Pylon::CCameraEventHandler::OnCameraEvent "

This method is called when a camera event has been received.  

Only very short processing tasks should be performed by this method. Otherwise,
the event notification will block the processing of images.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `userProvidedId` :  
    The ID passed when registering for the event. It can be used to distinguish
    between different events.  
* `pNode` :  
    The node identified by node name when registering.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified. \\threading This method is called outside the lock of the
camera object, outside the lock of the node map, and inside the lock of the
camera event handler registry.  
";

%feature("docstring") Pylon::CCameraEventHandler::OnCameraEventHandlerRegistered "

This method is called when the camera event handler has been registered.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `nodeName` :  
    The name of the event data node updated on camera event, e.g.
    \"ExposureEndEventTimestamp\" for exposure end event.  
* `userProvidedId` :  
    This ID is passed as a parameter in CCameraEventHandler::OnCameraEvent and
    can be used to distinguish between different events.  

\\error Exceptions from this call will propagate through. \\threading This
method is called inside the lock of the camera event handler registry.  
";

%feature("docstring") Pylon::CCameraEventHandler::OnCameraEventHandlerDeregistered "

This method is called when the camera event handler has been deregistered.  

The camera event handler is automatically deregistered when the Instant Camera
object is destroyed.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `nodeName` :  
    The name of the event data node updated on camera event, e.g.
    \"ExposureEndEventTimestamp\" for exposure end event.  
* `userProvidedId` :  
    This ID is passed as a parameter in CCameraEventHandler::OnCameraEvent and
    can be used to distinguish between different events.  

\\error C++ exceptions from this call will be caught and ignored. \\threading
This method is called inside the lock of the camera event handler registry.  
";

%feature("docstring") Pylon::CCameraEventHandler::DestroyCameraEventHandler "

Destroys the camera event handler.  

\\error C++ exceptions from this call will be caught and ignored.  
";

%feature("docstring") Pylon::CCameraEventHandler::CCameraEventHandler "

Create.  
";

%feature("docstring") Pylon::CCameraEventHandler::CCameraEventHandler "

Copy.  
";

%feature("docstring") Pylon::CCameraEventHandler::~CCameraEventHandler "

Destruct.  
";

%feature("docstring") Pylon::CCameraEventHandler::DebugGetEventHandlerRegistrationCount "
";

// File: class_pylon_1_1_c_camera_pixel_type_mapper_t.xml


%feature("docstring") Pylon::CCameraPixelTypeMapperT "

A camera specific pixeltypemapper (maps device specific pixelformats contained
in the generated camera classes to pylon pixeltypes by their name).  

Use this mapper to convert a PixelTypeEnums or ChunkPixelFormatEnums enum values
to a Pylon_PixelType used for PixelTypeConverter creation. When passing the
symbolic name of the pixeltype you can use the static version
GetPylonPixelTypeByName. This function will do the lookup everytime you call it.
The non-static member function GetPylonPixelTypeFromPixelFormatEnum uses caching
to speed up subsequent calls.  

The template parameter EnumT is the enumeration type from the camera class
(typically Basler_UniversalCameraParams::PixelFormatEnums for GigE cameras)  

C++ includes: PixelTypeMapper.h
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::CCameraPixelTypeMapperT "

Create an empty mapper. Before calling any non-static function.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::CCameraPixelTypeMapperT "

create a mapper by using the enum node passed.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::~CCameraPixelTypeMapperT "
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::IsValid "

Checks the objects validity.  

Returns
-------
Returns true if the object is initialized properly.  

Essentially this function checks whether you've called SetPixelFormatEnumNode.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::SetPixelFormatEnumNode "

Lazy initialization of the object.  

Parameters
----------
* `pEnumT` :  
    Pointer to the enumeration node containing the PixelFormats.  

Call this function initialize the mapper when using the default c'tor.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::GetPylonPixelTypeFromPixelFormatEnum "

Converts a enumeration node value to a Pylon::EPixelType enum.  

Parameters
----------
* `pixelFormatEnumValue` :  
    enumeration value to convert. You obtain this value by calling
    GenApi::IEnumerationT::GetValue.  

Returns
-------
Returns the Pylon::EPixelType for a given pixelformat enum value defined in the
enum node passed in c'tor  

Converts a enumeration node value to a Pylon::EPixelType enum. You must have
initialized the mapper before you can call this function.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::GetPylonPixelTypeByName "

Returns a Pylon::EPixelType for a given symbolic name.  

Parameters
----------
* `pszSymbolicName` :  
    pointer to the symbolic name. Note: Symbolic names are case sensitive. You
    can obtain the symbolic name by calling GenApi::IEnumEntry::GetSymbolic()  

Returns
-------
Returns the Pylon_PixelType for a given symbolic name.  

Static version which does the lookup soley by symbolic string comparison.
Passing \"Mono16\" will return Pylon::PixelType_Mono16. If the name is not found
Pylon::PixelType_Undefined will be returned.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::GetPylonPixelTypeByName "

Returns a Pylon::EPixelType for a given symbolic name.  

Parameters
----------
* `symbolicName` :  
    The symbolic name. Note: Symbolic names are case sensitive. You can obtain
    the symbolic name by calling GenApi::IEnumEntry::GetSymbolic()  

Returns
-------
Returns the Pylon_PixelType for a given symbolic name.  

Static version which does the lookup solely by symbolic string comparison.
Passing \"Mono16\" will return Pylon::PixelType_Mono16. If the name is not found
Pylon::PixelType_Undefined will be returned.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::GetNameByPixelType "

Static function that returns a string representation of the given EPixelType.  

Parameters
----------
* `pixelType` :  
    The pixel type to return the name for.  
* `sfncVer` :  
    SFNC Version to use when doing the mapping. Some names have been changed in
    SFNC 2.0  

Returns
-------
Returns the pointer to a null terminated string representing the symbolic name
of the pixel type.  

Passing Pylon::PixelType_Mono16 will return \"Mono16\" will be returned. If the
pixel type is not known an empty string is returned.  

note: The returned name cannot be used to parameterize the pixel format of a
    camera device, because the camera's pixel format name can be different. The
    camera's pixel format name depends on the used standard feature naming
    convention (SFNC).  
";

// File: class_pylon_1_1_c_chunk_parser.xml


%feature("docstring") Pylon::CChunkParser "

Low Level API: Base class for chunk parsers returned by camera objects.  

Part implementation of chunk parser of common functionality.  

C++ includes: ChunkParser.h
";

%feature("docstring") Pylon::CChunkParser::AttachBuffer "
";

%feature("docstring") Pylon::CChunkParser::DetachBuffer "
";

%feature("docstring") Pylon::CChunkParser::UpdateBuffer "
";

%feature("docstring") Pylon::CChunkParser::GetChunkDataNodeMap "
";

%feature("docstring") Pylon::CChunkParser::Destroy "
";

// File: class_pylon_1_1_c_command_parameter.xml


%feature("docstring") Pylon::CCommandParameter "

CCommandParameter class used to simplify access to GenApi parameters.  

C++ includes: CommandParameter.h
";

%feature("docstring") Pylon::CCommandParameter::CCommandParameter "

Creates an empty CCommandParameter object. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::CCommandParameter "

Creates a CCommandParameter object and attaches it to a node, typically
retrieved for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to attach.  

post:  

    *   If the passed node does not match the parameter type, the parameter will
        be empty, see IsValid().  
    *   If the passed node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::CCommandParameter "

Creates a CCommandParameter object and attaches it to a node of a matching type.  

Parameters
----------
* `pCommand` :  
    The node to attach.  

post: The parameter object must not be used to access the node's functionality
    if the source of the attached `pCommand` has been destroyed. In this case,
    call Release() or attach a new node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::CCommandParameter "

Creates a CCommandParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::CCommandParameter "

Creates a CCommandParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `name` is NULL, the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::CCommandParameter "

Copies a CCommandParameter object.  

Parameters
----------
* `rhs` :  
    The object to copy. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::~CCommandParameter "

Destroys the CCommandParameter object. Does not access the attached node.
\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `name` is NULL the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::Attach "

Attaches a node, typically retrieved for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::Attach "

Assigns a node of the same type to the parameter object.  

Parameters
----------
* `pCommand` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::Equals "

Returns true if the same nodes are attached or both parameters are empty.  

Parameters
----------
* `rhs` :  
    The object to compare to.  

Returns
-------
Returns true if the same nodes are attached or both parameters are empty.
\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pNode` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pCommand` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::Release "

Releases the attached node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CCommandParameter::IsValid "
";

%feature("docstring") Pylon::CCommandParameter::Execute "
";

%feature("docstring") Pylon::CCommandParameter::IsDone "
";

%feature("docstring") Pylon::CCommandParameter::TryExecute "
";

// File: class_pylon_1_1_c_configuration_event_handler.xml


%feature("docstring") Pylon::CConfigurationEventHandler "

The configuration event handler base class.  

C++ includes: ConfigurationEventHandler.h
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnAttach "

This method is called before a Pylon Device (Pylon::IPylonDevice) is attached by
calling the Instant Camera object's Attach() method.  

This method can not be used for detecting that a camera device has been attached
to the PC. The camera's Attach() method must not be called from here or from
subsequent calls to avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnAttached "

This method is called after a Pylon Device (Pylon::IPylonDevice) has been
attached by calling the Instant Camera object's Attach() method.  

This method can not be used for detecting that a camera device has been attached
to the PC. The camera's Attach() method must not be called from here or from
subsequent calls to avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnDetach "

This method is called before the attached Pylon Device is detached from the
Instant Camera object.  

The camera's Detach() method must not be called from here or from subsequent
calls to avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnDetached "

This method is called after the attached Pylon Device has been detached from the
Instant Camera object.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnDestroy "

This method is called before the attached Pylon Device is destroyed.  

Camera DestroyDevice must not be called from here or from subsequent calls to
avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnDestroyed "

This method is called after the attached Pylon Device has been destroyed.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnOpen "

This method is called before the attached Pylon Device is opened.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnOpened "

This method is called after the attached Pylon Device has been opened.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnClose "

This method is called before the attached Pylon Device is closed.  

Camera Close must not be called from here or from subsequent calls to avoid
infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnClosed "

This method is called after the attached Pylon Device has been closed.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnGrabStart "

This method is called before a grab session is started.  

Camera StartGrabbing must not be called from here or from subsequent calls to
avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnGrabStarted "

This method is called after a grab session has been started.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnGrabStop "

This method is called before a grab session is stopped.  

Camera StopGrabbing must not be called from here or from subsequent calls to
avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnGrabStopped "

This method is called after a grab session has been stopped.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnGrabError "

This method is called when an exception has been triggered during grabbing.  

An exception has been triggered by a grab thread. The grab will be stopped after
this event call.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `errorMessage` :  
    The message of the exception that signaled an error during grabbing.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnCameraDeviceRemoved "

This method is called when a camera device removal from the PC has been
detected.  

The Pylon Device attached to the Instant Camera is not operable after this
event. After it is made sure that no access to the Pylon Device or any of its
node maps is made anymore the Pylon Device should be destroyed using
InstantCamera::DeviceDestroy(). The access to the Pylon Device can be protected
using the lock provided by GetLock(), e.g. when accessing parameters.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. All event
handlers are notified.  

\\threading This method is called inside the lock of the camera object from an
additional thread.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnConfigurationRegistered "

This method is called when the configuration event handler has been registered.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. \\threading This
method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnConfigurationDeregistered "

This method is called when the configuration event handler has been
deregistered.  

The configuration event handler is automatically deregistered when the Instant
Camera object is destroyed.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. \\threading
This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::DestroyConfiguration "

Destroys the configuration event handler.  

\\error C++ exceptions from this call will be caught and ignored.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::CConfigurationEventHandler "

Create.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::CConfigurationEventHandler "

Copy.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::~CConfigurationEventHandler "

Destruct.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::DebugGetEventHandlerRegistrationCount "
";

// File: class_pylon_1_1_c_configuration_helper.xml


%feature("docstring") Pylon::CConfigurationHelper "

Helper functions for different camera configuration classes.  

C++ includes: ConfigurationHelper.h
";

%feature("docstring") Pylon::CConfigurationHelper::DisableAllTriggers "

DisableAllTriggers disables all trigger types that can be turned off.  
";

%feature("docstring") Pylon::CConfigurationHelper::DisableCompression "

DisableCompression disables all compressions modes that can be turned off.  
";

%feature("docstring") Pylon::CConfigurationHelper::DisableGenDC "

DisableGenDC disables GenDC streaming when available.  
";

%feature("docstring") Pylon::CConfigurationHelper::SelectRangeComponent "

Select the 'Range' component.  

Some cameras, such as Basler blaze and stereo ace, provide multiple components.
Default is component 'Range' with pixel format 'Mono16' respective 'Mono8'.  
";

%feature("docstring") Pylon::CConfigurationHelper::ProbePacketSize "
";

// File: class_pylon_1_1_c_device_info.xml


%feature("docstring") Pylon::CDeviceInfo "

Holds information about an enumerated device.  

The device enumeration process creates a list of CDeviceInfo objects
(Pylon::DeviceInfoList_t). Each CDeviceInfo objects stores information about a
device. The information is retrieved during the device enumeration process
(ITransportLayer::EnumerateDevices resp. CTlFactory::EnumerateDevices)  

C++ includes: DeviceInfo.h
";

%feature("docstring") Pylon::CDeviceInfo::CDeviceInfo "
";

%feature("docstring") Pylon::CDeviceInfo::CDeviceInfo "
";

%feature("docstring") Pylon::CDeviceInfo::~CDeviceInfo "
";

%feature("docstring") Pylon::CDeviceInfo::GetSerialNumber "

Retrieves the serial number if it supported by the underlying implementation
This property is identified by Key::SerialNumberKey.  
";

%feature("docstring") Pylon::CDeviceInfo::SetSerialNumber "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::IsSerialNumberAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::GetUserDefinedName "

Retrieves the user-defined name if present. This property is identified by
Key::UserDefinedNameKey.  
";

%feature("docstring") Pylon::CDeviceInfo::SetUserDefinedName "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::IsUserDefinedNameAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::GetModelName "

Retrieves the model name of the device. This property is identified by
Key::ModelNameKey.  
";

%feature("docstring") Pylon::CDeviceInfo::SetModelName "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::IsModelNameAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::GetDeviceVersion "

Retrieves the version string of the device. This property is identified by
Key::DeviceVersionKey.  
";

%feature("docstring") Pylon::CDeviceInfo::SetDeviceVersion "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::IsDeviceVersionAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::GetDeviceFactory "

Retrieves the identifier for the transport layer able to create this device.
This property is identified by Key::DeviceFactoryKey.  
";

%feature("docstring") Pylon::CDeviceInfo::SetDeviceFactory "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::IsDeviceFactoryAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::GetXMLSource "

Retrieves the location where the XML file was loaded from. This property is
identified by Key::XMLSourceKey. You must use the DeviceInfo of an opened
IPylonDevice to retrieve this property.  
";

%feature("docstring") Pylon::CDeviceInfo::SetXMLSource "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::IsXMLSourceAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::SetFriendlyName "

Sets the display friendly name of the device. This property is identified by
Key::FriendlyNameKey. This method overrides a method of a base class returning a
reference to CDeviceInfo  
";

%feature("docstring") Pylon::CDeviceInfo::SetFullName "

Sets the full name identifying the device. This property is identified by
Key::FullNameKey. This method overrides a method of a base class returning a
reference to CDeviceInfo  
";

%feature("docstring") Pylon::CDeviceInfo::SetVendorName "

Sets the vendor name of the device. This property is identified by
Key::VendorNameKey. This method overrides a method of a base class returning a
reference to CDeviceInfo  
";

%feature("docstring") Pylon::CDeviceInfo::SetDeviceClass "

Sets the device class device, e.g. BaslerUsb. This property is identified by
Key::DeviceClassKey. This method overrides a method of a base class returning a
reference to CDeviceInfo  
";

%feature("docstring") Pylon::CDeviceInfo::GetInterfaceID "

Retrieves the ID of the interface that the device is connected to. This property
is identified by Key::InterfaceIDKey.  
";

%feature("docstring") Pylon::CDeviceInfo::SetInterfaceID "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::IsInterfaceIDAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::GetAddress "

Retrieves the IP address the device IP address in a human-readable
representation including the port number. This property is identified by
Key::AddressKey. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::SetAddress "

Sets the above property. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::IsAddressAvailable "

Returns true if the above property is available. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::GetIpAddress "

Retrieves the IP address the device IP address in a human-readable
representation. This property is identified by Key::IpAddressKey. Applies to:
GigE  
";

%feature("docstring") Pylon::CDeviceInfo::SetIpAddress "

Sets the above property. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::IsIpAddressAvailable "

Returns true if the above property is available. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::GetSubnetAddress "

Retrieves the IP address of the subnet. This property is identified by
Key::SubnetAddressKey Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::SetSubnetAddress "

Sets the above property. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::IsSubnetAddressAvailable "

Returns true if the above property is available. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::GetDefaultGateway "

Retrieves the default gateway the device IP address in a human-readable
representation. This property is identified by Key::DefaultGatewayKey. Applies
to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::SetDefaultGateway "

Sets the above property. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::IsDefaultGatewayAvailable "

Returns true if the above property is available. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::GetSubnetMask "

Retrieves the subnet mask the device IP address in a human-readable
representation. This property is identified by Key::SubnetMaskKey. Applies to:
GigE  
";

%feature("docstring") Pylon::CDeviceInfo::SetSubnetMask "

Sets the above property. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::IsSubnetMaskAvailable "

Returns true if the above property is available. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::GetPortNr "

Retrieves the port number used. This property is identified by Key::PortNrKey.
Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::SetPortNr "

Sets the above property. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::IsPortNrAvailable "

Returns true if the above property is available. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::GetMacAddress "

Retrieves the MAC address of the device the device IP address in a human-
readable representation. This property is identified by Key::MacAddressKey.
Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::SetMacAddress "

Sets the above property. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::IsMacAddressAvailable "

Returns true if the above property is available. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::GetInterface "

Retrieves the address of the network interface the device is connected. This
property is identified by Key::InterfaceKey. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::SetInterface "

Sets the above property. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::IsInterfaceAvailable "

Returns true if the above property is available. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::GetIpConfigOptions "

Retrieves the persistent IP configuration options. This property is identified
by Key::IpConfigOptionsKey. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::SetIpConfigOptions "

Sets the above property. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::IsIpConfigOptionsAvailable "

Returns true if the above property is available. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::GetIpConfigCurrent "

Retrieves the current IP configuration of the device. This property is
identified by Key::IpConfigCurrentKey. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::SetIpConfigCurrent "

Sets the above property. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::IsIpConfigCurrentAvailable "

Returns true if the above property is available. Applies to: GigE  
";

%feature("docstring") Pylon::CDeviceInfo::GetDeviceGUID "

Retrieves the device GUID. This property is identified by Key::DeviceGUIDKey.
Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::IsDeviceGUIDAvailable "

Returns true if the above property is available. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::GetManufacturerInfo "

Retrieves the manufacturer info. This property is identified by
Key::ManufacturerInfoKey. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::IsManufacturerInfoAvailable "

Returns true if the above property is available. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::GetDeviceIdx "

Retrieves the device index. For internal use only. This property is identified
by Key::DeviceIdxKey. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::IsDeviceIdxAvailable "

Returns true if the above property is available. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::GetProductId "

Retrieves the product ID. For internal use only. This property is identified by
Key::ProductIdKey. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::IsProductIdAvailable "

Returns true if the above property is available. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::GetVendorId "

Retrieves the vendor ID. For internal use only. This property is identified by
Key::VendorIdKey. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::IsVendorIdAvailable "

Returns true if the above property is available. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::GetDriverKeyName "

Retrieves the driver key name. For internal use only. This property is
identified by Key::DriverKeyNameKey. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::IsDriverKeyNameAvailable "

Returns true if the above property is available. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::GetUsbDriverType "

Retrieves the usb driver type. For internal use only. This property is
identified by Key::UsbDriverTypeKey. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::IsUsbDriverTypeAvailable "

Returns true if the above property is available. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::GetTransferMode "

Applies to: Usb.  

Retrieves the transfer mode. For internal use only. This property is identified
by Key::TransferModeKey  
";

%feature("docstring") Pylon::CDeviceInfo::IsTransferModeAvailable "

Returns true if the above property is available. Applies to: Usb  
";

%feature("docstring") Pylon::CDeviceInfo::GetPortID "

Retrieves the ID of the serial port the device is connected to. This property is
identified by Key::PortIDKey. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::SetPortID "

Sets the above property. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::IsPortIDAvailable "

Returns true if the above property is available. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::GetDeviceID "

Retrieves the device ID. This property is identified by Key::DeviceIDKey.
Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::SetDeviceID "

Sets the above property. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::IsDeviceIDAvailable "

Returns true if the above property is available. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::GetInitialBaudRate "

Retrieves the initial baud rate of the serial port the device is connected to.
This property is identified by Key::InitialBaudRateKey. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::SetInitialBaudRate "

Sets the above property. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::IsInitialBaudRateAvailable "

Returns true if the above property is available. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::GetDeviceXMLFileOverride "

Retrieves the device xml file override used. Internal use only. This property is
identified by Key::DeviceXMLFileOverrideKey. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::SetDeviceXMLFileOverride "

Sets the above property. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::IsDeviceXMLFileOverrideAvailable "

Returns true if the above property is available. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::GetDeviceSpecificString "

Retrieves the device specific string. Internal use only. This property is
identified by Key::DeviceSpecificStringKey. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::SetDeviceSpecificString "

Sets the above property. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::IsDeviceSpecificStringAvailable "

Returns true if the above property is available. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::GetPortSpecificString "

Retrieves the port specific string of the device. Internal use only. This
property is identified by Key::PortSpecificStringKey. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::SetPortSpecificString "

Sets the above property. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::IsPortSpecificStringAvailable "

Returns true if the above property is available. Applies to: CameraLink  
";

%feature("docstring") Pylon::CDeviceInfo::SetPropertyValue "

Modifies a property value This method overrides a method of a base class
returning a reference to CDeviceInfo  
";

%feature("docstring") Pylon::CDeviceInfo::IsPersistentIpActive "

Returns true when the device is configured for a persistent IP address.  
";

%feature("docstring") Pylon::CDeviceInfo::IsDhcpActive "

Returns true when the device is configured for using DHCP.  
";

%feature("docstring") Pylon::CDeviceInfo::IsAutoIpActive "

Returns true when the device is configured for using Auto IP (aka LLA).  
";

%feature("docstring") Pylon::CDeviceInfo::IsPersistentIpSupported "

Returns true when the device supports configuring a persistent IP address.  
";

%feature("docstring") Pylon::CDeviceInfo::IsDhcpSupported "

Returns true when the device supports DHCP.  
";

%feature("docstring") Pylon::CDeviceInfo::IsAutoIpSupported "

Returns true when the device supports Auto IP (aka LLA).  
";

%feature("docstring") Pylon::CDeviceInfo::IsSubset "

Returns true when subset, applies special knowledge on how to compare GigE
specific values.  
";

// File: class_pylon_1_1_c_enum_parameter.xml


%feature("docstring") Pylon::CEnumParameter "

CEnumParameter class used to simplify access to GenApi parameters.  

C++ includes: EnumParameter.h
";

%feature("docstring") Pylon::CEnumParameter::CEnumParameter "

Creates an empty CEnumParameter object. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::CEnumParameter "

Creates a CEnumParameter object and attaches it to a node, typically retrieved
for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to attach.  

post:  

    *   If the passed node does not match the parameter type, the parameter will
        be empty, see IsValid().  
    *   If the passed node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::CEnumParameter "

Creates a CEnumParameter object and attaches it to a node of a matching type.  

Parameters
----------
* `pEnumeration` :  
    The node to attach.  

post: The parameter object must not be used to access the node's functionality
    if the source of the attached `pEnumeration` has been destroyed. In this
    case, call Release() or attach a new node. \\error Does not throw C++
    exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::CEnumParameter "

Creates a CEnumParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::CEnumParameter "

Creates a CEnumParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `name` is NULL, the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::CEnumParameter "

Copies a CEnumParameter object.  

Parameters
----------
* `rhs` :  
    The object to copy. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::~CEnumParameter "

Destroys the CEnumParameter object. Does not access the attached node. \\error
Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `name` is NULL the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::Attach "

Attaches a node, typically retrieved for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::Attach "

Assigns a node of the same type to the parameter object.  

Parameters
----------
* `pEnumeration` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::Equals "

Returns true if the same nodes are attached or both parameters are empty.  

Parameters
----------
* `rhs` :  
    The object to compare to.  

Returns
-------
Returns true if the same nodes are attached or both parameters are empty.
\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pNode` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pEnumeration` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::Release "

Releases the attached node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CEnumParameter::IsValid "
";

%feature("docstring") Pylon::CEnumParameter::GetSymbolics "
";

%feature("docstring") Pylon::CEnumParameter::GetEntries "
";

%feature("docstring") Pylon::CEnumParameter::SetIntValue "
";

%feature("docstring") Pylon::CEnumParameter::GetIntValue "
";

%feature("docstring") Pylon::CEnumParameter::GetEntryByName "
";

%feature("docstring") Pylon::CEnumParameter::GetEntry "
";

%feature("docstring") Pylon::CEnumParameter::GetCurrentEntry "
";

%feature("docstring") Pylon::CEnumParameter::GetValueOrDefault "
";

%feature("docstring") Pylon::CEnumParameter::TrySetValue "
";

%feature("docstring") Pylon::CEnumParameter::TrySetValue "
";

%feature("docstring") Pylon::CEnumParameter::SetValue "
";

%feature("docstring") Pylon::CEnumParameter::SetValue "
";

%feature("docstring") Pylon::CEnumParameter::CanSetValue "
";

%feature("docstring") Pylon::CEnumParameter::GetValue "
";

%feature("docstring") Pylon::CEnumParameter::GetSettableValues "
";

%feature("docstring") Pylon::CEnumParameter::GetAllValues "
";

%feature("docstring") Pylon::CEnumParameter::GetEntryByNameAsParameter "
";

%feature("docstring") Pylon::CEnumParameter::GetCurrentEntryAsParameter "
";

// File: class_pylon_1_1_c_enum_parameter_t.xml


%feature("docstring") Pylon::CEnumParameterT "
";

%feature("docstring") Pylon::CEnumParameterT::CEnumParameterT "
";

%feature("docstring") Pylon::CEnumParameterT::CEnumParameterT "
";

%feature("docstring") Pylon::CEnumParameterT::SetValue "
";

%feature("docstring") Pylon::CEnumParameterT::SetValue "
";

%feature("docstring") Pylon::CEnumParameterT::SetValue "
";

%feature("docstring") Pylon::CEnumParameterT::SetValue "
";

%feature("docstring") Pylon::CEnumParameterT::GetValue "
";

%feature("docstring") Pylon::CEnumParameterT::GetEntry "
";

%feature("docstring") Pylon::CEnumParameterT::GetValueOrDefault "
";

%feature("docstring") Pylon::CEnumParameterT::TrySetValue "
";

%feature("docstring") Pylon::CEnumParameterT::CanSetValue "
";

// File: class_pylon_1_1_c_event_grabber_proxy_t.xml


%feature("docstring") Pylon::CEventGrabberProxyT "

Low Level API: The event grabber class with parameter access methods.  

This is the base class for pylon event grabber providing access to configuration
parameters.  

See also: configuringcameras  

templateparam
-------------
* `TParams` :  
    The specific parameter class (auto generated from the parameter xml file)  

C++ includes: EventGrabberProxy.h
";

/*
 Implementation of the IEventGrabber interface 
*/

/*
See Pylon::IEventGrabber for more details.  

*/

/*
 Construction 
*/

/*
 Some smart pointer functionality 
*/

/*
 Assignment and copying is not supported 
*/

%feature("docstring") Pylon::CEventGrabberProxyT::Open "
";

%feature("docstring") Pylon::CEventGrabberProxyT::Close "
";

%feature("docstring") Pylon::CEventGrabberProxyT::IsOpen "
";

%feature("docstring") Pylon::CEventGrabberProxyT::RetrieveEvent "
";

%feature("docstring") Pylon::CEventGrabberProxyT::GetWaitObject "
";

%feature("docstring") Pylon::CEventGrabberProxyT::GetNodeMap "
";

%feature("docstring") Pylon::CEventGrabberProxyT::CEventGrabberProxyT "

Creates a CEventGrabberProxyT object that is not attached to a pylon stream
grabber. Use the Attach() method to attach the pylon event grabber.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::CEventGrabberProxyT "

Creates a CEventGrabberProxyT object and attaches it to a pylon event grabber.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::~CEventGrabberProxyT "

Destructor.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::Attach "

Attach a pylon event grabber.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::IsAttached "

Checks if a pylon stream grabber is attached.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::GetEventGrabber "

Returns the pylon event grabber interface pointer.  
";

// File: class_pylon_1_1_c_feature_persistence.xml


%feature("docstring") Pylon::CFeaturePersistence "

Utility class for saving and restoring camera features to and from a file or
string.  

note: When saving features, the behavior of cameras supporting sequencers
    depends on the current setting of the \"SequenceEnable\" (some GigE models)
    or \"SequencerConfigurationMode\" (USB only) features respectively.  

Only if the sequencer is in configuration mode, are the sequence sets exported.
Otherwise, the camera features are exported without sequence sets.  

C++ includes: FeaturePersistence.h
";

%feature("docstring") Pylon::CFeaturePersistence::Load "

Loads the features from the file to the node map.  

Parameters
----------
* `FileName` :  
    Name of the file that contains the node map values.  
* `pNodeMap` :  
    Pointer to the node map  
* `validate` :  
    If validate==true, all node values will be validated. In case of an error, a
    GenICam::RuntimeException will be thrown  

\\error Throws an exception if loading fails.  
";

%feature("docstring") Pylon::CFeaturePersistence::Save "

Saves the node map to the file.  

Sequence sets of a camera are automatically saved if SequenceEnable or
SequencerConfigurationMode is enabled.  

Parameters
----------
* `FileName` :  
    Name of the file that contains the node map values  
* `pNodeMap` :  
    Pointer to the node map  

\\error Throws an exception if saving fails.  
";

%feature("docstring") Pylon::CFeaturePersistence::LoadFromString "

Loads the features from the string to the node map.  

Parameters
----------
* `Features` :  
    String containing the node map values.  
* `pNodeMap` :  
    Pointer to the node map.  
* `validate` :  
    If validate==true, all node values will be validated. In case of an error, a
    GenICam::RuntimeException will be thrown.  

\\error Throws an exception if loading fails.  
";

%feature("docstring") Pylon::CFeaturePersistence::SaveToString "

Saves the node map to the string. Sequence sets of a camera are automatically
saved, if SequenceEnable or SequencerConfigurationMode is enabled.  

Parameters
----------
* `Features` :  
    String containing the node map values  
* `pNodeMap` :  
    Pointer to the node map  

\\error Throws an exception if saving fails.  
";

// File: class_pylon_1_1_c_float_parameter.xml


%feature("docstring") Pylon::CFloatParameter "

CFloatParameter class used to simplify access to GenApi parameters.  

C++ includes: FloatParameter.h
";

%feature("docstring") Pylon::CFloatParameter::CFloatParameter "

Creates an empty CFloatParameter object. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::CFloatParameter "

Creates a CFloatParameter object and attaches it to a node, typically retrieved
for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to attach.  

post:  

    *   If the passed node does not match the parameter type, the parameter will
        be empty, see IsValid().  
    *   If the passed node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::CFloatParameter "

Creates a CFloatParameter object and attaches it to a node of a matching type.  

Parameters
----------
* `pFloat` :  
    The node to attach.  

post: The parameter object must not be used to access the node's functionality
    if the source of the attached `pFloat` has been destroyed. In this case,
    call Release() or attach a new node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::CFloatParameter "

Creates a CFloatParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::CFloatParameter "

Creates a CFloatParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `name` is NULL, the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::CFloatParameter "

Copies a CFloatParameter object.  

Parameters
----------
* `rhs` :  
    The object to copy. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::~CFloatParameter "

Destroys the CFloatParameter object. Does not access the attached node. \\error
Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `name` is NULL the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::Attach "

Attaches a node, typically retrieved for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::Attach "

Assigns a node of the same type to the parameter object.  

Parameters
----------
* `pFloat` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::Equals "

Returns true if the same nodes are attached or both parameters are empty.  

Parameters
----------
* `rhs` :  
    The object to compare to.  

Returns
-------
Returns true if the same nodes are attached or both parameters are empty.
\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pNode` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pFloat` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::Release "

Releases the attached node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CFloatParameter::IsValid "
";

%feature("docstring") Pylon::CFloatParameter::SetValue "
";

%feature("docstring") Pylon::CFloatParameter::SetValue "
";

%feature("docstring") Pylon::CFloatParameter::GetValue "
";

%feature("docstring") Pylon::CFloatParameter::GetMin "
";

%feature("docstring") Pylon::CFloatParameter::GetMax "
";

%feature("docstring") Pylon::CFloatParameter::HasInc "
";

%feature("docstring") Pylon::CFloatParameter::GetIncMode "
";

%feature("docstring") Pylon::CFloatParameter::GetInc "
";

%feature("docstring") Pylon::CFloatParameter::GetListOfValidValues "
";

%feature("docstring") Pylon::CFloatParameter::GetRepresentation "
";

%feature("docstring") Pylon::CFloatParameter::GetUnit "
";

%feature("docstring") Pylon::CFloatParameter::GetDisplayNotation "
";

%feature("docstring") Pylon::CFloatParameter::GetDisplayPrecision "
";

%feature("docstring") Pylon::CFloatParameter::ImposeMin "
";

%feature("docstring") Pylon::CFloatParameter::ImposeMax "
";

%feature("docstring") Pylon::CFloatParameter::TrySetValue "
";

%feature("docstring") Pylon::CFloatParameter::TrySetValue "
";

%feature("docstring") Pylon::CFloatParameter::GetValueOrDefault "
";

%feature("docstring") Pylon::CFloatParameter::GetValuePercentOfRange "
";

%feature("docstring") Pylon::CFloatParameter::SetValuePercentOfRange "
";

%feature("docstring") Pylon::CFloatParameter::TrySetValuePercentOfRange "
";

%feature("docstring") Pylon::CFloatParameter::SetToMaximum "
";

%feature("docstring") Pylon::CFloatParameter::SetToMinimum "
";

%feature("docstring") Pylon::CFloatParameter::TrySetToMaximum "
";

%feature("docstring") Pylon::CFloatParameter::TrySetToMinimum "
";

%feature("docstring") Pylon::CFloatParameter::GetAlternativeIntegerRepresentation "
";

// File: class_pylon_1_1_c_grab_result_data.xml


%feature("docstring") Pylon::CGrabResultData "

Makes the data for one grabbed buffer available.  

C++ includes: GrabResultData.h
";

%feature("docstring") Pylon::CGrabResultData::GrabSucceeded "

Returns true if an image has been grabbed successfully and false in the case of
an error.  
";

%feature("docstring") Pylon::CGrabResultData::GetErrorDescription "

This method returns a description of the error if GrabSucceeded() returns false
due to an error.  
";

%feature("docstring") Pylon::CGrabResultData::GetErrorCode "

This method returns the error code if GrabSucceeded() returns false due to an
error.  
";

%feature("docstring") Pylon::CGrabResultData::GetPayloadType "

Get the current payload type.  
";

%feature("docstring") Pylon::CGrabResultData::GetPixelType "

Get the current pixel type.  
";

%feature("docstring") Pylon::CGrabResultData::GetWidth "

Get the current number of columns.  
";

%feature("docstring") Pylon::CGrabResultData::GetHeight "

Get the current number of rows expressed as number of pixels.  
";

%feature("docstring") Pylon::CGrabResultData::GetOffsetX "

Get the current starting column.  
";

%feature("docstring") Pylon::CGrabResultData::GetOffsetY "

Get the current starting row.  
";

%feature("docstring") Pylon::CGrabResultData::GetPaddingX "

Get the number of extra data at the end of each row in bytes.  
";

%feature("docstring") Pylon::CGrabResultData::GetPaddingY "

Get the number of extra data at the end of the image data in bytes.  
";

%feature("docstring") Pylon::CGrabResultData::GetBuffer "

Get the pointer to the buffer.  

If the chunk data feature is activated for the device, chunk data is appended to
the image data. When writing past the image section while performing image
processing, the chunk data will be corrupted.  
";

%feature("docstring") Pylon::CGrabResultData::GetPayloadSize "

Get the current payload size in bytes.  
";

%feature("docstring") Pylon::CGrabResultData::GetBufferSize "

Get the size of the buffer returned by GetBuffer() in bytes.  
";

%feature("docstring") Pylon::CGrabResultData::GetBlockID "

Get the block ID of the grabbed frame (camera device specific).  

par: GigE Camera Devices
    If the Extended ID mode is disabled (default), the sequence number starts
    with 1 and wraps at 65535. If the Extended ID mode is enabled, the sequence
    number starts with 1 and uses the full 64-bit unsigned integer value range.  

A value of 0 indicates that this feature is not supported by the camera. You can
configure the Extended ID mode by setting the GevGVSPExtendedIDMode or the
BslGevGVSPExtendedIDMode parameter, if available. The Instant Camera class and
the pylon GigE stream grabber provide additional parameters for controlling the
Extended ID mode.  

par: USB Camera Devices
    The sequence number starts with 0 and uses the full 64 Bit range.  

attention: A block ID with the value UINT64_MAX indicates that the block ID is
    invalid and must not be used.  
";

%feature("docstring") Pylon::CGrabResultData::GetTimeStamp "

Get the camera specific tick count (camera device specific).  

This describes when the image exposure was started. Cameras that do not support
this feature return zero. If supported, this can be used to determine which
image AOIs were acquired simultaneously.  
";

%feature("docstring") Pylon::CGrabResultData::GetStride "

Get the stride in bytes.  
";

%feature("docstring") Pylon::CGrabResultData::GetImageSize "

Get the size of the image in byte.  
";

%feature("docstring") Pylon::CGrabResultData::GetCameraContext "

Get the context value assigned to the camera object. The context is attached to
the result when it is retrieved.  
";

%feature("docstring") Pylon::CGrabResultData::GetID "

Get the ID of the grabbed image.  

Always returns a number larger than 0. The counting starts with 1 and is never
reset during the lifetime of the Instant Camera object.  
";

%feature("docstring") Pylon::CGrabResultData::GetImageNumber "

Get the number of the image. This number is incremented when an image is
retrieved using CInstantCamera::RetrieveResult().  

Always returns a number larger than 0. The counting starts with 1 and is reset
with every call to CInstantCamera::StartGrabbing().  
";

%feature("docstring") Pylon::CGrabResultData::GetNumberOfSkippedImages "

Get the number of skipped images before this image.  

This value can be larger than 0 if EGrabStrategy_LatestImageOnly grab strategy
or GrabStrategy_LatestImages grab strategy is used. Always returns a number
larger than or equal 0. This number does not include the number of images lost
in case of a buffer underrun in the driver.  
";

%feature("docstring") Pylon::CGrabResultData::IsChunkDataAvailable "

Returns true if chunk data is available.  

This is the case if the chunk mode is enabled for the camera device. The
parameter CInstantCamera::ChunkNodeMapsEnable of the used Instant Camera object
is set to true (default setting). Chunk data node maps are supported by the
Transport Layer of the camera device.  
";

%feature("docstring") Pylon::CGrabResultData::GetChunkDataNodeMap "

Get the reference to the chunk data node map connected to the result.  

An empty node map is returned when the device does not support this feature or
when chunks are disabled.  
";

%feature("docstring") Pylon::CGrabResultData::HasCRC "

Checks if buffer has a CRC attached. This needs not be activated for the device.
See the PayloadCRC16 chunk.  
";

%feature("docstring") Pylon::CGrabResultData::CheckCRC "

Checks CRC sum of buffer, returns true if CRC sum is OK.  
";

%feature("docstring") Pylon::CGrabResultData::GetBufferContext "

Get the context value assigned to the buffer. The context is set when
CInstamtCamera is using a custom buffer factory.  
";

%feature("docstring") Pylon::CGrabResultData::GetDataContainer "

Returns the grab result as a CPylonDataContainer.  
";

%feature("docstring") Pylon::CGrabResultData::GetDataComponentCount "

Returns the number of components contained in the container.  

Returns
-------
Returns the number of components contained in the container.  

You can use the return value to iterate over the existing components by calling
`Pylon::CPylonDataContainer::GetDataComponent()`.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CGrabResultData::GetDataComponent "

Returns a specific component from the container.  

Parameters
----------
* `index` :  
    Index of the component to return. The index must be less than the value
    returned by `Pylon::CPylonDataContainer::GetComponentCount()`.  

Returns
-------
Returns the component specified by the index parameter.  

\\error Throws an exception if the index parameter is out of range. Can throw
exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CGrabResultData::GetDataComponent "

Returns a list of components of the specified type from the container.  

Parameters
----------
* `type` :  
    Type of the components to return.  

Returns
-------
A list of components matching the specified type.  

\\error Can throw exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CGrabResultData::GetFirstImageDataComponent "

Returns the first found image data component.  

Parameters
----------
* `throwIfNotFound` :  
    If true an exception is thrown if no matching component is found. If false,
    an empty component is returned in this case.  

Returns
-------
Returns the component found by
GetFirstImageDataComponent(ComponentType_Intensity, 0, false) if a component is
found. Falls back to delivering any 2D uncompressed image data component found
first in the container otherwise.  

\\error Throws an exception if not matching image is found and throwIfNotFound
is true. Can throw exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CGrabResultData::GetFirstImageDataComponent "

Returns the first found image data component.  

Parameters
----------
* `type` :  
    The type of the component to find.  
* `sourceId` :  
    The source of the component to find.  
* `throwIfNotFound` :  
    If true an exception is thrown if no matching component is found. If false,
    an empty component is returned in this case.  

Returns
-------
Returns the component specified by the type and sourceId parameters.  

\\error Throws an exception if not matching image is found and throwIfNotFound
is true. Can throw exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CGrabResultData::GetGrabResultDataImpl "
";

%feature("docstring") Pylon::CGrabResultData::~CGrabResultData "
";

// File: class_pylon_1_1_c_grab_result_image_t.xml


%feature("docstring") Pylon::CGrabResultImageT "

Low Level API: Adapts grab result to Pylon::IImage.  

C++ includes: ResultImage.h
";

%feature("docstring") Pylon::CGrabResultImageT::CGrabResultImageT "

Creates a grab result image object.  

Parameters
----------
* `grabResult` :  
    A grab result.  
* `isUnique` :  
    User provided info whether the buffer is referenced only by this grab
    result.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CGrabResultImageT::~CGrabResultImageT "

Destroys a grab result image object.  
";

%feature("docstring") Pylon::CGrabResultImageT::IsValid "
";

%feature("docstring") Pylon::CGrabResultImageT::GetPixelType "
";

%feature("docstring") Pylon::CGrabResultImageT::GetWidth "
";

%feature("docstring") Pylon::CGrabResultImageT::GetHeight "
";

%feature("docstring") Pylon::CGrabResultImageT::GetPaddingX "
";

%feature("docstring") Pylon::CGrabResultImageT::GetOrientation "
";

%feature("docstring") Pylon::CGrabResultImageT::GetBuffer "
";

%feature("docstring") Pylon::CGrabResultImageT::GetBuffer "
";

%feature("docstring") Pylon::CGrabResultImageT::GetImageSize "
";

%feature("docstring") Pylon::CGrabResultImageT::IsUnique "
";

%feature("docstring") Pylon::CGrabResultImageT::GetStride "
";

// File: class_pylon_1_1_c_grab_result_ptr.xml


%feature("docstring") Pylon::CGrabResultPtr "

A smart pointer holding a reference to grab result data.  

This class is used for distributing the grab result data of a camera. It
controls the reuse and lifetime of the referenced buffer. When all smart
pointers referencing a buffer go out of scope the referenced buffer is reused or
destroyed. The data and the held buffer are still valid after the camera object
it originated from has been destroyed.  

attention: The grabbing will stop with an input queue underrun, when the grab
    results are never released, e.g. when put into a container.  

The CGrabResultPtr class provides a cast operator that allows passing the grab
result directly to functions or methods that take an const IImage& as parameter,
e.g. image saving functions or image format converter methods.  

attention: The returned reference to IImage is only valid as long the
    CGrabResultPtr object it came from is not destroyed.  

\\threading Instances of CGrabResultPtr referencing the same grab result can be
used from any thread context.  

C++ includes: GrabResultPtr.h
";

%feature("docstring") Pylon::CGrabResultPtr::PylonPrivate::CGrabResultDataConverter "

Internal use only.  
";

%feature("docstring") Pylon::CGrabResultPtr::CGrabResultPtr "

Creates a smart pointer.  

post: No grab result is referenced.  
";

%feature("docstring") Pylon::CGrabResultPtr::CGrabResultPtr "

Creates a copy of a smart pointer.  

Parameters
----------
* `rhs` :  
    Another smart pointer, source of the result data to reference.  

The data itself is not copied.  

post:  

    *   Another reference to the grab result of the source is held if it
        references a grab result.  
    *   No grab result is referenced if the source does not reference a grab
        result.  

\\error Still valid after error.  
";

%feature("docstring") Pylon::CGrabResultPtr::~CGrabResultPtr "

Destroys the smart pointer.  

post: The currently referenced data is released.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CGrabResultPtr::IsValid "

Check whether data is referenced.  

Returns
-------
True if data is referenced.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CGrabResultPtr::Release "

The currently referenced data is released.  

post: The currently referenced data is released.  

\\error Still valid after error.  
";

%feature("docstring") Pylon::CGrabResultPtr::IsUnique "

Indicates that the held grab result data and buffer is only referenced by this
grab result.  

Returns
-------
Returns true if the held grab result data and buffer is only referenced by this
grab result. Returns false if the grab result is invalid.  

\\error Does not throw C++ exceptions.  
";

// File: class_pylon_1_1_c_image_decompressor.xml


%feature("docstring") Pylon::CImageDecompressor "

Provides convenient access to cameras that support image compression and helps
with decompressing these images.  

      A decompressor requires a compression descriptor in order to be able to
decompress images. You can set
      a compression descriptor via the constructor or the
SetCompressionDescriptor methods (in both cases,
      either using the node map or manually).

      A compression descriptor can be identified via a hash. This hash can be
used to identify the matching
      compression descriptor for a particular compressed image. It can be
computed using the
      ComputeCompressionDescriptorHash method or retrieved from the camera,
decompressor, or a grab buffer/result
      using one of the GetCompressionDescriptorHash methods.

      Grab buffers/results may contain different kinds of data. You can use the
      decompressor's GetCompressionInfo methods to distinguish between them. For
that to work, a
      grab buffer/result must have been received successfully and it must
contain the
      payload type chunk (for grab results you can get the payload type using
the
      GetPayloadType method).

      If compression info for the grab buffer/result provided is available,
      GetCompressionInfo returns true and you will receive the compression info
      via the CompressionInfo_t struct.
      If the field hasCompressedImage in the struct is true, the grab
buffer/result
      contains a compressed image. In this case, you should check the
compressionStatus
      field in the struct to check whether the camera was able to compress
      the image properly. The camera can't compress an image if the amount of
      data required for compressing the image exceeds the desired compression
ratio.
      The image can be decompressed if compressionStatus is
CompressionStatus_Ok.
      If the field hasCompressedImage in the struct is false, the grab
buffer/result
      contains an already decompressed image. In this case, the
decompressedImageSize
      and decompressedPayloadSize fields will not be used. All other fields
contain
      information about the decompressed data.
  

C++ includes: ImageDecompressor.h
";

%feature("docstring") Pylon::CImageDecompressor::CImageDecompressor "

Creates an empty decompressor without compression descriptor.  

       This constructor does not initialize the decompressor with a compression
descriptor. You will have to
       initialize the decompressor first by using one of the
SetCompressionDescriptor methods in order to be
       able to decompress images. You will get an exception if you access
methods that require the decompressor
       to be initialized (see method descriptions for which methods are affected
by that precondition).
 \\error Throws an exception if no memory can be allocated.  
";

%feature("docstring") Pylon::CImageDecompressor::CImageDecompressor "

Creates a decompressor by copying from another decompressor.  

Parameters
----------
* `imageDecompressor` :  
    Decompressor to copy from during initialization. \\error Throws an exception
    if no memory can be allocated.  
";

%feature("docstring") Pylon::CImageDecompressor::CImageDecompressor "

Creates a decompressor and initializes it with the compression descriptor
provided.  

Parameters
----------
* `pCompressionDescriptor` :  
    Pointer to the compression descriptor. This parameter must not be NULL.  
* `sizeCompressionDescriptor` :  
    Size of the data (in bytes) of the compression descriptor. \\error Throws an
    exception if no memory can be allocated or the compression descriptor
    provided is invalid (e.g., because it is corrupt) or incompatible (e.g.,
    because a compression descriptor of a newer compression implementation is
    passed).  
";

%feature("docstring") Pylon::CImageDecompressor::CImageDecompressor "

Creates a decompressor and initializes it with a compression descriptor that is
retrieved from the camera's node map.  

Parameters
----------
* `nodeMap` :  
    Node map of the camera to be used for retrieving the compression descriptor.
    \\error Throws an exception if no memory can be allocated or no proper
    compression descriptor can be retrieved from the camera.  
";

%feature("docstring") Pylon::CImageDecompressor::~CImageDecompressor "

Destroys the decompressor instance. \\error Does not throw C++ exceptions.
\\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::HasCompressionDescriptor "

Determines whether the decompressor already has a compression descriptor.  

Returns
-------
Returns true if the decompressor is already initialized with a compression
descriptor or false otherwise. \\error Does not throw C++ exceptions.
\\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::ResetCompressionDescriptor "

Resets the compression descriptor in the decompressor.  

note: After calling this method, no images can be decompressed by the
    decompressor because it is back in uninitialized state. \\error Does not
    throw C++ exceptions. \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::SetCompressionDescriptor "

Initializes a decompressor with the compression descriptor provided.  

Parameters
----------
* `pCompressionDescriptor` :  
    Pointer to the compression descriptor. This parameter must not be NULL.  
* `sizeCompressionDescriptor` :  
    Size of the data (in bytes) of the compression descriptor. \\error Throws an
    exception if no memory can be allocated or the compression descriptor
    provided is invalid (e.g., because it is corrupt) or incompatible (e.g.,
    because a compression descriptor of a newer compression implementation is
    passed). \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::SetCompressionDescriptor "

Initializes a decompressor with a compression descriptor that is retrieved from
the camera's node map.  

Parameters
----------
* `nodeMap` :  
    Node map of the camera to be used for retrieving the compression descriptor.
    \\error Throws an exception if no memory can be allocated or no proper
    compression descriptor can be retrieved from the camera. \\threading This
    method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::GetCompressionDescriptor "

Gets the currently set compression descriptor.  

       This method requires that a compression descriptor has been set
previously via the constructor or
       the SetCompressionDescriptor methods. You can determine this via the
HasCompressionDescriptor method.
  

Parameters
----------
* `pCompressionDescriptor` :  
    Pointer to the buffer that will receive the compression descriptor or NULL
    if you only want to get the size of the buffer for buffer allocation.  
* `pSizeCompressionDescriptor` :  
    On input, the variable specifies the size of the buffer (in bytes) for the
    compression descriptor (if pCompressionDescriptor is not NULL). On output,
    the variable will receive the actual buffer size required for the current
    compression descriptor. This parameter must not be NULL. \\error Throws an
    exception if the decompressor has no compression descriptor set or the input
    parameters are invalid (e.g., if the size provided is not sufficient to hold
    the compression descriptor). \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::GetCompressionDescriptor "

Gets the current compression descriptor from the camera's node map.  

       This method requires image compression to be enabled in the camera. You
can determine this via the
       GetCompressionMode method.
  

Parameters
----------
* `pCompressionDescriptor` :  
    Pointer to the buffer that will receive the compression descriptor or NULL
    if you only want to get the size of the buffer for buffer allocation.  
* `pSizeCompressionDescriptor` :  
    On input, the variable specifies the size of the buffer (in bytes) for the
    compression descriptor (if pCompressionDescriptor is not NULL). On output,
    the variable will receive the actual buffer size required for the current
    compression descriptor. This parameter must not be NULL.  
* `nodeMap` :  
    Node map of the camera to be used for retrieving the compression descriptor.
    \\error Throws an exception if compression is not enabled in the camera (or
    unavailable) or the input parameters are invalid (e.g., if the size provided
    is not sufficient to hold the compression descriptor). \\threading This
    method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::GetCompressionDescriptorHash "

Gets the hash of the currently set compression descriptor.  

       This method requires that a compression descriptor has been set
previously via the constructor or
       the SetCompressionDescriptor methods. You can determine this via the
HasCompressionDescriptor method.
  

Parameters
----------
* `pHash` :  
    Pointer to the buffer that will receive the compression descriptor hash or
    NULL if you only want to get the size of the buffer for buffer allocation.  
* `pSizeHash` :  
    On input, the variable specifies the size of the buffer (in bytes) for the
    compression descriptor hash (if pHash is not NULL). On output, the variable
    will receive the actual buffer size required for the current compression
    descriptor hash. This parameter must not be NULL. \\error Throws an
    exception if the decompressor has no compression descriptor set or the input
    parameters are invalid (e.g., if the size provided is not sufficient to hold
    the compression descriptor hash). \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::GetCompressionDescriptorHash "

Gets the hash of the current compression descriptor from the camera's node map.  

       This method requires image compression to be enabled in the camera. You
can determine this via the
       GetCompressionMode method.
  

Parameters
----------
* `pHash` :  
    Pointer to the buffer that will receive the compression descriptor hash or
    NULL if you only want to get the size of the buffer for buffer allocation.  
* `pSizeHash` :  
    On input, the variable specifies the size of the buffer (in bytes) for the
    compression descriptor hash (if pHash is not NULL). On output, the variable
    will receive the actual buffer size required for the current compression
    descriptor hash. This parameter must not be NULL.  
* `nodeMap` :  
    Node map of the camera to be used for retrieving the compression descriptor
    hash. \\error Throws an exception if compression is not active in the camera
    (or unavailable) or the input parameters are invalid (e.g., if the size
    provided is not sufficient to hold the compression descriptor hash).
    \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::GetCompressionDescriptorHash "

Gets the hash of the compression descriptor that is required for decompressing
the grab buffer provided.  

       The grab buffer provided must contain the entire camera payload,
including chunk data. The payload must have
       been received without errors. It must include a compressed image.
  

Parameters
----------
* `pHash` :  
    Pointer to the buffer that will receive the compression descriptor hash or
    NULL if you only want to get the size of the buffer for buffer allocation.  
* `pSizeHash` :  
    On input, the variable specifies the size of the buffer (in bytes) for the
    compression descriptor hash (if pHash is not NULL). On output, the variable
    will receive the actual buffer size required for the current compression
    descriptor hash. This parameter must not be NULL.  
* `pGrabBuffer` :  
    Pointer to the grab buffer that holds the compressed data. This parameter
    must not be NULL.  
* `payloadSize` :  
    Payload size (in bytes) of the data received (must be less or equal to the
    size of the grab buffer).  
* `endianness` :  
    Endianness of the grab buffer's content. If not known, auto detection can be
    used. \\error Throws an exception if the grab buffer does not contain
    compressed data, the data is corrupt, or the input parameters are invalid
    (e.g., if the size provided is not sufficient to hold the compression
    descriptor hash). \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::GetCompressionDescriptorHash "

Gets the hash of the compression descriptor that is required for decompressing
the grab result provided.  

Parameters
----------
* `pHash` :  
    Pointer to the buffer that will receive the compression descriptor hash or
    NULL if you only want to get the size of the buffer for buffer allocation.  
* `pSizeHash` :  
    On input, the variable specifies the size of the buffer (in bytes) for the
    compression descriptor hash (if pHash is not NULL). On output, the variable
    will receive the actual buffer size required for the current compression
    descriptor hash. This parameter must not be NULL.  
* `grabResult` :  
    Grab result that holds the compressed data.  
* `endianness` :  
    Endianness of the grab result content. If not known, auto detection can be
    used. \\error Throws an exception if the grab result does not contain
    compressed data, the data is corrupt, or the input parameters are invalid
    (e.g., if the size provided is not sufficient to hold the compression
    descriptor hash). \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::GetCompressionDescriptorHash "

Gets the hash of the compression descriptor that is required for decompressing
the grab result provided.  

Parameters
----------
* `pHash` :  
    Pointer to the buffer that will receive the compression descriptor hash or
    NULL if you only want to get the size of the buffer for buffer allocation.  
* `pSizeHash` :  
    On input, the variable specifies the size of the buffer (in bytes) for the
    compression descriptor hash (if pHash is not NULL). On output, the variable
    will receive the actual buffer size required for the current compression
    descriptor hash. This parameter must not be NULL.  
* `grabResultPtr` :  
    Pointer to grab result that holds the compressed data.  
* `endianness` :  
    Endianness of the grab result content. If not known, auto detection can be
    used. \\error Throws an exception if the grab result does not contain
    compressed data, the data is corrupt, or the input parameters are invalid
    (e.g., if the size provided is not sufficient to hold the compression
    descriptor hash). \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::DecompressImage "

Decompresses the image of the grab buffer provided.  

       This method requires that a compression descriptor has been set
previously via the constructor or
       the SetCompressionDescriptor methods. You can determine this via the
HasCompressionDescriptor method.

       The grab buffer provided must contain the entire camera payload,
including chunk data. The payload must have
       been received without errors. It must include a compressed image.
  

Parameters
----------
* `pOutputBuffer` :  
    Pointer to the buffer that will receive the decompressed image. This
    parameter must not be NULL.  
* `pSizeOutputBuffer` :  
    On input, the variable specifies the size of the buffer (in bytes) for the
    decompressed image (must be larger or equal to the value in the
    decompressedImageSize field in the CompressionInfo_t struct received via the
    GetCompressionInfo methods; alternatively, the GetImageSizeForDecompression
    method can be used to get the image size required for decompression). On
    output, the variable will receive the actual buffer size required for the
    decompressed image. This parameter must not be NULL.  
* `pGrabBuffer` :  
    Pointer to the grab buffer that holds the compressed data. This parameter
    must not be NULL.  
* `payloadSize` :  
    Payload size (in bytes) of the data received (must be less or equal to the
    size of the grab buffer).  

Returns
-------
Returns the struct with the compression information of the compressed image.
\\error Throws an exception if the grab buffer does not contain compressed data,
the data is corrupt, the image cannot be decompressed, or the input parameters
are invalid (e.g., if the size provided is not sufficient to hold the
decompressed image). \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::DecompressImage "

Decompresses the image of the grab result provided.  

       This method requires that a compression descriptor has been set
previously via the constructor or
       the SetCompressionDescriptor methods. You can determine this via the
HasCompressionDescriptor method.

       The grab result provided must contain a compressed image that has been
received without errors.
  

Parameters
----------
* `pOutputBuffer` :  
    Pointer to the buffer that will receive the decompressed image. This
    parameter must not be NULL.  
* `pSizeOutputBuffer` :  
    On input, the variable specifies the size of the buffer (in bytes) for the
    decompressed image (must be larger or equal to the value in the
    decompressedImageSize field in the CompressionInfo_t struct received via the
    GetCompressionInfo methods; alternatively, the GetImageSizeForDecompression
    method can be used to get the image size required for decompression). On
    output, the variable will receive the actual buffer size required for the
    decompressed image. This parameter must not be NULL.  
* `grabResult` :  
    Grab result that holds the compressed data.  

Returns
-------
Returns the struct with the compression information about the compressed image.
\\error Throws an exception if the grab result does not contain compressed data,
the data is corrupt, the image cannot be decompressed or the input parameters
are invalid (e.g., if the size provided is not sufficient to hold the
decompressed image). \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::DecompressImage "

Decompresses the image of the grab result provided.  

       This method requires that a compression descriptor has been set
previously via the constructor or
       the SetCompressionDescriptor methods. You can determine this via the
HasCompressionDescriptor method.

       The grab result provided must contain a compressed image that has been
received without errors.
  

Parameters
----------
* `pOutputBuffer` :  
    Pointer to the buffer that will receive the decompressed image. This
    parameter must not be NULL.  
* `pSizeOutputBuffer` :  
    On input, the variable specifies the size of the buffer (in bytes) for the
    decompressed image (must be larger or equal to the value in the
    decompressedImageSize field in the CompressionInfo_t struct received via the
    GetCompressionInfo methods; alternatively, the GetImageSizeForDecompression
    method can be used to get the image size required for decompression). On
    output, the variable will receive the actual buffer size required for the
    decompressed image. This parameter must not be NULL.  
* `grabResultPtr` :  
    Pointer to grab result that holds the compressed data.  

Returns
-------
Returns the struct with the compression information about the compressed image.
\\error Throws an exception if the grab result does not contain compressed data,
the data is corrupt, the image cannot be decompressed or the input parameters
are invalid (e.g., if the size provided is not sufficient to hold the
decompressed image). \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::DecompressImage "

Decompresses the image of the grab buffer provided.  

       This method requires that a compression descriptor has been set
previously via the constructor or
       the SetCompressionDescriptor methods. You can determine this via the
HasCompressionDescriptor method.

       The grab buffer provided must contain the entire camera payload,
including chunk data. The payload must have
       been received without errors. It must include a compressed image.
  

Parameters
----------
* `destinationImage` :  
    Image object (e.g., instance of CPylonImage) that will be filled with the
    decompressed image (will be resized if required).  
* `pGrabBuffer` :  
    Pointer to the grab buffer that holds the compressed data. This parameter
    must not be NULL.  
* `payloadSize` :  
    Payload size (in bytes) of the data received (must be less or equal to the
    size of the grab buffer).  

Returns
-------
Returns the struct with the compression information about the compressed image.
\\error Throws an exception if the grab buffer does not contain compressed data,
the data is corrupt, the image cannot be decompressed or the input parameters
are invalid. \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::DecompressImage "

Decompresses the image of the grab result provided.  

       This method requires that a compression descriptor has been set
previously via the constructor or
       the SetCompressionDescriptor methods. You can determine this via the
HasCompressionDescriptor method.

       The grab result provided must contain a compressed image that has been
received without errors.
  

Parameters
----------
* `destinationImage` :  
    Image object (e.g., instance of CPylonImage) that will be filled with the
    decompressed image (will be resized if required).  
* `grabResult` :  
    Grab result that holds the compressed data.  

Returns
-------
Returns the struct with the compression information about the compressed image.
\\error Throws an exception if the grab result does not contain compressed data,
the data is corrupt, the image cannot be decompressed, or the input parameters
are invalid. \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::DecompressImage "

Decompresses the image of the grab result provided.  

       This method requires that a compression descriptor has been set
previously via the constructor or
       the SetCompressionDescriptor methods. You can determine this via the
HasCompressionDescriptor method.

       The grab result provided must contain a compressed image that has been
received without errors.
  

Parameters
----------
* `destinationImage` :  
    Image object (e.g., instance of CPylonImage) that will be filled with the
    decompressed image (will be resized if required).  
* `grabResultPtr` :  
    Pointer to grab result that holds the compressed data.  

Returns
-------
Returns the struct with the compression information about the compressed image.
\\error Throws an exception if the grab result does not contain compressed data,
the data is corrupt, the image cannot be decompressed, or the input parameters
are invalid. \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::GetCompressionMode "

Retrieves the current compression mode from the camera's node map.  

       This indicates which kind of compression is active or whether compression
is not enabled (or unavailable).
  

Parameters
----------
* `nodeMap` :  
    Node map of the camera to be used for retrieving the compression mode.  

Returns
-------
Returns the current compression mode of the camera. \\error Throws an exception
if an error is encountered while determining the compression mode. \\threading
This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::GetCompressionInfo "

Gets compression information about a grab buffer.  

       The grab buffer provided must contain the entire camera payload,
including chunk data. The payload must have
       been received without errors. It must include a compressed image.
  

Parameters
----------
* `compressionInfo` :  
    Reference to the struct that will receive the compression information if the
    grab buffer contains such information.  
* `pGrabBuffer` :  
    Pointer to the grab buffer that holds the compressed data. This parameter
    must not be NULL.  
* `payloadSize` :  
    Payload size (in bytes) of the data received (must be less or equal to the
    size of the grab buffer).  
* `endianness` :  
    Endianness of the grab buffer's content. If not known, auto detection can be
    used.  

Returns
-------
Returns true if compression information could be extracted from the the grab
buffer or false otherwise. \\error Throws an exception if the input parameters
are invalid. \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::GetCompressionInfo "

Gets compression information about a grab result.  

Parameters
----------
* `compressionInfo` :  
    Reference to the struct that will receive the compression information if the
    grab result contains such information.  
* `grabResult` :  
    Grab result that holds the compressed data.  
* `endianness` :  
    Endianness of the grab result content. If not known, auto detection can be
    used.  

Returns
-------
Returns true if compression information could be extracted from the the grab
result or false otherwise. \\error Throws an exception if the input parameters
are invalid. \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::GetCompressionInfo "

Gets compression information about a grab result.  

Parameters
----------
* `compressionInfo` :  
    Reference to the struct that will receive the compression information if the
    grab result contains such information.  
* `grabResultPtr` :  
    Pointer to grab result that holds the compressed data.  
* `endianness` :  
    Endianness of the grab result content. If not known, auto detection can be
    used.  

Returns
-------
Returns true if compression information could be extracted from the the grab
result or false otherwise. \\error Throws an exception if the input parameters
are invalid. \\threading This method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::ComputeCompressionDescriptorHash "

Computes the hash for a given compression descriptor.  

Parameters
----------
* `pHash` :  
    Pointer to the buffer that will receive the compression descriptor hash or
    NULL if you only want to get the size of the buffer for buffer allocation.  
* `pSizeHash` :  
    On input, the variable specifies the size of the buffer (in bytes) for the
    compression descriptor hash (if pHash is not NULL). On output, the variable
    will receive the actual buffer size required for the current compression
    descriptor hash. This parameter must not be NULL.  
* `pCompressionDescriptor` :  
    Pointer to the compression descriptor. This parameter must not be NULL.  
* `sizeCompressionDescriptor` :  
    Size of the data (in bytes) of the compression descriptor. \\error Throws an
    exception if the input parameters are invalid (e.g., if the size provided is
    not sufficient to hold the compression descriptor hash). \\threading This
    method is thread-safe.  
";

%feature("docstring") Pylon::CImageDecompressor::GetImageSizeForDecompression "

Gets size (in bytes) required for allocating buffers for decompressing the
images during streaming.  

       This method requires image compression to be enabled in the camera. You
can determine this via the
       GetCompressionMode method.
  

Parameters
----------
* `nodeMap` :  
    Node map of the camera to be used for retrieving the image size required for
    decompression.  

Returns
-------
Returns the buffer size (in bytes) required for image decompression. \\error
Throws an exception if an error is encountered while determining the image size
required for decompression. \\threading This method is thread-safe.  
";

// File: class_pylon_1_1_c_image_event_handler.xml


%feature("docstring") Pylon::CImageEventHandler "

The image event handler base class.  

C++ includes: ImageEventHandler.h
";

%feature("docstring") Pylon::CImageEventHandler::OnImagesSkipped "

This method is called when images have been skipped using the
GrabStrategy_LatestImageOnly strategy or the GrabStrategy_LatestImages strategy.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `countOfSkippedImages` :  
    The number of images skipped. This `countOfSkippedImages` does not include
    the number of images lost in the case of a buffer under run in the driver.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called outside the lock of the camera object but
inside the lock of the image event handler registry.  
";

%feature("docstring") Pylon::CImageEventHandler::OnImageGrabbed "

This method is called when an image has been grabbed.  

The grab result smart pointer passed does always reference a grab result data
object. The status of the grab needs to be checked before accessing the grab
result data. See CGrabResultData::GrabSucceeded(),
CGrabResultData::GetErrorCode() and CGrabResultData::GetErrorDescription() for
more information.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `grabResult` :  
    The grab result data.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called outside the lock of the camera object but
inside the lock of the image event handler registry.  
";

%feature("docstring") Pylon::CImageEventHandler::OnImageEventHandlerRegistered "

This method is called when the image event handler has been registered.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. \\threading This
method is called inside the lock of the image event handler registry.  
";

%feature("docstring") Pylon::CImageEventHandler::OnImageEventHandlerDeregistered "

This method is called when the image event handler has been deregistered.  

The image event handler is automatically deregistered when the Instant Camera
object is destroyed.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error C++ exceptions from this call will be caught and ignored. \\threading
This method is called inside the lock of the image event handler registry.  
";

%feature("docstring") Pylon::CImageEventHandler::DestroyImageEventHandler "

Destroys the image event handler.  

\\error C++ exceptions from this call will be caught and ignored.  
";

%feature("docstring") Pylon::CImageEventHandler::CImageEventHandler "

Create.  
";

%feature("docstring") Pylon::CImageEventHandler::CImageEventHandler "

Copy.  
";

%feature("docstring") Pylon::CImageEventHandler::~CImageEventHandler "

Destruct.  
";

%feature("docstring") Pylon::CImageEventHandler::DebugGetEventHandlerRegistrationCount "
";

// File: class_pylon_1_1_c_image_format_converter.xml


%feature("docstring") Pylon::CImageFormatConverter "

Creates new images by converting a source image to another format.  

Supported input image formats defined by the pixel type:  

*   PixelType_Mono1packed  
*   PixelType_Mono2packed  
*   PixelType_Mono4packed  
*   PixelType_Mono8  
*   PixelType_Mono10  
*   PixelType_Mono10packed  
*   PixelType_Mono10p  
*   PixelType_Mono12  
*   PixelType_Mono12packed  
*   PixelType_Mono12p  
*   PixelType_Mono16  

*   PixelType_BayerGR8  
*   PixelType_BayerRG8  
*   PixelType_BayerGB8  
*   PixelType_BayerBG8  
*   PixelType_BayerGR10  
*   PixelType_BayerRG10  
*   PixelType_BayerGB10  
*   PixelType_BayerBG10  
*   PixelType_BayerGR12  
*   PixelType_BayerRG12  
*   PixelType_BayerGB12  
*   PixelType_BayerBG12  
*   PixelType_BayerGR12Packed  
*   PixelType_BayerRG12Packed  
*   PixelType_BayerGB12Packed  
*   PixelType_BayerBG12Packed  
*   PixelType_BayerGR10p  
*   PixelType_BayerRG10p  
*   PixelType_BayerGB10p  
*   PixelType_BayerBG10p  
*   PixelType_BayerGR12p  
*   PixelType_BayerRG12p  
*   PixelType_BayerGB12p  
*   PixelType_BayerBG12p  
*   PixelType_BayerGR16  
*   PixelType_BayerRG16  
*   PixelType_BayerGB16  
*   PixelType_BayerBG16  

*   PixelType_RGB8packed  
*   PixelType_BGR8packed  
*   PixelType_RGBA8packed  
*   PixelType_BGRA8packed  
*   PixelType_RGB10packed  
*   PixelType_BGR10packed  
*   PixelType_RGB12packed  
*   PixelType_BGR12packed  
*   PixelType_RGB12V1packed  
*   PixelType_RGB16packed  
*   PixelType_RGB8planar  
*   PixelType_RGB16planar  

*   PixelType_BiColorRGBG8  
*   PixelType_BiColorBGRG8  
*   PixelType_BiColorRGBG10  
*   PixelType_BiColorBGRG10  
*   PixelType_BiColorRGBG10p  
*   PixelType_BiColorBGRG10p  
*   PixelType_BiColorRGBG12  
*   PixelType_BiColorBGRG12  
*   PixelType_BiColorRGBG12p  
*   PixelType_BiColorBGRG12p  

*   PixelType_YUV422packed  
*   PixelType_YUV422_YUYV_Packed  
*   PixelType_YCbCr422_8_YY_CbCr_Semiplanar  
*   PixelType_YCbCr420_8_YY_CbCr_Semiplanar  

*   PixelType_Confidence8  
*   PixelType_Coord3D_C8  
*   PixelType_Confidence16  
*   PixelType_Coord3D_C16  
*   PixelType_Error8  
  

Supported output image formats defined by the pixel type:  

*   PixelType_BGRA8packed - This pixel type can be used in Windows bitmaps. See
    Pylon::SBGRA8Pixel.  
*   PixelType_BGR8packed - This pixel type can be used in Windows bitmaps. See
    Pylon::SBGR8Pixel.  
*   PixelType_RGBA8packed - See Pylon::SRGBA8Pixel.  
*   PixelType_RGB8packed - See Pylon::SRGB8Pixel.  
*   PixelType_RGB16packed - See Pylon::SRGB16Pixel.  
*   PixelType_RGB8planar  
*   PixelType_RGB16planar  
*   PixelType_Mono8  
*   PixelType_Mono16  
*   PixelType_YUV444planar  
*   PixelType_YUV422planar  
*   PixelType_YUV420planar  
  

All input image formats can be converted to all output image formats.  

RGB, BGR and Bayer image formats are converted to monochrome formats by using
the following formula:  


YUV formats are converted to 16 bit bit depth in an intermediate conversion
step. This is why the output is always aligned at the most significant bit when
converting to 16 bit color output formats like PixelType_RGB16packed.  

par: Limitations:
    The last column of a YUV input image with odd width cannot be converted. The
    last column and the last row of a Bayer input image cannot be converted.  

The default treatment of rows and columns that cannot be converted due to their
location on edges, can be controlled using the
CImageFormatConverter::InconvertibleEdgeHandling parameter. See also the
Convert() method description.  

\\threading The CImageFormatConverter class is not thread-safe.  

C++ includes: ImageFormatConverter.h
";

%feature("docstring") Pylon::CImageFormatConverter::CImageFormatConverter "

Creates an image format converter.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::~CImageFormatConverter "

Destroys the image format converter.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::Initialize "

Optionally initializes the image format converter before conversion.  

Parameters
----------
* `sourcePixelType` :  
    The pixel type of the source image.  

*   Depending on parameter settings and the input format, data structures
    required for conversion are created, e.g. lookup tables.  
*   Initialization is done automatically when calling Convert() if needed. This
    may add a delay when converting the first image.  

pre:  

    *   The converter parameters are set up.  
    *   The `pixelTypeSource` must be supported by the converter.  

Lookup tables are created when using monochrome images as input and when the
gamma conversion method is selected or when the shift conversion method is
selected and the value of AdditionalLeftShift is not zero. The converter can be
reinitialized with other settings if required.  

\\error Throws an exception if the passed pixel type does not represent a valid
input format. The converter object is still valid after error and can be
initialized again.  
";

%feature("docstring") Pylon::CImageFormatConverter::IsInitialized "

Returns information about the converter being initialized.  

Parameters
----------
* `sourcePixelType` :  
    The pixel type of the source image.  

The result depends on the converter settings.  

Returns
-------
True if initialized.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::Uninitialize "

Destroys data structures required for conversion.  

This function can be called to free resources held by the format converter.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::ImageHasDestinationFormat "

Checks to see if a conversion is required or if the source image already has the
desired format.  

Parameters
----------
* `sourceImage` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

Returns
-------
Returns true if the source image already has the desired format.  

A conversion may even be required image format does not change e.g. if the gamma
conversion method is selected and the format describes a monochrome image.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::ImageHasDestinationFormat "

Checks to see if a conversion is required or if the source image already has the
desired format.  

Parameters
----------
* `sourcePixelType` :  
    The pixel type of the source image.  
* `sourcePaddingX` :  
    The number of extra data bytes at the end of each row. The default value is
    usually 0.  
* `sourceOrientation` :  
    The vertical orientation of the image in the image buffer. The default value
    is usually ImageOrientation_TopDown.  

Returns
-------
Returns true if the source image already has the desired format. This is done
according to the current converter settings.  

A conversion may even be required image format does not change e.g. if the gamma
conversion method is selected and the format describes a monochrome image.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::GetBufferSizeForConversion "

Computes the size of the destination image buffer in byte.  

Parameters
----------
* `sourceImage` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

Returns
-------
The size of the destination image when converting the given source image using
current converter settings.  

\\error Throws an exception if the destination image size for the passed input
cannot be computed. The converter object is still valid after error.  
";

%feature("docstring") Pylon::CImageFormatConverter::GetBufferSizeForConversion "

Computes the size of the destination image buffer in byte.  

Parameters
----------
* `sourceWidth` :  
    The number of pixels in a row in the source image.  
* `sourceHeight` :  
    The number of rows in the source image.  
* `sourcePixelType` :  
    The pixel type of the source image.  

Returns
-------
The size of the destination image when converting the source image using current
converter settings.  

pre:  

    *   The `sourceWidth` value must be >= 0 and < _I32_MAX.  
    *   The `sourceHeight` value must be >= 0 and < _I32_MAX.  

\\error Throws an exception if the destination image size for the passed input
cannot be computed. The converter object is still valid after error.  
";

%feature("docstring") Pylon::CImageFormatConverter::Convert "

Creates a new image by converting an image to a different format.  

The IReusableImage::Reset() method of the destination image is called to set the
destination format. The image is converted to the destination image according to
the current converter settings. The padding area of a row in the destination
image is set to zero.  

The OutputPaddingX setting is ignored for images that do not support user
defined padding, e.g. CPylonBitmapImage. See also
IReusableImage::IsAdditionalPaddingSupported().  

Parameters
----------
* `destinationImage` :  
    The destination image, e.g. a CPylonImage or CPylonBitmapImage object. When
    passing a CPylonBitmapImage object the target format must be supported by
    the CPylonBitmapImage class.  
* `sourceImage` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

pre:  

    *   The source and destination images must be different images.  
    *   The source image must be valid.  
    *   The format of the source image must be supported by the converter.  
    *   The destination image must support the destination format.  
    *   The destination image must be able to provide a large enough buffer to
        hold the image.  

\\error Throws an exception if the passed parameters are not valid. The
converter object is still valid after error.  
";

%feature("docstring") Pylon::CImageFormatConverter::Convert "

Creates a new image by converting an image to a different format.  

The IReusableImage::Reset() method of the destination image is called to set the
destination format. The image is converted to the destination image according to
the current converter settings. The padding area of a row in the destination
image is set to zero.  

The OutputPaddingX setting is ignored for images that do not support user
defined padding, e.g. CPylonBitmapImage. See also
IReusableImage::IsAdditionalPaddingSupported().  

Parameters
----------
* `destinationImage` :  
    The destination image.  
* `pSourceBuffer` :  
    The pointer to the buffer of the source image.  
* `sourceBufferSizeBytes` :  
    The size of the buffer of the source image.  
* `sourcePixelType` :  
    The pixel type of the source image.  
* `sourceWidth` :  
    The number of pixels in a row in the source image.  
* `sourceHeight` :  
    The number of rows in the source image.  
* `sourcePaddingX` :  
    The number of extra data bytes at the end of each row. The default value is
    usually 0.  
* `sourceOrientation` :  
    The vertical orientation of the source image in the image buffer. The
    default value is usually ImageOrientation_TopDown.  

pre:  

    *   The pixel type must be valid.  
    *   The `sourceWidth` value must be >= 0 and < _I32_MAX.  
    *   The `sourceHeight` value must be >= 0 and < _I32_MAX.  
    *   The pointer to the source buffer must not be NULL.  
    *   The source buffer must be large enough to hold the image described by
        the parameters.  
    *   The format of the input image represented by the given parameter must be
        supported by the converter.  
    *   The destination image must support the destination format.  
    *   The destination image must be able to provide a large enough buffer to
        hold the image.  
    *   The source image buffer and the destination image buffer must not be
        identical.  

\\error Throws an exception if the passed parameters are not valid. The
converter object is still valid after error.  
";

%feature("docstring") Pylon::CImageFormatConverter::Convert "

Creates a new image by converting an image to a different format.  

The image is converted to the destination image according to the current
converter settings. The padding area of a row in the destination image is set to
zero.  

Parameters
----------
* `pDestinationBuffer` :  
    The pointer to the buffer of the destination image.  
* `destinationBufferSizeBytes` :  
    The size of the buffer of the destination image.  
* `sourceImage` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

pre:  

    *   The format of the source image must be supported by the converter.  
    *   The destination image buffer must be large enough to hold the
        destination image.  
    *   The source image buffer and the destination image buffer must not be
        identical.  

\\error Throws an exception if the passed parameters are not valid. The
converter object is still valid after error.  
";

%feature("docstring") Pylon::CImageFormatConverter::Convert "

Creates a new image by converting an image to a different format.  

The image is converted to the destination image according to the current
converter settings. The padding area of a row in the destination image is set to
zero.  

Parameters
----------
* `pDestinationBuffer` :  
    The pointer to the buffer of the destination image.  
* `destinationBufferSizeBytes` :  
    The size of the buffer of the destination image.  
* `pSourceBuffer` :  
    The pointer to the buffer of the source image.  
* `sourceBufferSizeBytes` :  
    The size of the buffer of the source image.  
* `sourcePixelType` :  
    The pixel type of the source image.  
* `sourceWidth` :  
    The number of pixels in a row in the source image.  
* `sourceHeight` :  
    The number of rows in the source image.  
* `sourcePaddingX` :  
    The number of extra data bytes at the end of each row. The default value is
    usually 0.  
* `sourceOrientation` :  
    The vertical orientation of the source image in the image buffer. The
    default value is usually ImageOrientation_TopDown.  

pre:  

    *   The parameters regarding the source buffer must describe a valid image.  
    *   The format of the input image represented by the given parameter must be
        supported by the converter.  
    *   If the destination image buffer must be large enough to hold the
        destination image.  
    *   The the source buffer can not be equal the destination buffer.  

\\error Throws an exception if the passed parameters are not valid. The
converter object is still valid after error.  
";

%feature("docstring") Pylon::CImageFormatConverter::GetNodeMap "

Provides access to the node map of the format converter.  

Returns
-------
Reference to the node map of the format converter.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::IsSupportedInputFormat "

Returns true if the image format defined by the given pixel type is a supported
input format.  

Parameters
----------
* `sourcePixelType` :  
    The pixel type of the source image.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::IsSupportedOutputFormat "

Returns true if the image format defined by the given pixel type is a supported
output format.  

Parameters
----------
* `destinationPixelType` :  
    The pixel type of the destination image.  

\\error Does not throw C++ exceptions.  
";

// File: class_pylon_1_1_c_image_persistence.xml


%feature("docstring") Pylon::CImagePersistence "

Contains static functions supporting loading and saving of images.  

C++ includes: ImagePersistence.h
";

%feature("docstring") Pylon::CImagePersistence::Save "

Saves the image to disk. Converts the image to a format that can be saved if
required.  

If required, the image is automatically converted to a new image and then saved.
See CanSaveWithoutConversion() for more information. An image with a bit depth
higher than 8 bit is stored with 16 bit bit depth if supported by the image file
format. In this case the pixel data is MSB aligned.  

If more control over the conversion is required then the CImageFormatConverter
class can be used to convert the input image before saving it.  

Depending on your operating system, the following file types are supported:  

*   Windows: BMP, JPG, PNG, TIFF  
*   Linux: BMP, JPG, PNG, TIFF  
*   MacOS: BMP, JPG, PNG, TIFF  

Parameters
----------
* `imageFileFormat` :  
    The file format to save the image in.  
* `filename` :  
    Name and path of the image.  
* `pBuffer` :  
    The pointer to the buffer of the image.  
* `bufferSize` :  
    The size of the buffer in byte.  
* `pixelType` :  
    The pixel type of the image to save.  
* `width` :  
    The number of pixels in a row of the image to save.  
* `height` :  
    The number of rows of the image to save.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  
* `pOptions` :  
    Additional options.  

pre:  

    *   The pixel type of the image to save must be a supported input format of
        the Pylon::CImageFormatConverter.  
    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  

\\error Throws an exception if saving the image fails.  
";

%feature("docstring") Pylon::CImagePersistence::Save "

Saves the image to disk. Converts the image to a format that can be if required.  

If required, the image is automatically converted to a new image and then saved.
See CanSaveWithoutConversion() for more information. An image with a bit depth
higher than 8 bit is stored with 16 bit bit depth if supported by the image file
format. In this case the pixel data is MSB aligned.  

If more control over the conversion is required then the CImageFormatConverter
class can be used to convert the input image before saving it.  

Depending on your operating system, the following file types are supported:  

*   Windows: BMP, JPG, PNG, TIFF  
*   Linux: BMP, JPG, PNG, TIFF  
*   MacOS: BMP, JPG, PNG, TIFF  

Parameters
----------
* `imageFileFormat` :  
    The target file format for the image to save.  
* `filename` :  
    Name and path of the image.  
* `image` :  
    The image to save, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  
* `pOptions` :  
    Additional options.  

pre: The pixel type of the image to save must be a supported input format of the
    Pylon::CImageFormatConverter.  

\\error Throws an exception if saving the image fails.  
";

%feature("docstring") Pylon::CImagePersistence::CanSaveWithoutConversion "

Can be used to check whether the given image can be saved without prior
conversion.  

See the CImagePersistence::CanSaveWithoutConversion( EImageFileFormat, const
IImage&) method documentation for a list of supported pixel formats.  

Parameters
----------
* `imageFileFormat` :  
    The target file format for the image to save.  
* `pixelType` :  
    The pixel type of the image to save.  
* `width` :  
    The number of pixels in a row of the image to save.  
* `height` :  
    The number of rows of the image to save.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

Returns
-------
Returns true if the image can be saved without prior conversion.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImagePersistence::CanSaveWithoutConversion "

Can be used to check whether the image can be saved without prior conversion.  

Supported formats for TIFF:  

*   PixelType_Mono8  
*   PixelType_Mono16  
*   PixelType_RGB8packed  
*   PixelType_RGB16packed  
  

Supported formats for BMP, JPEG and PNG:  

*   PixelType_Mono8  
*   PixelType_BGR8packed  
*   PixelType_BGRA8packed  
  

Supported formats for DNG:  

*   PixelType_BayerGR*  
*   PixelType_BayerRG*  
*   PixelType_BayerGB*  
*   PixelType_BayerBG*  
  
 With *: 8, 10, 12, 16, 10p, 12p, 12packed  

Parameters
----------
* `imageFileFormat` :  
    The target file format for the image to save.  
* `image` :  
    The image to save, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

Returns
-------
Returns true if the image can be saved without prior conversion.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImagePersistence::Load "

Loads an image from disk.  

The orientation of loaded images is always ImageOrientation_TopDown. Depending
on your operating system, the following file types are supported:  

*   Windows: BMP, JPG, PNG, TIFF  
*   Linux: BMP, JPG, PNG, TIFF  
*   MacOS: BMP, JPG, PNG, TIFF  

Parameters
----------
* `filename` :  
    Name and path of the image.  
* `image` :  
    The target image object, e.g. a CPylonImage or CPylonBitmapImage object.
    When passing a CPylonBitmapImage object the loaded format must be supported
    by the CPylonBitmapImage class.  

\\error Throws an exception if the image cannot be loaded. The image buffer
content is undefined when the loading of the image fails.  
";

%feature("docstring") Pylon::CImagePersistence::LoadFromMemory "

Loads an image from memory.  

The orientation of loaded images is always ImageOrientation_TopDown. Depending
on your operating system, the following file types are supported:  

*   Windows: BMP, JPG, PNG, TIFF  
*   Linux: PNG, TIFF  
*   MacOS: PNG, TIFF  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the source image.  
* `bufferSizeBytes` :  
    The size of the buffer of the source image.  
* `image` :  
    The target image object, e.g. a CPylonImage or CPylonBitmapImage object.
    When passing a CPylonBitmapImage object the loaded format must be supported
    by the CPylonBitmapImage class.  

\\error Throws an exception if the image cannot be loaded. The image buffer
content is undefined when the loading of the image fails.  
";

// File: class_pylon_1_1_c_image_persistence_options.xml


%feature("docstring") Pylon::CImagePersistenceOptions "

Used to pass options to CImagePersistence methods.  

C++ includes: ImagePersistence.h
";

%feature("docstring") Pylon::CImagePersistenceOptions::CImagePersistenceOptions "
";

%feature("docstring") Pylon::CImagePersistenceOptions::~CImagePersistenceOptions "
";

%feature("docstring") Pylon::CImagePersistenceOptions::SetQuality "

Set the image quality options. Valid quality values range from 0 to 100.  
";

%feature("docstring") Pylon::CImagePersistenceOptions::GetQuality "

Returns the set quality level.  
";

// File: class_pylon_1_1_c_info_base.xml


%feature("docstring") Pylon::CInfoBase "

Base implementation for PYLON info container.  

Info container allow a generic access to implemented properties. All Properties
and their values can be accessed without knowing them in advance. It is possible
to enumerate all properties available and corresponding values. Properties and
values are represented as String_t. The normal usage is to have enumerators that
create the info objects and clients that read only.  

If the type of the info object is known before client can use specific accessor
function to retrieve the property values  

C++ includes: Info.h
";

%feature("docstring") Pylon::CInfoBase::GetFriendlyName "

Retrieves the human readable name of the device. This property is identified by
Key::FriendlyNameKey.  
";

%feature("docstring") Pylon::CInfoBase::SetFriendlyName "

Sets the above property.  
";

%feature("docstring") Pylon::CInfoBase::IsFriendlyNameAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CInfoBase::GetFullName "

Retrieves the full name identifying the device. This property is identified by
Key::FullNameKey.  
";

%feature("docstring") Pylon::CInfoBase::SetFullName "

Sets the above property.  
";

%feature("docstring") Pylon::CInfoBase::IsFullNameAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CInfoBase::GetVendorName "

Retrieves the vendor name of the device. This property is identified by
Key::VendorNameKey.  
";

%feature("docstring") Pylon::CInfoBase::SetVendorName "

Sets the above property.  
";

%feature("docstring") Pylon::CInfoBase::IsVendorNameAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CInfoBase::GetDeviceClass "

Retrieves the device class device, e.g. BaslerUsb. This property is identified
by Key::DeviceClassKey.  
";

%feature("docstring") Pylon::CInfoBase::SetDeviceClass "

Sets the above property.  
";

%feature("docstring") Pylon::CInfoBase::IsDeviceClassAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CInfoBase::GetTLType "

Retrieves the transport layer type. This property is identified by
Key::TLTypeKey.  
";

%feature("docstring") Pylon::CInfoBase::SetTLType "

Sets the above property.  
";

%feature("docstring") Pylon::CInfoBase::IsTLTypeAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CInfoBase::GetPropertyNames "
";

%feature("docstring") Pylon::CInfoBase::GetPropertyAvailable "
";

%feature("docstring") Pylon::CInfoBase::GetPropertyValue "
";

%feature("docstring") Pylon::CInfoBase::SetPropertyValue "
";

%feature("docstring") Pylon::CInfoBase::IsUserProvided "
";

%feature("docstring") Pylon::CInfoBase::IsSubset "
";

%feature("docstring") Pylon::CInfoBase::GetPropertyNotAvailable "
";

// File: class_pylon_1_1_c_instant_camera.xml


%feature("docstring") Pylon::CInstantCamera "

Provides convenient access to a camera device.  

*   Establishes a single access point for accessing camera functionality.  
*   The class can be used off the shelf without any parameters. The camera uses
    a default configuration for the camera device. This can be overridden.  
*   Handles Pylon device lifetime. This can be overridden.  
*   Handles opening and closing of a Pylon device automatically.  
*   Handles chunk data parsing automatically returning the chunk data in the
    grab result.  
*   Handles event grabbing automatically providing a convenient interface for
    event callbacks. This can be overridden.  
*   Handles physical camera device removal.  
*   Handles the creation, reuse, and destruction of buffers.  
*   The grabbing can be done in the context of the caller or by using an
    additional grab loop thread.  
*   The Instant Camera class is extensible using derivation or by registering
    event handler objects.  

C++ includes: InstantCamera.h
";

%feature("docstring") Pylon::CInstantCamera::CInstantCamera "

Creates an Instant Camera object with no attached Pylon device.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCamera::CInstantCamera "

Creates an Instant Camera object and calls Attach().  

See Attach() for more information.  

Parameters
----------
* `pDevice` :  
    The Pylon device to attach.  
* `cleanupProcedure` :  
    If cleanupProcedure equals Cleanup_Delete, the Pylon device is destroyed
    when the Instant Camera object is destroyed.  

\\error May throw an exception if the passed Pylon device is open. Does not
throw C++ exceptions if the passed Pylon device is closed or NULL.  
";

%feature("docstring") Pylon::CInstantCamera::~CInstantCamera "

Destroys an Instant Camera object.  

Calls Attach( NULL) for destroying or removing a Pylon device depending on the
passed cleanup procedure.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCamera::Attach "

Attaches a Pylon device to the Instant Camera.  

Parameters
----------
* `pDevice` :  
    The Pylon device to attach.  
* `cleanupProcedure` :  
    If cleanupProcedure equals Cleanup_Delete, the Pylon device is destroyed
    when the Instant Camera object is destroyed.  

*   If a Pylon device is currently attached, it is destroyed (DestroyDevice())
    or removed (DetachDevice()) depending on the previously set cleanup
    procedure value.  
*   If the pDevice parameter is NULL, nothing more is done.  
*   The OnAttach configuration event is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  
*   The new Pylon device is attached.  
*   The instant camera migration mode setting is applied to the Pylon device
    transport layer node map.  
*   If the passed Pylon device is open, callbacks for camera events are
    registered at the camera node map. (This may fail)  
*   If the passed Pylon device is open, a device removal call back is
    registered. (This may fail)  
*   If the passed Pylon device is open, access modifiers (see
    IPylonDevice::Open()) are carried over as camera parameters.  
*   The OnAttached configuration event is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  

post:  

    *   If the passed pointer to the Pylon device is NULL, the Instant Camera
        object is in the \"no device attached\" state.  
    *   If the passed pointer to the Pylon device is not NULL, the passed Pylon
        device is attached.  
    *   If the set cleanup procedure equals Cleanup_Delete, the Pylon device is
        destroyed when the Instant Camera object is destroyed or a new device is
        attached.  
    *   If the passed Pylon device is open and the registration of callbacks
        fails, the Instant Camera object is in the \"no device attached\" state.  
    *   The opened-by-user flag is set, preventing closing of the Pylon device
        on StopGrabbing() when the attached Pylon device is already open.  

\\error May throw an exception if the passed Pylon device is open. Does not
throw C++ exceptions if the passed Pylon device is closed or NULL.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsPylonDeviceAttached "

Returns the Pylon device attached state of the Instant Camera object.  

Returns
-------
True if a Pylon device is attached.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsCameraDeviceRemoved "

Returns the connection state of the camera device.  

attention: Due to technical reasons, the IsCameraDeviceRemoved() property may
    not be updated immediately after the first error caused by a device removal
    occurs.  

The device removal is only detected while the Instant Camera and therefore the
attached Pylon device are open.  

The attached Pylon device is not operable anymore if the camera device has been
removed from the PC. After it is made sure that no access to the Pylon device or
any of its node maps is made anymore the Pylon device should be destroyed using
CInstantCamera::DeviceDestroy(). The access to the Pylon device can be protected
using the lock provided by GetLock(), e.g. when accessing parameters.  

Returns
-------
True if the camera device removal from the PC has been detected.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::HasOwnership "

Returns the ownership of the attached Pylon device.  

Returns
-------
True if a Pylon device is attached and the Instant Camera object has been given
the ownership by passing the cleanup procedure Cleanup_Delete when calling
Attach().  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::DestroyDevice "

Destroys the attached Pylon device.  

attention: The node maps, e.g. the camera node map, of the attached Pylon device
    must not be accessed anymore while destroying the Pylon device.  

*   If no Pylon device is attached, nothing is done.  
*   If the Pylon device is open, it is closed by calling Close().  
*   The configuration event OnDestroy is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  
*   The Pylon device is destroyed even if the cleanup procedure Cleanup_None has
    been passed when calling Attach() before.  
*   The configuration event OnDestroyed is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  

post: No Pylon device is attached.  

\\error Does not throw C++ exceptions. Possible C++ exceptions are caught and
ignored.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::DetachDevice "

Detaches an attached Pylon device.  

*   If no Pylon device is attached, nothing is done.  
*   If a grab is in progress, it is stopped by calling StopGrabbing().  
*   The configuration event OnDetach is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  
*   The Pylon device is detached.  
*   The configuration event OnDetached is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  

Returns
-------
The attached Pylon device or NULL if nothing has been attached before.  

post:  

    *   No Pylon device is attached.  
    *   The ownership of the Pylon device goes to the caller who is responsible
        for destroying the Pylon device.  

\\error Does not throw C++ exceptions. Possible C++ exceptions are caught and
ignored.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::Open "

Opens the attached Pylon device.  

*   Opened by user flag is set, preventing closing of the device on
    StopGrabbing().  
*   If the Pylon device is already open, nothing more is done.  
*   The OnOpen configuration event is fired. The notification of event handlers
    stops when an event call triggers an exception.  
*   The Pylon device is opened and a connection to the camera device is
    established.  
*   The instant camera migration mode setting is applied to the Pylon device
    transport layer node map.  
*   A device removal call back is registered at the Pylon device.  
*   Callbacks for camera events are registered at the camera node map.  
*   The OnOpened configuration event is fired if the Pylon device has been
    opened successfully. The notification of event handlers stops when an event
    call triggers an exception.  

pre: A Pylon device is attached.  

post:  

    *   The Pylon device is open and a connection to the camera device has been
        established.  
    *   Opened by user flag is set, preventing closing of the Pylon device on
        StopGrabbing().  

\\error The Instant Camera object is still valid after error. The Pylon device
open may throw. Configuration event calls may throw. Callback registrations may
throw. The Pylon device is closed with Close() if the OnOpened event call
triggers an exception.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsOpen "

Returns the open state of the attached Pylon device object.  

note: This method still returns true if the camera device has been physically
    removed from the PC while the attached Pylon device object is open. The
    Pylon device object will not automatically close itself on device removal.
    It must be closed by calling CInstantCamera::Close(). The
    IsCameraDeviceRemoved() method can be used to check if the connection to the
    camera device has been lost while the attached Pylon device object is open.
    \\error Does not throw C++ exceptions.  

Returns
-------
Returns true if a Pylon device is attached and it is open. \\threading This
method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::Close "

Closes the attached Pylon device.  

*   If no Pylon device is attached, nothing is done.  
*   If the Pylon device is already closed, nothing is done.  
*   If a grab is in progress, it is stopped by calling StopGrabbing().  
*   The configuration event OnClose is fired. Possible C++ exceptions from event
    calls are caught and ignored. All event handlers are notified.  
*   The connection to the camera device is closed and the Pylon device is
    closed.  
*   The configuration event OnClosed is fired if the Pylon device has been
    closed successfully. Possible C++ exceptions from event calls are caught and
    ignored. All event handlers are notified.  

post: The connection to the camera device is closed and the Pylon device is
    closed.  

\\error Does not throw C++ exceptions. Possible C++ exceptions are caught and
ignored.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::StartGrabbing "

Starts the grabbing of images.  

*   If a grab loop thread has been used in the last grab session, the grab loop
    thread context is joined with the caller's context.  
*   If the Pylon device is not already open, it is opened by calling Open().  
*   The configuration event OnGrabStart is fired. The notification of event
    handlers stops when an event call triggers an exception.  
*   Grab-specific parameters of the camera object are locked, e.g.
    MaxNumBuffers.  
*   If the camera device parameter ChunkModeActive is enabled, the Instant
    Camera chunk parsing support is initialized.  
*   If the Instant Camera parameter GrabCameraEvents is enabled, the Instant
    Camera event grabbing support is initialized.  
*   The grabbing is started.  
*   The AcquisitionStart command of the camera device is executed.  
*   The configuration event OnGrabStarted is fired if the grab has been started
    successfully. The notification of event handlers stops when an event call
    triggers an exception.  
*   If grabLoopType equals GrabLoop_ProvidedByInstantCamera, an additional grab
    loop thread is started calling RetrieveResult( GrabLoopThreadTimeout,
    grabResult) in a loop.  

Parameters
----------
* `strategy` :  
    The grab strategy. See Pylon::EGrabStrategy for more information  
* `grabLoopType` :  
    If grabLoopType equals GrabLoop_ProvidedByInstantCamera, an additional grab
    loop thread is used to run the grab loop.  

pre:  

    *   A Pylon device is attached.  
    *   The stream grabber of the Pylon device is closed.  
    *   The grabbing is stopped.  
    *   The attached Pylon device supports grabbing.  
    *   Must not be called while holding the lock provided by GetLock() when
        using the grab loop thread.  

post:  

    *   The grabbing is started.  
    *   Grab-specific parameters of the camera object are locked, e.g.
        MaxNumBuffers.  
    *   If grabLoopType equals GrabLoop_ProvidedByInstantCamera, an additional
        grab loop thread is running that calls RetrieveResult(
        GrabLoopThreadTimeout, grabResult) in a loop. Images are processed by
        registered image event handlers.  
    *   Operating the stream grabber from outside the camera object will result
        in undefined behavior.  

\\error The Instant Camera object is still valid after error. Open() may throw.
Configuration event calls may throw. The grab implementation may throw. The
grabbing is stopped with StopGrabbing() if the OnGrabStarted event call triggers
an exception. Throws a C++ exception, if Upcoming Image grab strategy is used
together with USB camera devices.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::StartGrabbing "

Starts the grabbing for a maximum number of images.  

Extends the StartGrabbing(EStrategy, EGrabLoop) by a number of images to grab.
If the passed count of images has been reached, StopGrabbing is called
automatically. The images are counted according to the grab strategy. Skipped
images are not taken into account.  

The amount of allocated buffers is reduced to maxImages when grabbing fewer
images than according to the value of the `MaxNumBuffer`  parameter and the grab
strategy is GrabStrategy_OneByOne.  

Parameters
----------
* `maxImages` :  
    The count of images to grab. This value must be larger than zero.  
* `strategy` :  
    The grab strategy. See Pylon::InstantCamera::EStrategy for more information.  
* `grabLoopType` :  
    If grabLoopType equals GrabLoop_ProvidedByInstantCamera, an additional grab
    loop thread is used to run the grab loop.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::RetrieveResult "

Retrieves a grab result according to the strategy, waits if it is not yet
available.  

*   The content of the passed grab result is released.  
*   If no Pylon device is attached or the grabbing is not started, the method
    returns immediately \"false\".  
*   Wait for a grab result if it is not yet available. The access to the camera
    is not locked during waiting. Camera events are handled.  
*   Only if camera events are used: Incoming camera events are handled.  
*   One grab result is retrieved per call according to the strategy applied.  
*   Only if chunk mode is used: The chunk data parsing is performed. The grab
    result data is updated using chunk data.  
*   The image event OnImagesSkipped is fired if grab results have been skipped
    according to the strategy. The notification of event handlers stops when an
    event call triggers an exception.  
*   The image event OnImageGrabbed is fired if a grab result becomes available.
    The notification of event handlers stops when an event call triggers an
    exception.  
*   Stops the grabbing by calling StopGrabbing() if the maximum number of images
    has been grabbed.  
  

It needs to be checked whether the grab represented by the grab result has been
successful, see CGrabResultData::GrabSucceeded().  

Parameters
----------
* `timeoutMs` :  
    A timeout value in ms for waiting for a grab result, or the INFINITE value.  
* `grabResult` :  
    Receives the grab result.  
* `timeoutHandling` :  
    If timeoutHandling equals TimeoutHandling_ThrowException, a timeout
    exception is thrown on timeout.  

Returns
-------
True if the call successfully retrieved a grab result, false otherwise.  

pre:  

    *   There is no other thread waiting for a result. This will be the case
        when the Instant Camera grab loop thread is used.  

post:  

    *   If a grab result has been retrieved, one image is removed from the
        output queue and is returned in the grabResult parameter.  
    *   If no grab result has been retrieved, an empty grab result is returned
        in the grabResult parameter.  
    *   If the maximum number of images has been grabbed, the grabbing is
        stopped.  
    *   If camera event handling is enabled and camera events were received, at
        least one or more camera event messages have been processed.  

\\error The Instant Camera object is still valid after error. The grabbing is
stopped if an exception is thrown.  

\\threading This method is synchronized using the lock provided by GetLock()
while not waiting.  
";

%feature("docstring") Pylon::CInstantCamera::StopGrabbing "

Stops the grabbing of images.  

*   Nothing is done if the Instant Camera is not currently grabbing.  
*   The configuration event OnGrabStop is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  
*   The AcquisitionStop command of the camera device is executed.  
*   The grabbing is stopped.  
*   All buffer queues of the Instant Camera are cleared.  
*   The OnGrabStopped configuration event is fired if the grab has been stopped
    successfully. Possible C++ exceptions from event calls are caught and
    ignored. All event handlers are notified.  
*   If the Instant Camera has been opened by StartGrabbing, it is closed by
    calling Close().  
*   Grab-specific parameters of the camera object are unlocked, e.g.
    MaxNumBuffers.  

post:  

    *   The grabbing is stopped.  
    *   If the Pylon device has been opened by StartGrabbing and no other camera
        object service requires it to be open, it is closed.  
    *   Grab specific parameters of the camera object are unlocked, e.g.
        MaxNumBuffers.  

\\error Does not throw C++ exceptions. Possible C++ exceptions are caught and
ignored.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsGrabbing "

Returns state of grabbing.  

The camera object is grabbing after a successful call to StartGrabbing() until
StopGrabbing() is called.  

Returns
-------
Returns true if still grabbing.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GrabOne "

Grabs one image.  

The following code shows a simplified version of what is done (happy path):  


GrabOne() can be used to together with the CAcquireSingleFrameConfiguration.  

note: Using GrabOne is more efficient if the Pylon device is already open,
    otherwise the Pylon device is opened and closed for each call.  

note: Grabbing single images using Software Trigger
    (CSoftwareTriggerConfiguration) is recommended if you want to maximize frame
    rate. This is because the overhead per grabbed image is reduced compared to
    Single Frame Acquisition. The grabbing can be started using StartGrabbing().
    Images are grabbed using the WaitForFrameTriggerReady(),
    ExecuteSoftwareTrigger() and RetrieveResult() methods instead of using
    GrabOne. The grab can be stopped using StopGrabbing() when done.  

Parameters
----------
* `timeoutMs` :  
    A timeout value in ms for waiting for a grab result, or the INFINITE value.  
* `grabResult` :  
    Receives the grab result.  
* `timeoutHandling` :  
    If timeoutHandling equals TimeoutHandling_ThrowException, a timeout
    exception is thrown on timeout.  

Returns
-------
Returns true if the call successfully retrieved a grab result and the grab
succeeded (CGrabResultData::GrabSucceeded()).  

pre: Must meet the preconditions of start grabbing.  

post: Meets the postconditions of stop grabbing.  

\\error The Instant Camera object is still valid after error. See
StartGrabbing(), RetrieveResult(), and StopGrabbing() . In the case of
exceptions after StartGrabbing() the grabbing is stopped using StopGrabbing().  
";

%feature("docstring") Pylon::CInstantCamera::GetQueuedBufferCount "

Deprecated: This method has been deprecated. Use the NumQueuedBuffers parameter
instead.  

Returns
-------
The number of buffers that are queued for grabbing.  
";

%feature("docstring") Pylon::CInstantCamera::GetGrabResultWaitObject "

Provides access to a wait object indicating available grab results.  

Returns
-------
A wait object indicating available grab results.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetGrabStopWaitObject "

Provides access to a wait object indicating that the grabbing has stopped.  

Returns
-------
A wait object indicating that the grabbing has stopped.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetCameraEventWaitObject "

Provides access to a wait object indicating available camera events.  

This wait object is Pylon device specific and changes when a new Pylon device is
attached to the camera.  

Returns
-------
A wait object indicating available camera events.  

pre:  

    *   A Pylon device is attached.  
    *   The Pylon device is open.  

\\error The Instant Camera object is still valid after error.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::RegisterConfiguration "

Adds a configurator to the list of registered configurator objects.  

*   If mode equals RegistrationMode_ReplaceAll, the list of registered
    configurators is cleared.  
*   If pointer `pConfigurator` is not NULL, it is appended to the list of
    configurators.  

Parameters
----------
* `pConfigurator` :  
    The receiver of configuration events.  
* `mode` :  
    Indicates how to register the new configurator.  
* `cleanupProcedure` :  
    If cleanupProcedure equals Cleanup_Delete, the passed event handler is
    deleted when no longer needed.  

post: The configurator is registered and called on configuration events.  

\\error Does not throw C++ exceptions, except when memory allocation fails.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::DeregisterConfiguration "

Removes a configurator from the list of registered configurator objects.  

If the configurator is not found, nothing is done.  

Parameters
----------
* `configurator` :  
    The registered receiver of configuration events.  

Returns
-------
True if successful  

post:  

    *   The configurator is deregistered.  
    *   If the configuration has been registered by passing a pointer and the
        cleanup procedure is Cleanup_Delete, the event handler is deleted.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::RegisterImageEventHandler "

Adds an image event handler to the list of registered image event handler
objects.  

*   If mode equals RegistrationMode_ReplaceAll, the list of registered image
    event handlers is cleared.  
*   If pointer `pImageEventHandler` is not NULL, it is appended to the list of
    image event handlers.  

Parameters
----------
* `pImageEventHandler` :  
    The receiver of image events.  
* `mode` :  
    Indicates how to register the new imageEventHandler.  
* `cleanupProcedure` :  
    If cleanupProcedure equals Cleanup_Delete, the passed event handler is
    deleted when no longer needed.  

post: The imageEventHandler is registered and called on image related events.  

\\error Does not throw C++ exceptions, except when memory allocation fails.  

\\threading This method is synchronized using the internal image event handler
registry lock.  
";

%feature("docstring") Pylon::CInstantCamera::DeregisterImageEventHandler "

Removes an image event handler from the list of registered image event handler
objects.  

If the image event handler is not found, nothing is done.  

Parameters
----------
* `imageEventHandler` :  
    The registered receiver of configuration events.  

Returns
-------
True if successful  

post:  

    *   The imageEventHandler is deregistered.  
    *   If the image event handler has been registered by passing a pointer and
        the cleanup procedure is Cleanup_Delete, the event handler is deleted.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the internal image event handler
registry lock.  
";

%feature("docstring") Pylon::CInstantCamera::RegisterCameraEventHandler "

Adds an camera event handler to the list of registered camera event handler
objects.  

*   If mode equals RegistrationMode_ReplaceAll, the list of registered camera
    event handlers is cleared.  
*   If the pointer `pCameraEventHandler` is not NULL, it is appended to the list
    of camera event handlers.  

Parameters
----------
* `pCameraEventHandler` :  
    The receiver of camera events.  
* `nodeName` :  
    The name of the event data node updated on camera event, e.g.
    \"ExposureEndEventTimestamp\" for exposure end event.  
* `userProvidedId` :  
    This ID is passed as a parameter in CCameraEventHandler::OnCameraEvent and
    can be used to distinguish between different events. It is recommended to
    create an own application specific enum and use it's values as IDs.  
* `mode` :  
    Indicates how to register the new cameraEventHandler.  
* `cleanupProcedure` :  
    If cleanupProcedure equals Cleanup_Delete, the passed event handler is
    deleted when no longer needed.  
* `availability` :  
    If availability equals CameraEventAvailability_Mandatory, the camera must
    support the data node specified by node name. If not, an exception is thrown
    when the Instant Camera is open, the Instant Camera is opened, or an open
    Pylon device is attached.  

Internally, a GenApi node call back is registered for the node identified by
`nodeName`. This callback triggers a call to the
`CCameraEventHandler::OnCameraEvent()` method. That's why a Camera Event Handler
can be registered for any node of the camera node map to get informed about
changes.  

post: The cameraEventHandler is registered and called on camera events.  

\\error Throws an exception if the availability is set to
CameraEventAvailability_Mandatory and the node with the name `nodeName` is not
available in the camera node map (see GetNodeMap()). Throws an exception fail if
the node callback registration fails. The event handler is not registered when
an C++ exception is thrown.  

\\threading This method is synchronized using the camera event handler lock. If
the camera is open, the lock provided by GetLock() and the camera node map lock
are also used for synchronization.  
";

%feature("docstring") Pylon::CInstantCamera::DeregisterCameraEventHandler "

Removes a camera event handler from the list of registered camera event handler
objects.  

If the camera event handler is not found, nothing is done.  

Parameters
----------
* `cameraEventHandler` :  
    The registered receiver of camera events.  
* `nodeName` :  
    The name of the event data node updated on camera event, e.g.
    \"ExposureEndEventTimestamp\" for exposure end event.  

Returns
-------
True if successful  

post:  

    *   The cameraEventHandler is deregistered.  
    *   If the camera event handler has been registered by passing a pointer and
        the cleanup procedure is Cleanup_Delete, the event handler is deleted.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the camera event handler lock. If
the camera is open, the camera node map lock is also used for synchronization.  
";

%feature("docstring") Pylon::CInstantCamera::WaitForFrameTriggerReady "

Actively waits until the the camera is ready to accept a frame trigger.  

The implementation selects 'FrameTriggerWait' for the
'AcquisitionStatusSelector' and waits until the 'AcquisitionStatus' is true. If
the above mentioned nodes are not available and the 'SoftwareTrigger' node is
readable, the implementation waits for SoftwareTrigger.IsDone().  

Parameters
----------
* `timeoutMs` :  
    The timeout in ms for active waiting.  
* `timeoutHandling` :  
    If timeoutHandling equals TimeoutHandling_ThrowException, a timeout
    exception is thrown on timeout.  

Returns
-------
True if the camera can execute a frame trigger.  

pre: The 'AcquisitionStatusSelector' node is writable and the
    'AcquisitionStatus' node is readable or the 'SoftwareTrigger' node is
    readable. This depends on the used camera model.  

\\error Accessing the camera registers may fail.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::CanWaitForFrameTriggerReady "

Checks to see whether the camera device can be queried whether it is ready to
accept the next frame trigger.  

If 'FrameTriggerWait' can be selected for 'AcquisitionStatusSelector' and
'AcquisitionStatus' is readable, the camera device can be queried whether it is
ready to accept the next frame trigger.  

If the nodes mentioned above are not available and the 'SoftwareTrigger' node is
readable, the camera device can be queried whether it is ready to accept the
next frame trigger.  

note: If a camera device can't be queried whether it is ready to accept the next
    frame trigger, the camera device is ready to accept the next trigger after
    the last image triggered has been grabbed, e.g. after you have retrieved the
    last image triggered using RetrieveResult(). Camera devices that can be
    queried whether they are ready to accept the next frame trigger, may not be
    ready for the next frame trigger after the last image triggered has been
    grabbed.  

Returns
-------
Returns true if the camera is open and the camera device can be queried whether
it is ready to accept the next frame trigger.  

post: The 'AcquisitionStatusSelector' is set to 'FrameTriggerWait' if writable.  

\\error Accessing the camera registers may fail.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::ExecuteSoftwareTrigger "

Executes the software trigger command.  

The camera needs to be configured for software trigger mode. Additionally, the
camera needs to be ready to accept triggers. When triggering a frame this can be
checked using the WaitForFrameTriggerReady() method;  

note: The application has to make sure that the correct trigger is selected
    before calling ExecuteSoftwareTrigger(). This can be done via the camera's
    TriggerSelector node. The `Pylon::CSoftwareTriggerConfiguration` selects the
    correct trigger when the Instant Camera is opened.  

pre:  

    *   The grabbing is started.  
    *   The camera device supports software trigger.  
    *   The software trigger is available. This depends on the configuration of
        the camera device.  

\\error Accessing the camera registers may fail.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::SetCameraContext "

Sets a context that is attached to each grab result of the camera object on
RetrieveResult(). This is useful when handling multiple cameras. It has nothing
in common with the context passed to the stream grabber when queuing a buffer.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetCameraContext "

Returns the context that is attached to each grab result of the camera object.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetDeviceInfo "

Provides access to the device info object of the attached Pylon device or an
empty one.  

Returns
-------
The info object of the attached Pylon device or an empty one.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetNodeMap "

Provides access to the node map of the camera device.  

The Pylon device must be opened before reading ore writing any parameters of the
camera device. This can be done using the Open() method of the Instant Camera
class.  

Returns
-------
Reference to the node map of the camera device.  

pre: A Pylon device is attached.  

\\error The Instant Camera object is still valid after error.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetTLNodeMap "

Provides access to the transport layer node map of the attached Pylon device.  

Returns
-------
Reference to the transport layer node map of the attached Pylon device or the
reference to the empty node map if a transport layer node map is not supported.
The GenApi::INodeMap::GetNumNodes() method can be used to check whether the node
map is empty.  

pre: A Pylon device is attached.  

\\error The Instant Camera object is still valid after error.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetStreamGrabberNodeMap "

Provides access to the stream grabber node map of the attached Pylon device.  

Returns
-------
Reference to the stream grabber node map of the attached Pylon device or the
reference to the empty node map if grabbing is not supported. The
GenApi::INodeMap::GetNumNodes() method can be used to check whether the node map
is empty.  

pre:  

    *   A Pylon device is attached.  
    *   The Pylon device is open.  

\\error The Instant Camera object is still valid after error.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetEventGrabberNodeMap "

Provides access to the event grabber node map of the attached Pylon device.  

Returns
-------
Reference to the event grabber node map of the attached Pylon device or a
reference to the empty node map if event grabbing is not supported. The
GenApi::INodeMap::GetNumNodes() method can be used to check whether the node map
is empty.  

pre:  

    *   A Pylon device is attached.  
    *   The Pylon device is open.  

\\error The Instant Camera object is still valid after error.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetInstantCameraNodeMap "

Provides access to the node map of the Instant Camera object.  

The node map of the camera device is made available by the GetNodeMap() method.  

Returns
-------
Reference to the node map of the Instant Camera object.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::SetBufferFactory "

Sets an alternative buffer factory that is used for buffer allocation.  

This use of this method is optional and intended for advanced use cases only.  

If NULL is passed as buffer factory then the default buffer factory is used.
Buffers are allocated when StartGrabbing is called. A buffer factory must not be
deleted while it is attached to the camera object and it must not be deleted
until the last buffer is freed. To free all buffers the grab needs to be stopped
and all grab results must be released or destroyed.  

Parameters
----------
* `pFactory` :  
    A pointer to a buffer factory.  
* `cleanupProcedure` :  
    If ownership is cleanupProcedure Cleanup_Delete, the passed factory is
    destroyed when no longer needed.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsGigE "

Returns true if a GigE Pylon device is attached to the Instant Camera object.  

This method is provided for convenience only. The device type can also be
determined as shown in the following example.  


\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsUsb "

Returns true if a USB Pylon device is attached to the Instant Camera object.  

This method is provided for convenience only. The device type can also be
determined as shown in the following example.  


\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsCameraLink "

Returns true if a Camera Link Pylon device is attached to the Instant Camera
object.  

This method is provided for convenience only. The device type can also be
determined as shown in the following example.  


\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsCxp "

Returns true if a CoaXPress GenTL device is attached to the Instant Camera
object.  

This method is provided for convenience only.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetSfncVersion "

Returns the SFNC version read from the camera node map.  

The SFNC version is read from the camera node map using the integer nodes
DeviceSFNCVersionMajor, DeviceSFNCVersionMinor, and DeviceSFNCVersionSubMinor.  

Returns
-------
The SFNC version used by the camera device. The returned SFNC version is 0.0.0
(Pylon::Sfnc_VersionUndefined) if no SFNC version information is provided by the
camera device.  

pre: A Pylon device is attached.  

\\error The Instant Camera object is still valid after error.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetExtensionInterface "
";

// File: class_pylon_1_1_c_instant_camera_array.xml


%feature("docstring") Pylon::CInstantCameraArray "

Supports grabbing with multiple camera devices.  

\\threading The CInstantCameraArray class is not thread-safe.  

C++ includes: InstantCameraArray.h
";

%feature("docstring") Pylon::CInstantCameraArray::CInstantCameraArray "

Creates an Instant Camera Array of size 0.  

Initialize() can be used to adjust the size of the array.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::CInstantCameraArray "

Creates an Instant Camera Array.  

Calls Initialize() to adjust the size of the array.  

Parameters
----------
* `numberOfCameras` :  
    The number of cameras the array shall hold. Can be 0.  

The index operator can be used to access the individual cameras for attaching a
Pylon Device or for configuration.  

Example:  

\\error Does not throw C++ exceptions, except when memory allocation fails.  
";

%feature("docstring") Pylon::CInstantCameraArray::~CInstantCameraArray "

Destroys the Instant Camera Array.  

If a grab is in progress, it is stopped by calling StopGrabbing().  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::Initialize "

Initializes the array.  

*   If a grab is in progress, it is stopped by calling StopGrabbing().  
*   All cameras of the array are destroyed.  
*   A new set of cameras is created. No Pylon Devices are attached.  
*   The camera context values are set to the index of the camera in the array
    using CInstantCamera::SetCameraContext.  
  

The index operator can be used to access the individual cameras for attaching a
Pylon Device or for configuration.  

Parameters
----------
* `numberOfCameras` :  
    The number of cameras the array shall hold.  

\\error Does not throw C++ exceptions, except when memory allocation fails.  
";

%feature("docstring") Pylon::CInstantCameraArray::IsPylonDeviceAttached "

Returns the attachment state of cameras in the array.  

Returns
-------
True if all cameras in the array have a Pylon Device attached. False is returned
if the size of the array is 0.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::IsCameraDeviceRemoved "

Returns the connection state of the camera devices used by the Instant Cameras
in the array.  

The device removal is only detected if the Instant Cameras and therefore the
attached Pylon Devices are open.  

The Pylon Device is not operable after this event. After it is made sure that no
access to the Pylon Device or any of its node maps is made anymore the Pylon
Device should be destroyed using InstantCamera::DeviceDestroy(). The access to
the Pylon Device can be protected using the lock provided by GetLock(), e.g.
when accessing parameters.  

Returns
-------
True if the camera device removal from the PC for any camera in the array has
been detected.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::DestroyDevice "

Destroys the Pylon Devices that are attached to the Instant Cameras in the
array.  

attention: The node maps, e.g. the camera node map, of the attached Pylon Device
    must not be accessed anymore while destroying the Pylon Device.  

*   If a grab is in progress, it is stopped by calling StopGrabbing().  
*   DestroyDevice is called for all cameras. See CInstantCamera::DestroyDevice()
    for more information.  

post: No Pylon Devices are attached to the cameras in the array.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::DetachDevice "

Detaches all Pylon Devices that are attached to the Instant Cameras in the
array.  

*   If a grab is in progress, it is stopped by calling StopGrabbing().  
*   DetachDevice is called for all cameras, see CInstantCamera::DetachDevice()
    for more information.  

post:  

    *   No Pylon Devices are attached to the cameras in the array.  
    *   The ownership of the Pylon Devices goes to the caller who is responsible
        for destroying the Pylon Devices.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::Open "

Opens all cameras in the array.  

Open is called for all cameras. See CInstantCamera::Open() for more information.  

pre:  

    *   The size of the array is larger than 0.  
    *   All devices are attached.  

post: The cameras are open.  

\\error If one camera throws an exception, all cameras are closed by calling
Close().  
";

%feature("docstring") Pylon::CInstantCameraArray::IsOpen "

Returns the open state of the cameras in the array. \\error Does not throw C++
exceptions.  

Returns
-------
Returns true if all cameras in the array are open. False is returned if the size
of the array is 0.  
";

%feature("docstring") Pylon::CInstantCameraArray::Close "

Closes all cameras in the array.  

*   If a grab is in progress, it is stopped by calling StopGrabbing().  
*   Close is called for all cameras, see CInstantCamera::Close() for more
    information.  

post: All cameras in the array are closed.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::GetSize "

Returns the size of the array.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::StartGrabbing "

Starts the grabbing of images for all cameras.  

*   StartGrabbing is called for all cameras with the provided parameters, see
    CInstantCamera::StartGrabbing() for more information.  
*   The grabbing is started.  
*   The starting position for retrieving results is set to the first camera.  

Parameters
----------
* `strategy` :  
    The grab strategy, see Pylon::InstantCamera::EStrategy for more information.  
* `grabLoopType` :  
    Indicates using the internal grab thread of the camera.  

pre:  

    *   The size of the array is larger than 0.  
    *   All devices are attached.  
    *   The grabbing is stopped.  
    *   The preconditions for calling StartGrabbing() are met for every camera
        in the array.  

post: The grabbing is started.  

\\error The camera objects may throw an exception. The grabbing is stopped
calling StopGrabbing() in this case.  
";

%feature("docstring") Pylon::CInstantCameraArray::RetrieveResult "

Retrieves a grab result according to the strategy, waits if it is not yet
available.  

*   The content of the passed grab result is released.  
*   If the grabbing is not started, the method returns immediately false.  
*   If GrabStrategy_UpcomingImage strategy: RetrieveResult is called for a
    camera. Cameras are processed using a round-robin strategy.  
*   If GrabStrategy_OneByOne, GrabStrategy_LatestImageOnly or
    GrabStrategy_LatestImages strategy: Pending images or camera events are
    retrieved. Cameras are processed using a round-robin strategy.  
*   If GrabStrategy_OneByOne, GrabStrategy_LatestImageOnly or
    GrabStrategy_LatestImages strategy: Wait for a grab result if it is not yet
    available. Camera events are handled.  
  

The camera array index is assigned to the context value of the instant camera
when Initialize() is called. This context value is attached to the result when
the result is retrieved and can be obtained using the grab result method
GrabResultData::GetCameraContext(). The context value can be used to associate
the result with the camera from where it originated.  

Parameters
----------
* `timeoutMs` :  
    A timeout value in ms for waiting for a grab result, or the INFINITE value.  
* `grabResult` :  
    Receives the grab result.  
* `timeoutHandling` :  
    If timeoutHandling equals TimeoutHandling_ThrowException, a timeout
    exception is thrown on timeout.  

Returns
-------
True if the call successfully retrieved a grab result, false otherwise.  

pre: The preconditions for calling StartGrabbing() are met for every camera in
    the array.  

post:  

    *   If successful, one image is removed from the output queue of a camera
        and is returned in the grabResult parameter.  
    *   If not successful, an empty grab result is returned in the grabResult
        parameter.  

\\error The Instant Camera Array object is still valid after error. The grabbing
is stopped by calling StopGrabbing() if an exception is thrown.  
";

%feature("docstring") Pylon::CInstantCameraArray::StopGrabbing "

Stops the grabbing of images.  

The grabbing is stopped. StopGrabbing is called for all cameras. See
CInstantCamera::StopGrabbing() for more information.  

post: The grabbing is stopped.  

\\error Does not throw C++ exceptions.  

\\threading Can be called while one other thread is polling RetrieveResult() in
a IsGrabbing()/RetrieveResult() loop to stop grabbing.  
";

%feature("docstring") Pylon::CInstantCameraArray::IsGrabbing "

Returns state of grabbing.  

The camera array is grabbing after a successful call to StartGrabbing() until
StopGrabbing() has been called.  

Returns
-------
Returns true if still grabbing.  

\\error Does not throw C++ exceptions.  
";

// File: class_pylon_1_1_c_instant_interface.xml


%feature("docstring") Pylon::CInstantInterface "

Provides convenient access to an interface. An interface is used to represent a
frame grabber board, a network card, etc.  

*   Establishes a single access point for accessing interface functionality.  
*   Handles Pylon interface lifetime.  
*   Handles opening and closing of a Pylon interface automatically.  

note: Currently, this object type is mainly used for the pylon GenTL Consumer
    Transport Layer, e.g., for CoaXPress. All other pylon transport layers
    currently return one default interface.  

C++ includes: InstantInterface.h
";

%feature("docstring") Pylon::CInstantInterface::CInstantInterface "

Constructor. Creates a CInstantInterface object from a CDeviceInfo or
CInterfaceInfo object.  

The following steps are taken:  

*   The DeviceClass property is used to create the transport layer.  
*   If the DeviceClass property is not available, the TlType property is used to
    create the first matching transport layer.  
*   If the DeviceClass and TlType properties are not be available, an error will
    be thrown.  
*   If the provided argument is of CInterfaceInfo type, this is used to create
    the interface.  
*   If the provided argument is of CDeviceInfo type, use the InterfaceID
    property to create the interface.  
*   If the above steps fail, the first interface is created.  

\\error May throw an exception if the passed argument cannot be used to create
an interface object.  
";

%feature("docstring") Pylon::CInstantInterface::~CInstantInterface "

Destructor. All created objects are destroyed correctly.  
";

%feature("docstring") Pylon::CInstantInterface::Open "

Opens the attached Pylon interface.  

This call is neccessary to work with all parameters.  

post:  

    *   The interface is opened.  
    *   The nodemap and parameters are available and accessable.  

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::IsOpen "

Checks if the interface is open.  

note: The 'open' status of an interface instance won't change even if an
    attached camera is used, e.g., opened or closed.  

Returns
-------
Returns true if the interface is open.  

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::Close "

Closes an interface.  

post:  

    *   The interface is closed.  
    *   Any previously acquired objects and references have been deleted and
        must not be used any longer.  

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::GetInterfaceInfo "

Returns the interface info object storing information like the Interface ID
property.  

This information is available at all times regardless of whether the interface
is open or closed.  

Returns
-------
A reference to the interface info object.  

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::GetNodeMap "

Returns the GenApi node map used for accessing parameters provided by the
interface.  

note: The default interface object does not provide a node map.  

note: Interfaces will only provide a nodemap after calling Open().  

Returns
-------
Returns the GenApi node map used for accessing parameters provided by the
interface. If no parameters are available, NULL is returned.  

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::EnumerateDevices "

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::EnumerateDevices "

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::CreateDevice "

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::CreateDevice "

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::CreateDevice "

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::CreateFirstDevice "

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::CreateFirstDevice "

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::DestroyDevice "

\\error May throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantInterface::IsDeviceAccessible "

\\error May throw C++ exceptions.  
";

// File: class_pylon_1_1_c_integer_parameter.xml


%feature("docstring") Pylon::CIntegerParameter "

CIntegerParameter class used to simplify access to GenApi parameters.  

C++ includes: IntegerParameter.h
";

%feature("docstring") Pylon::CIntegerParameter::CIntegerParameter "

Creates an empty CIntegerParameter object. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::CIntegerParameter "

Creates a CIntegerParameter object and attaches it to a node, typically
retrieved for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to attach.  

post:  

    *   If the passed node does not match the parameter type, the parameter will
        be empty, see IsValid().  
    *   If the passed node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::CIntegerParameter "

Creates a CIntegerParameter object and attaches it to a node of a matching type.  

Parameters
----------
* `pInteger` :  
    The node to attach.  

post: The parameter object must not be used to access the node's functionality
    if the source of the attached `pInteger` has been destroyed. In this case,
    call Release() or attach a new node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::CIntegerParameter "

Creates a CIntegerParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::CIntegerParameter "

Creates a CIntegerParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `name` is NULL, the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::CIntegerParameter "

Copies a CIntegerParameter object.  

Parameters
----------
* `rhs` :  
    The object to copy. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::~CIntegerParameter "

Destroys the CIntegerParameter object. Does not access the attached node.
\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `name` is NULL the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::Attach "

Attaches a node, typically retrieved for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::Attach "

Assigns a node of the same type to the parameter object.  

Parameters
----------
* `pInteger` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::Equals "

Returns true if the same nodes are attached or both parameters are empty.  

Parameters
----------
* `rhs` :  
    The object to compare to.  

Returns
-------
Returns true if the same nodes are attached or both parameters are empty.
\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pNode` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pInteger` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::Release "

Releases the attached node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CIntegerParameter::IsValid "
";

%feature("docstring") Pylon::CIntegerParameter::SetValue "
";

%feature("docstring") Pylon::CIntegerParameter::SetValue "
";

%feature("docstring") Pylon::CIntegerParameter::GetValue "
";

%feature("docstring") Pylon::CIntegerParameter::GetMin "
";

%feature("docstring") Pylon::CIntegerParameter::GetMax "
";

%feature("docstring") Pylon::CIntegerParameter::GetIncMode "
";

%feature("docstring") Pylon::CIntegerParameter::GetInc "
";

%feature("docstring") Pylon::CIntegerParameter::GetListOfValidValues "
";

%feature("docstring") Pylon::CIntegerParameter::GetRepresentation "
";

%feature("docstring") Pylon::CIntegerParameter::GetUnit "
";

%feature("docstring") Pylon::CIntegerParameter::ImposeMin "
";

%feature("docstring") Pylon::CIntegerParameter::ImposeMax "
";

%feature("docstring") Pylon::CIntegerParameter::TrySetValue "
";

%feature("docstring") Pylon::CIntegerParameter::TrySetValue "
";

%feature("docstring") Pylon::CIntegerParameter::GetValueOrDefault "
";

%feature("docstring") Pylon::CIntegerParameter::GetValuePercentOfRange "
";

%feature("docstring") Pylon::CIntegerParameter::SetValuePercentOfRange "
";

%feature("docstring") Pylon::CIntegerParameter::TrySetValuePercentOfRange "
";

%feature("docstring") Pylon::CIntegerParameter::SetToMaximum "
";

%feature("docstring") Pylon::CIntegerParameter::SetToMinimum "
";

%feature("docstring") Pylon::CIntegerParameter::TrySetToMaximum "
";

%feature("docstring") Pylon::CIntegerParameter::TrySetToMinimum "
";

// File: class_pylon_1_1_c_interface_info.xml


%feature("docstring") Pylon::CInterfaceInfo "

Class used for storing information about an interface object provided by a
transport layer.  

Enumerating the available Transport Layer Interface objects returns a list of
CInterface objects (Pylon::InterfaceInfoList_t). A CInterfaceInfo object holds
information about the enumerated interface.  

C++ includes: InterfaceInfo.h
";

%feature("docstring") Pylon::CInterfaceInfo::CInterfaceInfo "

Creates an empty interface info. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInterfaceInfo::CInterfaceInfo "

Copy constructor.  
";

%feature("docstring") Pylon::CInterfaceInfo::~CInterfaceInfo "

Destructor.  
";

%feature("docstring") Pylon::CInterfaceInfo::GetInterfaceID "

Retrieves the interface ID identifying the interface. This property is
identified by Key::InterfaceIDKey.  
";

%feature("docstring") Pylon::CInterfaceInfo::SetInterfaceID "

Sets the above property.  
";

%feature("docstring") Pylon::CInterfaceInfo::IsInterfaceIDAvailable "

Returns true if the above property is available.  
";

// File: class_pylon_1_1_c_node_map_proxy_t.xml


%feature("docstring") Pylon::CNodeMapProxyT "

Implementation Detail: This class wraps programming interfaces that are
generated from GenICam parameter description files to provide native parameter
access.  

See also: configuringcameras  

templateparam
-------------
* `TParams` :  
    The specific parameter class (auto generated from the parameter xml file)  

C++ includes: NodeMapProxy.h
";

/*
 Partial implementation of the INodeMap interface 
*/

/*
See GenApi::INodeMap for more details  

*/

/*
 Construction 
*/

/*
 Some smart pointer functionality 
*/

/*
 Assignment and copying is not supported 
*/

%feature("docstring") Pylon::CNodeMapProxyT::GetNodes "
";

%feature("docstring") Pylon::CNodeMapProxyT::GetNode "
";

%feature("docstring") Pylon::CNodeMapProxyT::InvalidateNodes "
";

%feature("docstring") Pylon::CNodeMapProxyT::Poll "
";

%feature("docstring") Pylon::CNodeMapProxyT::CNodeMapProxyT "

Creates a CNodeMapProxyT object that is not attached to a node map. Use the
Attach() method to attach the pylon node map.  
";

%feature("docstring") Pylon::CNodeMapProxyT::CNodeMapProxyT "

Creates a CNodeMapProxyT object and attaches it to a pylon node map.  
";

%feature("docstring") Pylon::CNodeMapProxyT::~CNodeMapProxyT "

Destructor.  
";

%feature("docstring") Pylon::CNodeMapProxyT::Attach "

Attach a pylon node map.  
";

%feature("docstring") Pylon::CNodeMapProxyT::IsAttached "

Checks if a pylon node map is attached.  
";

%feature("docstring") Pylon::CNodeMapProxyT::GetNodeMap "

Returns the pylon node map interface pointer.  
";

// File: struct_pylon_1_1_compression_info__t.xml


%feature("docstring") Pylon::CompressionInfo_t "

The struct containing information about a grab buffer/result.  

      You can find more information about the usage of this struct in the
description of
      the CImageDecompressor class.
  

C++ includes: ImageDecompressor.h
";

%feature("docstring") Pylon::CompressionInfo_t::CompressionInfo_t "

Creates and initializes a compression info struct. \\error Does not throw C++
exceptions.  
";

// File: class_pylon_1_1_t_list_1_1const__iterator.xml


%feature("docstring") Pylon::TList::const_iterator "
";

%feature("docstring") Pylon::TList::const_iterator::const_iterator "
";

// File: class_pylon_1_1_c_parameter.xml


%feature("docstring") Pylon::CParameter "

CParameter class used to simplify access to GenApi parameters.  

C++ includes: Parameter.h
";

%feature("docstring") Pylon::CParameter::CParameter "

Creates an empty CParameter object. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CParameter::CParameter "

Creates a CParameter object and attaches it to a node, typically retrieved for a
nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to attach.  

post:  

    *   If the passed node does not match the parameter type, the parameter will
        be empty, see IsValid().  
    *   If the passed node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CParameter::CParameter "

Creates a CParameter object and attaches it to a node of a matching type.  

Parameters
----------
* `pValue` :  
    The node to attach.  

post: The parameter object must not be used to access the node's functionality
    if the source of the attached `pValue` has been destroyed. In this case,
    call Release() or attach a new node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CParameter::CParameter "

Creates a CParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CParameter::CParameter "

Creates a CParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `name` is NULL, the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CParameter::CParameter "

Copies a CParameter object.  

Parameters
----------
* `rhs` :  
    The object to copy. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CParameter::~CParameter "

Destroys the CParameter object. Does not access the attached node. \\error Does
not throw C++ exceptions.  
";

%feature("docstring") Pylon::CParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `name` is NULL the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CParameter::Attach "

Attaches a node, typically retrieved for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CParameter::Attach "

Assigns a node of the same type to the parameter object.  

Parameters
----------
* `pValue` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CParameter::Equals "

Returns true if the same nodes are attached or both parameters are empty.  

Parameters
----------
* `rhs` :  
    The object to compare to.  

Returns
-------
Returns true if the same nodes are attached or both parameters are empty.
\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pNode` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pValue` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CParameter::Release "

Releases the attached node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CParameter::GetAccessMode "
";

%feature("docstring") Pylon::CParameter::GetNode "
";

%feature("docstring") Pylon::CParameter::ToString "
";

%feature("docstring") Pylon::CParameter::FromString "
";

%feature("docstring") Pylon::CParameter::IsValueCacheValid "
";

%feature("docstring") Pylon::CParameter::IsReadable "
";

%feature("docstring") Pylon::CParameter::IsWritable "
";

%feature("docstring") Pylon::CParameter::IsValid "
";

%feature("docstring") Pylon::CParameter::GetInfo "
";

%feature("docstring") Pylon::CParameter::GetInfoOrDefault "
";

%feature("docstring") Pylon::CParameter::ToStringOrDefault "
";

// File: class_pylon_1_1_c_pixel_type_mapper.xml


%feature("docstring") Pylon::CPixelTypeMapper "

A simple pixeltypemapper (maps device specific pixelformats read from device-
node map to pylon pixeltypes by their name).  

Use this mapper to convert a device specifc Pylon::PixelFormat value to a
Pylon::EPixelType used for PixelFormatConverters. When passing the symbolic name
of the pixeltype you can use the static function
CPixelTypeMapper::GetPylonPixelTypeByName(). If you want to convert a nodeValue
you must first create a CPixelTypeMapper instance and pass the constructor a
pointer the PixelFormat node of the device you want the node value to be
converted. Then call CPixelTypeMapper::GetPylonPixelTypeFromNodeValue() to get
the corresponding Pylon::EPixelType.  

C++ includes: PixelTypeMapper.h
";

%feature("docstring") Pylon::CPixelTypeMapper::CPixelTypeMapper "

Create an empty mapper. Before calling any non-static function you must call
SetPixelFormatEnumNode to initialize the mapper.  
";

%feature("docstring") Pylon::CPixelTypeMapper::CPixelTypeMapper "

create and initialize a mapper by using the enum node passed.  
";

%feature("docstring") Pylon::CPixelTypeMapper::~CPixelTypeMapper "

default d'tor  
";

%feature("docstring") Pylon::CPixelTypeMapper::IsValid "

Checks the objects validity.  

Returns
-------
Returns true if the object is initialized properly.  

Essentially this function checks whether you've called SetPixelFormatEnumNode.  
";

%feature("docstring") Pylon::CPixelTypeMapper::SetPixelFormatEnumNode "

Lazy initialization of the object.  

Parameters
----------
* `pEnum` :  
    Pointer to the enumeration node containing the PixelFormats.  

Call this function initialize the mapper when using the default c'tor.  
";

%feature("docstring") Pylon::CPixelTypeMapper::GetPylonPixelTypeFromNodeValue "

Converts an enumeration node value to a Pylon::EPixelType enum.  

Parameters
----------
* `nodeValue` :  
    node value to convert. You can obtain this value by calling
    GenApi::IEnumeration::GetIntValue.  

Returns
-------
Returns the Pylon::EPixelType for a given pixelformat enum value defined in the
Enum passed in c'tor  

Converts a enumeration node value to a Pylon::EPixelType enum. You must have
initialized the mapper before you can call this function.  
";

%feature("docstring") Pylon::CPixelTypeMapper::GetPylonPixelTypeByName "

Returns a Pylon::EPixelType for a given symbolic name.  

Parameters
----------
* `pszSymbolicName` :  
    pointer to the symbolic name. Note: Symbolic names are case sensitive. You
    can obtain the symbolic name by calling GenApi::IEnumEntry::GetSymbolic()  

Returns
-------
Returns the Pylon_PixelType for a given symbolic name.  

Static version which does the lookup soley by symbolic string comparison.
Passing \"Mono16\" will return Pylon::PixelType_Mono16. If the name is not found
Pylon::PixelType_Undefined will be returned.  
";

%feature("docstring") Pylon::CPixelTypeMapper::GetPylonPixelTypeByName "

Returns a Pylon::EPixelType for a given symbolic name.  

Parameters
----------
* `symbolicName` :  
    The symbolic name. Note: Symbolic names are case sensitive. You can obtain
    the symbolic name by calling GenApi::IEnumEntry::GetSymbolic()  

Returns
-------
Returns the Pylon_PixelType for a given symbolic name.  

Static version which does the lookup solely by symbolic string comparison.
Passing \"Mono16\" will return Pylon::PixelType_Mono16. If the name is not found
Pylon::PixelType_Undefined will be returned.  
";

%feature("docstring") Pylon::CPixelTypeMapper::GetNameByPixelType "

Static function that returns a string representation of the given EPixelType.  

Parameters
----------
* `pixelType` :  
    The pixel type to return the name for.  
* `sfncVer` :  
    SFNC Version to use when doing the mapping. Some names have been changed in
    SFNC 2.0  

Returns
-------
Returns the pointer to a null terminated string representing the symbolic name
of the pixel type.  

Passing Pylon::PixelType_Mono16 will return \"Mono16\" will be returned. If the
pixel type is not known an empty string is returned.  

note: The returned name cannot be used to parameterize the pixel format of a
    camera device, because the camera's pixel format name can be different. The
    camera's pixel format name depends on the used standard feature naming
    convention (SFNC).  
";

// File: class_pylon_1_1_c_pylon_bitmap_image.xml


%feature("docstring") Pylon::CPylonBitmapImage "

This class can be used to easily create Windows bitmaps for displaying images.  

*   Automatically handles the bitmap creation and lifetime.  
*   Provides methods for loading and saving an image in different file formats.  
*   Serves as target format for the `CImageFormatConverter` image format
    converter.  

par: Buffer Handling:
    The bitmap buffer that is automatically created by the CPylonBitmapImage
    class. The Release() method can be used to release a bitmap.  

\\threading The CPylonBitmapImage class is not thread-safe.  

C++ includes: PylonBitmapImage.h
";

%feature("docstring") Pylon::CPylonBitmapImage::CPylonBitmapImage "

Creates an invalid image.  

See Pylon::IImage on how the properties of an invalid image are returned.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonBitmapImage::CPylonBitmapImage "

Copies the image properties and creates a reference to the bitmap of the source
image.  

Parameters
----------
* `source` :  
    The source image.  

post:  

    *   Another reference to the source bitmap is created.  
    *   Creates an invalid image if the source image is invalid.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonBitmapImage::~CPylonBitmapImage "

Destroys a pylon image object.  

attention: The bitmap handle must not be currently selected into a DC. Otherwise
    the bitmap is not freed.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonBitmapImage::CopyImage "

Copies the image data from a different image.  

The input image is automatically converted if needed to PixelType_Mono8 if
Pylon::IsMonoImage( pixelTypeSource) is true, otherwise it is converted to
PixelType_BGR8packed. The orientation of the image is changed to bottom up.  

If more control over the conversion is required, the CImageFormatConverter class
can be used to convert other images with a CPylonBitmapImage object as target.  

Parameters
----------
* `image` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

pre: The preconditions of the Reset() method must be met.  

post:  

    *   The source image is automatically converted.  
    *   Creates an invalid image if the source image is invalid.  

\\error Throws an exception when the bitmap could not be created. Throws an
exception when the preconditions of the Reset() method are not met.  
";

%feature("docstring") Pylon::CPylonBitmapImage::CopyImage "

Sets an image from a user buffer.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the source image.  
* `bufferSizeBytes` :  
    The size of the buffer of the source image.  
* `pixelType` :  
    The pixel type of the source image.  
* `width` :  
    The number of pixels in a row in the source image.  
* `height` :  
    The number of rows in the source image.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The pixel type must be valid.  
    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  
    *   The pointer to the source buffer must not be NULL.  
    *   The source buffer must be large enough to hold the image described by
        the parameters.  
    *   The preconditions of the Reset() method must be met.  

post: The source image is automatically converted. See CopyImage().  

\\error Throws an exception when when the bitmap could not be created. Throws an
exception when the preconditions of the Reset() method are not met.  
";

%feature("docstring") Pylon::CPylonBitmapImage::IsValid "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetPixelType "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetWidth "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetHeight "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetPaddingX "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetOrientation "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetBuffer "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetBuffer "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetImageSize "
";

%feature("docstring") Pylon::CPylonBitmapImage::IsUnique "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetStride "
";

%feature("docstring") Pylon::CPylonBitmapImage::IsSupportedPixelType "
";

%feature("docstring") Pylon::CPylonBitmapImage::IsAdditionalPaddingSupported "
";

%feature("docstring") Pylon::CPylonBitmapImage::Reset "

Resets the image properties and creates a new Windows bitmap if required.  

Parameters
----------
* `pixelType` :  
    The pixel type of the new image.  
* `width` :  
    The number of pixels in a row in the new image.  
* `height` :  
    The number of rows in the new image.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The `width` value must be > 0 and < _I32_MAX.  
    *   The `height` value must be > 0 and < _I32_MAX.  

post:  

    *   If the previously referenced bitmap is also referenced by another pylon
        bitmap image, a new Windows bitmap is created.  
    *   If the previously referenced bitmap is able to hold an image with the
        given properties, a new Windows bitmap is created.  
    *   If no bitmap has been created before, a new Windows bitmap is created.  

\\error Throws an exception when the preconditions are not met. Throws an
exception when no buffer with the required size could be allocated.  
";

%feature("docstring") Pylon::CPylonBitmapImage::Release "
";

%feature("docstring") Pylon::CPylonBitmapImage::Detach "

Detach the windows bitmap.  

Returns
-------
Returns the handle of the windows bitmap or NULL if the image is invalid.  

pre: IsUnique() must return true. No other image must reference the bitmap.  

post:  

    *   The image is invalid.  
    *   The ownership of the bitmap goes to the caller who is responsible for
        deleting it.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonBitmapImage::Create "

Creates an image and a Windows bitmap for it.  

Parameters
----------
* `pixelType` :  
    The pixel type of the new image.  
* `width` :  
    The number of pixels in a row in the new image.  
* `height` :  
    The number of rows in the new image.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The pixel type must be supported, see IsSupportedPixelType().  
    *   The `width` value must be > 0 and < _I32_MAX.  
    *   The `height` value must be > 0 and < _I32_MAX.  

\\error Throws an exception when the parameters are invalid. Throws an exception
when the bitmap could not be created.  
";

// File: class_pylon_1_1_c_pylon_data_component.xml


%feature("docstring") Pylon::CPylonDataComponent "

Provides methods for accessing a single component of CPylonDataContainer.  

Some cameras can return complex grab results consisting of multiple components.
For example, Basler blaze cameras return a data stream that is composed of
range, intensity, and confidence components. To access the individual
components, you can use the `CPylonDataContainer` class.  

A `CPylonDataContainer` can hold one or more components. You can obtain a
container by calling `Pylon::CGrabResultData::GetDataContainer()`. You can then
use the container to query for the number of components by calling
`Pylon::CGrabResultData::GetDataComponentCount()`. To retrieve a specific
component, you can call `Pylon::CGrabResultData::GetDataComponent()`. Each
component in the container can be used to access the actual data, e.g., the
range values, and its metadata.  

attention: Any `CPylonDataContainer` or `CPylonDataComponent` will hold a
    reference to the `CGrabResultData` from which it has been created. To allow
    the instant camera to reuse the `CGrabResultData` and prevent buffer
    underruns, you must destroy the `CPylonDataContainer` and all its
    `CPylonDataComponent` objects.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  

C++ includes: PylonDataComponent.h
";

%feature("docstring") Pylon::CPylonDataComponent::CPylonDataComponent "

Creates an empty component.  

The default constructor will create an empty component.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::CPylonDataComponent "

Creates a copy of an existing component.  

Parameters
----------
* `rhs` :  
    Source component to copy.  

When creating a copy of a component, only the reference to the data in the
container is copied. The actual data pointed to by
Pylon::CPylonDataComponent::GetData() will not be copied.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::~CPylonDataComponent "

Destroys a pylon data component object.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::IsValid "

Can be used to check whether the component is valid.  

Returns
-------
Returns false if the component does not contain valid data or hasn't been
initialized yet.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetComponentType "

Get the type of data this component contains.  

Returns
-------
Returns the type of data in this component. See `Pylon::EComponentType` for
values.  

Use this function to distinguish between different component types like
intensity values or range values. See Pylon::EComponentType for values.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetComponentIndex "

Get the index of this component in the container.  

Returns
-------
Returns the index this component or 0 if the container is empty or invalid.  

Some Container query methods return single or lists of components. The index of
a component can be used to determine which component it is in the container.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetPixelType "

Get the type of pixels this component contains.  

Returns
-------
Returns an enumeration value describing the pixels in the component. See
`Pylon::EPixelType` for values. If the component does not contain valid data or
contains a unknown pixel format, `PixelType_Unknown` is returned.  

Use this function to determine how to interpret the data returned by
`Pylon::CPylonDataComponent::GetData()`.  

note: Not all components contain pixel data. Only components of type
    ComponentType_Intensity, ComponentType_Range, and ComponentType_Confidence
    return a valid pixel type.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetWidth "

Get the current number of columns.  

Returns
-------
Returns the current number of columns or 0 if the component is invalid.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetHeight "

Get the current number of rows.  

Returns
-------
Returns the current number of rows or 0 if the component is invalid.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetOffsetX "

Get the starting column.  

Returns
-------
Returns the starting column.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetOffsetY "

Get the starting row.  

Returns
-------
Returns the starting row.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetPaddingX "

Get the number of extra bytes at the end of each row.  

Returns
-------
Returns the number of extra bytes at the end of each row.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetPaddingY "

Get the number of extra data at the end of the image data in bytes.  

Returns
-------
Returns the number of extra data at the end of the image data in bytes.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetData "

Get the pointer to the data contained in the component.  

Returns
-------
Returns a pointer to the data contained in the component.  

Use this pointer to access the data in this component. The size in bytes of the
buffer can be obtained by calling Pylon::CPylonDataComponent::GetDataSize().
Call Pylon::CPylonDataComponent::GetPixelFormat() and other methods to determine
how to interpret the data.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetDataSize "

Get the size of the buffer returned by Pylon::CPylonDataComponent::GetData().  

Returns
-------
Returns the size in bytes of the buffer returned by
Pylon::CPylonDataComponent::GetData().  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetTimeStamp "

Get the camera-specific time the data was created on the camera.  

Returns
-------
Returns the camera-specific time the data was created on the camera or 0 if the
time is not available.  

note: Timestamp generation is available only on some camera models.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetStride "

Get the stride in bytes for the component.  

Parameters
----------
* `strideBytes` :  
    On successful return, the stride value can be read from this output
    parameter.  

Returns
-------
Returns true if the stride could be computed successfully and is returned in the
output parameter. Returns false if the preconditions are not met or the
component doesn't contain valid data. If the function returns false, the value
of strideBytes is undefined.  

This method uses `Pylon::ComputeStride()` to compute the component's stride
value. The stride describes the amount of bytes to advance from one row to the
next.  

pre:  

    *   The component type must be Pylon::ComponentType_Intensity,
        Pylon::ComponentType_Range, or Pylon::ComponentType_Confidence.  
    *   The preconditions of `ComputeStride()` must be met.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataComponent::GetSourceId "

Returns the identifier of the data source that generated this component.  

Example when source IDs are useful: If a device has two sensors each sensor can
be a source with its own identifier.  

Returns
-------
The unique identifier of the data source that generated this component. If the
device does not provide source IDs, 0 is returned.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must ensure access is properly synchronized.  
";

// File: class_pylon_1_1_c_pylon_data_container.xml


%feature("docstring") Pylon::CPylonDataContainer "

Provides methods for accessing grab results consisting of multiple components.  

Some cameras can return complex grab results consisting of multiple components.
For example, Basler blaze cameras return a data stream that is composed of
range, intensity, and confidence components. To access the individual
components, you can use the `CPylonDataContainer` class.  

A `CPylonDataContainer` can hold one or more components. You can obtain a
container by calling `Pylon::CGrabResultData::GetDataContainer()`. You can then
use the container to query for the number of components by calling
`Pylon::CGrabResultData::GetDataComponentCount()`. To retrieve a specific
component, you can call `Pylon::CGrabResultData::GetDataComponent()`. Each
component in the container can be used to access the actual data, e.g., the
range values, and its metadata.  

attention: Any `CPylonDataContainer` or `CPylonDataComponent` will hold a
    reference to the `CGrabResultData` from which it has been created. To allow
    the instant camera to reuse the `CGrabResultData` and prevent buffer
    underruns, you must destroy the `CPylonDataContainer` and all its
    `CPylonDataComponent` objects.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  

C++ includes: PylonDataContainer.h
";

%feature("docstring") Pylon::CPylonDataContainer::CPylonDataContainer "

Creates a `CPylonDataContainer` from a given `CGrabResultPtr`.  

Parameters
----------
* `ptrGrabResult` :  
    The grab result to create a container from.  

Creates a `CPylonDataContainer` from a given `CGrabResultPtr`. The
`CPylonDataContainer` instance created will hold a reference to the
`CGrabResultData` from which it has been created. To allow the instant camera to
reuse the grab result and prevent buffer underruns, you must destroy the
`CPylonDataContainer`.  

post:  

    *   A new reference to the grab result passed in ptrGrabResult has been set.  

\\error Does not throw an exception if the `CGrabResultPtr` was invalid or
points to an invalid/unsuccessful result. Instead, an empty container is
returned. Can throw exceptions if the data in the result is invalid or
malformed. Can throw exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataContainer::CPylonDataContainer "

Creates a `CPylonDataContainer` from a given `GrabResult`.  

Parameters
----------
* `grabResult` :  
    The grab result to create a container from.  

Creates a `CPylonDataContainer` from a given `GrabResult`. The
`CPylonDataContainer` instance created is only valid as long as the associated
buffer is not queued or deregistered and deleted.  

\\error Does not throw an exception if the GrabResult contains an unsuccessful
result. Instead, an empty container is returned. Can throw exceptions if the
data in the buffer of the GrabResult is invalid or malformed. Can throw
exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataContainer::CPylonDataContainer "

Creates a `CPylonDataContainer` by loading the data from the file passed.  

Parameters
----------
* `filename` :  
    Name and path of the file to load.  

Loads a container and all its components from a file on disk.  

post:  

    *   The reference to a previous grab result or buffer has been released.  
    *   A new buffer has been allocated to hold the data loaded.  

\\error Throws an exception if the container cannot be read. Throws an exception
if the contents of the file does not contain a valid container.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataContainer::CPylonDataContainer "

Creates an empty `CPylonDataContainer`.  

Creates an empty `CPylonDataContainer`. The `CPylonDataContainer` instance
created will not be valid.  

\\error Can throw exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataContainer::CPylonDataContainer "

Creates a shallow copy of an existing `CPylonDataContainer`.  

Parameters
----------
* `rhs` :  
    Container to copy from.  

post:  

    *   A new reference to the grab result or buffer of the container passed in
        rhs has been set.  

\\error Can throw exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataContainer::~CPylonDataContainer "

Destroys the `CPylonDataContainer` instance. If the instance has been created
through a GrabResultPtr, the reference to that `CGrabResultData` will be
released.  

post:  

    *   The reference to a grab result or buffer has been released.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataContainer::GetDataComponentCount "

Returns the number of components contained in the container.  

Returns
-------
Returns the number of components contained in the container.  

You can use the return value to iterate over the existing components by calling
`Pylon::CPylonDataContainer::GetDataComponent()`.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataContainer::GetDataComponent "

Returns a specific component from the container.  

Parameters
----------
* `index` :  
    Index of the component to return. The index must be less than the value
    returned by `Pylon::CPylonDataContainer::GetComponentCount()`.  

Returns
-------
Returns the component specified by the index parameter.  

\\error Throws an exception if the index parameter is out of range. Can throw
exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataContainer::GetDataComponent "

Returns a list of components of the specified type from the container.  

Parameters
----------
* `type` :  
    Type of the components to return.  

Returns
-------
A list of components matching the specified type.  

\\error Can throw exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataContainer::GetFirstImageDataComponent "

Returns the first found image data component.  

Parameters
----------
* `throwIfNotFound` :  
    If true an exception is thrown if no matching component is found. If false,
    an empty component is returned in this case.  

Returns
-------
Returns the component found by
GetFirstImageDataComponent(ComponentType_Intensity, 0, false) if a component is
found. Falls back to delivering any 2D uncompressed image data component found
first in the container otherwise.  

\\error Throws an exception if not matching image is found and throwIfNotFound
is true. Can throw exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataContainer::GetFirstImageDataComponent "

Returns the first found image data component.  

Parameters
----------
* `type` :  
    The type of the component to find.  
* `sourceId` :  
    The source of the component to find.  
* `throwIfNotFound` :  
    If true an exception is thrown if no matching component is found. If false,
    an empty component is returned in this case.  

Returns
-------
Returns the component specified by the type and sourceId parameters.  

\\error Throws an exception if not matching image is found and throwIfNotFound
is true. Can throw exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataContainer::Save "

Saves the container to disk.  

Parameters
----------
* `filename` :  
    Name and path of the file to save the container to.  

pre: The container must contain at least one component.  

\\error Throws an exception if the container cannot be saved.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::CPylonDataContainer::Load "

Loads a container from a file.  

Parameters
----------
* `filename` :  
    Name and path of the file to load.  

Loads a container and all its components from a file on disk.  

post:  

    *   The reference to a previous grab result or buffer has been released.  
    *   A new buffer has been allocated to hold the data loaded.  

\\error Throws an exception if the container cannot be read. Throws an exception
if the contents of the file does not contain a valid container.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

// File: class_pylon_1_1_c_pylon_device_proxy_t.xml


%feature("docstring") Pylon::CPylonDeviceProxyT "

Low Level API: The camera class for generic camera devices.  

This is the base class for pylon camera classes providing access to camera
parameters.  

See also: configuringcameras  

templateparam
-------------
* `TCameraParams` :  
    The camera specific parameter class (auto generated from camera xml file)  

C++ includes: PylonDeviceProxy.h
";

/*
 Implementation of the IPylonDevice interface. 
*/

/*
See Pylon::IPylonDevice for more details.  

*/

/*
 Construction 
*/

/*
 Some smart pointer functionality 
*/

/*
 Assignment and copying is not supported 
*/

%feature("docstring") Pylon::CPylonDeviceProxyT::Open "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::Close "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::IsOpen "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::AccessMode "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetDeviceInfo "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetNumStreamGrabberChannels "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetStreamGrabber "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetEventGrabber "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetNodeMap "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetTLNodeMap "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::CreateChunkParser "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::DestroyChunkParser "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::CreateEventAdapter "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::DestroyEventAdapter "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::CreateSelfReliantChunkParser "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::DestroySelfReliantChunkParser "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::RegisterRemovalCallback "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::DeregisterRemovalCallback "
";

%feature("docstring") Pylon::CPylonDeviceProxyT::CPylonDeviceProxyT "

Creates a camera object that is not attached to an pylon device. Use the
Attach() method to attach the device.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::CPylonDeviceProxyT "

Creates a camera object and attaches a camera object to a pylon device that
takes the ownership over an pylon device.  

When having the ownership, the destructor of this camera object destroys the
pylon device the camera object is attached to. Otherwise, the pylon device
object remains valid when the camera object has been destroyed.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::~CPylonDeviceProxyT "

Destructor.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::Attach "

Attach the camera object to a pylon device.  

It is not allowed to call Attach when the camera object is already attached!  

When having the ownership, the destructor of this camera object destroys the
pylon device the camera object is attached to. Otherwise, the pylon device
object remains valid when the camera object has been destroyed.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::IsAttached "

Checks if a pylon device is attached to the camera object.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::HasOwnership "

Checks if the camera object has the ownership of the pylon device.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetDevice "

Returns the pylon device interface pointer.  
";

// File: class_pylon_1_1_c_pylon_image.xml


%feature("docstring") Pylon::CPylonImage "

Describes an image.  

*   Automatically handles size and lifetime of the image buffer.  
*   Allows to take over a buffer of grab result which is preventing its reuse as
    long as required.  
*   Allows to connect user buffers or buffers provided by third party software
    packages.  
*   Provides methods for loading and saving an image in different file formats.  
*   Serves as the main target format for the image format converter
    `CImageFormatConverter`.  
*   Eases working with planar images.  
*   Eases extraction of AOIs, e.g. for thumbnail images of defects.  

par: Buffer Handling:
    The buffer that is automatically created by the CPylonImage class or a
    hosted grab result buffer are replaced by a larger buffer if required. The
    size of the allocated buffer is never decreased. Referenced user buffers are
    never automatically replaced by a larger buffer. Referenced grab result
    buffers are never reused. See the Reset() method for more details. The
    Release() method can be used to detach a user buffer, release a hosted grab
    result buffer or to free an allocated buffer.  

\\threading The CPylonImage class is not thread-safe.  

C++ includes: PylonImage.h
";

%feature("docstring") Pylon::CPylonImage::CPylonImage "

Creates an invalid image.  

See Pylon::IImage on how the properties of an invalid image are returned.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonImage::CPylonImage "

Copies the image properties and creates a reference to the buffer of the source
image.  

Parameters
----------
* `source` :  
    The source image.  

post:  

    *   Another reference to the source image buffer is created.  
    *   Creates an invalid image if the source image is invalid.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonImage::~CPylonImage "

Destroys a pylon image object.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonImage::CopyImage "

Copies the image data from a different image.  

This method is used for making a full copy of an image. Calls the Reset() method
to set the same image properties as the source image and copies the image data.  

Parameters
----------
* `image` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

pre: The preconditions of the Reset() method must be met.  

post:  

    *   The image contains a copy of the image data contained by the source
        image.  
    *   Creates an invalid image if the source image is invalid.  

\\error Throws an exception when no buffer with the required size could be
allocated. Throws an exception when the preconditions of the Reset() method are
not met.  
";

%feature("docstring") Pylon::CPylonImage::CopyImage "

Copies the image data from a different image and changes the padding while
copying.  

This method is used for making a full copy of an image except for changing the
padding. Calls the Reset() method to set the same image properties as the source
image and copies the image data. This method is useful in combination with the
GetAoi() method.  

Parameters
----------
* `image` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  
* `newPaddingX` :  
    The number of extra data bytes at the end of each row.  

pre:  

    *   The preconditions of the Reset() method must be met.  
    *   The rows of the source image must be byte aligned. This may not be the
        case for packed pixel types. See Pylon::IsPacked().  
    *   The rows of the newly created image must be byte aligned. This may not
        be the case for packed pixel types. See Pylon::IsPacked().  

post:  

    *   The image contains a copy of the image data contained by the source
        image.  
    *   The line padding is adjusted.  
    *   The byte aligned row padding area is set to zero.  
    *   Creates an invalid image if the source image is invalid.  

\\error Throws an exception when no buffer with the required size could be
allocated. Throws an exception when the preconditions of the Reset() method are
not met.  
";

%feature("docstring") Pylon::CPylonImage::CopyImage "

Copies the image data from a provided buffer.  

This method is used for making a full copy of an image. Calls the Reset() method
to set the same image properties as the source image and copies the image data.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the source image.  
* `bufferSizeBytes` :  
    The size of the buffer of the source image.  
* `pixelType` :  
    The pixel type of the source image.  
* `width` :  
    The number of pixels in a row in the source image.  
* `height` :  
    The number of rows in the source image.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The pixel type must be valid.  
    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  
    *   The pointer to the source buffer must not be NULL.  
    *   The source buffer must be large enough to hold the image described by
        the parameters.  
    *   The preconditions of the Reset() method must be met.  

post: A copy of the image contained by the source image buffer is made.  

\\error Throws an exception when no buffer with the required size could be
allocated. Throws an exception when the preconditions of the Reset() method are
not met.  
";

%feature("docstring") Pylon::CPylonImage::AttachGrabResultBufferWithUserHints "

Attaches a grab result buffer using additional hints.  

This allows to display grabbed data in a user-defined way. This method does not
handle GenDC containers.  

Parameters
----------
* `grabResult` :  
    The source buffer.  
* `pixelType` :  
    The pixel type of the source image.  
* `width` :  
    The number of pixels in a row in the source image.  
* `height` :  
    The number of rows in the source image.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The `grabResult` must be valid.  
    *   The `pixelType` must be valid.  
    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  

post:  

    *   The image properties are taken from the `width`, `height`, `pixelType`,
        `paddingX` and `orientation` parameters.  
    *   The grab result buffer is used by the image class.  
    *   Another reference to the grab result buffer is created. This prevents
        the buffer's reuse for grabbing.  

\\error Throws an exception if the preconditions are not met. Throws an
exception if the buffer size of the grabresult is too small for an image with
the given parameters.  
";

%feature("docstring") Pylon::CPylonImage::AttachGrabResultBuffer "

Attaches a grab result buffer.  

Parameters
----------
* `grabResult` :  
    The source image represented by a grab result.  

post:  

    *   The image properties are taken from the grab result if the grab result
        does not contain a GenDC container.  
    *   The image properties are taken from the component returned by
        grabResult->GetFirstImageDataComponent(false) for GenDC containers.  
    *   The grab result buffer is used by the image class.  
    *   Another reference to the grab result buffer is created. This prevents
        the buffer's reuse for grabbing.  
    *   Creates an invalid image if the `grabResult` is invalid.  
    *   Creates an invalid image if the `grabResult` contains a GenDC container
        and grabResult->GetFirstImageDataComponent(false) returns an invalid
        component.  
    *   Creates an invalid image if the grab was not successful. See
        CGrabResultData::GrabSucceeded().  

\\error Throws an exception when no buffer with the required size could be
allocated. Throws an exception when the preconditions of the Reset() method are
not met.  
";

%feature("docstring") Pylon::CPylonImage::AttachGrabResultBuffer "

Attaches a grab result buffer.  

Parameters
----------
* `componentIndex` :  
    The index of the component to attach.  
* `grabResult` :  
    The source image represented by a grab result component at `componentIndex`.  

post:  

    *   The image properties are taken from the component identified by
        `componentIndex`.  
    *   The grab result buffer is used by the image class.  
    *   Another reference to the grab result buffer is created. This prevents
        the buffer's reuse for grabbing.  
    *   Creates an invalid image if the `grabResult` is invalid.  
    *   Creates an invalid image if the grab was not successful. See
        CGrabResultData::GrabSucceeded().  

\\error Throws an exception if the component at `componentIndex` is not an image
component. Throws an exception if the component at `componentIndex` does not
exist. Throws an exception when no buffer with the required size could be
allocated. Throws an exception when the preconditions of the Reset() method are
not met.  
";

%feature("docstring") Pylon::CPylonImage::AttachUserBuffer "

Attaches a user buffer.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the source image. CPylonImage will never free
    any user buffers.  
* `bufferSizeBytes` :  
    The size of the buffer of the source image.  
* `pixelType` :  
    The pixel type of the source image.  
* `width` :  
    The number of pixels in a row in the source image.  
* `height` :  
    The number of rows in the source image.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  
* `pEventHandler` :  
    A pointer to an optional CPylonImageUserBufferEventHandler-derived object
    called when the user-supplied buffer is not used anymore. You can use this
    to free the user-supplied buffer. In case the function throws an exception,
    the handler will not be called.  

When attaching a user buffer and passing a pEventHandler, the user is
responsible for ensuring the object is valid until
CPylonImageUserBufferEventHandler::OnPylonImageUserBufferDetached() has been
called. The user is also responsible to free the handler object after
CPylonImageUserBufferEventHandler::OnPylonImageUserBufferDetached() has been
called. After the function has returned, CPylonImage won't access the object
anymore. See
`CPylonImageUserBufferEventHandler::OnPylonImageUserBufferDetached()` for a
sample.  

pre:  

    *   The pixel type must be valid.  
    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  
    *   The pointer to the source buffer must not be NULL.  
    *   The source buffer must be large enough to hold the image described by
        the parameters.  
    *   The buffer passed in `pBuffer` must not be currently attached.  

post:  

    *   The image properties are taken from the parameters passed.  
    *   The user buffer is used by the image class.  
    *   The user buffer must not be freed while being attached.  

\\error Throws an exception if the preconditions are not met. In this case the
an optional handler passed in \\ pEventHandler will not be called.  
";

%feature("docstring") Pylon::CPylonImage::IsValid "
";

%feature("docstring") Pylon::CPylonImage::GetPixelType "
";

%feature("docstring") Pylon::CPylonImage::GetWidth "
";

%feature("docstring") Pylon::CPylonImage::GetHeight "
";

%feature("docstring") Pylon::CPylonImage::GetPaddingX "
";

%feature("docstring") Pylon::CPylonImage::GetOrientation "
";

%feature("docstring") Pylon::CPylonImage::GetBuffer "
";

%feature("docstring") Pylon::CPylonImage::GetBuffer "
";

%feature("docstring") Pylon::CPylonImage::GetImageSize "
";

%feature("docstring") Pylon::CPylonImage::IsUnique "
";

%feature("docstring") Pylon::CPylonImage::GetStride "
";

%feature("docstring") Pylon::CPylonImage::IsSupportedPixelType "
";

%feature("docstring") Pylon::CPylonImage::IsAdditionalPaddingSupported "
";

%feature("docstring") Pylon::CPylonImage::Reset "

Resets the image properties and allocates a new buffer if required.  

Parameters
----------
* `pixelType` :  
    The pixel type of the new image.  
* `width` :  
    The number of pixels in a row in the new image.  
* `height` :  
    The number of rows in the new image.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  
    *   If a user buffer is referenced then this buffer must not be referenced
        by another pylon image. See the IsUnique() and IsUserBufferAttached()
        methods.  
    *   If a user buffer is referenced then this buffer must be large enough to
        hold the destination image. See the GetAllocatedBufferSize() and
        IsUserBufferAttached() methods.  

post:  

    *   If the previously referenced buffer is a grab result buffer, a new
        buffer has been allocated.  
    *   If the previously referenced buffer is also referenced by another pylon
        image, a new buffer has been allocated.  
    *   If the previously referenced buffer is not large enough to hold an image
        with the given properties, a new buffer has been allocated.  
    *   If no buffer has been allocated before, a buffer has been allocated.  

\\error Throws an exception when the preconditions are not met. Throws an
exception when no buffer with the required size could be allocated.  
";

%feature("docstring") Pylon::CPylonImage::Reset "

Extends the Reset( EPixelType, uint32_t, uint32_t, EImageOrientation) method by
settable paddingX.  

Parameters
----------
* `pixelType` :  
    The pixel type of the new image.  
* `width` :  
    The number of pixels in a row in the new image.  
* `height` :  
    The number of rows in the new image.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  
    *   If a user buffer is referenced then this buffer must not be referenced
        by another pylon image. See the IsUnique() and IsUserBufferAttached()
        methods.  
    *   If a user buffer is referenced then this buffer must be large enough to
        hold the destination image. See the GetAllocatedBufferSize() and
        IsUserBufferAttached() methods.  

post:  

    *   If the previously referenced buffer is a grab result buffer, a new
        buffer has been allocated.  
    *   If the previously referenced buffer is also referenced by another pylon
        image, a new buffer has been allocated.  
    *   If the previously referenced buffer is not large enough to hold an image
        with the given properties, a new buffer has been allocated.  
    *   If no buffer has been allocated before, a buffer has been allocated.  

\\error Throws an exception when the preconditions are not met. Throws an
exception when no buffer with the required size could be allocated.  

Parameters
----------
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
";

%feature("docstring") Pylon::CPylonImage::Release "
";

%feature("docstring") Pylon::CPylonImage::IsUserBufferAttached "

Returns true if the referenced buffer has been provided by the user.  
";

%feature("docstring") Pylon::CPylonImage::IsGrabResultBufferAttached "

Returns true if the referenced buffer has been provided by a grab result.  
";

%feature("docstring") Pylon::CPylonImage::GetAllocatedBufferSize "

Returns the size of the used buffer.  

This method is useful when working with so-called user buffers.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonImage::ChangePixelType "

Changes the pixel type of the image.  

Parameters
----------
* `pixelType` :  
    The new pixel type.  

pre:  

    *   Pylon::SamplesPerPixel( oldPixelType) == Pylon::SamplesPerPixel(
        newPixelType)  
    *   Pylon::BitPerPixel( oldPixelType) == Pylon::BitPerPixel( newPixelType)  

\\error Throws an exception when the new pixel type properties do not match the
existing ones.  
";

%feature("docstring") Pylon::CPylonImage::GetPlane "

Creates a new pylon image for a plane of the image. No image data is copied.  

Use CopyImage( const IImage& image) to create a full copy.  


Parameters
----------
* `planeIndex` :  
    The zero based index of the plane.  

Returns
-------
A pylon image referencing a plane of the image.  

pre: The value of planeIndex < Pylon::PlaneCount( GetPixelType()).  

post:  

    *   A reference to the same buffer is created. No image data is copied.  
    *   The returned image has the Pylon::GetPlanePixelType( GetPixelType())
        pixel type.  
    *   If the image is not planar only index 0 is allowed. A call passing index
        0 returns a copy of the image. No image data is copied.  

\\error Throws an exception when the plane index is out of range.  
";

%feature("docstring") Pylon::CPylonImage::GetAoi "

Creates a new pylon image for an image area of interest (Image AOI) derived from
the image. No image data is copied.  

Use CopyImage( const IImage& image, size_t newPaddingX) to create a full copy
and to remove the additional padding.  


Parameters
----------
* `topLeftX` :  
    The x-coordinate of the top left corner of the image AOI in pixels.  
* `topLeftY` :  
    The y-coordinate of the top left corner of the image AOI in pixels.  
* `width` :  
    The width of the image AOI in pixels.  
* `height` :  
    The height of the image AOI in pixels.  

Returns
-------
A pylon image referencing an image AOI of the image.  

pre:  

    *   The image must be valid.  
    *   The image AOI is located inside the image.  
    *   The image is not in a planar format, see Pylon::IsPlanar(). Use
        GetPlane() first in this case.  
    *   The rows of the image must be byte aligned. This may not be the case for
        packed pixel types. See Pylon::IsPacked().  
    *   The x-coordinate must be byte aligned. This may not be the case for
        packed pixel types. See Pylon::IsPacked().  
    *   The `topLeftX` parameter must be divisible by the return value of
        Pylon::GetPixelIncrementX() for the image's pixel type.  
    *   The `topLeftY` parameter must be divisible by the return value of
        Pylon::GetPixelIncrementY() for the image's pixel type.  

post:  

    *   A reference to the same buffer is created. The image data is not copied.  
    *   The returned image uses the paddingX property to skip over image content
        outside of the image AOI.  

\\error Throws an exception when the preconditions are not met.  
";

%feature("docstring") Pylon::CPylonImage::Create "

Creates an image and allocates a buffer for it.  

Parameters
----------
* `pixelType` :  
    The pixel type of the new image.  
* `width` :  
    The number of pixels in a row in the new image.  
* `height` :  
    The number of rows in the new image.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The pixel type must be valid.  
    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  

\\error Throws an exception when the parameters are invalid. Throws an exception
when no buffer with the required size could be allocated.  
";

// File: class_pylon_1_1_c_pylon_image_base.xml


%feature("docstring") Pylon::CPylonImageBase "

Provides basic functionality for pylon image classes.  

C++ includes: PylonImageBase.h
";

%feature("docstring") Pylon::CPylonImageBase::Save "

Saves the image to disk. Converts the image to a format that can be saved if
required.  

This is a convenience method that calls CImagePersistence::Save().  

If required, the image is automatically converted into a new image and saved
afterwards. See CImagePersistence::CanSaveWithoutConversion() for more
information. An image with a bit depth higher than 8 bit is stored with 16 bit
bit depth, if supported by the image file format. In this case the pixel data is
MSB aligned.  

If more control over the conversion is required, the CImageFormatConverter class
can be used to convert the input image before saving it.  

Parameters
----------
* `imageFileFormat` :  
    File format to save the image in.  
* `filename` :  
    Name and path of the image.  
* `pOptions` :  
    Additional options.  

pre: The pixel type of the image to be saved must be a supported input format of
    the Pylon::CImageFormatConverter.  

\\error Throws an exception if the saving of the image fails.  
";

%feature("docstring") Pylon::CPylonImageBase::Load "

Loads an image from a disk.  

This is a convenience method that calls CImagePersistence::Load()  

Parameters
----------
* `filename` :  
    Name and path of the image.  

pre: The image object must be able to hold the image format of the loaded image.  

\\error Throws an exception if the image cannot be loaded. The image buffer
content is undefined when the loading of the image fails.  
";

%feature("docstring") Pylon::CPylonImageBase::CanSaveWithoutConversion "

Can be used to check whether the image can be saved without prior conversion.  

This is a convenience method that calls
CImagePersistence::CanSaveWithoutConversion().  

Parameters
----------
* `imageFileFormat` :  
    Target file format for the image to be saved.  

Returns
-------
Returns true, if the image can be saved without prior conversion.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonImageBase::GetPixelData "

Retrieves the data of a pixel.  

note: This method is relativly slow. Do not use it for image processing tasks.  

Parameters
----------
* `posX` :  
    Horizontal position of the pixel. The first column has position 0.  
* `posY` :  
    Vertical position of the pixel. The first row has position 0.  

Returns
-------
Returns the data of a pixel for supported pixel types. For unsupported pixel
types pixel data of the SPixelData::PixelDataType_Unknown type is returned.  

pre:  

    *   The image must be valid.  
    *   The pixel position defined by `posX` and `posY` must be located inside
        the image area.  

Supported pixel types:  

*   PixelType_Mono1packed  
*   PixelType_Mono2packed  
*   PixelType_Mono4packed  
*   PixelType_Mono8  
*   PixelType_Mono8signed  
*   PixelType_Mono10  
*   PixelType_Mono10packed  
*   PixelType_Mono10p  
*   PixelType_Mono12  
*   PixelType_Mono12packed  
*   PixelType_Mono12p  
*   PixelType_Mono16  

*   PixelType_BayerGR8  
*   PixelType_BayerRG8  
*   PixelType_BayerGB8  
*   PixelType_BayerBG8  
*   PixelType_BayerGR10  
*   PixelType_BayerRG10  
*   PixelType_BayerGB10  
*   PixelType_BayerBG10  
*   PixelType_BayerGR12  
*   PixelType_BayerRG12  
*   PixelType_BayerGB12  
*   PixelType_BayerBG12  
*   PixelType_BayerGR12Packed  
*   PixelType_BayerRG12Packed  
*   PixelType_BayerGB12Packed  
*   PixelType_BayerBG12Packed  
*   PixelType_BayerGR10p  
*   PixelType_BayerRG10p  
*   PixelType_BayerGB10p  
*   PixelType_BayerBG10p  
*   PixelType_BayerGR12p  
*   PixelType_BayerRG12p  
*   PixelType_BayerGB12p  
*   PixelType_BayerBG12p  
*   PixelType_BayerGR16  
*   PixelType_BayerRG16  
*   PixelType_BayerGB16  
*   PixelType_BayerBG16  

*   PixelType_RGB8packed  
*   PixelType_BGR8packed  
*   PixelType_RGBA8packed  
*   PixelType_BGRA8packed  
*   PixelType_RGB10packed  
*   PixelType_BGR10packed  
*   PixelType_RGB12packed  
*   PixelType_BGR12packed  
*   PixelType_RGB12V1packed  
*   PixelType_RGB16packed  
*   PixelType_RGB8planar  
*   PixelType_RGB10planar  
*   PixelType_RGB12planar  
*   PixelType_RGB16planar  

*   PixelType_YUV422packed  
*   PixelType_YUV422_YUYV_Packed  

\\error Throws an exception, if the preconditions are not met.  
";

// File: class_pylon_1_1_c_pylon_image_user_buffer_event_handler.xml


%feature("docstring") Pylon::CPylonImageUserBufferEventHandler "

The CPylonImage user buffer event handler base class.  

You can optionally pass an object derived from this class when calling
CPylonImage::AttachUserBuffer(). When the CPylonImage doesn't need the user
buffer anymore, it will call the
CPylonImageUserBufferEventHandler::OnPylonImageUserBufferDetached() method. You
can override this function to execute your custom code when the user buffer has
been detached implicitly.  

The user is responsible for ensuring the object is valid until
CPylonImageUserBufferEventHandler::OnPylonImageUserBufferDetached() has been
called.  

C++ includes: PylonImageUserBufferEventHandler.h
";

%feature("docstring") Pylon::CPylonImageUserBufferEventHandler::OnPylonImageUserBufferDetached "

This method is called after the image class has released its user buffer.  

This method is called after the image class releases its image buffer. In case a
user buffer has been attached using CPylonImage::AttachUserBuffer() you can use
this to free your user buffer.  

In case you created the event handler on the heap using `new`, you can call
`delete this` at the end of the function.  


The default implementation does nothing. You can override this function to
execute custom code.  

Parameters
----------
* `pUserBuffer` :  
    Pointer to the user buffer passed when the user buffer was attached using
    CPylonImage::AttachUserBuffer().  
* `bufferSizeBytes` :  
    Size of the user buffer passed when the user buffer was attached using
    CPylonImage::AttachUserBuffer().  

\\error This function must not throw any exceptions.  
";

// File: class_pylon_1_1_c_shared_byte_buffer.xml


%feature("docstring") Pylon::CSharedByteBuffer "

Byte buffer with smart pointer semantics. Not thread safe.  

C++ includes: SharedByteBuffer.h
";

%feature("docstring") Pylon::CSharedByteBuffer::CSharedByteBuffer "

default constructer for shared buffer  
";

%feature("docstring") Pylon::CSharedByteBuffer::CSharedByteBuffer "

constructer for shared buffer form buffer size  
";

%feature("docstring") Pylon::CSharedByteBuffer::CSharedByteBuffer "

copy constructor  
";

%feature("docstring") Pylon::CSharedByteBuffer::~CSharedByteBuffer "

destructor  
";

%feature("docstring") Pylon::CSharedByteBuffer::Release "

release the referenz on buffer and memory if last referenzing object.  
";

%feature("docstring") Pylon::CSharedByteBuffer::GetSize "

return size of buffer in bytes  
";

%feature("docstring") Pylon::CSharedByteBuffer::GetBuffer "

get pointer to buffer memory  

Returns
-------
nullptr if buffer references no memory  
";

%feature("docstring") Pylon::CSharedByteBuffer::GetBuffer "

get pointer to buffer memory  

Returns
-------
nullptr if buffer references no memory  
";

%feature("docstring") Pylon::CSharedByteBuffer::IsNull "

test if buffer references memory  
";

// File: class_pylon_1_1_c_software_trigger_configuration.xml


%feature("docstring") Pylon::CSoftwareTriggerConfiguration "

Changes the configuration of the camera so that the acquisition of frames is
triggered by software trigger. Use together with
CInstantCamera::WaitForFrameTriggerReady() and
CInstantCamera::ExecuteSoftwareTrigger().  

The CSoftwareTriggerConfiguration is provided as header-only file. The code can
be copied and modified for creating own configuration classes.  

C++ includes: SoftwareTriggerConfiguration.h
";

%feature("docstring") Pylon::CSoftwareTriggerConfiguration::ApplyConfiguration "

Apply software trigger configuration.  
";

%feature("docstring") Pylon::CSoftwareTriggerConfiguration::OnOpened "

This method is called after the attached Pylon Device has been opened.  

Parameters
----------
* `camera` :  
    The source of the call.  

\\error Exceptions from this call will propagate through. The notification of
event handlers stops when an exception is triggered.  

\\threading This method is called inside the lock of the camera object.  
";

// File: class_pylon_1_1_c_static_defect_pixel_correction.xml


%feature("docstring") Pylon::CStaticDefectPixelCorrection "

Provides utility functions to use Static Defect Pixel Correction on certain ace
2 cameras.  

C++ includes: StaticDefectPixelCorrection.h
";

%feature("docstring") Pylon::CStaticDefectPixelCorrection::GetDefectPixelList "

Gets the defect pixel list from the camera.  

The camera stores all defect pixels in a sorted list. For more details, consult
the camera's documentation.  

Parameters
----------
* `pNodeMap` :  
    The nodemap of the camera.  
* `pixelList` :  
    List of defect pixels read from camera.  
* `listType` :  
    The type of list to read.  

Returns
-------
Returns true if the list was read successfully. Otherwise, false is returned.
\\error Can throw exceptions if the communication with the camera fails.  
";

%feature("docstring") Pylon::CStaticDefectPixelCorrection::SetDefectPixelList "

Sets the defect pixel list in the camera.  

The camera stores all defect pixels in a sorted list. The list will be
normalized, see NormalizePixelList, before it is written to the camera. For more
details, consult the camera's documentation.  

Parameters
----------
* `pNodeMap` :  
    The nodemap of the camera.  
* `pixelList` :  
    A list of defect pixels.  
* `listType` :  
    The type of list to write.  

Returns
-------
Returns true if the list was written successfully. Otherwise, false is returned.
\\error Can throw exceptions if the communication with the camera fails.  
";

%feature("docstring") Pylon::CStaticDefectPixelCorrection::NormalizePixelList "

Sort and erase duplicates of a defect pixel list.  

Normalizing the list is optional. The list will be normalized automatically when
SetDefectPixelList is called.  

Parameters
----------
* `pNodeMap` :  
    : The nodemap of the camera.  
* `pixelList` :  
    : The pixel list to normalize. The normalized pixel list will be returned.  

Returns
-------
True if the normalization runs correctly. Otherwise, false is returned.  

Exceptions
----------
* `May` :  
    throw a RuntimeException if the camera doesn't support user-specific defect
    pixel lists or if there are too many entries in the pixel list.  
";

// File: class_pylon_1_1_c_stream_grabber_proxy_t.xml


%feature("docstring") Pylon::CStreamGrabberProxyT "

Low Level API: The stream grabber class with parameter access methods.  

This is the base class for pylon stream grabber providing access to
configuration parameters.  

See also: configuringcameras  

templateparam
-------------
* `TParams` :  
    The specific parameter class (auto generated from the parameter xml file)  

C++ includes: StreamGrabberProxy.h
";

/*
 Implementation of the IStreamGrabber interface 
*/

/*
See Pylon::IStreamGrabber for more details.  

*/

/*
 Construction 
*/

/*
 Some smart pointer functionality 
*/

/*
 Assignment and copying is not supported 
*/

%feature("docstring") Pylon::CStreamGrabberProxyT::Open "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::Close "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::IsOpen "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::RegisterBuffer "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::DeregisterBuffer "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::PrepareGrab "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::IsStartAndStopStreamingMandatory "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::StartStreamingIfMandatory "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::StopStreamingIfMandatory "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::FinishGrab "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::QueueBuffer "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::FlushBuffersToOutput "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::CancelGrab "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::RetrieveResult "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::GetWaitObject "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::GetNodeMap "
";

%feature("docstring") Pylon::CStreamGrabberProxyT::CStreamGrabberProxyT "

Creates a CStreamGrabberProxyT object that is not attached to a pylon stream
grabber. Use the Attach() method to attach the pylon stream grabber.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::CStreamGrabberProxyT "

Creates a CStreamGrabberProxyT object and attaches it to a pylon stream grabber.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::~CStreamGrabberProxyT "

Destructor.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::Attach "

Attach a pylon stream grabber.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::IsAttached "

Checks if a pylon stream grabber is attached.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::GetStreamGrabber "

Returns the pylon stream grabber interface pointer.  
";

// File: class_pylon_1_1_c_string_parameter.xml


%feature("docstring") Pylon::CStringParameter "

CStringParameter class used to simplify access to GenApi parameters.  

C++ includes: StringParameter.h
";

%feature("docstring") Pylon::CStringParameter::CStringParameter "

Creates an empty CStringParameter object. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CStringParameter::CStringParameter "

Creates a CStringParameter object and attaches it to a node, typically retrieved
for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to attach.  

post:  

    *   If the passed node does not match the parameter type, the parameter will
        be empty, see IsValid().  
    *   If the passed node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CStringParameter::CStringParameter "

Creates a CStringParameter object and attaches it to a node of a matching type.  

Parameters
----------
* `pString` :  
    The node to attach.  

post: The parameter object must not be used to access the node's functionality
    if the source of the attached `pString` has been destroyed. In this case,
    call Release() or attach a new node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CStringParameter::CStringParameter "

Creates a CStringParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CStringParameter::CStringParameter "

Creates a CStringParameter object and attaches it to a node retrieved from the
provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

post:  

    *   If `name` is NULL, the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CStringParameter::CStringParameter "

Copies a CStringParameter object.  

Parameters
----------
* `rhs` :  
    The object to copy. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CStringParameter::~CStringParameter "

Destroys the CStringParameter object. Does not access the attached node. \\error
Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CStringParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `pNodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `pNodeMap` or `name` is NULL, the parameter will be empty, see
        IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CStringParameter::Attach "

Attaches a node retrieved from the provided node map.  

Parameters
----------
* `nodeMap` :  
    The node map. The source of the parameter.  
* `pName` :  
    The name of the parameter to attach.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If `name` is NULL the parameter will be empty, see IsValid().  
    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the provided node map has been destroyed. In this case, call
        Release() or attach a new node.  

    \\error The call to GenApi::INodeMap::GetNode can throw C++ exceptions.  
";

%feature("docstring") Pylon::CStringParameter::Attach "

Attaches a node, typically retrieved for a nodemap calling GetNode().  

Parameters
----------
* `pNode` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached.  

post:  

    *   If the node does not match the parameter type, the parameter will be
        empty, see IsValid().  
    *   If the node does match the parameter type, it is attached and the
        parameter object can be used to access the node's functionality.  
    *   The parameter object must not be used to access the node's functionality
        if the source of the attached `pNode` has been destroyed. In this case,
        call Release() or attach a new node.  

    \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CStringParameter::Attach "

Assigns a node of the same type to the parameter object.  

Parameters
----------
* `pString` :  
    The node to assign.  

Returns
-------
Returns true if the node has been attached. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CStringParameter::Equals "

Returns true if the same nodes are attached or both parameters are empty.  

Parameters
----------
* `rhs` :  
    The object to compare to.  

Returns
-------
Returns true if the same nodes are attached or both parameters are empty.
\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CStringParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pNode` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CStringParameter::Equals "

Returns true if the attached node pointer is equal.  

Parameters
----------
* `pString` :  
    The node to compare to.  

Returns
-------
Returns true if the attached node pointer is equal. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CStringParameter::Release "

Releases the attached node. \\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CStringParameter::IsValid "
";

%feature("docstring") Pylon::CStringParameter::SetValue "
";

%feature("docstring") Pylon::CStringParameter::GetValue "
";

%feature("docstring") Pylon::CStringParameter::GetMaxLength "
";

%feature("docstring") Pylon::CStringParameter::TrySetValue "
";

%feature("docstring") Pylon::CStringParameter::GetValueOrDefault "
";

// File: class_pylon_1_1_c_tl_factory.xml


%feature("docstring") Pylon::CTlFactory "

the Transport Layer Factory  

Creates, Destroys and Enumerates transport layers as well as their devices.  

C++ includes: TlFactory.h
";

%feature("docstring") Pylon::CTlFactory::GetInstance "

Retrieve the transport layer factory singleton. Throws an exception when
Pylon::PylonInitialize() has not been called before.  
";

%feature("docstring") Pylon::CTlFactory::EnumerateTls "

Retrieves a list of available transport layers.  

The list contains Pylon::CTlInfo objects used for transport layer creation.  

Parameters
----------
* `list` :  
    List to be filled with transport layer info objects.  

Returns
-------
Number of transport layers found.  
";

%feature("docstring") Pylon::CTlFactory::CreateTl "

Creates a transport layer object from a transport layer info object.  

This method accepts a transport layer info object which can be obtained by
calling EnumerateTls. For each successfully returned transport layer object, you
must call ReleaseTl to free the transport layer object.  

If the creation fails, a GenApi::GenericException will be thrown.  

Parameters
----------
* `ti` :  
    Transport layer info object specifying which transport layer to create.  

Returns
-------
Pointer to the transport layer object created. If no matching transport layer
could be found, NULL will be returned.  
";

%feature("docstring") Pylon::CTlFactory::CreateTl "

Creates a transport layer object from a device class string.  

This method accepts a device class string. You can see a list of available
device classes in the DeviceClass.h file. For each successfully returned
transport layer object, you must call ReleaseTl to free the transport layer
object.  

If the creation fails, a GenApi::GenericException will be thrown.  

Parameters
----------
* `deviceClass` :  
    Transport layer info object specifying which transport layer to create.  

Returns
-------
Pointer to the transport layer object created. If no matching transport layer
could be found, NULL will be returned.  
";

%feature("docstring") Pylon::CTlFactory::ReleaseTl "

Releases a transport layer object created by a call to CreateTl().  

For each successfully returned transport layer object from any CreateTl()
function, you must call this function to free the transport layer object.  

Parameters
----------
* `pTl` :  
    Pointer to the transport layer object to be released.  
";

%feature("docstring") Pylon::CTlFactory::EnumerateDevices "
";

%feature("docstring") Pylon::CTlFactory::EnumerateDevices "
";

%feature("docstring") Pylon::CTlFactory::CreateDevice "
";

%feature("docstring") Pylon::CTlFactory::CreateDevice "
";

%feature("docstring") Pylon::CTlFactory::CreateDevice "
";

%feature("docstring") Pylon::CTlFactory::CreateFirstDevice "
";

%feature("docstring") Pylon::CTlFactory::CreateFirstDevice "
";

%feature("docstring") Pylon::CTlFactory::DestroyDevice "
";

%feature("docstring") Pylon::CTlFactory::IsDeviceAccessible "
";

// File: class_pylon_1_1_c_tl_info.xml


%feature("docstring") Pylon::CTlInfo "

    \\ingroup Pylon_TransportLayer
    \\brief Class used for storing the result of the transport
           layer enumeration process.  

Enumerating the available Transport Layer objects returns a list of CTlInfo
objects (Pylon::TlInfoList_t). A CTlInfo object holds information about the
enumerated transport layer.  

C++ includes: TlInfo.h
";

%feature("docstring") Pylon::CTlInfo::GetFileName "

Retrieves the filename of the GenTL producer [GenTL consumer only]. This
property is identified by Key::FileNameKey.  
";

%feature("docstring") Pylon::CTlInfo::SetFileName "

Sets the above property.  
";

%feature("docstring") Pylon::CTlInfo::IsFileNameAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CTlInfo::GetInfoID "

Retrieves the InfoID of the GenTL producer [GenTL consumer only]. This property
is identified by Key::VendorNameKey.  
";

%feature("docstring") Pylon::CTlInfo::SetInfoID "

Sets the above property.  
";

%feature("docstring") Pylon::CTlInfo::IsInfoIDAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CTlInfo::GetModelName "

Retrieves the model name of the data producer This property is identified by
Key::ModelNameKey.  
";

%feature("docstring") Pylon::CTlInfo::SetModelName "

Sets the above property.  
";

%feature("docstring") Pylon::CTlInfo::IsModelNameAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CTlInfo::GetVersion "

Retrieves the version of the transport layer. This property is identified by
Key::VersionKey.  
";

%feature("docstring") Pylon::CTlInfo::SetVersion "

Sets the above property.  
";

%feature("docstring") Pylon::CTlInfo::IsVersionAvailable "

Returns true if the above property is available.  
";

// File: class_pylon_1_1_c_video_writer.xml


%feature("docstring") Pylon::CVideoWriter "

Supports writing video files.  

note: Note that a supplementary software package containing additional libraries
    has to be installed for this.  

C++ includes: VideoWriter.h
";

%feature("docstring") Pylon::CVideoWriter::CVideoWriter "

Creates a video writer object.  

\\error Throws a RuntimeException when no memory can be allocated.  
";

%feature("docstring") Pylon::CVideoWriter::~CVideoWriter "

Destroys the video writer object.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CVideoWriter::SetParameter "

Easy way to set parameters required for video recording.  

This is a convenient way to set all required parameters in a single function
call. The parameters `width`, `height`, `framesPerSecondPlaybackSpeed` and
`quality` are set in the nodemap. The parameter `inputPixelType` is checked for
its convertibility to YUV420p or whether it is already YUV420p. Advanced
parameters can be accessed using the nodemap provided by GetNodeMap().  

Parameters
----------
* `width` :  
    The number of pixels in a row of the video file to save.  
* `height` :  
    The number of rows of the video file to save.  
* `inputPixelType` :  
    The pixel type of the images that will be added to the video writer. This
    input is used to derive the video format. Currently the output is always
    YUV420p.  
* `framesPerSecondPlaybackSpeed` :  
    The playback speed in frames per second.  
* `quality` :  
    The quality setting, valid range is 1 ... 100.  

pre: The VideoWriter ist closed.  

\\error Throws a C++ exception when a parameter is out of range, set to an
invalid value or parameters cannot be changed (e.g., after calling Open()).  
";

%feature("docstring") Pylon::CVideoWriter::Open "

Opens a video file for writing.  

If a file with the same `filename` already exists, it will be overwritten.  

Parameters
----------
* `filename` :  
    Name and path of the video file.  

pre:  

    *   The VideoWriter ist closed.  
    *   The width and height parameters are larger than 1.  

\\error Throws a RuntimeException if the video file cannot be opened. Throws a
RuntimeException if the current parameters do not meet codec requirements.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CVideoWriter::IsOpen "

Returns the open state of the video file.  

Returns
-------
Returns true if open.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CVideoWriter::Close "

Closes the video file.  

\\error Does not throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CVideoWriter::Add "

Adds the image to the video file. Converts the image to the correct format if
required.  

The image is automatically converted to YUV420p unless the input `pixelType` is
already YUV420p. The orientation of the image is always converted to
`ImageOrientation_TopDown` unless the input`pixelType` is YUV420p. In that case,
the `orientation` of the image must already be `ImageOrientation_TopDown`. See
preconditions.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the image.  
* `bufferSize` :  
    The size of the buffer in byte.  
* `pixelType` :  
    The pixel type of the image to save.  
* `width` :  
    The number of pixels in a row of the image to save.  
* `height` :  
    The number of rows of the image to save.  
* `paddingX` :  
    The number of extra data bytes at the end of each line.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The file is open.  
    *   The image added is valid.  
    *   The `pixelType` of the image to add is a supported input format of the
        Pylon::CImageFormatConverter or YUV420p.  
    *   If the pixelType is YUV420p the `orientation` has to be
        `ImageOrientation_TopDown`.  
    *   The width and height of the image match the values passed when opening
        the video file.  

\\error Throws an InvalidArgumentException exception if the image does not match
the requirements like size or pixelformat. The InvalidArgumentException does not
invalidate the VideoWriter. Throws a RuntimeException in case of an internal
error. When throwing a RuntimeException all internal resources are freed and the
VideoWriter must be closed.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CVideoWriter::Add "

Adds the image to the video file. Converts the image to the correct format if
required.  

The image is automatically converted to YUV420p unless the input `pixelType` is
already YUV420p. The orientation of the image is always converted to
`ImageOrientation_TopDown` unless the input `pixelType` is YUV420p. In that
case, the `orientation` of the image must already be `ImageOrientation_TopDown`.
See preconditions.  

Parameters
----------
* `image` :  
    The image to add, e.g., a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

pre:  

    *   The file is open.  
    *   The image added is valid.  
    *   The `pixelType` of the image to add is a supported input format of the
        Pylon::CImageFormatConverter or YUV420p.  
    *   If the pixelType is YUV420p the `orientation` has to be
        `ImageOrientation_TopDown`.  
    *   The width and height of the image match the values passed when opening
        the video file.  

\\error Throws an InvalidArgumentException exception if the image does not match
the requirements like size or pixelformat. The InvalidArgumentException does not
invalidate the VideoWriter. Throws a RuntimeException in case of an internal
error. When throwing a RuntimeException all internal resources are freed and the
VideoWriter must be closed.  

\\threading This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CVideoWriter::CanAddWithoutConversion "

Can be used to check whether the given image is added to the video file without
prior conversion when Add() is called.  

Parameters
----------
* `pixelType` :  
    The pixel type of the image to save.  
* `width` :  
    The number of pixels in a row of the image to save.  
* `height` :  
    The number of rows of the image to save.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image data in the video file.  

Returns
-------
Returns true if the image is added to the video stream without prior conversion
when Add() is called. Returns false if the image is automatically converted when
Add() is called. Returns false if the image cannot be added at all. See the
preconditions of Add() for more information.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CVideoWriter::CanAddWithoutConversion "

Can be used to check whether the given image is added to the video file without
prior conversion when Add() is called.  

Parameters
----------
* `image` :  
    The image to save, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

Returns
-------
Returns true if the image is added to the video stream without prior conversion
when Add() is called. Returns false if the image is automatically converted when
Add() is called. Returns false if the image cannot be added at all. See the
preconditions of Add() for more information.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CVideoWriter::GetNodeMap "

Provides access to all parameters via a nodemap. \\error Does not throw C++
exceptions.  
";

%feature("docstring") Pylon::CVideoWriter::IsSupported "

Checks if video writing is supported.  

Checks if all necessary dynamic libraries of the supplementary software package
are installed and can be loaded. This does not check if the codec for the video
can be used. This is checked in Open().  

Returns
-------
Returns true if video writing is supported.  

\\error Does not throw C++ exceptions.  
";

// File: class_pylon_1_1_device_info_list.xml


%feature("docstring") Pylon::DeviceInfoList "

STL std::vector like container for Pylon::CDeviceInfo objects.  

C++ includes: Container.h
";

%feature("docstring") Pylon::DeviceInfoList::DeviceInfoList "
";

%feature("docstring") Pylon::DeviceInfoList::DeviceInfoList "
";

%feature("docstring") Pylon::DeviceInfoList::DeviceInfoList "
";

%feature("docstring") Pylon::DeviceInfoList::~DeviceInfoList "
";

// File: class_pylon_1_1_event_result.xml


%feature("docstring") Pylon::EventResult "

Low Level API: An event result.  

C++ includes: Result.h
";

%feature("docstring") Pylon::EventResult::EventResult "
";

%feature("docstring") Pylon::EventResult::~EventResult "
";

%feature("docstring") Pylon::EventResult::Succeeded "
";

%feature("docstring") Pylon::EventResult::ErrorDescription "
";

%feature("docstring") Pylon::EventResult::ErrorCode "
";

// File: class_pylon_1_1_function___callback_body.xml


%feature("docstring") Pylon::Function_CallbackBody "
";

%feature("docstring") Pylon::Function_CallbackBody::Function_CallbackBody "

Constructor.  
";

%feature("docstring") Pylon::Function_CallbackBody::clone "

virtual copy constructor  
";

// File: class_pylon_1_1_grab_result.xml


%feature("docstring") Pylon::GrabResult "

Low Level API: A grab result that combines the used image buffer and status
information.  

Note that depending on the used interface technology, the specific camera and
the situation some of the attributes are not meaningful, e. g. timestamp in case
of an canceled grab.  

C++ includes: Result.h
";

%feature("docstring") Pylon::GrabResult::GrabResult "
";

%feature("docstring") Pylon::GrabResult::GrabResult "
";

%feature("docstring") Pylon::GrabResult::~GrabResult "
";

%feature("docstring") Pylon::GrabResult::Succeeded "

True if status is grabbed.  
";

%feature("docstring") Pylon::GrabResult::Handle "

Get the buffer handle.  
";

%feature("docstring") Pylon::GrabResult::Buffer "

Get the pointer to the buffer.  
";

%feature("docstring") Pylon::GrabResult::Status "

Get the grab status.  
";

%feature("docstring") Pylon::GrabResult::Context "

Get the pointer the user provided context.  
";

%feature("docstring") Pylon::GrabResult::GetPayloadType "

Get the actual payload type.  
";

%feature("docstring") Pylon::GrabResult::GetPixelType "

Get the actual pixel type. This is only defined in case of image data.  
";

%feature("docstring") Pylon::GrabResult::GetTimeStamp "

Get the camera specific tick count.  

In case of GigE-Vision this describes when the image exposure was started.
Cameras that do not support this feature return zero. If supported this may be
used to determine which ROIs were acquired simultaneously.  
";

%feature("docstring") Pylon::GrabResult::GetSizeX "

Get the actual number of columns in pixel. This is only defined in case of image
data.  
";

%feature("docstring") Pylon::GrabResult::GetSizeY "

Get the actual number of rows in pixel. This is only defined in case of image
data.  
";

%feature("docstring") Pylon::GrabResult::GetOffsetX "

Get the actual starting column. This is only defined in case of image data.  
";

%feature("docstring") Pylon::GrabResult::GetOffsetY "

Get the actual starting row. This is only defined in case of image data.  
";

%feature("docstring") Pylon::GrabResult::GetPaddingX "

Get the number of extra data at the end of each row in bytes. This is only
defined in case of image data.  
";

%feature("docstring") Pylon::GrabResult::GetPaddingY "

Get the number of extra data at the end of the image data in bytes. This is only
defined in case of image data.  
";

%feature("docstring") Pylon::GrabResult::GetPayloadSize "

Get the number of valid bytes in the buffer returned by Buffer().  
";

%feature("docstring") Pylon::GrabResult::GetPayloadSize_t "

Get the number of valid bytes in the buffer returned by Buffer() as size_t.  
";

%feature("docstring") Pylon::GrabResult::GetErrorDescription "

Get a description of the current error.  
";

%feature("docstring") Pylon::GrabResult::GetErrorCode "

Get the current error code.  
";

%feature("docstring") Pylon::GrabResult::GetImage "

Provides an adapter from the grab result to Pylon::IImage interface.  

This returned adapter allows passing the grab result to saving functions or
image format converter.  

attention: The returned reference is only valid as long the grab result is not
    destroyed.  
";

%feature("docstring") Pylon::GrabResult::GetBlockID "

Get the block ID of the grabbed frame (camera device specific).  

par: GigE Camera Devices
    If the Extended ID mode is disabled (default), the sequence number starts
    with 1 and wraps at 65535. If the Extended ID mode is enabled, the sequence
    number starts with 1 and uses the full 64-bit unsigned integer value range.  

A value of 0 indicates that this feature is not supported by the camera. You can
configure the Extended ID mode by setting the GevGVSPExtendedIDMode or the
BslGevGVSPExtendedIDMode parameter, if available. The Instant Camera class and
the pylon GigE stream grabber provide additional parameters for controlling the
Extended ID mode.  

par: USB Camera Devices
    The sequence number starts with 0 and uses the full 64 Bit range.  

attention: A block ID of value UINT64_MAX indicates that the Block ID is invalid
    and must not be used.  
";

%feature("docstring") Pylon::GrabResult::GetDataContainer "

Returns the grab result as a CPylonDataContainer.  
";

%feature("docstring") Pylon::GrabResult::GetDataComponentCount "

Returns the number of components contained in the container.  

Returns
-------
Returns the number of components contained in the container.  

You can use the return value to iterate over the existing components by calling
`Pylon::CPylonDataContainer::GetDataComponent()`.  

\\error Does not throw C++ exceptions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::GrabResult::GetDataComponent "

Returns a specific component from the container.  

Parameters
----------
* `index` :  
    Index of the component to return. The index must be less than the value
    returned by `Pylon::CPylonDataContainer::GetComponentCount()`.  

Returns
-------
Returns the component specified by the index parameter.  

\\error Throws an exception if the index parameter is out of range. Can throw
exceptions in low-memory conditions.  

\\threading This class is not thread-safe. If you access the same instance from
multiple threads, you must make sure to synchronize the access accordingly.  
";

%feature("docstring") Pylon::GrabResult::GetBufferSize "

Get the size of the buffer returned by Buffer().  
";

%feature("docstring") Pylon::GrabResult::HasChunkData "

Get information if chunk data is present in the buffer returned by Buffer().  
";

// File: class_i_buffer_factory.xml


%feature("docstring") IBufferFactory "

Usable to create a custom buffer factory when needed.  

C++ includes: BufferFactory.h
";

// File: interface_i_chunk_parser.xml

// File: interface_i_device.xml

// File: interface_i_device_factory.xml

// File: interface_i_event_adapter.xml

// File: interface_i_event_grabber.xml

// File: interface_i_image.xml

// File: interface_i_interface.xml

// File: class_pylon_1_1_interface_info_list.xml


%feature("docstring") Pylon::InterfaceInfoList "

STL std::vector like container for Pylon::CInterfaceInfo objects.  

C++ includes: Container.h
";

%feature("docstring") Pylon::InterfaceInfoList::InterfaceInfoList "
";

%feature("docstring") Pylon::InterfaceInfoList::InterfaceInfoList "
";

%feature("docstring") Pylon::InterfaceInfoList::InterfaceInfoList "
";

%feature("docstring") Pylon::InterfaceInfoList::~InterfaceInfoList "
";

// File: class_pylon_1_1_c_image_format_converter_1_1_i_output_pixel_format_enum.xml


%feature("docstring") Pylon::CImageFormatConverter::IOutputPixelFormatEnum "
";

%feature("docstring") Pylon::CImageFormatConverter::IOutputPixelFormatEnum::SetValue "
";

%feature("docstring") Pylon::CImageFormatConverter::IOutputPixelFormatEnum::GetValue "
";

// File: interface_i_properties.xml

// File: interface_i_pylon_device.xml

// File: interface_i_reusable_image.xml

// File: interface_i_self_reliant_chunk_parser.xml

// File: interface_i_stream_grabber.xml

// File: class_pylon_1_1_t_list_1_1iterator.xml


%feature("docstring") Pylon::TList::iterator "
";

%feature("docstring") Pylon::TList::iterator::iterator "
";

// File: interface_i_transport_layer.xml

// File: class_pylon_1_1_member___callback_body.xml


%feature("docstring") Pylon::Member_CallbackBody "
";

%feature("docstring") Pylon::Member_CallbackBody::Member_CallbackBody "

Constructor.  
";

%feature("docstring") Pylon::Member_CallbackBody::clone "

virtual copy constructor  
";

// File: class_pylon_1_1_pylon_auto_init_term.xml


%feature("docstring") Pylon::PylonAutoInitTerm "

Helper class to automagically call PylonInitialize and PylonTerminate in
constructor and destructor.  

  

C++ includes: PylonBase.h
";

%feature("docstring") Pylon::PylonAutoInitTerm::PylonAutoInitTerm "
";

%feature("docstring") Pylon::PylonAutoInitTerm::~PylonAutoInitTerm "
";

// File: class_pylon_1_1_pylon_data_component_list.xml


%feature("docstring") Pylon::PylonDataComponentList "
";

%feature("docstring") Pylon::PylonDataComponentList::PylonDataComponentList "
";

%feature("docstring") Pylon::PylonDataComponentList::PylonDataComponentList "
";

%feature("docstring") Pylon::PylonDataComponentList::PylonDataComponentList "
";

%feature("docstring") Pylon::PylonDataComponentList::~PylonDataComponentList "
";

// File: struct_pylon_1_1_s_b_g_r8_pixel.xml


%feature("docstring") Pylon::SBGR8Pixel "

Describes the memory layout of a BGR8 pixel. This pixel is used in Windows
bitmaps.  

C++ includes: Pixel.h
";

// File: struct_pylon_1_1_s_b_g_r_a8_pixel.xml


%feature("docstring") Pylon::SBGRA8Pixel "

Describes the memory layout of a BGRA8 pixel. This pixel is used in Windows
bitmaps.  

C++ includes: Pixel.h
";

// File: struct_pylon_1_1_s_pixel_data.xml


%feature("docstring") Pylon::SPixelData "

Describes the data of one pixel.  

C++ includes: PixelData.h
";

%feature("docstring") Pylon::SPixelData::SPixelData "

Construct and clear.  
";

%feature("docstring") Pylon::SPixelData::~SPixelData "
";

// File: struct_pylon_1_1_s_r_g_b16_pixel.xml


%feature("docstring") Pylon::SRGB16Pixel "

Describes the memory layout of a RGB16 pixel.  

C++ includes: Pixel.h
";

// File: struct_pylon_1_1_s_r_g_b8_pixel.xml


%feature("docstring") Pylon::SRGB8Pixel "

Describes the memory layout of a RGB8 pixel.  

C++ includes: Pixel.h
";

// File: struct_pylon_1_1_s_r_g_b_a8_pixel.xml


%feature("docstring") Pylon::SRGBA8Pixel "

Describes the memory layout of a RGBA8 pixel.  

C++ includes: Pixel.h
";

// File: struct_pylon_1_1_static_defect_pixel.xml


%feature("docstring") Pylon::StaticDefectPixel "

A single defect pixel.  

C++ includes: StaticDefectPixel.h
";

// File: class_pylon_1_1_static_defect_pixel_list.xml


%feature("docstring") Pylon::StaticDefectPixelList "

STL std::vector like container for Pylon::StaticDefectPixel objects.  

C++ includes: Container.h
";

%feature("docstring") Pylon::StaticDefectPixelList::StaticDefectPixelList "
";

%feature("docstring") Pylon::StaticDefectPixelList::StaticDefectPixelList "
";

%feature("docstring") Pylon::StaticDefectPixelList::StaticDefectPixelList "
";

%feature("docstring") Pylon::StaticDefectPixelList::~StaticDefectPixelList "
";

%feature("docstring") Pylon::StaticDefectPixelList::sort "
";

// File: struct_pylon_1_1_s_y_u_v422___u_y_v_y.xml


%feature("docstring") Pylon::SYUV422_UYVY "

Describes the memory layout of a YUV422_UYVY pixel with information about
brightness and chroma for two pixels.  

C++ includes: Pixel.h
";

// File: struct_pylon_1_1_s_y_u_v422___y_u_y_v.xml


%feature("docstring") Pylon::SYUV422_YUYV "

Describes the memory layout of a YUV422_YUYV pixel with information about
brightness and chroma for two pixels.  

C++ includes: Pixel.h
";

// File: class_pylon_1_1_c_enum_parameter_1_1_table__t.xml


%feature("docstring") Pylon::CEnumParameter::Table_t "
";

%feature("docstring") Pylon::CEnumParameter::Table_t::Table_t "
";

%feature("docstring") Pylon::CEnumParameter::Table_t::Table_t "
";

%feature("docstring") Pylon::CEnumParameter::Table_t::GetItems "
";

%feature("docstring") Pylon::CEnumParameter::Table_t::GetSizeOfTable "
";

// File: class_pylon_1_1_c_enum_parameter_1_1_table_item__t.xml


%feature("docstring") Pylon::CEnumParameter::TableItem_t "
";

%feature("docstring") Pylon::CEnumParameter::TableItem_t::TableItem_t "
";

%feature("docstring") Pylon::CEnumParameter::TableItem_t::TableItem_t "
";

%feature("docstring") Pylon::CEnumParameter::TableItem_t::GetName "
";

%feature("docstring") Pylon::CEnumParameter::TableItem_t::GetSizeOfName "
";

// File: class_pylon_1_1_tl_info_list.xml


%feature("docstring") Pylon::TlInfoList "

STL std::vector like container for Pylon::CTlInfo objects.  

C++ includes: Container.h
";

%feature("docstring") Pylon::TlInfoList::TlInfoList "
";

%feature("docstring") Pylon::TlInfoList::TlInfoList "
";

%feature("docstring") Pylon::TlInfoList::TlInfoList "
";

%feature("docstring") Pylon::TlInfoList::~TlInfoList "
";

// File: class_pylon_1_1_t_list.xml


%feature("docstring") Pylon::TList "

STL std::vector like container class.  

Based on the GenICam::gcstring_vector class.  

C++ includes: Container.h
";

%feature("docstring") Pylon::TList::TList "
";

%feature("docstring") Pylon::TList::TList "
";

%feature("docstring") Pylon::TList::TList "
";

%feature("docstring") Pylon::TList::~TList "
";

%feature("docstring") Pylon::TList::assign "
";

%feature("docstring") Pylon::TList::clear "
";

%feature("docstring") Pylon::TList::erase "
";

%feature("docstring") Pylon::TList::erase "
";

%feature("docstring") Pylon::TList::at "
";

%feature("docstring") Pylon::TList::at "
";

%feature("docstring") Pylon::TList::back "
";

%feature("docstring") Pylon::TList::back "
";

%feature("docstring") Pylon::TList::begin "
";

%feature("docstring") Pylon::TList::begin "
";

%feature("docstring") Pylon::TList::capacity "
";

%feature("docstring") Pylon::TList::end "
";

%feature("docstring") Pylon::TList::end "
";

%feature("docstring") Pylon::TList::front "
";

%feature("docstring") Pylon::TList::front "
";

%feature("docstring") Pylon::TList::max_size "
";

%feature("docstring") Pylon::TList::size "
";

%feature("docstring") Pylon::TList::insert "
";

%feature("docstring") Pylon::TList::insert "
";

%feature("docstring") Pylon::TList::empty "
";

%feature("docstring") Pylon::TList::pop_back "
";

%feature("docstring") Pylon::TList::push_back "
";

%feature("docstring") Pylon::TList::resize "
";

%feature("docstring") Pylon::TList::reserve "
";

// File: class_pylon_1_1_version_info.xml


%feature("docstring") Pylon::VersionInfo "

Holds a four-part version number consisting of major.minor.subminor.build.  

This class stores a four-part version number and provides comparison operators.
If you use the constructor with one parameter, the version info object will be
initialized with pylon base version numbers.  

C++ includes: PylonVersionInfo.h
";

%feature("docstring") Pylon::VersionInfo::VersionInfo "

Constructs a version info object using pylon base version numbers. If checkBuild
is set to false, the build number will not be used in comparison operators.  
";

%feature("docstring") Pylon::VersionInfo::VersionInfo "

Constructs a version info object using the version number parts passed.  
";

%feature("docstring") Pylon::VersionInfo::VersionInfo "

Constructs a version info object using the version number parts passed.  
";

%feature("docstring") Pylon::VersionInfo::~VersionInfo "

The VersionInfo destructor.  
";

%feature("docstring") Pylon::VersionInfo::getMajor "

Returns the major version number. For version 2.1.3.1234 the value 2 would be
returned.  
";

%feature("docstring") Pylon::VersionInfo::getMinor "

Returns the minor version number. For version 2.1.3.1234 the value 1 would be
returned.  
";

%feature("docstring") Pylon::VersionInfo::getSubminor "

Returns the subminor version number. For version 2.1.3.1234 the value 3 would be
returned.  
";

%feature("docstring") Pylon::VersionInfo::getBuild "

Returns the build number. For version 2.1.3.1234 the value 1234 would be
returned.  
";

// File: class_pylon_1_1_wait_object.xml


%feature("docstring") Pylon::WaitObject "

A platform independent wait object.  

Wait objects are used by the Pylon::IStreamGrabber and Pylon::IEventGrabber
interfaces to provide a platform independent mechanism for allowing an
application to wait for data buffers to be filled.  

For the Windows version of pylon, WaitObjects are wrappers for Win32 objects
that can be used with `WaitForSingleObject()` and `WaitForMultipleObjects()`.  

For the Linux version of pylon, WaitObjects are implemented based on file
descriptors. The wait operation is implemented using the `poll()` function.  

Although the class provides a default constructor, the default constructor
doesn't create a \"usable\" wait objects wrapping a handle resp. file
descriptor. Valid instances of Pylon::WaitObject cannot be created by the
application, instead the pylon libraries return fully created wait objects. The
Pylon::WaitObjectEx class can be used to create wait objects that can be
controlled by the application.  

The Pylon::WaitObject class provides access to the wrapped handle resp. file
descriptor. This allows to use to allow use pylon wait objects as input for
\"native\" APIs like `WaitForMultipleObjects()` (Windows), and `poll()` (Linux).  

Multiple Pylon::WaitObjects can be put in the Pylon::WaitObjects container class
allowing to wait \"simultaneously\" for multiple events.  

C++ includes: WaitObject.h
";

%feature("docstring") Pylon::WaitObject::WaitObject "

Constructs an \"empty\" wait object, i.e., the wait object is not attached to a
platform dependent wait object (IsValid() == false).  

The Pylon::WaitObjectEx class can be used to create wait objects controllable by
an application.  
";

%feature("docstring") Pylon::WaitObject::WaitObject "

Copy constructor (duplicates the wrapped handle/file descriptor).  
";

%feature("docstring") Pylon::WaitObject::WaitObject "

Constructor taking existing handle (duplicate=false -> take ownership like
std:auto_ptr).  

This method allows to wrap an existing windows handle that can be used with the
`WaitForSingleObject()` and `WaitForMultipleObjects` methods.  
";

%feature("docstring") Pylon::WaitObject::~WaitObject "

Destructor.  
";

%feature("docstring") Pylon::WaitObject::IsValid "

Checks if the wait object is valid.  

Don't call the Wait methods() for an invalid wait object. Wait objects returned
by the pylon libraries are valid.  

Returns
-------
true if the object contains a valid handle/file descriptor  
";

%feature("docstring") Pylon::WaitObject::Wait "

Wait for the object to be signaled.  

Parameters
----------
* `timeout` :  
    timeout in ms  

Returns
-------
false when the timeout has been expired, true when the waiting was successful
before the timeout has been expired.  
";

%feature("docstring") Pylon::WaitObject::WaitEx "

Wait for the object to be signaled (interruptible).  

Parameters
----------
* `timeout` :  
    timeout in ms  
* `bAlertable` :  
    When the bAlertable parameter is set to true, the function waits until
    either the timeout elapses, the object enters the signaled state, or the
    wait operation has been interrupted. For Windows, the wait operation is
    interrupted by queued APCs or I/O completion routines. For Linux, the wait
    operation can be interrupted by signals.  

Returns
-------
The returned Pylon::EWaitExResult value indicates the result of the wait
operation.  
";

%feature("docstring") Pylon::WaitObject::Sleep "

Suspend calling thread for specified time.  

Parameters
----------
* `ms` :  
    wait time in ms  
";

// File: class_pylon_1_1_wait_object_ex.xml


%feature("docstring") Pylon::WaitObjectEx "

A wait object that the user may signal.  

C++ includes: WaitObject.h
";

%feature("docstring") Pylon::WaitObjectEx::Create "

Creates an event object (manual reset event).  
";

%feature("docstring") Pylon::WaitObjectEx::WaitObjectEx "

Constructs an \"empty\" wait object, i.e., the wait object is not attached to a
platform dependent wait object (IsValid() == false).  

Use the static WaitObjectEx::Create() method to create instances of the
WaitObjectEx class instead.  
";

%feature("docstring") Pylon::WaitObjectEx::~WaitObjectEx "

Destroys the waitobject.  
";

%feature("docstring") Pylon::WaitObjectEx::Signal "

Set the object to signaled state.  
";

%feature("docstring") Pylon::WaitObjectEx::Reset "

Reset the object to unsignaled state.  
";

// File: class_pylon_1_1_wait_objects.xml


%feature("docstring") Pylon::WaitObjects "

A set of wait objects.  

C++ includes: WaitObjects.h
";

%feature("docstring") Pylon::WaitObjects::WaitObjects "

Creates an empty wait object set.  
";

%feature("docstring") Pylon::WaitObjects::WaitObjects "

copy constructor  
";

%feature("docstring") Pylon::WaitObjects::~WaitObjects "

destructor  
";

%feature("docstring") Pylon::WaitObjects::Add "

Add an object to wait on and return the index of the added object.  

Calling Add from another thread during wait operations will cause undefined
behaviour.  
";

%feature("docstring") Pylon::WaitObjects::RemoveAll "

Removes all added wait objects.  

Calling RemoveAll from another thread during wait operations will cause
undefined behaviour.  
";

%feature("docstring") Pylon::WaitObjects::WaitForAll "

Wait for all objects to get signaled.  

Parameters
----------
* `timeout` :  
    maximum wait period in milliseconds  

Returns
-------
true if all objects were signaled  
";

%feature("docstring") Pylon::WaitObjects::WaitForAny "

Wait for any one object to get signaled.  

Parameters
----------
* `timeout` :  
    maximum wait period in milliseconds  
* `*pIndex` :  
    (optional) pointer to buffer taking the index of the signaled object  

Returns
-------
true if any object was signaled.  
";

%feature("docstring") Pylon::WaitObjects::WaitForAllEx "

Wait for all objects to get signaled.  

Parameters
----------
* `bAlertable` :  
    If true, the wait operation can be interrupted (Windows: APC; UNIX: signal)  
* `timeout` :  
    maximum wait period in milliseconds  
";

%feature("docstring") Pylon::WaitObjects::WaitForAnyEx "

Wait for any one object to get signaled.  

Parameters
----------
* `timeout` :  
    maximum wait period in milliseconds  
* `bAlertable` :  
    If true, the wait operation can be interrupted (Windows: APC; UNIX: signal)  
* `*pIndex` :  
    (optional) pointer to buffer taking the index of the signaled object  
";

// File: namespace_basler___image_format_converter_params.xml

// File: namespace_basler___instant_camera_params.xml

// File: namespace_basler___universal_chunk_data_params.xml

// File: namespace_basler___universal_event_params.xml

// File: namespace_basler___universal_interface_params.xml

// File: namespace_basler___universal_stream_params.xml

// File: namespace_basler___universal_t_l_params.xml

// File: namespace_basler___video_writer_params.xml

// File: namespace_g_e_n_a_p_i___n_a_m_e_s_p_a_c_e.xml

// File: namespace_pylon.xml

%feature("docstring") Pylon::TrySetValue "

Sets the Boolean value of the parameter if the parameter is writable.  

Returns
-------
Returns false if the parameter is not writable.  

Parameters
----------
* `value` :  
    The Boolean value to set. \\threading The method accesses the parameter
    multiple times. These accesses are not synchronized by a lock. \\error Can
    throw exceptions if the preconditions are not met or if writing the value
    fails.  
";

%feature("docstring") Pylon::TrySetValue "

Sets the value of the parameter if the parameter is writable and the value is
contained in the set of settable enumeration values.  

Sets the value of the parameter if the parameter is writable.  

Returns
-------
Returns false if the parameter is not writable or the value is not contained in
the set of settable enumeration values.  

Parameters
----------
* `value` :  
    The value to set. \\threading The method accesses the parameter multiple
    times. These accesses are not synchronized by a lock. \\error- Can throw
    exceptions if the preconditions are not met or if writing the value fails.  

Returns
-------
Returns false if the parameter is not writable.  

Parameters
----------
* `value` :  
    The string value to set.  

pre:  

    *   The length of the string must be less than
        GenApi::IString::GetMaxLength().  

    \\threading The method accesses the parameter multiple times. These accesses
    are not synchronized by a lock. \\error Can throw exceptions if the
    preconditions are not met or if writing the value fails.  
";

%feature("docstring") Pylon::TrySetValue "

If the parameter is writable, sets the value of the parameter to the first valid
value in a list of values. Example:  

  

Parameters
----------
* `nullTerminatedList` :  
    The list of possible values to set. The list is terminated by a NULL value.  

Returns
-------
Returns false if the parameter is not writable.  

pre: At least one value within the passed list must be contained in the set of
    settable enumeration values. \\threading The method accesses the parameter
    multiple times. These accesses are not synchronized by a lock. \\error Can
    throw exceptions if the parameter is not writable, no value
    `nullTerminatedList` is settable, or writing the value fails.  
";

%feature("docstring") Pylon::TrySetValue "

Sets the value passed if the parameter is writable and the value is contained in
the set of settable enumeration values.  

Returns
-------
Returns false if the parameter is not writable or the value is not contained in
the set of settable enumeration values.  

Parameters
----------
* `value` :  
    The value to set. \\threading The method accesses the parameter multiple
    times. These accesses are not synchronized by a lock. \\error Can throw
    exceptions if the preconditions are not met or if writing the value fails.  
";

%feature("docstring") Pylon::TrySetValue "

Sets the value of the parameter if the parameter is writable.  

The value must be in the valid range and the increment must be correct.  

Returns
-------
Returns false if the parameter is not writable.  

Parameters
----------
* `value` :  
    The value to set.  

If the float parameter has an increment, the increment is automatically
corrected.  

pre:  

    *   The passed value must be >= GenApi::IFloat::GetMin().  
    *   The passed value must be <= GenApi::IFloat::GetMax().  

    \\threading The method accesses the parameter multiple times. These accesses
    are not synchronized by a lock. \\error Can throw exceptions if the
    preconditions are not met or if writing the value fails.  
";

%feature("docstring") Pylon::TrySetValue "

Sets the value of the parameter if the parameter is writable and readable.  

The value is automatically corrected if needed.  

Returns
-------
Returns false if the parameter is not readable or not writable.  

Parameters
----------
* `value` :  
    The value to set.  
* `correction` :  
    The correction method.  

note: Calls TrySetValue(GenApi::IFloatParameter, double) if `correction` equals
    FloatValueCorrection_None. \\threading The method accesses the parameter
    multiple times. These accesses are not synchronized by a lock. \\error Can
    throw exceptions if writing the value fails.  
";

%feature("docstring") Pylon::TrySetValue "

Sets the value of the parameter if the parameter is writable.  

The value must be in the valid range and the increment must be correct.  

Returns
-------
Returns false if the parameter is not writable.  

Parameters
----------
* `value` :  
    The value to set.  

pre:  

    *   The passed value must be >= GenApi::IInteger::GetMin().  
    *   The passed value must be <= GenApi::IInteger::GetMax().  
    *   The passed value must be aligned to the increment returned by
        GenApi::IInteger::GetInc().  

    \\threading The method accesses the parameter multiple times. These accesses
    are not synchronized by a lock. \\error Can throw exceptions if the
    preconditions are not met or if writing the value fails.  
";

%feature("docstring") Pylon::TrySetValue "

Sets the value of the parameter if the parameter is writable and readable.  

The value is automatically corrected if needed.  

Returns
-------
Returns false if the parameter is not readable or not writable.  

Parameters
----------
* `value` :  
    The value to set.  
* `correction` :  
    The correction method.  

note: Calls TrySetValue(GenApi::IInteger*, int64_t) if `correction` equals
    IntegerValueCorrection_None. \\threading The method accesses the parameter
    multiple times. These accesses are not synchronized by a lock. \\error Can
    throw exceptions if writing the value fails.  
";

%feature("docstring") Pylon::GetValueOrDefault "

Gets the Boolean value of the parameter if the parameter is readable.  

Otherwise returns the default value.  

Returns
-------
Returns the parameter value if the parameter is readable. Otherwise returns the
default value.  

Parameters
----------
* `defaultValue` :  
    The default value returned if the parameter is not readable. \\threading The
    method accesses the parameter multiple times. These accesses are not
    synchronized by a lock. \\error Can throw exceptions if reading the value
    fails.  
";

%feature("docstring") Pylon::GetValueOrDefault "

Gets the value of the parameter if the parameter is readable. Otherwise returns
the default value.  

Returns
-------
Returns the parameter value if the parameter is readable. Otherwise returns the
default value.  

Parameters
----------
* `defaultValue` :  
    The default value returned if the parameter is not readable. \\threading The
    method accesses the parameter multiple times. These accesses are not
    synchronized by a lock. \\error Can throw exceptions if reading the value
    fails.  

Returns
-------
Returns the value of the parameter if the parameter is readable. Otherwise
returns the default value.  

Parameters
----------
* `defaultValue` :  
    The default value returned if the parameter is not readable. \\threading The
    method accesses the parameter multiple times. These accesses are not
    synchronized by a lock. \\error Can throw exceptions if reading the value
    fails.  
";

%feature("docstring") Pylon::GetValueOrDefault "

Gets the parameter value if the parameter is readable. Otherwise returns the
default value.  

Returns
-------
Returns the parameter value if the parameter is readable. Otherwise returns the
default value.  

Parameters
----------
* `defaultValue` :  
    The default value returned if the parameter is not readable. \\threading The
    method accesses the parameter multiple times. These accesses are not
    synchronized by a lock. \\error Can throw exceptions if reading the value
    fails.  
";

%feature("docstring") Pylon::GetValueOrDefault "

Gets the value of the parameter if the parameter is readable.  

Otherwise returns the default value.  

Returns
-------
Returns the parameter value if the parameter is readable. Otherwise returns the
default value.  

Parameters
----------
* `defaultValue` :  
    The default value returned if the parameter is not readable. \\threading The
    method accesses the parameter multiple times. These accesses are not
    synchronized by a lock. \\error Can throw exception if reading the value
    fails.  
";

%feature("docstring") Pylon::GetValueOrDefault "

Gets the value of the parameter if the parameter is readable.  

Otherwise returns the default value.  

Returns
-------
Returns the parameter value if the parameter is readable. Otherwise returns the
default value.  

Parameters
----------
* `defaultValue` :  
    The default value returned if the parameter is not readable. \\threading The
    method accesses the parameter multiple times. These accesses are not
    synchronized by a lock. \\error Can throw exception if reading the value
    fails.  
";

%feature("docstring") Pylon::AllocateBuffer "

Allocates a buffer and provides additional context information.  

Parameters
----------
* `bufferSize` :  
    The size of the buffer that has to be allocated.  
* `pCreatedBuffer` :  
    Return the pointer to the allocated buffer. May return NULL if the
    allocation fails.  
* `bufferContext` :  
    Context information that belongs to the buffer. This context information is
    provided when FreeBuffer() is called. The value can be left unchanged if not
    needed.  

\\threading This method can be run by different threads. It is called from
threads that call Pylon::CInstantCamera::StartGrabbing() and it can be called by
the internal grab engine thread.  

\\error May throw an exception if the allocation fails.  
";

%feature("docstring") Pylon::FreeBuffer "

Frees a previously allocated buffer.  

Parameters
----------
* `pCreatedBuffer` :  
    The pointer to the allocated buffer. Created by this factory.  
* `bufferContext` :  
    Context information of the buffer returned by AllocateBuffer().  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::DestroyBufferFactory "

Destroys the buffer factory.  

This method is called when the buffer factory is not needed any longer. The
object implementing IBufferFactory can be deleted by calling: delete this.  

\\threading This method can be run by different threads. It is called from
threads that are running the destructor of a Pylon::CGrabResultPtr or call
Pylon::CInstantCamera::StopGrabbing().  

\\error C++ exceptions from this call will be caught and ignored.  
";

%feature("docstring") Pylon::make_FunctionCallback "
";

%feature("docstring") Pylon::make_MemberFunctionCallback "
";

%feature("docstring") Pylon::DetachBuffer "

Detaches a buffer from the chunk parser. The buffer will no longer accessed by
the chunk parser.  

An attached buffer must be detached before freeing it. When attaching a new
buffer, the previous one gets detached automatically.  
";

%feature("docstring") Pylon::UpdateBuffer "

Pass in a buffer and let the chunk parser update the camera object's parameters.  

This method can be used when the layout of the chunk data hasn't changed since a
previous buffer has been attached to the chunk parser. In this case UpdateBuffer
is slightly faster than AttachBuffer, because the buffer's layout is reused. If
you call UpdateBuffer without having called AttachBuffer first, a
LogicalErrorException is raised.  

Parameters
----------
* `pBaseAddress` :  
    Pointer to the new buffer  
";

%feature("docstring") Pylon::HasCRC "

Checks if buffer has a CRC attached.  

Returns
-------
true if the buffer contains CRC value.  
";

%feature("docstring") Pylon::CheckCRC "

Checks CRC sum of buffer.  

Returns
-------
true if the contained CRC equals the computed value.  
";

%feature("docstring") Pylon::Destroy "

Makes the object to destroy itself.  

This is an alternative to destroying it via the IPylonDevice interface. It is
used when the device has been destroyed already.  
";

%feature("docstring") Pylon::TryExecute "

Executes the command and returns immediately if the parameter is writable.  

Returns
-------
Returns false if the parameter is not writable. \\threading The method accesses
the parameter multiple times. These accesses are not synchronized by a lock.
\\error Can throw exceptions if accessing the camera failed.  
";

%feature("docstring") Pylon::Close "

Closes a device.  

Closes the stream grabber.  

Closes an interface.  

Close the event grabber.  

The close method closes all involved drivers and an existing connection to the
device will be released. Other applications now can access the device.  

\\threading This method is thread-safe.  

post:  

    *   The interface is closed.  
    *   Any previously acquired node map using GetNodeMap() has been deleted and
        must not be used any longer.  

\\error Does not throw C++ exceptions.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

This method calls FinishGrab() automatically if needed.  

post:  

    *   Any running grab has been stopped by calling FinishGrab().  
    *   The stream grabber is closed.  
    *   All results waiting in the output queue are discarded.  

\\threading This method is synchronized using an internal stream grabber lock.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::IsOpen "

Checks if a device already is opened.  

Retrieve whether the stream grabber is open.  

Checks if the interface is open.  

Retrieve whether the event grabber is open.  

Returns
-------
true, when the device already has been opened by the calling application.  

note: When a device has been opened an application A, IsOpen() will return false
    when called by an application B not having called the device's open method.  

note: The 'open' status of an interface instance won't change even if an
    attached camera is used, e.g., opened or closed.  

Returns
-------
Returns true if when the interface is open.  

\\threading This method is thread-safe.  

\\error Does not throw C++ exceptions.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

Returns
-------
Returns true if the stream grabber is open.  

\\threading This method can be synchronized using an internal stream grabber
lock.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::AccessMode "

Returns the access mode used to open the device.  
";

%feature("docstring") Pylon::GetDeviceInfo "

Returns the device info object storing information like the device's name.  

Returns
-------
A reference to the device info object used to create the device by a device
factory  
";

%feature("docstring") Pylon::GetStreamGrabber "

Returns a pointer to a stream grabber.  

Stream grabbers (IStreamGrabber) are the objects used to grab images from a
camera device. A camera device might be able to send image data over more than
one logical channel called stream. A stream grabber grabs data from one single
stream.  

Parameters
----------
* `index` :  
    The number of the grabber to return  

Returns
-------
A pointer to a stream grabber, NULL if index is out of range  
";

%feature("docstring") Pylon::GetEventGrabber "

Returns a pointer to an event grabber.  

Event grabbers are used to handle events sent from a camera device.  
";

%feature("docstring") Pylon::GetNodeMap "

Returns the set of camera parameters.  

Returns the GenApi node map used for accessing parameters provided by the
transport layer.  

Returns the associated stream grabber parameters.  

Returns the GenApi node map used for accessing parameters provided by the
interface.  

Return the associated event grabber parameters.  

Returns
-------
Pointer to the GenApi node map holding the parameters  

If no parameters are available, NULL is returned.  

note: The default interface object does not provide a node map.  

Returns
-------
Returns the GenApi node map used for accessing parameters provided by the
interface. If no parameters are available, NULL is returned.  

\\threading This method is thread-safe.  

\\error Can throw C++ exceptions.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

Returns
-------
Returns the associated stream grabber parameters. The returned pointer is never
NULL.  

\\threading This method can be synchronized using an internal stream grabber
lock.  

\\error Does not throw C++ exceptions.  

Returns
-------
NULL, if the transport layer doesn't provide parameters, a pointer to the
parameter node map otherwise.  
";

%feature("docstring") Pylon::GetTLNodeMap "

Returns the set of camera related transport layer parameters.  

Returns
-------
Pointer to the GenApi node holding the transport layer parameter. If there are
no transport layer parameters for the device, NULL is returned.  
";

%feature("docstring") Pylon::CreateChunkParser "

Creates a chunk parser used to update those camera object members reflecting the
content of additional data chunks appended to the image data.  

Returns
-------
Pointer to the created chunk parser  

note: Don't try to delete a chunk parser pointer by calling free or delete.
    Instead, use the DestroyChunkParser() method  
";

%feature("docstring") Pylon::DestroyChunkParser "

Deletes a chunk parser.  

Parameters
----------
* `pChunkParser` :  
    Pointer to the chunk parser to be deleted  
";

%feature("docstring") Pylon::CreateEventAdapter "

Creates an Event adapter  
";

%feature("docstring") Pylon::DestroyEventAdapter "

Deletes an Event adapter  
";

%feature("docstring") Pylon::CreateSelfReliantChunkParser "

Creates a a self-reliant chunk parser, returns NULL if not supported  
";

%feature("docstring") Pylon::DestroySelfReliantChunkParser "

Deletes a self-reliant chunk parser  
";

%feature("docstring") Pylon::RegisterRemovalCallback "

Registers a surprise removal callback object.  

Parameters
----------
* `d` :  
    reference to a device callback object  

Returns
-------
A handle which must be used to deregister a callback It is recommended to use
one of the RegisterRemovalCallback() helper functions to register a callback.  

Example how to register a C function  

Example how to register a class member function  
";

%feature("docstring") Pylon::RegisterRemovalCallback "

Low Level API: Register a C-function as a removal callback.  

See also: Pylon::IPylonDevice::RegisterRemovalCallback()  

Parameters
----------
* `pDevice` :  
    Pointer to the device that generates callbacks  
* `f` :  
    The function to be called  
";

%feature("docstring") Pylon::RegisterRemovalCallback "

Low Level API: Register a C++-member function as removal callback.  

See also: Pylon::IPylonDevice::RegisterRemovalCallback()  

Parameters
----------
* `pDevice` :  
    Pointer to the device that generates callbacks  
* `c` :  
    The client object  
* `m` :  
    The member function to be called  
";

%feature("docstring") Pylon::DeregisterRemovalCallback "

Deregisters a surprise removal callback object.  

Parameters
----------
* `h` :  
    Handle of the callback to be removed  
";

%feature("docstring") Pylon::EnumerateDevices "

Retrieves a list of available devices filtered by given properties, usable for
looking for specific devices.  

The list contains Pylon::CDeviceInfo objects used for the device creation and is
ordered by device class and serial number using the operator
Pylon::CDeviceInfo::operator<(). By default, the list will be cleared before the
device discovery is started. The filter list can contain a list of device info
objects containing properties a device must have, e.g., the user-provided name
or the serial number. A device is returned if it matches the properties of any
of the device info objects on the filter list. If the device class property is
set in the filter device info objects, the search is limited to the required
transport layers.  

Parameters
----------
* `list` :  
    List to be filled with device info objects.  
* `filter` :  
    A list of device info objects with user-provided properties that a device
    can match.  
* `addToList` :  
    If true, the devices found will be appended to the list instead of deleting
    the list. Only newly discovered devices are sorted and not the entire list.  

Returns
-------
Number of devices found.  
";

%feature("docstring") Pylon::CreateDevice "

Creates a camera object from a device info object.  

This method accepts either a device info object from a device enumeration or a
user-provided device info object. User-provided device info objects can be
preset with properties required for a device, e.g. the user-provided name or the
serial number. The implementation tries to find a matching camera by using
device enumeration. When the device class property is set, the search is limited
to the required transport layer.  

If the device creation fails, a GenApi::GenericException will be thrown.  

Parameters
----------
* `di` :  
    Device info object containing all information needed to identify exactly one
    device.  
";

%feature("docstring") Pylon::CreateDevice "

Creates a camera object from a device info object, injecting additional GenICam
XML definition strings. Currently only one injected xml string is supported.  
";

%feature("docstring") Pylon::CreateDevice "

This method is deprecated. Use CreateDevice and pass a CDeviceInfo object
containing the full name as a property. Example: IPylonDevice* device =
TlFactory.CreateDevice( CDeviceInfo().SetFullName( fullname)); creates a device
that matches its full name (i.e., as returned by CDeviceInfo::GetFullName).  
";

%feature("docstring") Pylon::CreateFirstDevice "

If multiple devices match the provided properties, the first device found is
created. The order in which the devices are found can vary from call to call.  
";

%feature("docstring") Pylon::CreateFirstDevice "

Creates the first found camera device matching the provided properties,
injecting additional GenICam XML definition strings. Currently only one injected
xml string is supported.  
";

%feature("docstring") Pylon::DestroyDevice "

Destroys a device.  

note: Never try to delete a pointer to a camera device by calling free or
    delete. Always use the DestroyDevice method.  
";

%feature("docstring") Pylon::IsDeviceAccessible "

This method can be used to check if a camera device can be created and opened.  

This method accepts either a device info object from a device enumeration or a
user-provided device info object. User-provided device info objects can be
preset with properties required for a device, e.g. the user-provided name or the
serial number. The implementation tries to find a matching camera by using
device enumeration. When the device class property is set, see DeviceClass.h
header file, the search is limited to the required transport layer. For more
information, see Applying a Filter when Enumerating Cameras.  

Parameters
----------
* `deviceInfo` :  
    Properties to find/identify the camera device to check.  
* `mode` :  
    Used for defining how a device is accessed. The use of the mode information
    is transport layer-specific.  

    *   For CameraLink, and USB devices, the mode information is ignored.  
    *   For GigE devices, the `Exclusive` and `Control` flags are used for
        defining how a device is accessed. Other mode information is ignored.  
    *   For devices of any type that are accessed via the GenICam GenTL
        transport layer, the mode is ignored.  
* `pAccessibilityInfo` :  
    Optional parameter that provides more information about whether a device is
    accessible or not.  

Returns
-------
True if device can be opened with provided access mode.  

pre: The `deviceInfo` object properties specify exactly one device. This is the
    case when the device info object has been obtained using device enumeration.  

\\error Throws a C++ exception, if the preconditions are not met.  
";

%feature("docstring") Pylon::SetValue "

Sets the value of the parameter to the first valid value in a list of values.
Example:  

  

Parameters
----------
* `nullTerminatedList` :  
    The list of possible values to set. The list is terminated by a NULL value.  

pre:  

    *   The parameter must be writable.  
    *   At least one value within the list passed must be contained in the set
        of settable enumeration values.  

    \\threading The method accesses the parameter multiple times. These accesses
    are not synchronized by a lock. \\error Can throw exceptions if the
    parameter is not writable, no value `nullTerminatedList` is settable, or
    writing the value fails.  
";

%feature("docstring") Pylon::SetValue "

Sets the value of the parameter. Calls FromString().  

Parameters
----------
* `value` :  
    The value to set.  

pre: The value must be contained in the set of settable enumeration values.
    \\threading The method accesses the parameter multiple times. These accesses
    are not synchronized by a lock. \\error Can throw exceptions if the
    parameter is not writable, no value is valid, or writing the value fails.  
";

%feature("docstring") Pylon::SetValue "

Sets the value passed.  

Parameters
----------
* `value` :  
    The value to set.  
* `verify` :  
    Enables AccessMode and Range verification (default = true). \\error Can
    throw exceptions if the parameter is not writable or if writing the value
    fails.  
";

%feature("docstring") Pylon::SetValue "

Sets the value of the parameter. The value is automatically corrected if needed.  

Parameters
----------
* `value` :  
    The value to set.  
* `correction` :  
    The correction method.  

pre:  

    *   The parameter must be writable.  
    *   The parameter must be readable.  

note: Calls GenApi::IFloatParameter::SetValue(double) if `correction` equals
    FloatValueCorrection_None. \\threading The method accesses the parameter
    multiple times. These accesses are not synchronized by a lock. \\error Can
    throw exceptions if the preconditions are not met or if writing the value
    fails.  
";

%feature("docstring") Pylon::SetValue "

Sets the value of the parameter. The value is automatically corrected if needed.  

Parameters
----------
* `value` :  
    The value to set.  
* `correction` :  
    The correction method.  

pre:  

    *   The parameter must be writable.  
    *   The parameter must be readable.  

note: Calls GenApi::IInteger::SetValue(int64_t) if `correction` equals
    IntegerValueCorrection_None. \\threading The method accesses the parameter
    multiple times. These accesses are not synchronized by a lock. \\error Can
    throw exceptions if the preconditions are not met or if writing the value
    fails.  
";

%feature("docstring") Pylon::CanSetValue "

Indicates whether the given value can be set.  

Returns
-------
Returns true if the value can be set, otherwise false.  

Parameters
----------
* `value` :  
    The value to be checked. \\threading The method accesses the parameter
    multiple times. These accesses are not synchronized by a lock. \\error Does
    not throw exceptions.  
";

%feature("docstring") Pylon::CanSetValue "

Indicates if the value passed can be set.  

Returns
-------
Returns true if the value can be set, otherwise false.  

Parameters
----------
* `value` :  
    The value to be checked. \\threading The method accesses the parameter
    multiple times. These accesses are not synchronized by a lock. \\error Does
    not throw exceptions.  
";

%feature("docstring") Pylon::GetValue "

Gets the value of the parameter.  

Returns
-------
Returns the current parameter value.  

pre: The parameter must be readable. \\threading The method accesses the
    parameter multiple times. These accesses are not synchronized by a lock.
    \\error Can throw exceptions if the parameter is not readable or if reading
    the value fails.  
";

%feature("docstring") Pylon::GetValue "

Gets the current parameter value.  

Parameters
----------
* `verify` :  
    Enables Range verification (default = false). The AccessMode is always
    checked.  
* `ignoreCache` :  
    If true, the value is read ignoring any caches (default = false).  

Returns
-------
Returns the current parameter value. \\error Can throw exceptions if the
parameter is not readable or if reading the value fails.  
";

%feature("docstring") Pylon::GetSettableValues "

Gets a list of all values of the enumeration that are currently settable.  

Parameters
----------
* `values` :  
    Returns a list of all values of the enumeration that are currently settable.  

pre: The parameter must be readable. \\threading The method accesses the
    parameter multiple times. These accesses are not synchronized by a lock.
    \\error Can throw exceptions.  
";

%feature("docstring") Pylon::GetAllValues "

Gets a list of all values of the enumeration including the values that are
currently not settable.  

Parameters
----------
* `values` :  
    Returns a list of all values of the enumeration including the values that
    are currently not settable.  

pre: The parameter must be readable. \\threading The method accesses the
    parameter multiple times. These accesses are not synchronized by a lock.
    \\error Can throw exceptions.  
";

%feature("docstring") Pylon::GetEntryByNameAsParameter "

Gets an enumeration entry by its symbolic name. The entry is returned as a
CParameter. This method can be used to access information about the enumeration
value represented by the entry using CParameter::GetInfo().  

Parameters
----------
* `value` :  
    The symbolic name of the enumeration entry, e.g., \"Testimage1\".  

pre: The parameter must be readable. \\threading The method accesses the
    parameter multiple times. These accesses are not synchronized by a lock.
    \\error Can throw exceptions.  
";

%feature("docstring") Pylon::GetCurrentEntryAsParameter "

Gets the currently selected entry of an enumeration. The entry is returned as a
CParameter. This method can be used to access information about the enumeration
value represented by the entry using CParameter::GetInfo().  

pre: The parameter must be readable. \\threading The method accesses the
    parameter multiple times. These accesses are not synchronized by a lock.
    \\error Can throw exceptions.  
";

%feature("docstring") Pylon::GetEntry "

Returns the EnumEntry object belonging to the value.  
";

%feature("docstring") Pylon::~IEventAdapter "
";

%feature("docstring") Pylon::RetrieveEvent "

Retrieve an event message from the output queue.  

Returns
-------
When the event was available true is returned and the event message is copied
into the EventResult.  
";

%feature("docstring") Pylon::GetWaitObject "

Return the event object associated with the grabber.  

Returns the result event object of the stream grabber.  

This object get signaled as soon as a event has occurred. It will be reset when
the output queue is empty.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

This object is associated with the output queue of the stream grabber. The event
is signaled when output queue is non-empty.  

Returns
-------
Returns the result event object of the stream grabber.  

\\threading This method can be synchronized using an internal stream grabber
lock.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::GetValuePercentOfRange "

Gets the value of the parameter in percent of its value range (from minimum to
maximum).  

Returns
-------
Returns the parameter value in percent of its value range. Returns 100 if
minimum equals maximum.  

pre: The parameter must be readable. \\threading The method accesses the
    parameter multiple times. These accesses are not synchronized by a lock.
    \\error Can throw exceptions if writing the value fails.  
";

%feature("docstring") Pylon::SetValuePercentOfRange "

Sets the value of the parameter to a value within its range, using this formula
(simplified): ((max - min) * (percentOfRange / 100.0)) + min.  

Parameters
----------
* `percentOfRange` :  
    The percentage of the range to be used in the calculation.  

pre:  

    *   The parameter must be writable.  
    *   The parameter must be readable.  

    \\threading The method accesses the parameter multiple times. These accesses
    are not synchronized by a lock. \\error Can throw exceptions if writing the
    value fails.  

The value is always corrected to the nearest valid value.  

Parameters
----------
* `percentOfRange` :  
    The percentage of the range to be used in the calculation.  

The parameter must be writable.  

pre:  

    *   The parameter must be writable.  
    *   The parameter must be readable.  

    \\threading The method accesses the parameter multiple times. These accesses
    are not synchronized by a lock. \\error Can throw exceptions if writing the
    value fails.  
";

%feature("docstring") Pylon::TrySetValuePercentOfRange "

If the parameter is writable and readable, sets the value of the parameter to a
value within its range, using this formula (simplified): ((max - min) *
(percentOfRange / 100.0)) + min.  

Returns
-------
Returns true if the value has been set.  

Parameters
----------
* `percentOfRange` :  
    The percentage of the range used in the calculation. Valid values are in the
    range of 0 to 100. \\threading The method accesses the parameter multiple
    times. These accesses are not synchronized by a lock. \\error Can throw
    exceptions if writing the value fails.  

The value is always corrected to the nearest valid value.  

Returns
-------
Returns true if the a value has been set.  

Parameters
----------
* `percentOfRange` :  
    The percentage of the range to be used in the calculation. \\threading The
    method accesses the parameter multiple times. These accesses are not
    synchronized by a lock. \\error Can throw exceptions if writing the value
    fails.  
";

%feature("docstring") Pylon::SetToMaximum "

Sets the parameter value to the maximum possible value.  

Sets the value of the parameter to the maximum possible value.  

pre:  

    *   The parameter must be writable.  
    *   The parameter must be readable.  

    \\threading The method accesses the parameter multiple times. These accesses
    are not synchronized by a lock. \\error Can throw exceptions if the
    parameter is not writable, not readable, or if reading or writing fails.  
";

%feature("docstring") Pylon::SetToMinimum "

Sets the parameter value to the minimum possible value.  

Sets the value of the parameter to the minimum possible value.  

pre:  

    *   The parameter must be writable.  
    *   The parameter must be readable.  

    \\threading The method accesses the parameter multiple times. These accesses
    are not synchronized by a lock. \\error Can throw exceptions if the
    parameter is not writable, not readable, or if reading or writing fails.  
";

%feature("docstring") Pylon::TrySetToMaximum "

Sets the parameter value to the maximum possible value if the parameter is
readable and writable.  

Sets the value of the parameter to the maximum possible value if the parameter
is readable and writable.  

Returns
-------
Returns true if the maximum value has been set. \\threading The method accesses
the parameter multiple times. These accesses are not synchronized by a lock.
\\error Can throw exceptions if reading or writing fails.  
";

%feature("docstring") Pylon::TrySetToMinimum "

Sets the parameter value to the minimum possible value if the parameter is
readable and writable.  

Sets the value of the parameter to the minimum possible value if the parameter
is readable and writable.  

Returns
-------
Returns true if the minimum value has been set. \\threading The method accesses
the parameter multiple times. These accesses are not synchronized by a lock.
\\error Can throw exceptions if reading or writing fails.  
";

%feature("docstring") Pylon::GetAlternativeIntegerRepresentation "

Gets the alternative integer representation of the float parameter, if
available. The alternative integer representation is typically used if a
parameter is represented as a float value in the node map, but as an integer
register in the camera device.  

Parameters
----------
* `parameter` :  
    The integer representation returned. The returned value will be empty if no
    alternative representation is available. \\threading The method accesses the
    parameter multiple times. These accesses are not synchronized by a lock.
    \\error Can throw exceptions.  
";

%feature("docstring") Pylon::GetPropertyAvailable "

Returns true if a property with the provided name is available.  
";

%feature("docstring") Pylon::GetPropertyValue "

Retrieves a property value.  
";

%feature("docstring") Pylon::SetPropertyValue "

Modifies a property value.  
";

%feature("docstring") Pylon::IsSubset "

Returns true if all properties of the subset can be found and the values are
equal The implementing container may use special knowledge on how to compare the
values For instance for IP adresses, 192.2.3.45 == 192.2.3.0x2D  
";

%feature("docstring") Pylon::GetInterfaceInfo "

Returns the interface info object storing information like the Interface ID
property.  

This information is available at all times regardless of whether the interface
is open or closed.  

Returns
-------
A reference to the interface info object.  

\\threading This method is thread-safe.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::IsWritable "

Indicates whether the parameter is writable. \\error Does not throw C++
exceptions.  

Returns
-------
Returns true if the parameter is writable.  
";

%feature("docstring") Pylon::GetInfo "

Gets the parameter information.  

Parameters
----------
* `info` :  
    The type information to return.  

Returns
-------
Returns the parameter information. \\threading The method accesses the parameter
multiple times. These accesses are not synchronized by a lock. \\error Throws an
exception if no node is attached. Can throw exceptions if the retrieval of the
information fails.  
";

%feature("docstring") Pylon::GetInfoOrDefault "

Gets the parameter information if the parameter is attached to a node. See
IsValid().  

Parameters
----------
* `info` :  
    The type information to return.  

Otherwise returns the default information. This method is useful if you want to
display parameter information and handle the case that some parameters are not
available for a device.  

Returns
-------
Returns the parameter information if the parameter is attached to a node.
Otherwise returns the default information.  

Parameters
----------
* `defaultInfo` :  
    The default information returned if the parameter is not attached to a node.
    \\threading The method accesses the parameter multiple times. These accesses
    are not synchronized by a lock. \\error Can throw exceptions if the
    retrieval of the information fails.  
";

%feature("docstring") Pylon::ToStringOrDefault "

Gets the parameter value as string if the parameter is readable.  

Otherwise returns the default value.  

Returns
-------
Returns the parameter value if the parameter is readable. Otherwise returns the
default value.  

Parameters
----------
* `defaultValue` :  
    The default value returned if the parameter is not readable. \\threading The
    method accesses the parameter multiple times. These accesses are not
    synchronized by a lock. \\error Can throw exceptions if reading the value
    fails.  
";

%feature("docstring") Pylon::PylonInitialize "

Initializes the pylon runtime system.  

You must call PylonInitialize before calling any other pylon functions. When
finished you must call PylonTerminate to free up all resources used by pylon.  

You can use the helperclass PylonAutoInitTerm to let the compiler call
PylonInitialze and PylonTerminate.  

Just create a local object on the stack in your main function and the
constructor and destructor will call the functions. See PylonAutoInitTerm for a
sample.  

PylonInitialize/PylonTerminate is reference counted. For every call of
PylonInitialize, a call to PylonTerminate is required. The last call to
PylonTerminate will free up all resources.  
";

%feature("docstring") Pylon::PylonTerminate "

Frees up resources allocated by the pylon runtime system.  

Call this function before terminating the application. Don't use any pylon
methods or pylon objects after having called PylonTerminate().  

PylonInitialize/PylonTerminate is reference counted. For every call of
PylonInitialize, a call to PylonTerminate is required. The last call to
PylonTerminate will free up all resources.  
";

%feature("docstring") Pylon::GetPylonVersion "

Returns the version number of pylon.  

It is possible to pass a NULL pointer for a version number category if the value
is not of interest.  
";

%feature("docstring") Pylon::GetPylonVersionString "

Returns the version number of pylon as string.  
";

%feature("docstring") Pylon::SetProperty "

Set the value of a property.  

Parameters
----------
* `propertyId` :  
    Identifies the property.  
* `pData` :  
    A pointer to the buffer containing the data.  
* `size` :  
    Size of the buffer in bytes.  

Call this function to set the value of a property.  

You must have called PylonInitialize() before you can call this function.  
";

%feature("docstring") Pylon::GetProperty "

Get the value of a property.  

Parameters
----------
* `propertyId` :  
    Identifies the property.  
* `pData` :  
    A pointer to the buffer containing the data.  
* `pSize` :  
    Size of the buffer in bytes when calling. Holds the resulting size on
    return.  

Call this function to get the value of a property.  

You must have called PylonInitialize() before you can call this function.  
";

%feature("docstring") Pylon::GetSfncVersion "

Helper function for getting the SFNC version from the camera device node map.  
";

%feature("docstring") Pylon::RegisterBuffer "

Registers a buffer for subsequent use.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

Parameters
----------
* `pBuffer` :  
    The pointer of the buffer that is to be used for grabbing e.g., for grabbing
    images.  
* `bufferSize` :  
    The size of the provided buffer in bytes.  

Returns
-------
Returns a handle for the registered buffer that can be used in subsequent calls.  

pre:  

    *   pBuffer must not be NULL.  
    *   The buffer size must not exceed the value of the node map integer
        parameter MaxBufferSize specified when PrepareGrab was called.  
    *   Less buffers are already registered than value of the node map integer
        parameter MaxNumBuffer specified when PrepareGrab was called.  
    *   The stream grabber is prepared, see PrepareGrab().  
    *   The buffer has not been registered already.  

post:  

    *   The buffer is registered.  
    *   Transport Layer specific preparations have been executed e.g., locking
        the memory pages of the buffer.  
    *   The buffer must not be freed while being registered.  
    *   If the stream grabber requires the additional streaming state, streaming
        must not be started, see IsStartAndStopStreamingMandatory() and
        StartStreamingIfMandatory().  

\\threading This method can be synchronized using an internal stream grabber
lock.  

\\error  

*   Throws a LogicalErrorException if the stream grabber state does not match
    the preconditions.  
*   Throws an exception if registering the buffer fails. The buffer is not
    registered after raising an exception.  
";

%feature("docstring") Pylon::DeregisterBuffer "

Deregisters the buffer.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

Parameters
----------
* `hStreamBuffer` :  
    The handle of a buffer that has been provided by RegisterBuffer()  

Returns
-------
Returns the pointer of the corresponding buffer.  

pre:  

    *   The buffer is registered.  
    *   The buffer is not queued. Either it has not been queued yet, see
        QueueBuffer(), or it has been retrieved after grabbing using
        RetrieveResult().  
    *   FinishGrab() or Close() have not been called for the grab session yet.  
    *   If the stream grabber requires the additional streaming state, streaming
        must not be started, see IsStartAndStopStreamingMandatory() and
        StartStreamingIfMandatory().  

post:  

    *   Transport layer-specific preparations have been reversed.  
    *   The buffer is deregistered.  
    *   The buffer can be freed if needed e.g., by calling delete.  

\\error Throws an exception if deregistering the buffer fails.  
";

%feature("docstring") Pylon::PrepareGrab "

Prepares grabbing.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

note: pylon uses a pool of buffers with a fixed amount of buffers to grab
    images. This is required because certain preparations e.g., locking the
    buffer's memory pages, must be made by the driver to be able to grab images
    into a buffer. Thus, using a pool of buffers is much more efficient than
    allocating a new buffer for every grabbed image.  

The node map integer parameters MaxBufferSize and MaxNumBuffer need to be set
before calling PrepareGrab().  

MaxNumBuffer should be set to the number of buffers you plan to use for
grabbing.  

note: There can be limitations depending on the transport layer technology used
    when using a large amount of buffers.  

MaxBufferSize needs to be set according to the PayloadSize parameter of the
camera device or the stream grabber. If the stream grabber provides a
PayloadSize parameter, the MaxBufferSize must be at least the size reported by
the stream grabber payload size. This is the case if for instance a frame
grabber or additional preprocessing is used. If the stream grabber does not
provide a PayloadSize parameter, the MaxBufferSize must be at least the size
reported by the camera device PayloadSize parameter.  

pre:  

    *   The node map integer parameter MaxBufferSize is set, see GetNodeNap().  
    *   The node map integer parameter MaxNumBuffer is set, see GetNodeNap().  
    *   The stream grabber is open.  
    *   No grab session is currently in progress.  

post:  

    *   Resources required for grabbing are allocated.  
    *   The camera is set up for grabbing.  
    *   Critical camera parameters, provided by IPylonDevice::GetNodeMap(), are
        locked.  
    *   The stream grabber is prepared.  

\\threading This method is synchronized using an internal stream grabber lock.  

\\error  

*   Throws a LogicalErrorException if the stream grabber state does not match
    the preconditions.  
*   Throws an exception if preparing the stream grabber fails. The stream
    grabber is not prepared after raising the exception.  
";

%feature("docstring") Pylon::IsStartAndStopStreamingMandatory "

Returns true if the Stream Grabber requires calling StartStreamingIfMandatory()
for operation.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

\\threading This method is synchronized using an internal stream grabber lock.  

\\error Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::StartStreamingIfMandatory "

Starts streaming for the stream grabber if this is mandatory for operation.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

Some stream grabbers e.g., some stream grabbers based on GenTL, have limitations
on when buffers can be registered. For these stream grabbers it is mandatory to
register all buffers first and call StartStreamingIfMandatory() aftwards.
Between the StartStreamingIfMandatory() and StopStreamingIfMandatory() calls no
buffers can be registered or deregistered if such a limitation exists.  

note: This method has been added in pylon 6.0 for supporting CoaXPress. Prior
    implementations of pylon stream grabbers did not require calling start and
    stop streaming. The IsStartAndStopStreamingMandatory(),
    StartStreamingIfMandatory(), and StopStreamingIfMandatory() methods allow
    backward-compatible operation.  

pre:  

    *   The stream grabber is prepared.  

post:  

    *   If the stream grabber does not require StartStreamingIfMandatory(),
        nothing is done.  
    *   Streaming is started. For GenTL-based stream grabbers DSStartAcquistion
        is called  

\\threading This method is synchronized using an internal stream grabber lock.  

\\error  

*   Throws a LogicalErrorException if the stream grabber state does not match
    the preconditions.  
*   Throws an exception if start streaming fails. The stream grabber is not
    streaming after raising the exception.  
";

%feature("docstring") Pylon::StopStreamingIfMandatory "

Stops streaming for the stream grabber if this is mandatory for operation.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

Some stream grabbers e.g., some stream grabbers based on GenTL, have limitations
on when buffers can be registered. For these stream grabbers it is mandatory to
call StopStreamingIfMandatory to be able to deregister buffer afterwards.  

pre:  

    *   The stream grabber is in streaming mode if start and stop streaming is
        mandatory.  

post:  

    *   If the stream grabber does not require StopStreamingIfMandatory(),
        nothing is done.  
    *   Streaming is stopped. For GenTL-based stream grabbers DSStopAcquistion
        is called.  

\\threading This method is synchronized using an internal stream grabber lock.  

\\error  

*   Throws a LogicalErrorException if the stream grabber state does not match
    the preconditions.  
*   Throws an exception if stop streaming fails. The stream grabber is not
    streaming after raising the exception.  
";

%feature("docstring") Pylon::FinishGrab "

Stops grabbing finally.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

This method calls FlushBuffersToOutput() automatically if needed.  

pre:  

    *   The stream grabber is prepared.  

post:  

    *   Resources required for grabbing are freed.  
    *   The camera is not set up for grabbing anymore  
    *   Critical camera parameters, provided by IPylonDevice::GetNodeMap(), are
        unlocked.  
    *   The stream grabber is open.  
    *   Queued buffers are available in the output queue of the stream grabber
        and can be retrieved calling RetrieveResult().  
    *   All buffers are deregistered.  

\\threading This method is synchronized using an internal stream grabber lock.  

\\error  

*   Throws a LogicalErrorException if the stream grabber state does not match
    the preconditions.  
*   Throws an exception if finishing the grab fails. The stream grabber is in
    open state after raising the exception.  
";

%feature("docstring") Pylon::QueueBuffer "

Enqueues a buffer in the input queue.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

Parameters
----------
* `hStreamBuffer` :  
    The handle of a buffer that has been provided by RegisterBuffer().  
* `pContext` :  
    A user-provided pointer passed along with buffer in the internal input and
    output queues.  

pre:  

    *   The buffer is registered, see RegisterBuffer().  
    *   The stream grabber is prepared.  
    *   The buffer has not been queued for grabbing yet.  
    *   The buffer is not waiting in the output queue of the stream grabber. The
        buffer can be queued again after it has been retrieved using
        RetrieveResult().  

post:  

    *   The buffer is queued to input queue of the stream grabber.  
    *   The buffer cannot be deregistered until it has been retrieved using
        RetrieveResult().  

\\threading This method is synchronized using an internal stream grabber lock.  

\\error  

*   Throws a LogicalErrorException if the stream grabber state does not match
    the preconditions.  
*   Throws an exception if queuing the buffer fails.  
";

%feature("docstring") Pylon::FlushBuffersToOutput "

Cancels grabbing the current buffer and flushes all buffers to the output queue.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

pre:  

    *   The stream grabber is prepared.  

post:  

    *   All queued buffers are placed in the output queue of the stream grabber
        and can be retrieved using RetrieveResult().  
    *   Buffers that have not been grabbed completely before calling
        FlushBuffersToOutput are marked with the EGrabStatus Canceled.  
    *   The stream grabber is prepared.  
    *   Buffers can be queued again to continue grabbing.  

\\threading This method is synchronized using an internal stream grabber lock.  

\\error  

*   Throws a LogicalErrorException if the stream grabber state does not match
    the preconditions.  
*   Throws an exception if canceling the grab fails.  
";

%feature("docstring") Pylon::CancelGrab "

This method has been renamed to FlushBuffersToOutput(). Calling CancelGrab calls
FlushBuffersToOutput();.  
";

%feature("docstring") Pylon::RetrieveResult "

Retrieves one grab result from the output queue.  

note: Basler recommends using one of the Instant Camera classes
    CBaslerUniversalInstantCamera or CInstantCamera for new projects. If you
    want to control which buffers are used for grabbing, you can use the
    Pylon::IBufferFactory.  

param[out] grabResult The object the grab result data is returned in if true is
returned. The `grabResult` remains unchanged if false is returned.  

Returns
-------
Returns true when result was available.  

pre:  

    *   The stream grabber is open.  

post:  

    *   If a grab result was available, it has been removed from the ouput
        queue.  
    *   The corresponding buffer can be queued again for grabbing.  

\\threading This method is synchronized using an internal stream grabber lock.  

\\error  

*   Throws a LogicalErrorException if the stream grabber state does not match
    the preconditions.  
*   Throws an exception if retrieving the result fails. This does not change the
    stream grabber state.  
";

%feature("docstring") Pylon::GetRTThreadPriorityCapabilities "

Queries the range of allowed thread priorities.  
";

%feature("docstring") Pylon::GetRTThreadPriority "

Indicates the current thread priority of a thread.  
";

%feature("docstring") Pylon::SetRTThreadPriority "

Allows to set the realtime thread priority of a thread.  

Typically a thread that receives image data should be set to realtime thread
priorities to reduce jitter and delays. Be aware that such a realtime thread
shouldn't perform time consuming tasks (like image processing). A realtime
thread that is continuously working can cause the whole operating system to be
blocked!  
";

%feature("docstring") Pylon::GetCurrentThreadHandle "

Get current running thread handle.  

This wrapper method return the handle of the current running thread.  
";

%feature("docstring") Pylon::GetCurrentThreadIdentifier "

Get current running thread id.  

This wrapper method return the id of the current running thread.  
";

%feature("docstring") Pylon::CreateDeviceInfo "

Creates and returns an 'empty' Device Info object appropriate for the transport
layer.  

Device Info objects returned by the CreateDeviceInfo() method are used to create
devices from device info objects that are not the result of a device enumeration
process but are provided by the user. The user is responsible for filling in the
fields of the Device Info object that are needed to identify and create a
device.  

Example: To open a GigE device for which the IP address is known, the user lets
the Transport Layer object create a Device Info object, specifies the IP address
and passes the device info object to the CreateDevice() method.  
";

%feature("docstring") Pylon::EnumerateInterfaces "

Retrieves a list of available interfaces. An interface may represent a frame
grabber board, a network card, etc.  

note: Currently, this method is used mainly for the pylon GenTL Consumer
    transport layer, which is used for CoaXPress, for example. All other pylon
    transport layers return one default interface. The default interface will
    forward all IDeviceFactory methods to the transport layer that created the
    interface object. The default interface does not provide a node map.  

Parameters
----------
* `list` :  
    The list to be filled with interface info objects. The list contains
    Pylon::CInterfaceInfo objects used for the interface creation. It is ordered
    by device class and interface ID using the operator
    Pylon::CInterfaceInfo::operator<().  
* `addToList` :  
    If true, devices found will be added to the list instead of clearing the
    list. By default, the list passed in will be cleared.  

Returns
-------
Number of interfaces provided by the transport layer.  

\\threading This method is thread-safe.  

\\error Can throw C++ exceptions.  
";

%feature("docstring") Pylon::CreateInterface "

Creates an interface object from an interface info object.  

Parameters
----------
* `interfaceInfo` :  
    The Interface info object. You can pass an interface info object returned by
    EnumerateInterfaces() or a user-provided interface info object. User-
    provided interface info objects can be preset with properties required for
    an interface, e.g. the interface ID. The implementation tries to find a
    matching interface.  

Returns
-------
Returns the pointer to the interface created.  

post: The interface created must be freed by calling DestroyInterface(). The
    transport layer is not destroyed as long as the interface is not destroyed.
    Never try to delete a pointer to an interface object by calling free or
    delete. Always use the DestroyInterface() method.  

\\error Throws an exception if creating the interface fails.  

\\threading This method is thread-safe.  
";

%feature("docstring") Pylon::DestroyInterface "

Destroys an interface.  

Parameters
----------
* `pInterface` :  
    The pointer to an interface created by this transport layer.  

pre: The interface has been created by this transport layer using
    CreateInterface() and has not been destroyed using DestroyInterface() yet.  

post: The interface is deleted and must not be used any longer.  

\\error Throws a C++ exception if the preconditions are not met.  

\\threading This method is thread-safe.  
";

%feature("docstring") Pylon::ProvideXmlFile "
";

// File: namespace_pylon_1_1_key.xml

// File: namespace_pylon_1_1_pylon_private.xml

// File: namespace_pylon_1_1_t_l_type.xml

// File: _acquire_continuous_configuration_8h.xml

// File: _acquire_single_frame_configuration_8h.xml

// File: _array_parameter_8h.xml

// File: _avi_compression_options_8h.xml

// File: _avi_writer_8h.xml

// File: _basler_universal_camera_event_handler_8h.xml

// File: _basler_universal_configuration_event_handler_8h.xml

// File: _basler_universal_grab_result_data_8h.xml

// File: _basler_universal_grab_result_ptr_8h.xml

// File: _basler_universal_image_event_handler_8h.xml

// File: _basler_universal_instant_camera_8h.xml

// File: _basler_universal_instant_camera_array_8h.xml

// File: _boolean_parameter_8h.xml

// File: _buffer_factory_8h.xml

// File: _callback_8h.xml

// File: _camera_event_handler_8h.xml

// File: _chunk_parser_8h.xml

// File: _command_parameter_8h.xml

// File: _configuration_event_handler_8h.xml

// File: _configuration_helper_8h.xml

// File: _container_8h.xml

// File: _device_8h.xml

// File: _device_access_mode_8h.xml

// File: _device_class_8h.xml

// File: _device_factory_8h.xml

// File: _device_info_8h.xml

// File: _e_cleanup_8h.xml

// File: _enum_parameter_8h.xml

// File: _enum_parameter_t_8h.xml

// File: _e_registration_mode_8h.xml

// File: _e_timeout_handling_8h.xml

// File: _event_adapter_8h.xml

// File: _event_grabber_8h.xml

// File: _event_grabber_proxy_8h.xml

// File: _feature_persistence_8h.xml

// File: _float_parameter_8h.xml

// File: _grab_result_data_8h.xml

// File: _grab_result_ptr_8h.xml

// File: _image_8h.xml

// File: _image_decompressor_8h.xml

// File: _image_event_handler_8h.xml

// File: _image_format_converter_8h.xml

// File: _image_persistence_8h.xml

// File: _info_8h.xml

// File: _instant_camera_8h.xml

// File: _instant_camera_array_8h.xml

// File: _instant_interface_8h.xml

// File: _integer_parameter_8h.xml

// File: _interface_8h.xml

// File: _interface_info_8h.xml

// File: _node_map_proxy_8h.xml

// File: _parameter_8h.xml

// File: _parameter_includes_8h.xml

// File: _payload_type_8h.xml

// File: _pixel_8h.xml

// File: _pixel_data_8h.xml

// File: _pixel_type_8h.xml

// File: _pixel_type_mapper_8h.xml

// File: _platform_8h.xml

// File: _pylon_base_8h.xml

// File: _pylon_bitmap_image_8h.xml

// File: _pylon_data_component_8h.xml

// File: _pylon_data_container_8h.xml

// File: _pylon_device_proxy_8h.xml

// File: _pylon_g_u_i_8h.xml

// File: _pylon_g_u_i_includes_8h.xml

// File: _pylon_image_8h.xml

// File: _pylon_image_base_8h.xml

// File: _pylon_image_user_buffer_event_handler_8h.xml

// File: _pylon_includes_8h.xml

// File: _pylon_linkage_8h.xml

// File: _pylon_utility_8h.xml

// File: _pylon_utility_includes_8h.xml

// File: _pylon_version_8h.xml

// File: _pylon_version_info_8h.xml

// File: _pylon_version_number_8h.xml

// File: _result_8h.xml

// File: _result_image_8h.xml

// File: _reusable_image_8h.xml

// File: _sfnc_version_8h.xml

// File: _shared_byte_buffer_8h.xml

// File: _software_trigger_configuration_8h.xml

// File: _static_defect_pixel_8h.xml

// File: _static_defect_pixel_correction_8h.xml

// File: stdinclude_8h.xml

// File: _stream_grabber_8h.xml

// File: _stream_grabber_proxy_8h.xml

// File: _string_parameter_8h.xml

// File: _thread_priority_8h.xml

// File: _tl_factory_8h.xml

// File: _tl_info_8h.xml

// File: _transport_layer_8h.xml

// File: _type_mappings_8h.xml

// File: _video_writer_8h.xml

// File: _wait_object_8h.xml

// File: _wait_objects_8h.xml

// File: _xml_file_provider_8h.xml

// File: group___pylon___instant_camera_api_generic.xml

// File: group___pylon___image_handling_support.xml

// File: group___pylon___instant_camera_api_universal.xml

// File: group___pylon___transport_layer.xml

// File: dir_fda5dbd265c4e0b31f39462b7177e062.xml

// File: dir_e6bb53534ac0e427887cf7a94c0c004e.xml

// File: dir_8a53cb3417c421d6e22675e810326db9.xml

// File: dir_4792e202dce0fa56dddef38746dee659.xml

// File: dir_f1243e97fe9b0c5516b3fd6668bdc794.xml

// File: dir_9f6818100ef0bcd1ba470133c65fb9cb.xml

// File: dir_608b79222d5ce563a8d650dbeba257e3.xml

