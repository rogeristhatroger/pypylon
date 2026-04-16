#!/usr/bin/env python3
"""\
This sample shows how to register a callback on a camera parameter node.

When a node value changes, all registered callbacks for that node are
invoked automatically. This mechanism can be used to react to parameter
changes made by the application, by the camera, or by external tools
such as the pylon Viewer.

The sample demonstrates two approaches:
1. A free function as a callback.
2. A bound method of a class instance (observer pattern).

Both are registered on the Width node. Changing the node value triggers
all registered callbacks. After deregistering, further changes no longer
invoke them.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon
from pypylon import genicam


def on_node_changed(node):
    """Free-function callback, invoked whenever the node value changes."""
    print(f"  [function] node changed: {node.Node.Name}")


class NodeObserver:
    """Observer whose bound method is used as a callback."""

    def on_node_changed(self, node):
        print(f"  [observer] node changed: {node.Node.Name}")


exit_code = 0
try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)

        original_width = camera.Width.Value

        # --- Approach 1: free function ---
        # genicam.Register accepts any callable. Here we pass a plain function.
        print("\n--- Free function callback ---")
        func_handle = genicam.Register(camera.Width.Node, on_node_changed)

        print(f"Setting Width to maximum ({camera.Width.Max})...")
        camera.Width.Value = camera.Width.Max

        print(f"Restoring Width to {original_width}...")
        camera.Width.Value = original_width

        genicam.Deregister(func_handle)

        # --- Approach 2: bound method (observer pattern) ---
        # A bound method (instance.method) is also a callable, so it works
        # the same way. This is useful when the callback needs access to
        # instance state.
        print("\n--- Bound method callback (observer) ---")
        observer = NodeObserver()
        observer_handle = genicam.Register(
            camera.Width.Node, observer.on_node_changed
        )

        print(f"Setting Width to maximum ({camera.Width.Max})...")
        camera.Width.Value = camera.Width.Max

        print(f"Restoring Width to {original_width}...")
        camera.Width.Value = original_width

        genicam.Deregister(observer_handle)

        # After deregistering, changes no longer trigger any callback.
        print("\n--- After deregistering both ---")
        print(f"Setting Width to maximum (no callback expected)...")
        camera.Width.Value = camera.Width.Max
        camera.Width.Value = original_width

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
