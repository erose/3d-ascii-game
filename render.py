from typing import *
import mesh

TERMINAL_WIDTH = 80
TERMINAL_HEIGHT = 80

# How many units of the scene the player can see at any time, at z = 1.
VIEWPORT_WIDTH = 2_000_000
VIEWPORT_HEIGHT = 2_000_000

# W <-- for safekeeping
ASCII_BLOCK = '▓'

class Point2D:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  @classmethod
  def from_point_3d(klass, point: mesh.Point3D):
    """
    Projects the input point onto a 2-D plane, scaling appropriately for distance.
    """

    return klass(point.x / point.z, point.y / point.z)

  @classmethod
  def from_terminal_space(klass, x: int, y: int):
    """
    From coordinates describing a point in the terminal, constructs the corresponding point in the
    scene.
    """

    return klass(x * (VIEWPORT_WIDTH / TERMINAL_WIDTH), y * (VIEWPORT_HEIGHT / TERMINAL_HEIGHT))

  def __repr__(self):
    return f'<{self.x}, {self.y}>'

def render(mesh: mesh.Mesh) -> Dict[Tuple[int, int], str]:
  """
  Returns a 2-D array representation of the mesh as viewed from the point (0, 0, 0). The values in
  the arrays are ASCII characters in the range [0, 255].
  """

  pixels = {}

  for x in range(-TERMINAL_WIDTH // 2, TERMINAL_WIDTH // 2):
    for y in range(-TERMINAL_HEIGHT // 2, TERMINAL_HEIGHT // 2):
      point = Point2D.from_terminal_space(x, y)
      # print(f'point in terminal space: {point}')
      for face in mesh.faces:
        if blocks_ray_cast(point, face):
          pixels[(x, y)] = ASCII_BLOCK

  return pixels

def blocks_ray_cast(point: Point2D, face: mesh.Face) -> bool:
  """
  Returns true if the face blocks a ray cast from the origin to the specified point.
  """

  # Our overall strategy: project the vertices onto the plane of the viewer, then check if the point
  # in question is contained within the projected vertices.

  projected_vertices = [Point2D.from_point_3d(v) for v in face.vertices]

  # We follow the method described here to determine whether the point is contained in the 2D
  # projection of the face.
  # https://math.stackexchange.com/questions/3350182/does-this-method-of-determining-whether-a-point-is-included-in-a-polygon-work-a
  
  # Calculate the area of various triangles.
  triangles = split_into_triangles(point, projected_vertices)
  areas = [calculate_2x_area(t) for t in triangles]

  return sum(areas) == calculate_2x_area(projected_vertices)

def split_into_triangles(point: Point2D, vertices: List[Point2D]) -> List[List[Point2D]]:
  # All consecutive pairs, wrapping around.
  pairs_of_vertices = zip(vertices, vertices[1:] + [vertices[0]])

  return [[point, a, b] for (a, b) in pairs_of_vertices]

def calculate_2x_area(vertices: List[Point2D]) -> int:
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
