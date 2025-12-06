from math import prod

def read_input(filename):
    lines = [line.strip() for line in open(filename, "r")]

    values = [[0 for _ in range(len(lines) -1)] for _ in range(len(lines[0].split()))]
    operators = []

    for j, line in enumerate(lines):
        if j != len(lines) - 1:
            per_line = line.split()
            for i, item in enumerate(per_line):
                values[i][j] = int(item)
        else:
            per_line = line.split()
            for i, item in enumerate(per_line):
                operators.append(item)

    return values, operators

def read_input_p2(filename):

    lines = [line for line in open(filename, "r")]
    operators = []

    length_per_column = []
    current_length = 1
    operators.append(lines[-1][0])

    for j in range(1, len(lines[-1])):
        if lines[-1][j] != " ":
            length_per_column.append(current_length-1)
            current_length = 1
            operators.append(lines[-1][j])
        else:
            current_length += 1

    length_per_column.append(current_length)

    current_pointer = 0
    cephalopod_values = []

    while current_pointer < len(lines[0]):
        for length in length_per_column:
            column_values = []
            for i in range(current_pointer, current_pointer + length):
                current_value = ""
                for j in range(len(lines) -1):
                    if lines[j][i] != " ":
                        current_value += lines[j][i]
                column_values.append(int(current_value))
                current_pointer += 1
            current_pointer += 1
            cephalopod_values.append(column_values)

    return cephalopod_values, operators



def day_6(filename):

    values, operators = read_input(filename)

    count_p1 = 0
    for i, operator in enumerate(operators):
        if operator == '+':
            count_p1 += sum(values[i])
        if operator == '*':
            count_p1 += prod(values[i])

    count_p2 = 0

    values_p2, operators = read_input_p2(filename)

    for i, operator in enumerate(operators):
        if operator == '+':
            count_p2 += sum(values_p2[i])
        if operator == '*':
            count_p2 += prod(values_p2[i])

    return count_p1, count_p2


def test_day_6():
     assert day_6("test.txt") == (4277556, 3263827)

test_day_6()

p1, p2 = day_6("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
