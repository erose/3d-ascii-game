from typing import *
import statistics, time, os, math, ctypes
import mesh, log, math

class EyeSpacePoint(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
  ]

  @classmethod
  def from_point_3d(klass, point: mesh.Point3D, theta: int):
    """
    Projects the input point onto a 2-D plane, scaling appropriately for distance.
    """

    distance = math.sqrt(point.x**2 + point.y**2 + point.z**2)
    return klass(
      (point.x * math.cos(math.radians(theta)) + point.z * math.sin(math.radians(theta))) / distance,
      point.y / distance
    )

  def __repr__(self):
    return f'<{self.x}, {self.y}>'

class EyeSpacePolygon(ctypes.Structure):
  _fields_ = [
    ('vertices', ctypes.POINTER(EyeSpacePoint)),
    ('num_vertices', ctypes.c_int),

    ('min_x', ctypes.c_float),
    ('max_x', ctypes.c_float),
    ('min_y', ctypes.c_float),
    ('max_y', ctypes.c_float),
  ]

  def __init__(self, vertices):
    self.vertices = (EyeSpacePoint * len(vertices))(*vertices)
    self.num_vertices = len(vertices)

  @classmethod
  def from_face(klass, face: mesh.Face, theta: int):
    vertices = [EyeSpacePoint.from_point_3d(v, theta) for v in face.vertices]
    return klass(vertices)

def render(mesh: mesh.Mesh, terminal_width: int, terminal_height: int) -> Dict[Tuple[int, int], str]:
  """
  Returns a 2-D array representation of the mesh as viewed from the point (0, 0, 0). The values in
  the arrays are ASCII characters in the range [0, 255].
  """

  pixels : Dict[Tuple[int, int], str] = {}

  librender = ctypes.CDLL('/home/eli/Personal/Repositories/3d-ascii-game/librender.so')
  polygons = [EyeSpacePolygon.from_face(face, mesh.theta) for face in mesh.faces]

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

  for x in range(terminal_width):
    for y in range(terminal_height):
      pixels[(x, y)] = (c_pixel_array[y][x]).decode("utf-8")

  return pixels
