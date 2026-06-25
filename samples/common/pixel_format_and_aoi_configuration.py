"""Configuration that sets a pixel format and maximizes the Image AOI."""

from pypylon import pylon


class PixelFormatAndAoiConfiguration(pylon.ConfigurationEventHandler):
    """Apply a Mono8 pixel format and maximize the AOI when the camera opens."""

    def OnOpened(self, camera):
        # Maximize the Image AOI. OffsetX/Y are read-only on some cameras,
        # so the Try* variants are used for the offsets.
        camera.OffsetX.TrySetToMinimum()
        camera.OffsetY.TrySetToMinimum()
        camera.Width.SetToMaximum()
        camera.Height.SetToMaximum()

        # Set the pixel data format. Not every device offers Mono8; the
        # Try variant leaves the current format in place if Mono8 is
        # unavailable.
        camera.PixelFormat.TrySetValue("Mono8")
