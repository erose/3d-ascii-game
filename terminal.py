from typing import *
import time, functools
import mesh, render

class CoolDownDecorator:
  def __init__(self, func, interval):
    self.func = func
    self.interval = interval
    self.last_run = 0

  # def __get__(self, obj):
  #   return partial(self, obj)

  def __call__(self, *args, **kwargs):
    now = time.time()
    if now - self.last_run < self.interval:
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
  print('Render took', time.time() - start, 'seconds')
  for (x, y) in pixels.keys():
    stdscreen.addstr(y, x, pixels[x, y])

FORWARD = ord('w')
BACK = ord('s')
LEFT = ord('a')
RIGHT = ord('d')

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
  # TODO: up and down.
  pass

def start_session(stdscreen, width: int, height: int, mesh: mesh.Mesh):
  while True:
    do_tick(stdscreen, width, height, mesh)
