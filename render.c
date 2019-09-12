#include <math.h>
#include <stdio.h>
#include <stdbool.h>
#include <sys/time.h>


typedef struct {
  float x;
  float y;
} Point;

typedef struct {
  Point start;
  Point end;
} Vector;

typedef struct {
  Point* vertices;
  int num_vertices;
  // Useful for determining bounding boxes.
  float min_x;
  float max_x;
  float min_y;
  float max_y;
} Polygon;

float min_x(Polygon polygon) {
  float result = INFINITY;
  for (int i = 0; i < polygon.num_vertices; i++) {
    if (result > polygon.vertices[i].x) {
      result = polygon.vertices[i].x;
    }
  }

  return result;
}

float max_x(Polygon polygon) {
  float result = -INFINITY;
  for (int i = 0; i < polygon.num_vertices; i++) {
    if (result < polygon.vertices[i].x) {
      result = polygon.vertices[i].x;
    }
  }

  return result;
}

float min_y(Polygon polygon) {
  float result = INFINITY;
  for (int i = 0; i < polygon.num_vertices; i++) {
    if (result > polygon.vertices[i].y) {
      result = polygon.vertices[i].y;
    }
  }

  return result;
}

float max_y(Polygon polygon) {
  float result = -INFINITY;
  for (int i = 0; i < polygon.num_vertices; i++) {
    if (result < polygon.vertices[i].y) {
      result = polygon.vertices[i].y;
    }
  }

  return result;
}


// TODO: Explain.
bool are_intersecting(Vector v1, Vector v2) {
  float d1, d2;
  float a1, a2, b1, b2, c1, c2;

  // Convert vector 1 to a line (line 1) of infinite length.
  // We want the line in linear equation standard form: A*x + B*y + C = 0
  // See: http://en.wikipedia.org/wiki/Linear_equation
  a1 = v1.end.y - v1.start.y;
  b1 = v1.start.x - v1.end.x;
  c1 = (v1.end.x * v1.start.y) - (v1.start.x * v1.end.y);

  // Every point (x,y), that solves the equation above, is on the line,
  // every point that does not solve it, is not. The equation will have a
  // positive result if it is on one side of the line and a negative one 
  // if is on the other side of it. We insert (x1,y1) and (x2,y2) of vector
  // 2 into the equation above.
  d1 = (a1 * v2.start.x) + (b1 * v2.start.y) + c1;
  d2 = (a1 * v2.end.x) + (b1 * v2.end.y) + c1;

  // If d1 and d2 both have the same sign, they are both on the same side
  // of our line 1 and in that case no intersection is possible. Careful, 
  // 0 is a special case, that's why we don't test ">=" and "<=", 
  // but "<" and ">".
  if (d1 > 0 && d2 > 0) return false;
  if (d1 < 0 && d2 < 0) return false;

  // The fact that vector 2 intersected the infinite line 1 above doesn't 
  // mean it also intersects the vector 1. Vector 1 is only a subset of that
  // infinite line 1, so it may have intersected that line before the vector
  // started or after it ended. To know for sure, we have to repeat the
  // the same test the other way round. We start by calculating the 
  // infinite line 2 in linear equation standard form.
  a2 = v2.end.y - v2.start.y;
  b2 = v2.start.x - v2.end.x;
  c2 = (v2.end.x * v2.start.y) - (v2.start.x * v2.end.y);

  // Calculate d1 and d2 again, this time using points of vector 1.
  d1 = (a2 * v1.start.x) + (b2 * v1.start.y) + c2;
  d2 = (a2 * v1.end.x) + (b2 * v1.end.y) + c2;

  // Again, if both have the same sign (and neither one is 0),
  // no intersection is possible.
  if (d1 > 0 && d2 > 0) return false;
  if (d1 < 0 && d2 < 0) return false;

  // If we get here, only two possibilities are left. Either the two
  // vectors intersect in exactly one point or they are collinear, which
  // means they intersect in any number of points from zero to infinite.
  if ((a1 * b2) - (a2 * b1) == 0.0f) return false;

  // If they are not collinear, they must intersect in exactly one point.
  return true;
}

/**
 * This is an optimization to fail fast when checking if a point is inside a polygon.
 */
bool is_within_bounding_box(Point coordinate, Polygon polygon) {
  return (
    coordinate.x > polygon.min_x
    && coordinate.x < polygon.max_x
    && coordinate.y > polygon.min_y
    && coordinate.y < polygon.max_y
  );
}

bool is_contained(Point point, Polygon polygon) {
  float epsilon = 1.0;

  if (!is_within_bounding_box(point, polygon)) {
    return false;
  }

  // Test the ray against all sides.
  // TODO: Explain.
  int ray_vector_x2 = (max_x(polygon) <= point.x)
    ? min_x(polygon) - epsilon
    : max_x(polygon) + epsilon;

  Vector ray = {
    .start = point,
    .end = { .x = ray_vector_x2, .y = point.y }
  };

  int intersections = 0;
  for (int i = 0; i < polygon.num_vertices; i++) {
    int j = (i + 1) % polygon.num_vertices;
    Vector side = { .start = polygon.vertices[i], .end = polygon.vertices[j] };

    if (are_intersecting(ray, side)) {
      intersections++;
    }
  }

  // If the number of intersections is even, we are outside the polygon. If odd, we are inside.
  return (intersections % 2) == 1;
}

void populate_extremas(Polygon polygons[], int num_polygons) {
  for (int i = 0; i < num_polygons; i++) {
    polygons[i].min_x = min_x(polygons[i]);
    polygons[i].max_x = max_x(polygons[i]);
    polygons[i].min_y = min_y(polygons[i]);
    polygons[i].max_y = max_y(polygons[i]);
  }
}

// TODO: Remove.
long millisecondsSinceEpoch() {
  struct timeval tv;
  gettimeofday(&tv, NULL);

  return (long)(tv.tv_sec) * 1000 + (long)(tv.tv_usec) / 1000;
}

// TODO: Comment.
float EYE_WIDTH = 2.0;
float EYE_HEIGHT = 2.0;

void render(Polygon polygons[], int num_polygons, int terminal_width, int terminal_height, char pixels[][terminal_width]) {
  // Cache information we need later.
  long start = millisecondsSinceEpoch();
  populate_extremas(polygons, num_polygons);
  printf("populate extremas %lu\n", millisecondsSinceEpoch() - start);

  for (int y = 0; y < terminal_height; y++) {
    for (int x = 0; x < terminal_width; x++) {

      // From coordinates describing a point in the terminal, constructs the corresponding point in the scene.
      // (x, y) is the upper left corner of the pixel we're filling in. (x + 0.5, y + 0.5) is the middle.
      Point terminal_coordinate = {
        .x = (x + 0.5 - terminal_width / 2.0) * (EYE_WIDTH / terminal_width),

        // TODO: Explain negative sign.
        .y = -(y + 0.5 - terminal_height / 2.0) * (EYE_HEIGHT / terminal_height)
      };


      for (int i = 0; i < num_polygons; i++) {
        if (is_contained(terminal_coordinate, polygons[i])) {
          pixels[y][x] = 'W'; // TODO: replace with '▓'?
          break;
        }
      }
    }
  }
}
