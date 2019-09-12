from typing import *
import statistics, time, os, ctypes
import mesh
import time

class EyeSpacePoint(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
  ]

  @classmethod
  def from_point_3d(klass, point: mesh.Point3D):
    """
    Projects the input point onto a 2-D plane, scaling appropriately for distance.
    """

    return klass(point.x / point.z, point.y / point.z)

  def __repr__(self):
    return f'<{self.x}, {self.y}>'

class EyeSpacePolygon(ctypes.Structure):
  _fields_ = [
    ('vertices', ctypes.POINTER(EyeSpacePoint)),
    ('num_vertices', ctypes.c_int),
  ]

  def __init__(self, vertices):
    self.vertices = (EyeSpacePoint * len(vertices))(*vertices)
    self.num_vertices = len(vertices)

  @classmethod
  def from_face(klass, face: mesh.Face):
    vertices = [EyeSpacePoint.from_point_3d(v) for v in face.vertices]
    return klass(vertices)

def render(mesh: mesh.Mesh, terminal_width: int, terminal_height: int) -> Dict[Tuple[int, int], str]:
  """
  Returns a 2-D array representation of the mesh as viewed from the point (0, 0, 0). The values in
  the arrays are ASCII characters in the range [0, 255].
  """

  pixels : Dict[Tuple[int, int], str] = {}

  librender = ctypes.CDLL('/home/eli/Personal/Repositories/3d-ascii-game/librender.so')
  polygons = [EyeSpacePolygon.from_face(face) for face in mesh.faces]

  # TODO: Explain.
  PixelsRow = ctypes.c_char * terminal_width
  PixelsType = PixelsRow * terminal_height

  librender.render.argtypes = (
    EyeSpacePolygon * len(polygons),
    
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,

    PixelsType,
  )

  # List of rows.
  pixel_array = [[b' ' for cell in range(terminal_width)] for row in range(terminal_height)]
  c_pixel_array = PixelsType(*[PixelsRow(*row) for row in pixel_array])
  c_polygons = (EyeSpacePolygon * len(polygons))(*polygons)

  # Mutates c_pixel_array.
  start = time.time()
  librender.render(c_polygons, len(c_polygons), terminal_width, terminal_height, c_pixel_array)
  print('C portion of render took', time.time() - start, 'seconds')

  for x in range(terminal_width):
    for y in range(terminal_height):
      pixels[(x, y)] = (c_pixel_array[y][x]).decode("utf-8")

  return pixels
