from collections import defaultdict

def read_input(filename):
    lines = [line.strip() for line in open(filename, "r")]

    return lines

def day_7(filename):

    count_p1 = 0

    matrix = read_input(filename)
    start = matrix[0].index('S')

    beams = {start}

    tachyons_per_layer = {layer: set(i for i, c in enumerate(matrix[layer]) if c == "^") for layer in range(1, len(matrix)-1)}

    for layer in range(1, len(matrix)-1):
        new_beams = set()
        tachyons = tachyons_per_layer[layer]
        for col in beams:
            if col in tachyons:
                new_beams.add(col+1)
                new_beams.add(col-1)
                count_p1 += 1
            else:
                new_beams.add(col)
        beams = new_beams

    path_counts = defaultdict(int)
    path_counts[start] = 1

    for layer in range(1, len(matrix)-1):
        new_counts = defaultdict(int)
        tachyons = tachyons_per_layer[layer]

        for col, count in path_counts.items():
            if col in tachyons:
                new_counts[col-1] += count
                new_counts[col+1] += count
            else:
                new_counts[col] += count

        path_counts = new_counts

    count_p2 = sum(path_counts.values())

    return count_p1, count_p2


def test_day_7():
     assert day_7("test.txt") == (21, 40)

test_day_7()

p1, p2 = day_7("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)