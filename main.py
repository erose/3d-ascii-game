import curses, sys
import terminal, render, parser

if __name__ == "__main__":
  filename = "teapot.obj" if len(sys.argv) <= 1 else sys.argv[1]

  with open(sys.argv[1]) as f:
    mesh = parser.mesh_from_obj_file(f)
    mesh.translate(0, 0, 3) # Don't be in the middle of the teapot!

    curses.wrapper(
      terminal.draw_frame,
      render.TERMINAL_WIDTH,
      render.TERMINAL_HEIGHT,
      render.render(mesh)
    )
