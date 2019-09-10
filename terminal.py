import time
from typing import *

def draw_frame(stdscreen, pixels: Dict[Tuple[int, int], str]) -> None:
  for (x, y) in pixels.keys():
    stdscreen.addstr(x, y, pixels[x, y])

  while True:
    time.sleep(0.5)
    stdscreen.refresh()
