import unittest
import mesh
from render import *

class TestRender(unittest.TestCase):
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

  def test_blocks_ray_cast_for_triangle(self):
    self.assertTrue(
      blocks_ray_cast(
        Point2D(1, 1),
        mesh.Face.from_vertices((0, 0, 0.1), (2, 0, 0.1), (2, 2, 2))
      )
    )

  def test_negative_point_not_blocks_ray_cast_for_triangle(self):
    self.assertFalse(
      blocks_ray_cast(
        Point2D(-1, 1),
        mesh.Face.from_vertices((0, 0, 0.1), (2, 0, 0.1), (2, 2, 2))
      )
    )

  def test_not_blocks_ray_cast_for_triangle(self):
    self.assertFalse(
      blocks_ray_cast(
        Point2D(100, 100),
        mesh.Face.from_vertices((0, 0, 0.1), (2, 0, 0.1), (2, 2, 2))
      )
    )

  def test_not_blocks_ray_cast_for_triangle(self):
    self.assertFalse(
      blocks_ray_cast(
        Point2D(100, 100),
        mesh.Face.from_vertices((0, 0, 0.1), (9, 0, 0.1), (9, 9, 0.1), (0, 9, 0.1))
      )
    )

if __name__ == "__main__":
  unittest.main()
