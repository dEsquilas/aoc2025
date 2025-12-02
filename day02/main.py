def read_input(filename):
    line = open(filename, "r").read().strip()
    items = line.split(',')
    tuples = [(int(x.split("-")[0]), int(x.split("-")[1])) for x in items]

    return tuples

def has_repeating_pattern(s, n):
    if len(s) % n != 0:
        return False
    part_len = len(s) // n
    first_part = s[:part_len]
    for i in range(1, n):
        part = s[i * part_len:(i + 1) * part_len]
        if part != first_part:
            return False
    return True

def day_2(filename):

    ids = read_input(filename)
    ret_p1 = 0
    ret_p2 = 0

    max_len = max(len(str(id_range[1])) for id_range in ids)

    for id_range in ids:
        for i in range(id_range[0], id_range[1] + 1):
            s = str(i)
            for n in range(2, max_len + 1):
                if has_repeating_pattern(s, n):
                    if n == 2:
                        ret_p1 += int(s)
                    ret_p2 += int(s)
                    break

    return ret_p1, ret_p2


def test_day_2():
     assert day_2("test.txt") == (1227775554, 4174379265)

test_day_2()

p1, p2 = day_2("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
