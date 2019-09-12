from typing import *
import time

def draw_frame(stdscreen, width, height, pixels: Dict[Tuple[int, int], str]) -> None:
  # print("pixel keys", pixels.keys())
  for (x, y) in pixels.keys():
    stdscreen.addstr(x, y, pixels[x, y])
    pass

  while True:
    time.sleep(0.5)
    stdscreen.refresh()
