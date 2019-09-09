from typing import List

class Point3D:
  """
  A point in 3D space.
  """

  def __init__(self, x: int, y: int, z: int):
    self.x = x
    self.y = y
    self.z = z

  def __repr__(self):
    return f'<{self.x}, {self.y}, {self.z}>'

class Face:
  """
  A face of a polygon with 3 or more vertices.
  """

  def __init__(self, vertices: List[Point3D]):
    if (len(vertices) < 3):
      raise Exception(f'A face must have three or more vertices, but {vertices} were provided.')

    self.vertices = vertices

  @classmethod
  def from_vertices(klass, *tuples):
    return klass([Point3D(t[0], t[1], t[2]) for t in tuples])

class Mesh:
  """
  A single 3D object.
  """

  def __init__(self, vertices: Point3D, faces: Face):
    self.vertices = vertices
    self.faces = faces

  def translate(self, x: int, y: int, z: int) -> None:
    raise Exception("Not implemented.")
