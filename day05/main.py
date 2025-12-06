def read_input(filename):
    blocks = open(filename).read().split("\n\n")
    ranges = [tuple(map(int, line.split("-"))) for line in blocks[0].split("\n") if line]
    numbers = [int(line) for line in blocks[1].split("\n") if line]
    return ranges, numbers

def day_5(filename):

    initial_ranges, values = read_input(filename)

    sorted_ranges = sorted(initial_ranges, key=lambda r: r[0])
    ranges = [sorted_ranges[0]]
    for r in sorted_ranges[1:]:
        last = ranges[-1]
        if r[0] <= last[1]:
            ranges[-1] = (last[0], max(last[1], r[1]))
        else:
            ranges.append(r)

    count_p1 = 0
    for v in values:
        for r in ranges:
            if r[0] <= v <= r[1]:
                count_p1 += 1
                break

    count_p2 = 0
    for r in ranges:
        count_p2 += r[1] - r[0] + 1

    return count_p1, count_p2


def test_day_5():
     assert day_5("test.txt") == (3, 14)

test_day_5()

p1, p2 = day_5("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
