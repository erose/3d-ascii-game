from typing import *
import time, functools
import mesh, render, log

class CoolDownDecorator:
  def __init__(self, func, interval):
    self.func = func
    self.interval = interval
    self.last_run = None

  def __call__(self, *args, **kwargs):
    now = time.time()
    if (self.last_run is not None) and (now - self.last_run < self.interval):
      return
    else:
      self.last_run = now
      return self.func(*args,**kwargs)

def with_cool_down(interval):
  def apply_decorator(func):
    decorator = CoolDownDecorator(func=func, interval=interval)
    return functools.wraps(func)(decorator)
  return apply_decorator

def draw_frame(stdscreen, width: int, height: int, mesh: mesh.Mesh) -> None:
  start = time.time()
  pixels: Dict[Tuple[int, int], str] = render.render(mesh, width, height)
  log.log('Render took', time.time() - start, 'seconds')
  for (x, y) in pixels.keys():
    stdscreen.addstr(y, x, pixels[x, y])

FORWARD = ord('w')
BACK = ord('s')
LEFT = ord('a')
RIGHT = ord('d')
ROTATE_COUNTERCLOCKWISE = ord('q')
ROTATE_CLOCKWISE = ord('e')

# TODO: Explain.
@with_cool_down(0.5) # seconds
def do_tick(stdscreen, width: int, height: int, mesh: mesh.Mesh):
  draw_frame(stdscreen, width, height, mesh)
  stdscreen.refresh()

  user_input = stdscreen.getch()
  if user_input == FORWARD:
    mesh.translate(0, 0, -100_000)
  elif user_input == BACK:
    mesh.translate(0, 0, 100_000)
  elif user_input == LEFT:
    mesh.translate(100_000, 0, 0)
  elif user_input == RIGHT:
    mesh.translate(-100_000, 0, 0)
  elif user_input == ROTATE_COUNTERCLOCKWISE:
    mesh.rotate_xz(-3)
  elif user_input == ROTATE_CLOCKWISE:
    mesh.rotate_xz(3)
  # TODO: up and down.
  pass

def start_session(stdscreen, width: int, height: int, mesh: mesh.Mesh):
  stdscreen.addstr(0, 0, 'a')
  stdscreen.addstr(1, 0, 'b')
  stdscreen.addstr(0, 1, 'c')
  stdscreen.addstr(1, 1, 'd')

  while True:
    do_tick(stdscreen, width, height, mesh)
