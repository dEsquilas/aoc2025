import matplotlib.pyplot as plt

def read_input(filename):
    lines = [line.strip() for line in open(filename, "r")]
    tuples = [tuple(map(int, line.split(","))) for line in lines]
    return tuples


def plot_polygon_and_rect(coords, rect_c1, rect_c2):
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]

    xs_closed = xs + [xs[0]]
    ys_closed = ys + [ys[0]]

    plt.figure(figsize=(10, 10))

    plt.plot(xs_closed, ys_closed, 'g-', linewidth=2, label='Polygon')
    plt.scatter(xs, ys, c='red', s=20, zorder=5, label='Vertices')

    x1, y1 = rect_c1
    x2, y2 = rect_c2
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    rect_xs = [x1, x2, x2, x1, x1]
    rect_ys = [y1, y1, y2, y2, y1]
    plt.plot(rect_xs, rect_ys, 'b-', linewidth=3, label='Rectangle')
    plt.fill(rect_xs, rect_ys, alpha=0.3, color='blue')

    plt.grid(True)
    plt.legend()
    plt.title(f'Rectangle: {rect_c1} -> {rect_c2}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('equal')
    plt.show()


def get_polygon_segments(coords):
    segments = []
    n = len(coords)
    for i in range(n):
        segments.append((coords[i], coords[(i + 1) % n]))
    return segments


def ray_hits_segment(px, py, direction, seg):
    (x1, y1), (x2, y2) = seg

    if direction == 'right':
        if y1 == y2:
            return False
        if not (min(y1, y2) < py < max(y1, y2)):
            return False
        x_cross = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
        return x_cross > px

    elif direction == 'left':
        if y1 == y2:
            return False
        if not (min(y1, y2) < py < max(y1, y2)):
            return False
        x_cross = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
        return x_cross < px

    elif direction == 'up':
        if x1 == x2:
            return False
        if not (min(x1, x2) < px < max(x1, x2)):
            return False
        y_cross = y1 + (px - x1) * (y2 - y1) / (x2 - x1)
        return y_cross > py

    elif direction == 'down':
        if x1 == x2:
            return False
        if not (min(x1, x2) < px < max(x1, x2)):
            return False
        y_cross = y1 + (px - x1) * (y2 - y1) / (x2 - x1)
        return y_cross < py

    return False


def count_ray_crossings(px, py, direction, segments):
    count = 0
    for seg in segments:
        if ray_hits_segment(px, py, direction, seg):
            count += 1
    return count


def point_inside_polygon(px, py, segments):
    return count_ray_crossings(px, py, 'right', segments) % 2 == 1


def segments_intersect(p1, p2, p3, p4):
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    d1 = cross(p3, p4, p1)
    d2 = cross(p3, p4, p2)
    d3 = cross(p1, p2, p3)
    d4 = cross(p1, p2, p4)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    return False


def rectangle_inside_polygon(c1, c2, segments):
    x1, y1 = c1
    x2, y2 = c2

    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    eps = 0.5
    corners = [
        (x1 + eps, y1 + eps),
        (x2 - eps, y1 + eps),
        (x1 + eps, y2 - eps),
        (x2 - eps, y2 - eps),
    ]

    for cx, cy in corners:
        if not point_inside_polygon(cx, cy, segments):
            return False

    rect_sides = [
        ((x1, y1), (x2, y1)),
        ((x2, y1), (x2, y2)),
        ((x2, y2), (x1, y2)),
        ((x1, y2), (x1, y1)),
    ]

    for rect_side in rect_sides:
        for poly_seg in segments:
            if segments_intersect(rect_side[0], rect_side[1], poly_seg[0], poly_seg[1]):
                return False

    return True


def day_9(filename):
    coords = read_input(filename)
    segments = get_polygon_segments(coords)

    areas = []

    for c1 in coords:
        for c2 in coords:
            if c1 == c2:
                continue

            nx = abs(c1[0] - c2[0]) + 1
            ny = abs(c1[1] - c2[1]) + 1

            area = nx * ny
            areas.append((area, c1, c2))

    areas.sort(reverse=True)

    larger_area = areas[0][0]

    largest_rect_inside = 0
    best_c1, best_c2 = None, None
    for i, (area, c1, c2) in enumerate(areas):
        if rectangle_inside_polygon(c1, c2, segments):
            largest_rect_inside = area
            best_c1, best_c2 = c1, c2
            break

    # if best_c1 is not None:
    #     plot_polygon_and_rect(coords, best_c1, best_c2)

    return larger_area, largest_rect_inside


def test_day_9():
     assert day_9("test.txt") == (50, 24)

test_day_9()

p1, p2 = day_9("input.txt")
print("Part 1: ", p1)
print("Part 2: ", p2)
