import unittest
import mesh
from render import *

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
        mesh.Face.covering_tuples((0, 0, 0.1), (2, 0, 0.1), (2, 2, 2))
      )
    )

  def test_negative_point_not_blocks_ray_cast_for_triangle(self):
    self.assertFalse(
      blocks_ray_cast(
        Point2D(-1, 1),
        mesh.Face.covering_tuples((0, 0, 0.1), (2, 0, 0.1), (2, 2, 2))
      )
    )

  def test_not_blocks_ray_cast_for_triangle(self):
    self.assertFalse(
      blocks_ray_cast(
        Point2D(100, 100),
        mesh.Face.covering_tuples((0, 0, 0.1), (2, 0, 0.1), (2, 2, 2))
      )
    )

  def test_not_blocks_ray_cast_for_square(self):
    self.assertFalse(
      blocks_ray_cast(
        Point2D(100, 100),
        mesh.Face.covering_tuples((0, 0, 0.1), (9, 0, 0.1), (9, 9, 0.1), (0, 9, 0.1))
      )
    )

  def test_blocks_ray_cast_for_square(self):
    self.assertTrue(
      blocks_ray_cast(
        Point2D(80, 80),
        mesh.Face.covering_tuples((0, 0, 0.1), (9, 0, 0.1), (9, 9, 0.1), (0, 9, 0.1))
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
    to_viewport = lambda x: x * VIEWPORT_WIDTH / 2

    vertex_tuples = [
      (0, 0, 10),
      (to_viewport(1), 0, 10),
      (to_viewport(1), to_viewport(1), 10),
      (0, to_viewport(1), 10)
    ]
    face = mesh.Face.covering_tuples(*vertex_tuples)
    test_mesh = mesh.Mesh([mesh.Point3D.from_tuple(p) for p in vertex_tuples], [face])

    self.assertEqual(
      render(test_mesh),
      {(a, b): ASCII_BLOCK for a in range(5) for b in range(5)}
    )

if __name__ == "__main__":
  unittest.main()
