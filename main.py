import curses
import terminal, mesh, render

if __name__ == "__main__":
  to_viewport = lambda x: x * render.VIEWPORT_WIDTH / 2

  vertex_tuples = [
    (0, 0, 1),
    (to_viewport(1), 0, 1),
    (to_viewport(1), to_viewport(1), 1),
    (0, to_viewport(1), 1)
  ]
  face = mesh.Face.covering_tuples(*vertex_tuples)
  test_mesh = mesh.Mesh([mesh.Point3D.from_tuple(p) for p in vertex_tuples], [face])

  curses.wrapper(terminal.draw_frame, render.render(test_mesh))
