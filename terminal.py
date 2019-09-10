import curses, time
import mesh, render
from typing import *

# TODO: Duplicated. Delete.
VIEWPORT_WIDTH = 2_000_000
VIEWPORT_HEIGHT = 2_000_000

def draw_frame(stdscreen, pixels: Dict[Tuple[int, int], str]) -> None:
  for (x, y) in pixels.keys():
    stdscreen.addstr(x, y, pixels[x, y])

  while True:
    time.sleep(0.5)
    stdscreen.refresh()

if __name__ == "__main__":
  to_viewport = lambda x: x * VIEWPORT_WIDTH / 2

  vertex_tuples = [
    (0, 0, 1),
    (to_viewport(1), 0, 1),
    (to_viewport(1), to_viewport(1), 1),
    (0, to_viewport(1), 1)
  ]
  face = mesh.Face.covering_tuples(*vertex_tuples)
  test_mesh = mesh.Mesh([mesh.Point3D.from_tuple(p) for p in vertex_tuples], [face])

  curses.wrapper(draw_frame, render.render(test_mesh))
