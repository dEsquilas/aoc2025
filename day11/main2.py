from functools import cache


def read_input(filename):
    lines = [line.strip() for line in open(filename, "r")]
    result = {}
    for line in lines:
        key, values = line.split(": ")
        result[key] = values.split()
    return result


def day_11_p1(filename):
    graph = read_input(filename)

    @cache
    def count_paths(node):
        if node == "out":
            return 1
        if node not in graph:
            return 0
        return sum(count_paths(v) for v in graph[node])

    return count_paths("you")


def day_11_p2(filename):
    graph = read_input(filename)

    @cache
    def count_paths(node, seen_dac, seen_fft):
        if node == "out":
            return 1 if seen_dac and seen_fft else 0
        if node not in graph:
            return 0
        total = 0
        for v in graph[node]:
            total += count_paths(v, seen_dac or v == "dac", seen_fft or v == "fft")
        return total

    return count_paths("svr", False, False)


def test_day_11():
    assert day_11_p1("test.txt") == 5
    assert day_11_p2("test2.txt") == 2


test_day_11()

p1 = day_11_p1("input.txt")
p2 = day_11_p2("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)