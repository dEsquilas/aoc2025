def read_input(filename):
    lines = [line.strip() for line in open(filename, "r")]
    tuples = [(x[0], int(x[1:])) for x in lines]

    return tuples


def day_1(filename):

    pointer = 50
    values = read_input(filename)
    counter_p1 = 0
    counter_p2 = 0

    for o, v in values:

        for _ in range(v):
            if o == 'R':
                pointer += 1
            if o == 'L':
                pointer -= 1

            if pointer == 100:
                pointer = 0

            if pointer == -1:
                pointer = 99

            if pointer == 0:
                counter_p2 += 1

        if pointer == 0:
            counter_p1 += 1

    return counter_p1, counter_p2

def test_day_1():
     assert day_1("test.txt") == (3, 6)

test_day_1()

p1, p2 = day_1("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
