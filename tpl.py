def read_input(filename):
    lines = [line.strip() for line in open(filename, "r")]
    
    return lines

def day_X(filename):

    return 0, 0


def test_day_X():
     assert day_X("test.txt") == (0, 0)

test_day_X()

p1, p2 = day_X("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
