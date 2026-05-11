import numpy as np
from pypylon import pylon

def create_mandelbrot_fractal(pixel_type, width, height):
    # Palette (same as C++)
    palette = np.array([
        [0, 28, 50], [0, 42, 75], [0, 56, 100], [0, 70, 125], [0, 84, 150],
        [0, 50, 0], [0, 100, 0], [0, 150, 0], [0, 200, 0], [0, 250, 0],
        [50, 0, 0], [100, 0, 0], [150, 0, 0], [200, 0, 0], [250, 0, 0]
    ], dtype=np.uint8)

    num_colors = len(palette)

    # Constants
    MAX_X, MIN_X = 1.0, -2.0
    MAX_Y, MIN_Y = 1.2, -1.2
    MAX_ITERATIONS = 50

    # Create coordinate grid
    x = np.linspace(MIN_X, MAX_X, width)
    y = np.linspace(MAX_Y, MIN_Y, height)
    grid_x, grid_y = np.meshgrid(x, y)

    # Initialize complex plane
    z_x = grid_x.copy()
    z_y = grid_y.copy()

    # Iteration counter
    iterations = np.zeros(grid_x.shape, dtype=np.uint32)

    # Mask for active pixels
    mask = np.ones(grid_x.shape, dtype=bool)

    # Mandelbrot iteration
    for i in range(MAX_ITERATIONS):
        # Work only on active pixels
        z_x_active = z_x[mask]
        z_y_active = z_y[mask]
        grid_x_active = grid_x[mask]
        grid_y_active = grid_y[mask]

        z_x_sq = z_x_active * z_x_active
        z_y_sq = z_y_active * z_y_active

        escaped = (z_x_sq + z_y_sq) > 4.0

        # Record iteration where escape happens
        iterations[mask] = i

        # Keep only those that did NOT escape
        still_active = ~escaped

        # Update Z only for still active pixels
        z_x_new = z_x_sq[still_active] - z_y_sq[still_active] + grid_x_active[still_active]
        z_y_new = 2 * z_x_active[still_active] * z_y_active[still_active] + grid_y_active[still_active]

        # Write back updates
        idx = np.where(mask)
        active_idx = tuple(i[still_active] for i in idx)

        z_x[active_idx] = z_x_new
        z_y[active_idx] = z_y_new

        # Update mask
        mask[mask] = still_active

        if not mask.any():
            break

    # Points that never escaped
    iterations[mask] = MAX_ITERATIONS

    # Create RGB image
    image = np.zeros((height, width, 3), dtype=np.uint8)

    inside = iterations >= MAX_ITERATIONS
    outside = ~inside

    image[inside] = palette[0]
    image[outside] = palette[iterations[outside] % num_colors]

    # Create Pylon image
    pylon_image = pylon.PylonImage()
    pylon_image.AttachArray(image, pylon.PixelType_RGB8packed)

    # Convert if needed
    if pylon_image.GetPixelType() != pixel_type:
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pixel_type
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        return converter.Convert(pylon_image)

    return pylon_image

