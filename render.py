from typing import *
import statistics, time, os, ctypes
import mesh

EYE_WIDTH = 2
EYE_HEIGHT = 2

# W <-- for safekeeping
ASCII_BLOCK = '▓'

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

  @classmethod
  def from_terminal_space(klass, x: int, y: int, terminal_width: int, terminal_height: int):
    """
    From coordinates describing a point in the terminal, constructs the corresponding point in the
    scene.
    """

    # (x, y) is the upper left corner of the pixel we're filling in. (x + 0.5, y + 0.5) is the middle.
    return klass(
      (x + 0.5 - terminal_width / 2) * (EYE_WIDTH / terminal_width),
      (y + 0.5 - terminal_height / 2) * (EYE_HEIGHT / terminal_height),
    )

  def __repr__(self):
    return f'<{self.x}, {self.y}>'

class EyeSpacePolygon:
  # _fields_ = [
  # ]

  def __init__(self, vertices: List[EyeSpacePoint]):
    self.vertices = vertices

  @classmethod
  def from_face(klass, face: mesh.Face):
    vertices = [EyeSpacePoint.from_point_3d(v) for v in face.vertices]
    return klass(vertices)

def render(mesh: mesh.Mesh, terminal_width: int, terminal_height: int) -> Dict[Tuple[int, int], str]:
  """
  Returns a 2-D array representation of the mesh as viewed from the point (0, 0, 0). The values in
  the arrays are ASCII characters in the range [0, 255].
  """

  pixels = {}

  for x in range(terminal_width):
    for y in range(terminal_height):
      point = EyeSpacePoint.from_terminal_space(x, y, terminal_width, terminal_height)

      for face in mesh.faces:
        if blocks_ray_cast(point, face):
          pixels[(x, y)] = ASCII_BLOCK
          break

    if os.environ.get('VERBOSE'):
      print(f'Column rendered! {x}')

  return pixels

def blocks_ray_cast(point: EyeSpacePoint, face: mesh.Face) -> bool:
  """
  Returns true if the face blocks a ray cast from the origin to the specified point.
  """

  # Our overall strategy: project the vertices onto the plane of the viewer, then check if the point
  # in question is contained within the projected vertices.
  polgyon = EyeSpacePolygon.from_face(face)

  # We follow the method described here to determine whether the point is contained in the 2D
  # projection of the face.
  # https://math.stackexchange.com/questions/3350182/does-this-method-of-determining-whether-a-point-is-included-in-a-polygon-work-a
  
  # Calculate the area of various triangles.
  triangles = split_into_triangles(point, polgyon.vertices)
  areas = [calculate_2x_area(t) for t in triangles]

  return sum(areas) == calculate_2x_area(polgyon.vertices)

def split_into_triangles(point: EyeSpacePoint, vertices: List[EyeSpacePoint]) -> List[List[EyeSpacePoint]]:
  # All consecutive pairs, wrapping around.
  pairs_of_vertices = zip(vertices, vertices[1:] + [vertices[0]])

  return [[point, a, b] for (a, b) in pairs_of_vertices]

def calculate_2x_area(vertices: List[EyeSpacePoint]) -> float:
  """
  Returns the area of the provided polygon, multiplied by 2. (This lets us avoid floats.) Note: this
  method will return incorrect values unless are specified in clockwise OR counterclockwise order.
  """

  # TODO: Check for correct order.

  # All consecutive pairs, wrapping around.
  pairs_of_vertices = zip(vertices, vertices[1:] + [vertices[0]])

  return abs(
    sum((a.x * b.y) - (a.y * b.x) for (a, b) in pairs_of_vertices)
  )
