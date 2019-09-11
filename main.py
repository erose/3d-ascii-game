import curses, sys
import terminal, render, parser

# Terminal space goes from (0, 0) to (TERMINAL_WIDTH, TERMINAL_HEIGHT).
TERMINAL_WIDTH = 60
TERMINAL_HEIGHT = 60

if __name__ == "__main__":
  filename = "teapot.obj" if len(sys.argv) <= 1 else sys.argv[1]

  with open(filename) as f:
    mesh = parser.mesh_from_obj_file(f)
    mesh.translate(0, 0, 4_000_000) # Don't be in the middle of the teapot!

    curses.wrapper(
      terminal.draw_frame,
      TERMINAL_WIDTH,
      TERMINAL_HEIGHT,
      render.render(mesh, TERMINAL_WIDTH, TERMINAL_HEIGHT)
    )
