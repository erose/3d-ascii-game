import parser, test_utils, time

if __name__ == "__main__":
  mesh = parser.mesh_from_obj_file(open("teapot.obj"))
  mesh.translate(0, 0, 4_000_000) # Don't be in the middle of the teapot!

  start = time.time()
  test_utils.render_to_string(mesh, 252, 252)
  print('total time taken:', time.time() - start)
