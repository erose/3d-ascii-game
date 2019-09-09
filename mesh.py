from typing import List

class Point:
  """
  A point in 3D space.
  """

  def __init__(self, x: float, y: float, z: float):
    self.x = x
    self.y = y
    self.z = z

  def __repr__(self):
    return f'<{self.x}, {self.y}, {self.z}>'

class Face:
  """
  A face of a polygon with 3 or more vertices.
  """

  def __init__(self, vertices: List[Point]):
    if (len(vertices) < 3):
      raise Exception(f'A face must have three or more vertices, but {vertices} were provided.')

    self.vertices = vertices

class Mesh:
  """
  A single 3D object.
  """

  def __init__(self, vertices: Point, faces: Face):
    self.vertices = vertices
    self.faces = faces
