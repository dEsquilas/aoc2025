def read_input(filename):
    lines = [line.strip() for line in open(filename, "r")]
    result = {}
    for line in lines:
        key, values = line.split(": ")
        result[key] = set(values.split())
    return result


def build_reverse_graph(graph):
    reverse = {}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor not in reverse:
                reverse[neighbor] = set()
            reverse[neighbor].add(node)
    return reverse


def count_paths(graph, current, visited):
    if current == "out":
        return 1
    if current not in graph:
        return 0

    total = 0
    for neighbor in graph[current]:
        if neighbor not in visited:
            total += count_paths(graph, neighbor, visited | {neighbor})
    return total


def count_paths_segment(graph, start, end, allowed_nodes, visited):
    if start == end:
        return 1
    if start not in graph:
        return 0

    total = 0
    for neighbor in graph[start]:
        if neighbor in allowed_nodes and neighbor not in visited:
            total += count_paths_segment(graph, neighbor, end, allowed_nodes, visited | {neighbor})
    return total


def day_11_p1(filename):
    data = read_input(filename)
    p1 = count_paths(data, "you", {"you"})
    return p1


def reachable_from(graph, start):
    visited = {start}
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node in graph:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    return visited


def day_11_p2(filename):
    graph = read_input(filename)
    reverse_graph = build_reverse_graph(graph)

    from_svr = reachable_from(graph, "svr")
    from_fft = reachable_from(graph, "fft")
    from_dac = reachable_from(graph, "dac")

    to_fft = reachable_from(reverse_graph, "fft")
    to_dac = reachable_from(reverse_graph, "dac")
    to_out = reachable_from(reverse_graph, "out")

    seg_svr_fft = from_svr & to_fft
    seg_svr_dac = from_svr & to_dac
    seg_fft_dac = from_fft & to_dac
    seg_dac_fft = from_dac & to_fft
    seg_fft_out = from_fft & to_out
    seg_dac_out = from_dac & to_out

    total = 0

    overlap_1 = (seg_svr_fft - {"fft"}) & (seg_fft_dac - {"fft", "dac"})
    overlap_2 = (seg_fft_dac - {"dac"}) & (seg_dac_out - {"dac"})
    overlap_3 = (seg_svr_fft - {"fft"}) & (seg_dac_out - {"dac"})

    if not overlap_1 and not overlap_2 and not overlap_3:
        count_svr_fft = count_paths_segment(graph, "svr", "fft", seg_svr_fft, {"svr"})
        count_fft_dac = count_paths_segment(graph, "fft", "dac", seg_fft_dac, {"fft"})
        count_dac_out = count_paths_segment(graph, "dac", "out", seg_dac_out, {"dac"})
        total += count_svr_fft * count_fft_dac * count_dac_out

    overlap_4 = (seg_svr_dac - {"dac"}) & (seg_dac_fft - {"dac", "fft"})
    overlap_5 = (seg_dac_fft - {"fft"}) & (seg_fft_out - {"fft"})
    overlap_6 = (seg_svr_dac - {"dac"}) & (seg_fft_out - {"fft"})

    if not overlap_4 and not overlap_5 and not overlap_6:
        count_svr_dac = count_paths_segment(graph, "svr", "dac", seg_svr_dac, {"svr"})
        count_dac_fft = count_paths_segment(graph, "dac", "fft", seg_dac_fft, {"dac"})
        count_fft_out = count_paths_segment(graph, "fft", "out", seg_fft_out, {"fft"})
        total += count_svr_dac * count_dac_fft * count_fft_out

    return total



def test_day_11():
    assert day_11_p1("test.txt") == 5
    assert day_11_p2("test2.txt") == 2


# Run tests first
test_day_11()

# Calculate real answers
p1 = day_11_p1("input.txt")
p2 = day_11_p2("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
