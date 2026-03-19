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
