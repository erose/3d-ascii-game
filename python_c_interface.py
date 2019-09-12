# import ctypes
# import render

# terminal_width = 10
# terminal_height = 10

# librender = ctypes.CDLL('/home/eli/Personal/Repositories/3d-ascii-game/librender.so')

# points = [render.EyeSpacePoint(-1, -1), render.EyeSpacePoint(1, 1), render.EyeSpacePoint(2, -1)]
# polygons = [render.EyeSpacePolygon(points)]

# # TODO: Explain.
# PixelsRow = ctypes.c_char * terminal_width
# PixelsType = PixelsRow * terminal_height

# librender.render.argtypes = (
#   render.EyeSpacePolygon * len(polygons),
  
#   ctypes.c_int,
#   ctypes.c_int,
#   ctypes.c_int,

#   PixelsType,
# )

# # List of rows.
# pixels = [[b' ' for cell in range(terminal_width)] for row in range(terminal_height)]
# c_pixels = PixelsType(*[PixelsRow(*row) for row in pixels])
# c_polygons = (render.EyeSpacePolygon * len(polygons))(*polygons)

# librender.render(c_polygons, len(c_polygons), terminal_width, terminal_height, c_pixels)

# for x in range(terminal_width):
#   for y in range(terminal_height):
#     print((c_pixels[y][x]).decode("utf-8"), end='')
#   print()
