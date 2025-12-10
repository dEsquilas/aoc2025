import re
from collections import deque
import pulp


def read_input(filename):
    lines = [line.strip() for line in open(filename, "r")]
    result = []

    for line in lines:
        lights_match = re.search(r'\[([^\]]+)\]', line)
        lights = lights_match.group(1) if lights_match else ""

        switches_matches = re.findall(r'\(([^)]+)\)', line)
        switches = [[int(x) for x in s.split(',')] for s in switches_matches]

        joltages_match = re.search(r'\{([^}]+)\}', line)
        joltages = [int(x) for x in joltages_match.group(1).split(',')] if joltages_match else []

        result.append((lights, switches, joltages))

    return result


def toggle_switch(lights, positions):
    lights = list(lights)
    for pos in positions:
        lights[pos] = '#' if lights[pos] == '.' else '.'
    return ''.join(lights)


def apply_switches(lights, switches, indices):
    for i in indices:
        lights = toggle_switch(lights, switches[i])
    return lights


def min_presses(lights, switches):
    target = '.' * len(lights)
    if lights == target:
        return 0

    visited = {lights}
    queue = deque([(lights, 0)])

    while queue:
        state, steps = queue.popleft()

        for switch in switches:
            new_state = toggle_switch(state, switch)
            if new_state == target:
                return steps + 1
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, steps + 1))

    return -1


def min_presses_joltages(switches, target_joltages):
    n_switches = len(switches)
    n_counters = len(target_joltages)

    prob = pulp.LpProblem("MinPresses", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x{i}", lowBound=0, cat='Integer') for i in range(n_switches)]
    prob += pulp.lpSum(x)

    for counter in range(n_counters):
        switches_affecting = []
        for sw_idx, switch in enumerate(switches):
            if counter in switch:
                switches_affecting.append(x[sw_idx])
        prob += pulp.lpSum(switches_affecting) == target_joltages[counter]

    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    return int(pulp.value(prob.objective))


def day_10(filename):
    diagrams = read_input(filename)
    result_p1 = 0
    result_p2 = 0

    for (lights, switches, joltages) in diagrams:
        result_p1 += min_presses(lights, switches)
        result_p2 += min_presses_joltages(switches, joltages)

    return result_p1, result_p2


def test_day_10():
    result = day_10("test.txt")
    assert result == (7, 33)  # TODO: Update expected values


# Run tests first
test_day_10()

# Calculate real answers
p1, p2 = day_10("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)