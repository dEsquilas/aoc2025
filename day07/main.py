import pprint
import copy

def read_input(filename):
    lines = [line.strip() for line in open(filename, "r")]

    return lines

def day_7(filename):

    count_p1 = 0

    matrix = read_input(filename)
    start = matrix[0].index('S')

    beams = set()
    beams.add((0, start))

    tachyon_manifolds = dict()

    for layer in range(1, len(matrix)-1):
        new_beams = set()
        tachyon_manifolds[layer] = [i for i, c in enumerate(matrix[layer]) if c == "^"]
        if len(tachyon_manifolds[layer]) == 0:
            for beam in beams:
                new_beams.add((layer, beam[1]))
        else:
            while beams:
                current_beam = beams.pop()
                added = False
                for taychon_manifold in tachyon_manifolds[layer]:
                    if current_beam[1] == taychon_manifold:
                        new_beams.add((layer, current_beam[1]+1))
                        new_beams.add((layer, current_beam[1]-1))
                        added = True
                        count_p1 += 1
                        break
                if not added:
                    new_beams.add((layer, current_beam[1]))
        beams = new_beams

    path_counts = {start: 1}

    for layer in range(1, len(matrix)-1):
        new_counts = {}
        tachyons = set(i for i, c in enumerate(matrix[layer]) if c == "^")

        for col, count in path_counts.items():
            if col in tachyons:
                new_counts[col-1] = new_counts.get(col-1, 0) + count
                new_counts[col+1] = new_counts.get(col+1, 0) + count
            else:
                new_counts[col] = new_counts.get(col, 0) + count

        path_counts = new_counts

    count_p2 = sum(path_counts.values())

    return count_p1, count_p2


def test_day_7():
     assert day_7("test.txt") == (21, 40)

test_day_7()

p1, p2 = day_7("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)