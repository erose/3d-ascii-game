from typing import *

class Point3D:
  """
  A point in 3D space.
  """

  def __init__(self, x: int, y: int, z: int):
    self.x = x
    self.y = y
    self.z = z

  @classmethod
  def from_tuple(klass, tuple: Tuple[int, int, int]):
    return klass(tuple[0], tuple[1], tuple[2])

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
  def covering_tuples(klass, *tuples: Tuple[int, int, int]):
    """
    Returns a face which connects the vertices represented by the input tuples.
    """
    return klass([Point3D.from_tuple(t) for t in tuples])

class Mesh:
  """
  A single 3D object.
  """

  def __init__(self, vertices: List[Point3D], faces: List[Face]):
    self.vertices = vertices
    self.faces = faces

  def translate(self, x: int, y: int, z: int) -> None:
    raise Exception("Not implemented.")
