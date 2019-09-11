import unittest
import mesh
from render import *
import test_utils

class TestCalculateArea(unittest.TestCase):
  def test_calculate_2x_area_for_simple_triangle(self):
    self.assertEqual(
      calculate_2x_area([Point2D(0, 0), Point2D(1, 0), Point2D(0, 1)]),
      1,
    )

  def test_calculate_2x_area_for_square(self):
    self.assertEqual(
      calculate_2x_area([Point2D(0, 0), Point2D(1, 0), Point2D(1, 1), Point2D(0, 1)]),
      2,
    )

class TestBlocksRayCast(unittest.TestCase):
  def test_blocks_ray_cast_for_triangle(self):
    self.assertTrue(
      blocks_ray_cast(
        Point2D(1, 1),
        mesh.Face.covering_tuples((0, 0, 1), (2, 0, 1), (2, 2, 2))
      )
    )

  def test_negative_point_not_blocks_ray_cast_for_triangle(self):
    self.assertFalse(
      blocks_ray_cast(
        Point2D(-1, 1),
        mesh.Face.covering_tuples((0, 0, 1), (2, 0, 1), (2, 2, 2))
      )
    )

  def test_not_blocks_ray_cast_for_triangle(self):
    self.assertFalse(
      blocks_ray_cast(
        Point2D(100, 100),
        mesh.Face.covering_tuples((0, 0, 1), (2, 0, 1), (2, 2, 2))
      )
    )

  def test_not_blocks_ray_cast_for_square(self):
    self.assertFalse(
      blocks_ray_cast(
        Point2D(100, 100),
        mesh.Face.covering_tuples((0, 0, 1), (9, 0, 1), (9, 9, 1), (0, 9, 1))
      )
    )

  def test_blocks_ray_cast_for_square(self):
    self.assertTrue(
      blocks_ray_cast(
        Point2D(8, 8),
        mesh.Face.covering_tuples((0, 0, 1), (9, 0, 1), (9, 9, 1), (0, 9, 1))
      )
    )

  def test_blocks_ray_cast_for_concave_face(self):
    self.assertFalse(
      blocks_ray_cast(
        Point2D(0, -1),
        mesh.Face.covering_tuples((0, 0, 1), (1, -2, 1), (0, 3, 1), (-1,-2, 1))
      )
    )

class TestRender(unittest.TestCase):
  def test_render_small_square(self):
    terminal_width, terminal_height = 10, 10

    vertex_tuples = [
      (0, 0, 5),
      (2, 0, 5),
      (2, 2, 5),
      (0, 2, 5),
    ]
    face = mesh.Face.covering_tuples(*vertex_tuples)
    test_mesh = mesh.Mesh([mesh.Point3D.from_tuple(p) for p in vertex_tuples], [face])

    print(test_utils.render_to_string(test_mesh, terminal_width, terminal_height))
    # self.maxDiff = None # These dicts are large; we want to see the whole diff if the test fails.
    # self.assertEqual(
    #   {(a, b): ASCII_BLOCK for a in range(5) for b in range(5)},
    #   render(test_mesh, terminal_width, terminal_height),
    # )

if __name__ == "__main__":
  unittest.main()
