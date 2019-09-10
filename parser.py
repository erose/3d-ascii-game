from typing import *
import mesh

VERTEX_PREFIX = 'v '
FACE_PREFIX = 'f '

def mesh_from_obj_file(file) -> mesh.Mesh:
  """
  Parse a .obj file (https://en.wikipedia.org/wiki/Wavefront_.obj_file) into a Mesh.
  """
  vertices: List[mesh.Point3D] = []
  faces: List[mesh.Face] = []

  for line in file:
    line = line.strip()

    if line.startswith(VERTEX_PREFIX):
      if faces:
        raise Exception(f'''A properly formatted .obj file declares all vertices before faces, but
          faces had length {len(faces)} as we read in line {line}.''')

      # Eat the 'v' token since we now know this is a vertex.
      vertex = _parse_vertex(line.replace(VERTEX_PREFIX, ''))
      vertices.append(vertex)

    if line.startswith(FACE_PREFIX):
      # Eat the 'f' token since we now know this is a face.
      face = _parse_face(vertices, line.replace(FACE_PREFIX, ''))
      faces.append(face)

  return mesh.Mesh(vertices, faces)


def _parse_vertex(line: str) -> mesh.Point3D:
  tokens = line.split(' ')
  if not (3 <= len(tokens) <= 4):
    raise Exception(f'A vertex is defined by exactly three or four numbers, but line was: {line}.')

  ints = [_to_int(token) for token in tokens]
  return mesh.Point3D(ints[0], ints[1], ints[2])

def _to_int(float_string: str) -> int:
  """
  We want to work with ints to avoid precision loss, but .obj files give values in floats.
  """
  scale_factor = 1_000_000
  f = float(float_string)

  digits_after_decimal = 0 if '.' not in float_string else len(float_string.split('.')[-1])
  zeroes_in_scale_factor = len(str(scale_factor)) - 1

  if digits_after_decimal > zeroes_in_scale_factor:
    raise Exception(f'More digits after the decimal point than zeroes in scale factor: {float_string}. digits_after_decimal: {digits_after_decimal}. zeroes_in_scale_factor: {zeroes_in_scale_factor}')
  
  return round(f * scale_factor)

def _parse_face(vertices: List[mesh.Point3D], line: str) -> mesh.Face:
  """
  Faces refer to vertices by index.
  """

  tokens = line.split(' ')
  if len(tokens) <= 2:
    raise Exception(f'A face is defined by three or more indices, but line was: {line}.')

  indices = [int(token) - 1 for token in tokens] # The indices start at 1.
  referenced_vertices = [vertices[i] for i in indices]

  return mesh.Face(referenced_vertices)
