import copy

def read_input(filename):
    lines = [list(line.strip()) for line in open(filename, "r")]
    return lines

def reacheables_rolls(matrix):

    count = 0
    near = [
            [-1, -1], [-1, 0], [-1, 1],
            [0, -1], [0, 1],
            [1, -1], [1, 0], [1, 1]
        ]

    new_matrix = copy.deepcopy(matrix)

    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == '@':
                rolls = 0
                for n in near:
                    ny, nx = y + n[0], x + n[1]
                    if 0 <= ny < len(matrix) and 0 <= nx < len(matrix[0]) and matrix[ny][nx] == '@':
                        rolls += 1
                if rolls < 4:
                    count += 1
                    new_matrix[y][x] = '.'

    return count, new_matrix

def day_4(filename):

    matrix = read_input(filename)

    count_p1 = 0
    count_p2 = 0
    i = 0

    while True:

        count, matrix = reacheables_rolls(matrix)
        count_p2 += count

        if count == 0:
            break
        if i == 0:
            count_p1 = count
            i += 1

    return count_p1, count_p2


def test_day_4():
     assert day_4("test.txt") == (13, 43)

test_day_4()

p1, p2 = day_4("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
