def read_input(filename):
    lines = [line.strip() for line in open(filename, "r")]
    return lines

def max_joltage_p1(battery, p = 2):

    mx = 0
    l = -1

    for i in range(len(battery) - (p-2)):
        for j in range(i+1, len(battery) - (p-2)): #dude
            if mx < int(battery[i] + battery[j]):
                l = j
                mx = int(battery[i] + battery[j])

    return mx,l

def max_joltage_p2(battery, r):

    rest = battery
    joltage = ""

    for i in range(0, 6):
        v = max_joltage_p1(rest, r)
        r -= 2
        rest = rest[v[1]+1:]
        joltage += str(v[0])

    return int(joltage)


def day_3(filename):

    batteries = read_input(filename)
    count_p1 = 0
    count_p2 = 0

    for battery in batteries:
        count_p1 += max_joltage_p1(battery)[0]
        count_p2 += max_joltage_p2(battery, 12)


    return count_p1, count_p2


def test_day_3():
     assert day_3("test.txt") == (357, 3121910778619)

test_day_3()

p1, p2 = day_3("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
