import sys

def log(*args):
  print(*args, file=sys.stderr)
