from typing import *
import mesh

def render(mesh: mesh.Mesh) -> List[List[int]]:
  """
  Returns a 2-D array representation of the mesh as viewed from the point (0, 0, 0). The values in
  the arrays are ASCII characters in the range [0, 255].
  """

  pass

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

  def __repr__(self):
    return f'<{self.x}, {self.y}>'

def blocks_ray_cast(point: Point2D, face: mesh.Face) -> bool:
  """
  Returns true if the face blocks a ray cast from the origin to the specified point.
  """

  # Project the vertices onto the plane of the viewer.
  projected_vertices = [Point2D.from_point_3d(v) for v in face.vertices]

  # TODO: Explain.
  # Calculate the area of various triangles.
  triangles = split_into_triangles(point, projected_vertices)
  areas = [abs(calculate_2x_area(t)) for t in triangles] # TODO: Explain heavily.

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
