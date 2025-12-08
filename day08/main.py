def read_input(filename):
    coords = [tuple(map(int, line.strip().split(","))) for line in open(filename, "r")]

    return coords

def day_8(filename, connections):

    coords = read_input(filename)

    all_distances = []
    for i, c1 in enumerate(coords):
        for j, c2 in enumerate(coords):
            if i >= j:
                continue
            dist = (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2
            all_distances.append((dist, c1, c2))

    all_distances.sort(key=lambda x: x[0])

    boxes = [{coord} for coord in coords]

    result_p1 = 0
    result_p2 = 0
    k = 0

    while len(boxes) > 1:
        _, pt1, pt2 = all_distances[k]

        box1 = None
        box2 = None
        for box in boxes:
            if pt1 in box:
                box1 = box
            if pt2 in box:
                box2 = box

        if box1 is not box2:
            box1.update(box2)
            boxes.remove(box2)

            if len(boxes) == 1:
                result_p2 = pt1[0] * pt2[0]

        k += 1

        if k == connections:
            sizes = sorted([len(box) for box in boxes], reverse=True)
            result_p1 = sizes[0] * sizes[1] * sizes[2]

    return result_p1, result_p2


def test_day_8():
     assert day_8("test.txt", 10) == (40, 25272)

test_day_8()

p1, p2 = day_8("input.txt", 1000)

print("Part 1: ", p1)
print("Part 2: ", p2)