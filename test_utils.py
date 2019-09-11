from typing import *
import mesh, render

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

def render_to_string(mesh_to_render: mesh.Mesh, terminal_width: int, terminal_height: int) -> str:
  """
  Returns a string representation of the mesh.
  """

  pixels = render.render(mesh_to_render, terminal_width, terminal_height)

  # List of rows.
  characters = [[' ' for cell in range(terminal_width)] for row in range(terminal_height)]

  for (x, y) in pixels.keys():
    characters[y][x] = pixels[x, y]

  return '\n'.join([''.join(column) for column in characters])
