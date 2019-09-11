import unittest
import mesh

class TestFace(unittest.TestCase):
  def test_raises_exception_if_fewer_than_three_vertices(self):
    with self.assertRaises(Exception):
      mesh.Face(
        [mesh.Point(1, 2, 3), mesh.Point(2, 2, 3)]
      )

if __name__ == "__main__":
  unittest.main()
