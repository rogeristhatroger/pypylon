from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon, genicam
import unittest


class NodeMapWrapperTestSuite(PylonEmuTestCase):
    def test_instantcamera_wrappers_present(self):
        """InstantCamera uses INodeMapWrapper for its parameters"""
        camera = self.create_first()
        camera.Open()

        self.assertIsInstance(camera.GetNodeMap(), pylon.INodeMapWrapper)
        self.assertIsInstance(camera.GetTLNodeMap(), pylon.INodeMapWrapper)
        self.assertIsInstance(camera.GetStreamGrabberNodeMap(), pylon.INodeMapWrapper)
        self.assertIsInstance(camera.GetEventGrabberNodeMap(), pylon.INodeMapWrapper)
        self.assertIsInstance(camera.GetInstantCameraNodeMap(), pylon.INodeMapWrapper)
        self.assertIsInstance(camera.NodeMap, pylon.INodeMapWrapper)
        self.assertIsInstance(camera.TLNodeMap, pylon.INodeMapWrapper)
        self.assertIsInstance(camera.StreamGrabberNodeMap, pylon.INodeMapWrapper)
        self.assertIsInstance(camera.EventGrabberNodeMap, pylon.INodeMapWrapper)
        self.assertIsInstance(camera.InstantCameraNodeMap, pylon.INodeMapWrapper)
        result = camera.GrabOne(1000)
        self.assertIsInstance(result.GetChunkDataNodeMap(), pylon.INodeMapWrapper)
        self.assertIsInstance(result.ChunkDataNodeMap, pylon.INodeMapWrapper)
        camera.Close()

    def test_format_converter_wrappers_present(self):
        """ImageFormatConverter uses INodeMapWrapper for its parameters"""
        converter = pylon.ImageFormatConverter()
        self.assertIsInstance(converter.GetNodeMap(), pylon.INodeMapWrapper)

    # ------------------------------------------------------------------
    # Tests that INodeMapWrapper.GetNode() maps INode* to Pylon C*Parameter
    # types instead of the raw genicam interface types returned by a plain
    # INodeMap.
    # ------------------------------------------------------------------

    def test_getnode_integer_returns_integer_parameter(self):
        """intfIInteger  ->  pylon.IntegerParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("GainRaw")
        self.assertIsInstance(node, pylon.IntegerParameter)
        camera.Close()

    def test_getnode_boolean_returns_boolean_parameter(self):
        """intfIBoolean  ->  pylon.BooleanParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("ReverseX")
        self.assertIsInstance(node, pylon.BooleanParameter)
        camera.Close()

    def test_getnode_command_returns_command_parameter(self):
        """intfICommand  ->  pylon.CommandParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("AcquisitionStart")
        self.assertIsInstance(node, pylon.CommandParameter)
        camera.Close()

    def test_getnode_float_returns_float_parameter(self):
        """intfIFloat  ->  pylon.FloatParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("Gain")
        self.assertIsInstance(node, pylon.FloatParameter)
        camera.Close()

    def test_getnode_string_returns_string_parameter(self):
        """intfIString  ->  pylon.StringParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("DeviceVendorName")
        self.assertIsInstance(node, pylon.StringParameter)
        camera.Close()

    def test_getnode_enumeration_returns_enum_parameter(self):
        """intfIEnumeration  ->  pylon.EnumParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("GainAuto")
        self.assertIsInstance(node, pylon.EnumParameter)
        camera.Close()

    def test_getnode_register_returns_array_parameter(self):
        """intfIRegister  ->  pylon.ArrayParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("BslImageCompressionBCBDescriptor")
        self.assertIsInstance(node, pylon.ArrayParameter)
        camera.Close()

    def test_getnode_category_falls_back_to_genicam_icategory(self):
        """intfICategory has no Pylon *Parameter equivalent -> genicam.ICategory"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("Root")
        self.assertIsInstance(node, genicam.ICategory)
        camera.Close()

    def test_getnode_enumentry_falls_back_to_genicam_ienumentry(self):
        """intfIEnumEntry has no Pylon *Parameter equivalent -> genicam.IEnumEntry"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("EnumEntry_GainAuto_Off")
        self.assertIsInstance(node, genicam.IEnumEntry)
        camera.Close()

    def test_camera_attribute_access_maps_to_parameter_types(self):
        """Attribute access via __getattr__ delegates to GetNode and returns
        Pylon *Parameter types for all mapped interface types."""
        camera = self.create_first()
        camera.Open()
        self.assertIsInstance(camera.GainRaw, pylon.IntegerParameter)
        self.assertIsInstance(camera.ReverseX, pylon.BooleanParameter)
        self.assertIsInstance(camera.AcquisitionStart, pylon.CommandParameter)
        self.assertIsInstance(camera.Gain, pylon.FloatParameter)
        self.assertIsInstance(camera.DeviceVendorName, pylon.StringParameter)
        self.assertIsInstance(camera.GainAuto, pylon.EnumParameter)
        self.assertIsInstance(camera.BslImageCompressionBCBDescriptor, pylon.ArrayParameter)
        camera.Close()

    def test_nodemap_attribute_access_maps_to_parameter_types(self):
        """Attribute access via __getattr__ delegates to GetNode and returns
        Pylon *Parameter types for all mapped interface types."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        self.assertIsInstance(nm.GainRaw, pylon.IntegerParameter)
        self.assertIsInstance(nm.ReverseX, pylon.BooleanParameter)
        self.assertIsInstance(nm.AcquisitionStart, pylon.CommandParameter)
        self.assertIsInstance(nm.Gain, pylon.FloatParameter)
        self.assertIsInstance(nm.DeviceVendorName, pylon.StringParameter)
        self.assertIsInstance(nm.GainAuto, pylon.EnumParameter)
        self.assertIsInstance(nm.BslImageCompressionBCBDescriptor, pylon.ArrayParameter)
        camera.Close()

    def test_getnodes_returns_pylon_parameter_types(self):
        """GetNodes() via INodeMapWrapper returns Pylon *Parameter types for
        the mapped interface types (Integer, Boolean, Command, Float, String,
        Enumeration, Register) and genicam fallback types for the rest
        (ICategory, IEnumEntry, IPort)."""
        camera = self.create_first()
        camera.Open()
        nodes = camera.GetNodeMap().GetNodes()

        # Build a name->node dict for easy lookup
        by_name = {n.GetNode().GetName(): n for n in nodes}

        # Mapped types -> Pylon *Parameter
        self.assertIsInstance(by_name["GainRaw"], pylon.IntegerParameter)
        self.assertIsInstance(by_name["ReverseX"], pylon.BooleanParameter)
        self.assertIsInstance(by_name["AcquisitionStart"], pylon.CommandParameter)
        self.assertIsInstance(by_name["Gain"], pylon.FloatParameter)
        self.assertIsInstance(by_name["DeviceVendorName"], pylon.StringParameter)
        self.assertIsInstance(by_name["GainAuto"], pylon.EnumParameter)
        self.assertIsInstance(by_name["BslImageCompressionBCBDescriptor"], pylon.ArrayParameter)

        # Fallback types -> genicam interface types
        self.assertIsInstance(by_name["Root"], genicam.ICategory)
        self.assertIsInstance(by_name["EnumEntry_GainAuto_Off"], genicam.IEnumEntry)

        camera.Close()

    def test_parameter_types_not_returned_by_raw_genicam_nodemap(self):
        """Contrast test: a raw genicam INodeMap (not wrapped by INodeMapWrapper)
        returns plain genicam interface types for GetNode(), NOT Pylon *Parameter
        objects.  This confirms that INodeMapWrapper is responsible for the
        type upgrade."""
        camera = self.create_first()
        camera.Open()

        # camera.GetNodeMap() returns an INodeMapWrapper; call _Get() to obtain
        # the underlying raw INodeMap pointer and cast it back via SWIG so that
        # the genicam typemaps are in effect.
        raw_nm = camera.GetNodeMap()._Get()

        # Raw INodeMap.GetNode returns genicam interface types
        self.assertIsInstance(raw_nm.GetNode("GainRaw"), genicam.IInteger)
        self.assertIsInstance(raw_nm.GetNode("ReverseX"), genicam.IBoolean)
        self.assertIsInstance(raw_nm.GetNode("AcquisitionStart"), genicam.ICommand)
        self.assertIsInstance(raw_nm.GetNode("Gain"), genicam.IFloat)
        self.assertIsInstance(raw_nm.GetNode("DeviceVendorName"), genicam.IString)
        self.assertIsInstance(raw_nm.GetNode("GainAuto"), genicam.IEnumeration)

        # And NOT Pylon *Parameter objects
        self.assertNotIsInstance(raw_nm.GetNode("GainRaw"), pylon.IntegerParameter)
        self.assertNotIsInstance(raw_nm.GetNode("ReverseX"), pylon.BooleanParameter)
        self.assertNotIsInstance(raw_nm.GetNode("Gain"), pylon.FloatParameter)

        camera.Close()

    # ------------------------------------------------------------------
    # Tests that INodeMapWrapper correctly exposes IDeviceInfo methods,
    # delegating to the underlying INodeMap which also implements IDeviceInfo.
    # ------------------------------------------------------------------

    def test_ideviceinfo_get_device_info_returns_ideviceinfo(self):
        """GetDeviceInfo() on INodeMapWrapper returns a genicam.IDeviceInfo instance"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        di = nm.GetDeviceInfo()
        self.assertIsInstance(di, genicam.IDeviceInfo)
        camera.Close()

    def test_ideviceinfo_string_properties(self):
        """IDeviceInfo string properties are correctly delegated through INodeMapWrapper"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()

        self.assertEqual(nm.GetModelName(), "BaslerCamEmu")
        self.assertEqual(nm.GetVendorName(), "Basler")
        self.assertIsInstance(nm.GetToolTip(), str)
        self.assertIsInstance(nm.GetStandardNameSpace(), str)
        self.assertIsInstance(nm.GetProductGuid(), str)
        self.assertIsInstance(nm.GetVersionGuid(), str)

        # Values must also be consistent when accessed through wrapped node map GetDeviceInfo()
        di = nm._Get().GetDeviceInfo()
        self.assertEqual(di.GetModelName(), nm.GetModelName())
        self.assertEqual(di.GetVendorName(), nm.GetVendorName())
        self.assertEqual(di.GetToolTip(), nm.GetToolTip())
        self.assertEqual(di.GetStandardNameSpace(), nm.GetStandardNameSpace())
        self.assertEqual(di.GetProductGuid(), nm.GetProductGuid())
        self.assertEqual(di.GetVersionGuid(), nm.GetVersionGuid())

        camera.Close()

    def test_ideviceinfo_version_properties(self):
        """IDeviceInfo version structs are correctly delegated through INodeMapWrapper"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()

        # GetGenApiVersion returns (Version, build:int)
        genapi_ver, build = nm.GetGenApiVersion()
        self.assertIsInstance(genapi_ver, genicam.Version)
        self.assertIsInstance(build, int)
        self.assertGreater(genapi_ver.Major, 0)

        # GetSchemaVersion returns a Version struct
        schema_ver = nm.GetSchemaVersion()
        self.assertIsInstance(schema_ver, genicam.Version)
        self.assertGreater(schema_ver.Major, 0)

        # GetDeviceVersion returns a Version struct
        device_ver = nm.GetDeviceVersion()
        self.assertIsInstance(device_ver, genicam.Version)
        self.assertGreater(device_ver.Major, 0)

        # Values must match those returned through GetDeviceInfo()
        di = nm.GetDeviceInfo()
        di_genapi_ver, di_build = di.GetGenApiVersion()
        self.assertEqual(di_genapi_ver.Major,    genapi_ver.Major)
        self.assertEqual(di_genapi_ver.Minor,    genapi_ver.Minor)
        self.assertEqual(di_genapi_ver.SubMinor, genapi_ver.SubMinor)
        self.assertEqual(di_build, build)

        di_schema_ver = di.GetSchemaVersion()
        self.assertEqual(di_schema_ver.Major,    schema_ver.Major)
        self.assertEqual(di_schema_ver.Minor,    schema_ver.Minor)
        self.assertEqual(di_schema_ver.SubMinor, schema_ver.SubMinor)

        di_device_ver = di.GetDeviceVersion()
        self.assertEqual(di_device_ver.Major,    device_ver.Major)
        self.assertEqual(di_device_ver.Minor,    device_ver.Minor)
        self.assertEqual(di_device_ver.SubMinor, device_ver.SubMinor)

        camera.Close()

    # ------------------------------------------------------------------
    # Tests for GetNodeMapType() / NodeMapType property
    # ------------------------------------------------------------------

    def test_getnodemap_type_camera(self):
        """GetNodeMap() wrapper reports NodeMapType_Camera"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        self.assertEqual(nm.GetNodeMapType(), pylon.NodeMapType_Camera)
        camera.Close()

    def test_nodemap_type_property_camera(self):
        """NodeMapType property equals NodeMapType_Camera for the camera nodemap"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetNodeMap().NodeMapType, pylon.NodeMapType_Camera)
        camera.Close()

    def test_getnodemap_type_stream_grabber(self):
        """GetStreamGrabberNodeMap() wrapper reports NodeMapType_StreamGrabber"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetStreamGrabberNodeMap().GetNodeMapType(), pylon.NodeMapType_StreamGrabber)
        camera.Close()

    def test_nodemap_type_property_stream_grabber(self):
        """NodeMapType property equals NodeMapType_StreamGrabber"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetStreamGrabberNodeMap().NodeMapType, pylon.NodeMapType_StreamGrabber)
        camera.Close()

    def test_getnodemap_type_transport_layer(self):
        """GetTLNodeMap() wrapper reports NodeMapType_DeviceTransportLayer"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetTLNodeMap().GetNodeMapType(), pylon.NodeMapType_DeviceTransportLayer)
        camera.Close()

    def test_nodemap_type_property_transport_layer(self):
        """NodeMapType property equals NodeMapType_DeviceTransportLayer"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetTLNodeMap().NodeMapType, pylon.NodeMapType_DeviceTransportLayer)
        camera.Close()

    def test_getnodemap_type_event_grabber(self):
        """GetEventGrabberNodeMap() wrapper reports NodeMapType_EventGrabber"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetEventGrabberNodeMap().GetNodeMapType(), pylon.NodeMapType_EventGrabber)
        camera.Close()

    def test_nodemap_type_property_event_grabber(self):
        """NodeMapType property equals NodeMapType_EventGrabber"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetEventGrabberNodeMap().NodeMapType, pylon.NodeMapType_EventGrabber)
        camera.Close()

    def test_getnodemap_type_instant_camera(self):
        """GetInstantCameraNodeMap() wrapper reports NodeMapType_InstantCamera"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetInstantCameraNodeMap().GetNodeMapType(), pylon.NodeMapType_InstantCamera)
        camera.Close()

    def test_nodemap_type_property_instant_camera(self):
        """NodeMapType property equals NodeMapType_InstantCamera"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetInstantCameraNodeMap().NodeMapType, pylon.NodeMapType_InstantCamera)
        camera.Close()

    def test_getnodemap_type_image_format_converter(self):
        """ImageFormatConverter nodemap wrapper reports NodeMapType_ImageFormatConverter"""
        converter = pylon.ImageFormatConverter()
        self.assertEqual(converter.GetNodeMap().GetNodeMapType(), pylon.NodeMapType_ImageFormatConverter)

    def test_nodemap_type_property_image_format_converter(self):
        """NodeMapType property equals NodeMapType_ImageFormatConverter"""
        converter = pylon.ImageFormatConverter()
        self.assertEqual(converter.GetNodeMap().NodeMapType, pylon.NodeMapType_ImageFormatConverter)

    def test_getnodemap_type_chunk_data(self):
        """ChunkDataNodeMap wrapper reports NodeMapType_ChunkData"""
        camera = self.create_first()
        camera.Open()
        result = camera.GrabOne(1000)
        self.assertEqual(result.GetChunkDataNodeMap().GetNodeMapType(), pylon.NodeMapType_ChunkData)
        camera.Close()

    def test_nodemap_type_property_chunk_data(self):
        """NodeMapType property equals NodeMapType_ChunkData for chunk-data nodemap"""
        camera = self.create_first()
        camera.Open()
        result = camera.GrabOne(1000)
        self.assertEqual(result.ChunkDataNodeMap.NodeMapType, pylon.NodeMapType_ChunkData)
        camera.Close()

    # ------------------------------------------------------------------
    # Tests for GetNodeMapTypeString() / NodeMapTypeString property
    # ------------------------------------------------------------------

    def test_getnodemap_type_string_camera(self):
        """GetNodeMapTypeString() returns 'Camera' for the camera nodemap"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetNodeMap().GetNodeMapTypeString(), "Camera")
        camera.Close()

    def test_nodemap_type_string_property_camera(self):
        """NodeMapTypeString property returns 'Camera'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetNodeMap().NodeMapTypeString, "Camera")
        camera.Close()

    def test_getnodemap_type_string_stream_grabber(self):
        """GetNodeMapTypeString() returns 'StreamGrabber'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetStreamGrabberNodeMap().GetNodeMapTypeString(), "StreamGrabber")
        camera.Close()

    def test_nodemap_type_string_property_stream_grabber(self):
        """NodeMapTypeString property returns 'StreamGrabber'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetStreamGrabberNodeMap().NodeMapTypeString, "StreamGrabber")
        camera.Close()

    def test_getnodemap_type_string_transport_layer(self):
        """GetNodeMapTypeString() returns 'DeviceTransportLayer'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetTLNodeMap().GetNodeMapTypeString(), "DeviceTransportLayer")
        camera.Close()

    def test_nodemap_type_string_property_transport_layer(self):
        """NodeMapTypeString property returns 'DeviceTransportLayer'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetTLNodeMap().NodeMapTypeString, "DeviceTransportLayer")
        camera.Close()

    def test_getnodemap_type_string_event_grabber(self):
        """GetNodeMapTypeString() returns 'EventGrabber'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetEventGrabberNodeMap().GetNodeMapTypeString(), "EventGrabber")
        camera.Close()

    def test_nodemap_type_string_property_event_grabber(self):
        """NodeMapTypeString property returns 'EventGrabber'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetEventGrabberNodeMap().NodeMapTypeString, "EventGrabber")
        camera.Close()

    def test_getnodemap_type_string_instant_camera(self):
        """GetNodeMapTypeString() returns 'InstantCamera'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetInstantCameraNodeMap().GetNodeMapTypeString(), "InstantCamera")
        camera.Close()

    def test_nodemap_type_string_property_instant_camera(self):
        """NodeMapTypeString property returns 'InstantCamera'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetInstantCameraNodeMap().NodeMapTypeString, "InstantCamera")
        camera.Close()

    def test_getnodemap_type_string_image_format_converter(self):
        """GetNodeMapTypeString() returns 'ImageFormatConverter'"""
        converter = pylon.ImageFormatConverter()
        self.assertEqual(converter.GetNodeMap().GetNodeMapTypeString(), "ImageFormatConverter")

    def test_nodemap_type_string_property_image_format_converter(self):
        """NodeMapTypeString property returns 'ImageFormatConverter'"""
        converter = pylon.ImageFormatConverter()
        self.assertEqual(converter.GetNodeMap().NodeMapTypeString, "ImageFormatConverter")

    def test_getnodemap_type_string_chunk_data(self):
        """GetNodeMapTypeString() returns 'ChunkData'"""
        camera = self.create_first()
        camera.Open()
        result = camera.GrabOne(1000)
        self.assertEqual(result.GetChunkDataNodeMap().GetNodeMapTypeString(), "ChunkData")
        camera.Close()

    def test_nodemap_type_string_property_chunk_data(self):
        """NodeMapTypeString property returns 'ChunkData'"""
        camera = self.create_first()
        camera.Open()
        result = camera.GrabOne(1000)
        self.assertEqual(result.ChunkDataNodeMap.NodeMapTypeString, "ChunkData")
        camera.Close()

    # ------------------------------------------------------------------
    # Tests for GetNode(name, throwIfNotFound=True/False)
    # ------------------------------------------------------------------

    def test_getnode_with_throw_true_raises_on_unknown_node(self):
        """GetNode(name, True) raises LogicalErrorException for an unknown node name"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        with self.assertRaises(genicam.LogicalErrorException):
            nm.GetNode("ThisNodeDoesNotExist_XYZ", True)
        camera.Close()

    def test_getnode_with_throw_false_returns_invalid_on_unknown_node(self):
        """GetNode(name, False) returns an unattached (invalid) parameter instead of raising"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        node = nm.GetNode("ThisNodeDoesNotExist_XYZ", False)
        self.assertIsNotNone(node)
        self.assertFalse(node.IsValid())
        self.assertIsInstance(node, pylon.Parameter)  # Should still be a Parameter object, just unattached/invalid
        camera.Close()

    def test_getnode_default_throws_on_unknown_node(self):
        """GetNode(name) (default throwIfNotFound=True) raises for an unknown node"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        with self.assertRaises(genicam.LogicalErrorException):
            nm.GetNode("ThisNodeDoesNotExist_XYZ")
        camera.Close()

    def test_getnode_with_throw_true_returns_valid_node(self):
        """GetNode(name, True) returns a valid node for a known name"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("GainRaw", True)
        self.assertIsInstance(node, pylon.IntegerParameter)
        self.assertTrue(node.IsValid())
        camera.Close()

    def test_getnode_with_throw_false_returns_valid_node(self):
        """GetNode(name, False) returns a valid node for a known name"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("GainRaw", False)
        self.assertIsInstance(node, pylon.IntegerParameter)
        self.assertTrue(node.IsValid())
        camera.Close()

    def test_getnode_error_message_contains_nodemap_type(self):
        """LogicalErrorException message from GetNode includes the nodemap type string"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        try:
            nm.GetNode("NoSuchNode_ABC", True)
            self.fail("Expected LogicalErrorException was not raised")
        except genicam.LogicalErrorException as e:
            self.assertIn("Camera", str(e))
        camera.Close()

    # ------------------------------------------------------------------
    # Tests for _LookupParameter fallback into the known-parameter lists
    # ------------------------------------------------------------------

    def test_lookup_unknown_parameter_raises_logical_error(self):
        """Accessing a completely unknown attribute raises LogicalErrorException"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        with self.assertRaises(genicam.LogicalErrorException):
            _ = nm.CompletelyUnknownParameter_XYZ
        camera.Close()

    @staticmethod
    def _node_exists_in_raw_nodemap(raw_nm, name):
        """Return True if the raw genicam INodeMap contains a node with the given name."""
        try:
            raw_nm.GetNode(name)
            return True
        except genicam.LogicalErrorException:
            return False

    def _find_absent_parameter(self, raw_nm, param_dict, intf_type):
        """Return the first name in param_dict with the given intf_type that is absent
        from raw_nm, or None if every listed name is present."""
        return next(
            (n for n, t in param_dict.items()
             if t == intf_type and not self._node_exists_in_raw_nodemap(raw_nm, n)),
            None,
        )

    def test_lookup_known_camera_integer_returns_empty_integer_parameter(self):
        """A known camera Integer parameter that is absent from the live nodemap returns
        an empty (unattached) IntegerParameter from the static lookup table."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        absent_name = self._find_absent_parameter(nm._Get(), pylon._CAMERA_PARAMETERS, genicam.intfIInteger)
        if absent_name is None:
            self.skipTest("No absent Integer camera parameter found in emulator")
        param = getattr(nm, absent_name)
        self.assertIsInstance(param, pylon.IntegerParameter)
        self.assertFalse(param.IsValid())
        camera.Close()

    def test_lookup_known_camera_boolean_returns_empty_boolean_parameter(self):
        """Absent but listed Boolean camera parameter -> BooleanParameter (unattached)"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        absent_name = self._find_absent_parameter(nm._Get(), pylon._CAMERA_PARAMETERS, genicam.intfIBoolean)
        if absent_name is None:
            self.skipTest("No absent Boolean camera parameter found in emulator")
        param = getattr(nm, absent_name)
        self.assertIsInstance(param, pylon.BooleanParameter)
        self.assertFalse(param.IsValid())
        camera.Close()

    def test_lookup_known_camera_float_returns_empty_float_parameter(self):
        """Absent but listed Float camera parameter -> FloatParameter (unattached)"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        absent_name = self._find_absent_parameter(nm._Get(), pylon._CAMERA_PARAMETERS, genicam.intfIFloat)
        if absent_name is None:
            self.skipTest("No absent Float camera parameter found in emulator")
        param = getattr(nm, absent_name)
        self.assertIsInstance(param, pylon.FloatParameter)
        self.assertFalse(param.IsValid())
        camera.Close()

    def test_lookup_known_camera_enum_returns_empty_enum_parameter(self):
        """Absent but listed Enumeration camera parameter -> EnumParameter (unattached)"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        absent_name = self._find_absent_parameter(nm._Get(), pylon._CAMERA_PARAMETERS, genicam.intfIEnumeration)
        if absent_name is None:
            self.skipTest("No absent Enumeration camera parameter found in emulator")
        param = getattr(nm, absent_name)
        self.assertIsInstance(param, pylon.EnumParameter)
        self.assertFalse(param.IsValid())
        camera.Close()

    def test_lookup_known_stream_integer_returns_empty_integer_parameter(self):
        """Absent but listed Integer stream parameter -> IntegerParameter (unattached)"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetStreamGrabberNodeMap()
        absent_name = self._find_absent_parameter(nm._Get(), pylon._STREAM_PARAMETERS, genicam.intfIInteger)
        if absent_name is None:
            self.skipTest("No absent Integer stream parameter found in emulator")
        param = getattr(nm, absent_name)
        self.assertIsInstance(param, pylon.IntegerParameter)
        self.assertFalse(param.IsValid())
        camera.Close()

    def test_lookup_known_tl_integer_returns_empty_integer_parameter(self):
        """Absent but listed Integer TL parameter -> IntegerParameter (unattached)"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetTLNodeMap()
        absent_name = self._find_absent_parameter(nm._Get(), pylon._TRANSPORT_LAYER_PARAMETERS, genicam.intfIInteger)
        if absent_name is None:
            self.skipTest("No absent Integer TL parameter found in emulator")
        param = getattr(nm, absent_name)
        self.assertIsInstance(param, pylon.IntegerParameter)
        self.assertFalse(param.IsValid())
        camera.Close()

    def test_lookup_known_event_grabber_integer_returns_empty_integer_parameter(self):
        """Absent but listed Integer event-grabber parameter -> IntegerParameter (unattached)"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetEventGrabberNodeMap()
        absent_name = self._find_absent_parameter(nm._Get(), pylon._EVENT_GRABBER_PARAMETERS, genicam.intfIInteger)
        if absent_name is None:
            self.skipTest("No absent Integer event-grabber parameter found in emulator")
        param = getattr(nm, absent_name)
        self.assertIsInstance(param, pylon.IntegerParameter)
        self.assertFalse(param.IsValid())
        camera.Close()

    def test_lookup_error_message_includes_nodemap_type_string(self):
        """LogicalErrorException from _LookupParameter contains the nodemap type string"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        try:
            _ = nm.CompletelyUnknownAttribute_ZZZZ
            self.fail("Expected LogicalErrorException was not raised")
        except genicam.LogicalErrorException as e:
            self.assertIn("Camera", str(e))
        camera.Close()

    def test_to_parameter(self):
        """Test ToParameter() on a raw genicam INodeMap (not wrapped by INodeMapWrapper) does NOT"""
        camera = self.create_first()
        camera.Open()

        # camera.GetNodeMap() returns an INodeMapWrapper; call _Get() to obtain
        # the underlying raw INodeMap pointer and cast it back via SWIG so that
        # the genicam typemaps are in effect.
        raw_nm = camera.GetNodeMap()._Get()

        # Raw INodeMap.GetNode returns genicam interface types
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("GainRaw").GetNode()), pylon.IntegerParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("GainRaw")), pylon.IntegerParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("ReverseX")), pylon.BooleanParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("AcquisitionStart")), pylon.CommandParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("Gain")), pylon.FloatParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("DeviceVendorName")), pylon.StringParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("GainAuto")), pylon.EnumParameter)

        camera.Close()

if __name__ == "__main__":
    unittest.main()
