#!/usr/bin/env python3
"""\
This sample illustrates how to traverse the tree of the pylon object hierarchy
and collect information about all available transport layers, interfaces,
devices, and their GenICam parameters.

The output is formatted as YAML — an unambiguous, human- and machine-readable
format that preserves the nested structure of the pylon object hierarchy.

Hierarchy traversed:
    TlFactory
    └── TransportLayer  (e.g. GigE, USB3, GenTL Producer)
        └── Interface   (e.g. a frame grabber)
            ├── NodeMap (interface-level parameters)
            └── Device  (a physical or emulated camera)
                ├── NodeMap             (camera device parameters: exposure, gain, …)
                ├── StreamGrabberNodeMap (stream grabber parameters: statistics, …)
                ├── TLNodeMap           (device transport-layer parameters: statistics, …)
                └── EventGrabberNodeMap (asynchronous event grabber parameters)

Requires PyYAML:  pip install pyyaml

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
import yaml
from pypylon import pylon

# The exit code of the sample application.
exit_code = 0


# ---------------------------------------------------------------------------
# Helper functions that collect data into plain Python dicts / strings.
# ---------------------------------------------------------------------------

def collect_category(category):
    """Recursively collect GenICam parameters from a category.

    CategoryParameters act as folders; all other parameter types are
    leaves whose current value is recorded as a string.

    Returns a nested dict:  { parameter_name: value_or_sub_dict, … }
    """
    if not category.IsValid():
        return {}

    result = {}
    if isinstance(category, pylon.CategoryParameter):
        for parameter in category.GetFeatures():
            parameter_name = parameter.GetInfo(pylon.ParameterInfo_Name)
            if isinstance(parameter, pylon.CategoryParameter):
                # Recurse: sub-category becomes a nested dict.
                result[parameter_name] = collect_category(parameter)
            else:
                # Leaf node: convert the current parameter value to a string.
                # str() on a pylon parameter returns its value representation.
                result[parameter_name] = str(parameter)
    return result


def collect_node_map(node_map):
    """Collect all parameters from a GenICam node map.

    Every node map has a virtual 'Root' category that is the single entry
    point for the whole parameter tree.
    """
    
    return collect_category(node_map.GetNode("Root"))

# ---------------------------------------------------------------------------
# Main traversal
# ---------------------------------------------------------------------------

try:
    # TlFactory is the central singleton that manages all installed pylon
    # transport layer plug-ins and hands out device / TL objects.
    transport_layer_factory = pylon.TlFactory.GetInstance()

    # Top-level output structure: a list, one entry per transport layer.
    output = {"transport_layers": []}

    for transport_layer_info in transport_layer_factory.EnumerateTls():
        # --- Transport Layer ---
        # Each installed TL plug-in (e.g. pylon GigE, USB3 Vision, emulation)
        # is represented here.  The info object carries metadata such as the
        # TL name, version, and supported device class.
        tl_entry = {
            "info": transport_layer_info.to_dict(),
            "interfaces": [],
        }

        with transport_layer_factory.TransportLayer(transport_layer_info) as transport_layer:

            for interface_info in transport_layer.EnumerateInterfaces():
                # --- Interface ---
                # An interface maps to a physical host-side port, e.g.,
                # a frame grabber. Some transport layers provide a default interface.
                iface_entry = {
                    "info": interface_info.to_dict(),
                    # Interface-level GenICam parameters (e.g. link speed)
                    "node_map": None,
                    "devices": [],
                }

                with transport_layer.Interface(interface_info) as interface:
                    with interface.NodeMap as node_map:
                        iface_entry["node_map"] = collect_node_map(node_map)

                    for device_info in interface.EnumerateDevices():
                        # --- Device ---
                        # Each device is a physical or emulated camera.
                        # Opening it as an InstantCamera gives access to all
                        # four node maps described below.
                        dev_entry = {
                            "info": device_info.to_dict(),
                            # Main camera node map: pixel format, exposure,
                            # gain, trigger, etc.
                            "node_map": None,
                            # Stream grabber node map: controls the low-level
                            # image acquisition pipeline.
                            "stream_grabber_node_map": None,
                            # Transport-layer node map: TL-specific parameters
                            # like GigE heartbeat timeout.
                            "tl_node_map": None,
                            # Event grabber node map: parameters for
                            # asynchronous camera event notifications
                            # (e.g. exposure end, frame start).
                            "event_grabber_node_map": None,
                        }
                        if transport_layer.IsDeviceAccessible(device_info):
                            with pylon.InstantCamera(device_info, pylon.Unambiguous) as camera:
                                dev_entry["node_map"] = collect_node_map(camera.NodeMap)
                                dev_entry["stream_grabber_node_map"] = collect_node_map(camera.StreamGrabberNodeMap)
                                dev_entry["tl_node_map"] = collect_node_map(camera.TLNodeMap)
                                dev_entry["event_grabber_node_map"] = collect_node_map(camera.EventGrabberNodeMap)

                        iface_entry["devices"].append(dev_entry)

                tl_entry["interfaces"].append(iface_entry)

        output["transport_layers"].append(tl_entry)

    # Note: You can navigate to the parameter documentation using the following URL patterns.
    # https://docs.baslerweb.com/?rhcsh=1&rhmapid={parameter_name}
    # https://docs.baslerweb.com/?rhcsh=1&filter=Camera:{device_info.ModelName}&rhmapid={parameter_name}
    # examples:
    # https://docs.baslerweb.com/?rhcsh=1&rhmapid=Gain
    # https://docs.baslerweb.com/?rhcsh=1&filter=Camera:a2A1920-160umPRO&rhmapid=Gain

    # Serialize the collected data as YAML.
    #   allow_unicode=True  — preserve non-ASCII characters in names/values.
    #   default_flow_style=False — use the readable block style throughout.
    #   sort_keys=False     — preserve the meaningful insertion order above.
    print(yaml.dump(output, allow_unicode=True, default_flow_style=False, sort_keys=False))

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
