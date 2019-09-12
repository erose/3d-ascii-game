import unittest
import mesh
from render import *
import test_utils

class TestRender(unittest.TestCase):
  def test_render_small_square(self):
    small_square = (
      '          \n'
      '          \n'
      '          \n'
      '     WW   \n'
      '     WW   \n'
      '          \n'
      '          \n'
      '          \n'
      '          \n'
      '          '
    )
    terminal_width, terminal_height = 10, 10

    vertex_tuples = [
      (0, 0, 5),
      (2, 0, 5),
      (2, 2, 5),
      (0, 2, 5),
    ]
    face = mesh.Face.covering_tuples(*vertex_tuples)
    test_mesh = mesh.Mesh([mesh.Point3D.from_tuple(p) for p in vertex_tuples], [face])

    self.maxDiff = None # These strings are large; we want to see the whole diff if the test fails.
    self.assertEqual(
      small_square,
      test_utils.render_to_string(test_mesh, terminal_width, terminal_height)
    )

if __name__ == "__main__":
  unittest.main()
