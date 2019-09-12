import curses, sys
import terminal, render, parser

# Terminal space goes from (0, 0) to (TERMINAL_WIDTH, TERMINAL_HEIGHT).
TERMINAL_WIDTH = 120
TERMINAL_HEIGHT = 120

def assert_terminal_size():
  # Initialize the curses window just to get the terminal size, de-initializing it immediately
  # afterward. (We use curses.wrapper to do the actual rendering.)
  max_terminal_height, max_terminal_width = curses.initscr().getmaxyx()
  curses.endwin()

  if max_terminal_width < TERMINAL_WIDTH:
    raise Exception(f'Requested terminal width is {TERMINAL_WIDTH}, but the window has width {max_terminal_width}.')
  if max_terminal_height < TERMINAL_HEIGHT:
    raise Exception(f'Requested terminal height is {TERMINAL_HEIGHT}, but the window has height {max_terminal_height}.')

if __name__ == "__main__":
  assert_terminal_size()
  filename = "teapot.obj" if len(sys.argv) <= 1 else sys.argv[1]

  with open(filename) as f:
    mesh = parser.mesh_from_obj_file(f)
    mesh.translate(0, 0, 4_000_000) # Don't be in the middle of the teapot!

    curses.wrapper(
      terminal.start_session,
      TERMINAL_WIDTH,
      TERMINAL_HEIGHT,
      mesh,
    )
