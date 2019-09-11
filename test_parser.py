import unittest
from parser import *
import mesh
import test_utils

class TestParseMeshFromObjFile(unittest.TestCase):
  def test_with_only_vertices(self):
    test_obj_file = [
      'v 0 0 10',
      'v 1 0 10',
      'v 1 1 10',
      'v 0 1 10',
    ]
    
    test_mesh = test_utils.mesh_from_small_tuples([
      (0, 0, 10),
      (1, 0, 10),
      (1, 1, 10),
      (0, 1, 10)
    ])
    test_mesh.faces = [] # Our test object file has no faces.

    self.assertEqual(
      test_mesh,
      mesh_from_obj_file(test_obj_file)
    )

  def test_square(self):
    test_obj_file = [
      'v 0 0 10',
      'v 1 0 10',
      'v 1 1 10',
      'v 0 1 10',
      'f 1 2 3 4',
    ]
    
    test_mesh = test_utils.mesh_from_small_tuples([
      (0, 0, 10),
      (1, 0, 10),
      (1, 1, 10),
      (0, 1, 10),
    ])

    self.assertEqual(
      test_mesh,
      mesh_from_obj_file(test_obj_file)
    )

  def test_weights_are_ignored(self):
    test_obj_file = [
      'v 0 0 10 5',
      'v 1 0 10 5',
      'v 1 1 10 5',
      'v 0 1 10 5',
    ]
    
    test_mesh = test_utils.mesh_from_small_tuples([
      (0, 0, 10),
      (1, 0, 10),
      (1, 1, 10),
      (0, 1, 10)
    ])
    test_mesh.faces = [] # Our test object file has no faces.

    self.assertEqual(
      test_mesh,
      mesh_from_obj_file(test_obj_file)
    )

if __name__ == "__main__":
  unittest.main()
