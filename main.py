import curses
import terminal, mesh, render, parser

if __name__ == "__main__":
  with open("teapot.obj") as f:
    mesh = parser.mesh_from_obj_file(f)
    mesh.translate(0, 0, 5) # Don't be in the middle of the teapot!

    curses.wrapper(
      terminal.draw_frame,
      render.TERMINAL_WIDTH,
      render.TERMINAL_HEIGHT,
      render.render(mesh)
    )
