from typing import *
import mesh

def mesh_from_small_tuples(vertex_tuples: List[Tuple[int, int, int]]) -> mesh.Mesh:
  """
  Constructs a mesh containing with the provided tuples as vertices and a single face which
  includes all its vertices
  """
  scale_factor = 1_000_000

  scaled_vertices = [
    (t[0] * scale_factor, t[1] * scale_factor, t[2] * scale_factor) for t in vertex_tuples
  ]
  face = mesh.Face.covering_tuples(*scaled_vertices)
  
  return mesh.Mesh([mesh.Point3D.from_tuple(p) for p in scaled_vertices], [face])
