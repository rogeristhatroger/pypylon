"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylon/DeviceInfo.i and src/pylon/Info.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class DeviceInfoTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_construction(self):
        """Default construction produces a valid empty DeviceInfo."""
        info = pylon.DeviceInfo()
        self.assertIsNotNone(info)

    def test_copy_construction(self):
        """Copy construction produces a DeviceInfo equal to the original."""
        original = pylon.DeviceInfo()
        original.ModelName = "TestModel"
        original.SerialNumber = "12345678"
        copy = pylon.DeviceInfo(original)
        self.assertEqual(copy.ModelName, original.ModelName)
        self.assertEqual(copy.SerialNumber, original.SerialNumber)

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

    def test_equality(self):
        """Two DeviceInfo objects with the same properties compare equal."""
        info = pylon.DeviceInfo()
        info.ModelName = "TestModel"
        self.assertEqual(info, pylon.DeviceInfo(info))

    def test_less_than(self):
        """Less-than orders by numeric serial number within the same device class."""
        info1 = pylon.DeviceInfo()
        info1.DeviceClass = "BaslerUsb"
        info1.SerialNumber = "1"
        info2 = pylon.DeviceInfo()
        info2.DeviceClass = "BaslerUsb"
        info2.SerialNumber = "2"
        self.assertTrue(info1 < info2)
        self.assertFalse(info2 < info1)

    # ------------------------------------------------------------------
    # CInfoBase properties (from Info.i)
    # ADD_PROP_GETSET(CInfoBase, FriendlyName)
    # ADD_PROP_GETSET(CInfoBase, FullName)
    # ADD_PROP_GETSET(CInfoBase, VendorName)
    # ADD_PROP_GETSET(CInfoBase, DeviceClass)
    # ADD_PROP_GETSET(CInfoBase, TLType)
    # ------------------------------------------------------------------

    def test_friendly_name(self):
        """FriendlyName property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsFriendlyNameAvailable())
        self.assertEqual(info.FriendlyName, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.FriendlyName = "Test Friendly"
        self.assertTrue(info.IsFriendlyNameAvailable())
        self.assertEqual(info.FriendlyName, "Test Friendly")

        # --- legacy: named getter / setter ---
        info.SetFriendlyName("Updated Friendly")
        self.assertEqual(info.GetFriendlyName(), "Updated Friendly")

        # --- generic: dict-style interface ---
        info[pylon.FriendlyNameKey] = "Dict Friendly"
        self.assertEqual(info["FriendlyName"], "Dict Friendly")

    def test_full_name(self):
        """FullName property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsFullNameAvailable())
        self.assertEqual(info.FullName, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.FullName = "Test Full Name"
        self.assertTrue(info.IsFullNameAvailable())
        self.assertEqual(info.FullName, "Test Full Name")

        # --- legacy: named getter / setter ---
        info.SetFullName("Updated Full Name")
        self.assertEqual(info.GetFullName(), "Updated Full Name")

        # --- generic: dict-style interface ---
        info[pylon.FullNameKey] = "Dict Full Name"
        self.assertEqual(info["FullName"], "Dict Full Name")

    def test_vendor_name(self):
        """VendorName property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsVendorNameAvailable())
        self.assertEqual(info.VendorName, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.VendorName = "Test Vendor"
        self.assertTrue(info.IsVendorNameAvailable())
        self.assertEqual(info.VendorName, "Test Vendor")

        # --- legacy: named getter / setter ---
        info.SetVendorName("Updated Vendor")
        self.assertEqual(info.GetVendorName(), "Updated Vendor")

        # --- generic: dict-style interface ---
        info[pylon.VendorNameKey] = "Dict Vendor"
        self.assertEqual(info["VendorName"], "Dict Vendor")

    def test_device_class(self):
        """DeviceClass property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsDeviceClassAvailable())
        self.assertEqual(info.DeviceClass, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.DeviceClass = "BaslerUsb"
        self.assertTrue(info.IsDeviceClassAvailable())
        self.assertEqual(info.DeviceClass, "BaslerUsb")

        # --- legacy: named getter / setter ---
        info.SetDeviceClass("BaslerGigE")
        self.assertEqual(info.GetDeviceClass(), "BaslerGigE")

        # --- generic: dict-style interface ---
        info[pylon.DeviceClassKey] = "BaslerCameraLink"
        self.assertEqual(info["DeviceClass"], "BaslerCameraLink")

    def test_tl_type(self):
        """TLType property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsTLTypeAvailable())
        self.assertEqual(info.TLType, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.TLType = "U3V"
        self.assertTrue(info.IsTLTypeAvailable())
        self.assertEqual(info.TLType, "U3V")

        # --- legacy: named getter / setter ---
        info.SetTLType("GigE")
        self.assertEqual(info.GetTLType(), "GigE")

        # --- generic: dict-style interface ---
        info[pylon.TLTypeKey] = "CameraLink"
        self.assertEqual(info["TLType"], "CameraLink")

    # ------------------------------------------------------------------
    # IProperties methods (from Info.i)
    #     static const char* GetPropertyNotAvailable();
    #     virtual int GetPropertyNames( StringList_t& ) const;
    #     virtual bool GetPropertyAvailable( const String_t& Name ) const;
    #     virtual bool GetPropertyValue( const String_t& Name, String_t& Value ) const;
    #     virtual IProperties& SetPropertyValue( const String_t& Name, const String_t& Value );
    #     virtual bool IsUserProvided() const;
    #     virtual bool IsSubset( const IProperties& Subset ) const;
    # ------------------------------------------------------------------

    def test_get_property_names(self):
        """keys() returns all set property names as strings."""
        info = pylon.DeviceInfo()
        info.ModelName = "TestModel"
        names = info.keys()
        self.assertIn("ModelName", names)
        self.assertTrue(all(isinstance(n, str) for n in names))

    def test_get_property_available(self):
        """GetPropertyAvailable returns True for a set property and False for an unknown key."""
        info = pylon.DeviceInfo()
        info.ModelName = "TestModel"
        self.assertTrue(info.GetPropertyAvailable("ModelName"))
        self.assertFalse(info.GetPropertyAvailable("NonExistentKey"))

    def test_get_property_value(self):
        """GetPropertyValue returns (True, value) for a known key and (False, ...) for an unknown one."""
        info = pylon.DeviceInfo()
        info.ModelName = "TestModel"
        ok, value = info.GetPropertyValue("ModelName")
        self.assertTrue(ok)
        self.assertEqual(str(value), "TestModel")
        ok_missing, _ = info.GetPropertyValue("NonExistentKey")
        self.assertFalse(ok_missing)

    def test_set_property_value(self):
        """SetPropertyValue sets a property accessible through the typed getter."""
        info = pylon.DeviceInfo()
        info.SetPropertyValue("ModelName", "FromGeneric")
        self.assertEqual(info.ModelName, "FromGeneric")

    def test_is_subset(self):
        """IsSubset returns True when all properties of the subset match."""
        info = pylon.DeviceInfo()
        info.ModelName = "TestModel"
        subset = pylon.DeviceInfo()
        subset.ModelName = "TestModel"
        self.assertTrue(info.IsSubset(subset))

    def test_is_subset_mismatch(self):
        """IsSubset returns False when a subset property does not match."""
        info = pylon.DeviceInfo()
        info.ModelName = "TestModel"
        other = pylon.DeviceInfo()
        other.ModelName = "OtherModel"
        self.assertFalse(info.IsSubset(other))

    def test_is_user_provided(self):
        """IsUserProvided returns a bool."""
        self.assertIsInstance(pylon.DeviceInfo().IsUserProvided(), bool)
        self.assertTrue(pylon.DeviceInfo().IsUserProvided())

    # ------------------------------------------------------------------
    # Python dict interface (from Info.i)
    # ------------------------------------------------------------------

    def test_dict_getitem(self):
        """info[key] returns the same value as the typed property getter."""
        info = pylon.DeviceInfo()
        info.ModelName = "TestModel"
        self.assertEqual(info["ModelName"], "TestModel")

    def test_dict_setitem(self):
        """info[key] = value sets the property accessible via the typed getter."""
        info = pylon.DeviceInfo()
        info["ModelName"] = "TestModel"
        self.assertEqual(info.ModelName, "TestModel")

    def test_dict_contains(self):
        """'key' in info returns True for a set property and False for an unknown key."""
        info = pylon.DeviceInfo()
        info.ModelName = "TestModel"
        self.assertIn("ModelName", info)
        self.assertNotIn("NonExistentKey", info)

    def test_dict_iter(self):
        """Iterating over info yields all set property name strings."""
        info = pylon.DeviceInfo()
        info.ModelName = "TestModel"
        self.assertIn("ModelName", list(info))

    def test_dict_keys_values_items(self):
        """keys(), values(), and items() return consistent parallel sequences."""
        info = pylon.DeviceInfo()
        info.ModelName = "TestModel"
        self.assertEqual(list(info.items()), list(zip(info.keys(), info.values())))

    def test_dict_to_dict(self):
        """to_dict() returns a plain Python dict with all set properties."""
        info = pylon.DeviceInfo()
        info.ModelName = "TestModel"
        d = info.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d["ModelName"], "TestModel")

    def test_dict_update(self):
        """update() sets multiple properties from a plain dict."""
        info = pylon.DeviceInfo()
        info.update({"ModelName": "UpdatedModel", "DeviceClass": "BaslerUsb"})
        self.assertEqual(info.ModelName, "UpdatedModel")
        self.assertEqual(info.DeviceClass, "BaslerUsb")

    # ------------------------------------------------------------------
    # General DeviceInfo properties (from DeviceInfo.i)
    # ADD_PROP_GETSET(DeviceInfo, SerialNumber)
    # ADD_PROP_GETSET(DeviceInfo, UserDefinedName)
    # ADD_PROP_GETSET(DeviceInfo, ModelName)
    # ADD_PROP_GETSET(DeviceInfo, DeviceVersion)
    # ADD_PROP_GETSET(DeviceInfo, DeviceFactory)
    # ADD_PROP_GETSET(DeviceInfo, XMLSource)
    # ADD_PROP_GETSET(DeviceInfo, InterfaceID)
    # ------------------------------------------------------------------

    def test_serial_number(self):
        """SerialNumber property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsSerialNumberAvailable())
        self.assertEqual(info.SerialNumber, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.SerialNumber = "12345678"
        self.assertTrue(info.IsSerialNumberAvailable())
        self.assertEqual(info.SerialNumber, "12345678")

        # --- legacy: named getter / setter ---
        info.SetSerialNumber("87654321")
        self.assertEqual(info.GetSerialNumber(), "87654321")

        # --- generic: dict-style interface ---
        info[pylon.SerialNumberKey] = "99999999"
        self.assertEqual(info["SerialNumber"], "99999999")

    def test_user_defined_name(self):
        """UserDefinedName property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsUserDefinedNameAvailable())
        self.assertEqual(info.UserDefinedName, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.UserDefinedName = "MyCamera"
        self.assertTrue(info.IsUserDefinedNameAvailable())
        self.assertEqual(info.UserDefinedName, "MyCamera")

        # --- legacy: named getter / setter ---
        info.SetUserDefinedName("UpdatedCamera")
        self.assertEqual(info.GetUserDefinedName(), "UpdatedCamera")

        # --- generic: dict-style interface ---
        info[pylon.UserDefinedNameKey] = "DictCamera"
        self.assertEqual(info["UserDefinedName"], "DictCamera")

    def test_model_name(self):
        """ModelName property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsModelNameAvailable())
        self.assertEqual(info.ModelName, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.ModelName = "TestModel"
        self.assertTrue(info.IsModelNameAvailable())
        self.assertEqual(info.ModelName, "TestModel")

        # --- legacy: named getter / setter ---
        info.SetModelName("UpdatedModel")
        self.assertEqual(info.GetModelName(), "UpdatedModel")

        # --- generic: dict-style interface ---
        info[pylon.ModelNameKey] = "DictModel"
        self.assertEqual(info["ModelName"], "DictModel")

    def test_device_version(self):
        """DeviceVersion property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsDeviceVersionAvailable())
        self.assertEqual(info.DeviceVersion, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.DeviceVersion = "1.0.0"
        self.assertTrue(info.IsDeviceVersionAvailable())
        self.assertEqual(info.DeviceVersion, "1.0.0")

        # --- legacy: named getter / setter ---
        info.SetDeviceVersion("2.0.0")
        self.assertEqual(info.GetDeviceVersion(), "2.0.0")

        # --- generic: dict-style interface ---
        info[pylon.DeviceVersionKey] = "3.0.0"
        self.assertEqual(info["DeviceVersion"], "3.0.0")

    def test_device_factory(self):
        """DeviceFactory property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsDeviceFactoryAvailable())
        self.assertEqual(info.DeviceFactory, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.DeviceFactory = "BaslerGigE"
        self.assertTrue(info.IsDeviceFactoryAvailable())
        self.assertEqual(info.DeviceFactory, "BaslerGigE")

        # --- legacy: named getter / setter ---
        info.SetDeviceFactory("BaslerUsb")
        self.assertEqual(info.GetDeviceFactory(), "BaslerUsb")

        # --- generic: dict-style interface ---
        info[pylon.DeviceFactoryKey] = "BaslerCameraLink"
        self.assertEqual(info["DeviceFactory"], "BaslerCameraLink")

    def test_xml_source(self):
        """XMLSource property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsXMLSourceAvailable())
        self.assertEqual(info.XMLSource, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.XMLSource = "device://0"
        self.assertTrue(info.IsXMLSourceAvailable())
        self.assertEqual(info.XMLSource, "device://0")

        # --- legacy: named getter / setter ---
        info.SetXMLSource("file://model.xml")
        self.assertEqual(info.GetXMLSource(), "file://model.xml")

        # --- generic: dict-style interface ---
        info[pylon.XMLSourceKey] = "device://1"
        self.assertEqual(info["XMLSource"], "device://1")

    def test_interface_id(self):
        """InterfaceID property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsInterfaceIDAvailable())
        self.assertEqual(info.InterfaceID, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.InterfaceID = "eth0"
        self.assertTrue(info.IsInterfaceIDAvailable())
        self.assertEqual(info.InterfaceID, "eth0")

        # --- legacy: named getter / setter ---
        info.SetInterfaceID("eth1")
        self.assertEqual(info.GetInterfaceID(), "eth1")

        # --- generic: dict-style interface ---
        info[pylon.InterfaceIDKey] = "eth2"
        self.assertEqual(info["InterfaceID"], "eth2")

    # ------------------------------------------------------------------
    # GigE properties (from DeviceInfo.i)
    # ADD_PROP_GETSET(DeviceInfo, Address)
    # ADD_PROP_GETSET(DeviceInfo, IpAddress)
    # ADD_PROP_GETSET(DeviceInfo, SubnetAddress)
    # ADD_PROP_GETSET(DeviceInfo, DefaultGateway)
    # ADD_PROP_GETSET(DeviceInfo, SubnetMask)
    # ADD_PROP_GETSET(DeviceInfo, PortNr)
    # ADD_PROP_GETSET(DeviceInfo, MacAddress)
    # ADD_PROP_GETSET(DeviceInfo, Interface)
    # ADD_PROP_GETSET(DeviceInfo, IpConfigOptions)
    # ADD_PROP_GETSET(DeviceInfo, IpConfigCurrent)
    # ------------------------------------------------------------------

    def test_address(self):
        """Address property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsAddressAvailable())
        self.assertEqual(info.Address, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.Address = "192.168.0.1:3956"
        self.assertTrue(info.IsAddressAvailable())
        self.assertEqual(info.Address, "192.168.0.1:3956")

        # --- legacy: named getter / setter ---
        info.SetAddress("192.168.0.2:3956")
        self.assertEqual(info.GetAddress(), "192.168.0.2:3956")

        # --- generic: dict-style interface ---
        info[pylon.AddressKey] = "192.168.0.3:3956"
        self.assertEqual(info["Address"], "192.168.0.3:3956")

    def test_ip_address(self):
        """IpAddress property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsIpAddressAvailable())
        self.assertEqual(info.IpAddress, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.IpAddress = "192.168.0.1"
        self.assertTrue(info.IsIpAddressAvailable())
        self.assertEqual(info.IpAddress, "192.168.0.1")

        # --- legacy: named getter / setter ---
        info.SetIpAddress("192.168.0.2")
        self.assertEqual(info.GetIpAddress(), "192.168.0.2")

        # --- generic: dict-style interface ---
        info[pylon.IpAddressKey] = "192.168.0.3"
        self.assertEqual(info["IpAddress"], "192.168.0.3")

    def test_subnet_address(self):
        """SubnetAddress property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsSubnetAddressAvailable())
        self.assertEqual(info.SubnetAddress, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.SubnetAddress = "192.168.0.0"
        self.assertTrue(info.IsSubnetAddressAvailable())
        self.assertEqual(info.SubnetAddress, "192.168.0.0")

        # --- legacy: named getter / setter ---
        info.SetSubnetAddress("10.0.0.0")
        self.assertEqual(info.GetSubnetAddress(), "10.0.0.0")

        # --- generic: dict-style interface ---
        info[pylon.SubnetAddressKey] = "172.16.0.0"
        self.assertEqual(info["SubnetAddress"], "172.16.0.0")

    def test_default_gateway(self):
        """DefaultGateway property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsDefaultGatewayAvailable())
        self.assertEqual(info.DefaultGateway, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.DefaultGateway = "192.168.0.254"
        self.assertTrue(info.IsDefaultGatewayAvailable())
        self.assertEqual(info.DefaultGateway, "192.168.0.254")

        # --- legacy: named getter / setter ---
        info.SetDefaultGateway("10.0.0.1")
        self.assertEqual(info.GetDefaultGateway(), "10.0.0.1")

        # --- generic: dict-style interface ---
        info[pylon.DefaultGatewayKey] = "172.16.0.1"
        self.assertEqual(info["DefaultGateway"], "172.16.0.1")

    def test_subnet_mask(self):
        """SubnetMask property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsSubnetMaskAvailable())
        self.assertEqual(info.SubnetMask, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.SubnetMask = "255.255.255.0"
        self.assertTrue(info.IsSubnetMaskAvailable())
        self.assertEqual(info.SubnetMask, "255.255.255.0")

        # --- legacy: named getter / setter ---
        info.SetSubnetMask("255.255.0.0")
        self.assertEqual(info.GetSubnetMask(), "255.255.0.0")

        # --- generic: dict-style interface ---
        info[pylon.SubnetMaskKey] = "255.0.0.0"
        self.assertEqual(info["SubnetMask"], "255.0.0.0")

    def test_port_nr(self):
        """PortNr property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsPortNrAvailable())
        self.assertEqual(info.PortNr, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.PortNr = "3956"
        self.assertTrue(info.IsPortNrAvailable())
        self.assertEqual(info.PortNr, "3956")

        # --- legacy: named getter / setter ---
        info.SetPortNr("3957")
        self.assertEqual(info.GetPortNr(), "3957")

        # --- generic: dict-style interface ---
        info[pylon.PortNrKey] = "3958"
        self.assertEqual(info["PortNr"], "3958")

    def test_mac_address(self):
        """MacAddress property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsMacAddressAvailable())
        self.assertEqual(info.MacAddress, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.MacAddress = "00:11:22:33:44:55"
        self.assertTrue(info.IsMacAddressAvailable())
        self.assertEqual(info.MacAddress, "00:11:22:33:44:55")

        # --- legacy: named getter / setter ---
        info.SetMacAddress("AA:BB:CC:DD:EE:FF")
        self.assertEqual(info.GetMacAddress(), "AA:BB:CC:DD:EE:FF")

        # --- generic: dict-style interface ---
        info[pylon.MacAddressKey] = "11:22:33:44:55:66"
        self.assertEqual(info["MacAddress"], "11:22:33:44:55:66")

    def test_interface(self):
        """Interface property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsInterfaceAvailable())
        self.assertEqual(info.Interface, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.Interface = "192.168.0.100"
        self.assertTrue(info.IsInterfaceAvailable())
        self.assertEqual(info.Interface, "192.168.0.100")

        # --- legacy: named getter / setter ---
        info.SetInterface("192.168.0.101")
        self.assertEqual(info.GetInterface(), "192.168.0.101")

        # --- generic: dict-style interface ---
        info[pylon.InterfaceKey] = "192.168.0.102"
        self.assertEqual(info["Interface"], "192.168.0.102")

    def test_ip_config_options(self):
        """IpConfigOptions property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsIpConfigOptionsAvailable())
        self.assertEqual(info.IpConfigOptions, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.IpConfigOptions = "6"
        self.assertTrue(info.IsIpConfigOptionsAvailable())
        self.assertEqual(info.IpConfigOptions, "6")

        # --- legacy: named getter / setter ---
        info.SetIpConfigOptions("7")
        self.assertEqual(info.GetIpConfigOptions(), "7")

        # --- generic: dict-style interface ---
        info[pylon.IpConfigOptionsKey] = "4"
        self.assertEqual(info["IpConfigOptions"], "4")

    def test_ip_config_current(self):
        """IpConfigCurrent property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsIpConfigCurrentAvailable())
        self.assertEqual(info.IpConfigCurrent, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.IpConfigCurrent = "4"
        self.assertTrue(info.IsIpConfigCurrentAvailable())
        self.assertEqual(info.IpConfigCurrent, "4")

        # --- legacy: named getter / setter ---
        info.SetIpConfigCurrent("6")
        self.assertEqual(info.GetIpConfigCurrent(), "6")

        # --- generic: dict-style interface ---
        info[pylon.IpConfigCurrentKey] = "2"
        self.assertEqual(info["IpConfigCurrent"], "2")

    # ------------------------------------------------------------------
    # GigE IP configuration methods (from DeviceInfo.i)
    # ------------------------------------------------------------------

    def test_gige_ip_config_methods_raise_without_config(self):
        """IP configuration methods raise GenericException when the config key has not been set."""
        info = pylon.DeviceInfo()
        self.assertRaises(pylon.GenericException, info.IsPersistentIpActive)
        self.assertRaises(pylon.GenericException, info.IsDhcpActive)
        self.assertRaises(pylon.GenericException, info.IsAutoIpActive)
        self.assertRaises(pylon.GenericException, info.IsPersistentIpSupported)
        self.assertRaises(pylon.GenericException, info.IsDhcpSupported)
        self.assertRaises(pylon.GenericException, info.IsAutoIpSupported)

    # ------------------------------------------------------------------
    # USB read-only properties (from DeviceInfo.i)
    # ADD_PROP_GET(DeviceInfo, DeviceGUID)
    # ADD_PROP_GET(DeviceInfo, ManufacturerInfo)
    # ADD_PROP_GET(DeviceInfo, ProductId)
    # ADD_PROP_GET(DeviceInfo, VendorId)
    # ADD_PROP_GET(DeviceInfo, DriverKeyName)
    # ADD_PROP_GET(DeviceInfo, UsbDriverType)   [key: pylon.UsbDriverTypeKey == "UsbDriverTypeName"]
    # ADD_PROP_GET(DeviceInfo, TransferMode)    [key: pylon.TransferModeKey  == "TransferModeKey"]
    # ------------------------------------------------------------------

    def test_device_guid(self):
        """DeviceGUID is read-only; use SetPropertyValue to seed the value."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsDeviceGUIDAvailable())
        self.assertEqual(info.DeviceGUID, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.SetPropertyValue(pylon.DeviceGUIDKey, "{12345678-1234-5678-1234-123456789012}")
        self.assertTrue(info.IsDeviceGUIDAvailable())
        self.assertEqual(info.DeviceGUID, "{12345678-1234-5678-1234-123456789012}")

        # --- legacy: named getter ---
        self.assertEqual(info.GetDeviceGUID(), "{12345678-1234-5678-1234-123456789012}")

    def test_manufacturer_info(self):
        """ManufacturerInfo is read-only; use SetPropertyValue to seed the value."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsManufacturerInfoAvailable())
        self.assertEqual(info.ManufacturerInfo, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.SetPropertyValue(pylon.ManufacturerInfoKey, "Test Manufacturer")
        self.assertTrue(info.IsManufacturerInfoAvailable())
        self.assertEqual(info.ManufacturerInfo, "Test Manufacturer")

        # --- legacy: named getter ---
        self.assertEqual(info.GetManufacturerInfo(), "Test Manufacturer")

    def test_product_id(self):
        """ProductId is read-only; use SetPropertyValue to seed the value."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsProductIdAvailable())
        self.assertEqual(info.ProductId, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.SetPropertyValue(pylon.ProductIdKey, "0x1234")
        self.assertTrue(info.IsProductIdAvailable())
        self.assertEqual(info.ProductId, "0x1234")

        # --- legacy: named getter ---
        self.assertEqual(info.GetProductId(), "0x1234")

    def test_vendor_id(self):
        """VendorId is read-only; use SetPropertyValue to seed the value."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsVendorIdAvailable())
        self.assertEqual(info.VendorId, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.SetPropertyValue(pylon.VendorIdKey, "0x2676")
        self.assertTrue(info.IsVendorIdAvailable())
        self.assertEqual(info.VendorId, "0x2676")

        # --- legacy: named getter ---
        self.assertEqual(info.GetVendorId(), "0x2676")

    def test_driver_key_name(self):
        """DriverKeyName is read-only; use SetPropertyValue to seed the value."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsDriverKeyNameAvailable())
        self.assertEqual(info.DriverKeyName, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.SetPropertyValue(pylon.DriverKeyNameKey, "BaslerDriver")
        self.assertTrue(info.IsDriverKeyNameAvailable())
        self.assertEqual(info.DriverKeyName, "BaslerDriver")

        # --- legacy: named getter ---
        self.assertEqual(info.GetDriverKeyName(), "BaslerDriver")

    def test_usb_driver_type(self):
        """UsbDriverType is read-only; use SetPropertyValue to seed the value.

        Note: pylon.UsbDriverTypeKey == 'UsbDriverTypeName' (not 'UsbDriverType').
        """
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsUsbDriverTypeAvailable())
        self.assertEqual(info.UsbDriverType, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.SetPropertyValue(pylon.UsbDriverTypeKey, "WinUSB")
        self.assertTrue(info.IsUsbDriverTypeAvailable())
        self.assertEqual(info.UsbDriverType, "WinUSB")

        # --- legacy: named getter ---
        self.assertEqual(info.GetUsbDriverType(), "WinUSB")

    def test_transfer_mode(self):
        """TransferMode is read-only; use SetPropertyValue to seed the value.

        Note: pylon.TransferModeKey == 'TransferModeKey' (not 'TransferMode').
        """
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsTransferModeAvailable())
        self.assertEqual(info.TransferMode, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.SetPropertyValue(pylon.TransferModeKey, "dtx")
        self.assertTrue(info.IsTransferModeAvailable())
        self.assertEqual(info.TransferMode, "dtx")

        # --- legacy: named getter ---
        self.assertEqual(info.GetTransferMode(), "dtx")

    # ------------------------------------------------------------------
    # CameraLink properties (from DeviceInfo.i)
    # ADD_PROP_GETSET(DeviceInfo, PortID)
    # ADD_PROP_GETSET(DeviceInfo, DeviceID)
    # ADD_PROP_GETSET(DeviceInfo, InitialBaudRate)
    # ADD_PROP_GETSET(DeviceInfo, DeviceXMLFileOverride)
    # ADD_PROP_GETSET(DeviceInfo, DeviceSpecificString)
    # ADD_PROP_GETSET(DeviceInfo, PortSpecificString)
    # ------------------------------------------------------------------

    def test_port_id(self):
        """PortID property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsPortIDAvailable())
        self.assertEqual(info.PortID, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.PortID = "COM1"
        self.assertTrue(info.IsPortIDAvailable())
        self.assertEqual(info.PortID, "COM1")

        # --- legacy: named getter / setter ---
        info.SetPortID("COM2")
        self.assertEqual(info.GetPortID(), "COM2")

        # --- generic: dict-style interface ---
        info[pylon.PortIDKey] = "COM3"
        self.assertEqual(info["PortID"], "COM3")

    def test_device_id(self):
        """DeviceID property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsDeviceIDAvailable())
        self.assertEqual(info.DeviceID, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.DeviceID = "Dev0"
        self.assertTrue(info.IsDeviceIDAvailable())
        self.assertEqual(info.DeviceID, "Dev0")

        # --- legacy: named getter / setter ---
        info.SetDeviceID("Dev1")
        self.assertEqual(info.GetDeviceID(), "Dev1")

        # --- generic: dict-style interface ---
        info[pylon.DeviceIDKey] = "Dev2"
        self.assertEqual(info["DeviceID"], "Dev2")

    def test_initial_baud_rate(self):
        """InitialBaudRate property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsInitialBaudRateAvailable())
        self.assertEqual(info.InitialBaudRate, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.InitialBaudRate = "9600"
        self.assertTrue(info.IsInitialBaudRateAvailable())
        self.assertEqual(info.InitialBaudRate, "9600")

        # --- legacy: named getter / setter ---
        info.SetInitialBaudRate("115200")
        self.assertEqual(info.GetInitialBaudRate(), "115200")

        # --- generic: dict-style interface ---
        info[pylon.InitialBaudRateKey] = "57600"
        self.assertEqual(info["InitialBaudRate"], "57600")

    def test_device_xml_file_override(self):
        """DeviceXMLFileOverride property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsDeviceXMLFileOverrideAvailable())
        self.assertEqual(info.DeviceXMLFileOverride, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.DeviceXMLFileOverride = "override.xml"
        self.assertTrue(info.IsDeviceXMLFileOverrideAvailable())
        self.assertEqual(info.DeviceXMLFileOverride, "override.xml")

        # --- legacy: named getter / setter ---
        info.SetDeviceXMLFileOverride("updated.xml")
        self.assertEqual(info.GetDeviceXMLFileOverride(), "updated.xml")

        # --- generic: dict-style interface ---
        info[pylon.DeviceXMLFileOverrideKey] = "dict.xml"
        self.assertEqual(info["DeviceXMLFileOverride"], "dict.xml")

    def test_device_specific_string(self):
        """DeviceSpecificString property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsDeviceSpecificStringAvailable())
        self.assertEqual(info.DeviceSpecificString, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.DeviceSpecificString = "specific"
        self.assertTrue(info.IsDeviceSpecificStringAvailable())
        self.assertEqual(info.DeviceSpecificString, "specific")

        # --- legacy: named getter / setter ---
        info.SetDeviceSpecificString("updated_specific")
        self.assertEqual(info.GetDeviceSpecificString(), "updated_specific")

        # --- generic: dict-style interface ---
        info[pylon.DeviceSpecificStringKey] = "dict_specific"
        self.assertEqual(info["DeviceSpecificString"], "dict_specific")

    def test_port_specific_string(self):
        """PortSpecificString property round-trips correctly."""
        info = pylon.DeviceInfo()

        # --- recommended: property interface ---
        self.assertFalse(info.IsPortSpecificStringAvailable())
        self.assertEqual(info.PortSpecificString, pylon.DeviceInfo.GetPropertyNotAvailable())
        info.PortSpecificString = "port_specific"
        self.assertTrue(info.IsPortSpecificStringAvailable())
        self.assertEqual(info.PortSpecificString, "port_specific")

        # --- legacy: named getter / setter ---
        info.SetPortSpecificString("updated_port_specific")
        self.assertEqual(info.GetPortSpecificString(), "updated_port_specific")

        # --- generic: dict-style interface ---
        info[pylon.PortSpecificStringKey] = "dict_port_specific"
        self.assertEqual(info["PortSpecificString"], "dict_port_specific")

    # ------------------------------------------------------------------
    # DeviceIdx methods (no Python property; key constant is ignored in .i)
    # ------------------------------------------------------------------

    def test_device_idx(self):
        """GetDeviceIdx returns the value set via SetPropertyValue; IsDeviceIdxAvailable reflects it."""
        info = pylon.DeviceInfo()
        self.assertFalse(info.IsDeviceIdxAvailable())
        info.SetPropertyValue("DeviceIdx", "3")
        self.assertEqual(info.GetDeviceIdx(), "3")
        self.assertTrue(info.IsDeviceIdxAvailable())


if __name__ == "__main__":
    unittest.main()
