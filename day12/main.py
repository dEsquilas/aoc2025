def read_input(filename):
    text = open(filename).read()
    parts = text.split('\n\n')

    figures = []
    for part in parts[:-1]:
        lines = part.strip().split('\n')
        grid = [list(row) for row in lines[1:]]
        figures.append(grid)

    inputs = []
    for line in parts[-1].strip().split('\n'):
        if not line:
            continue
        sz, ns = line.split(': ')
        C, R = map(int, sz.split('x'))
        counts = [int(x) for x in ns.split()]
        inputs.append(((R, C), counts))

    return figures, inputs

def get_cells(figure):
    cells = []
    for r, row in enumerate(figure):
        for c, ch in enumerate(row):
            if ch == '#':
                cells.append((r, c))
    return cells

def normalize(cells):
    min_r = min(r for r, c in cells)
    min_c = min(c for r, c in cells)
    return tuple(sorted((r - min_r, c - min_c) for r, c in cells))

def get_orientations(figure):
    cells = get_cells(figure)
    orientations = set()
    for _ in range(4):
        orientations.add(normalize(cells))
        orientations.add(normalize([(r, -c) for r, c in cells]))
        cells = [(c, -r) for r, c in cells]
    return list(orientations)

def solve(R, C, counts, all_orients):
    board = [[False] * C for _ in range(R)]

    def can_place(cells, sr, sc):
        for dr, dc in cells:
            r, c = sr + dr, sc + dc
            if r < 0 or r >= R or c < 0 or c >= C or board[r][c]:
                return False
        return True

    def place(cells, sr, sc, val):
        for dr, dc in cells:
            board[sr + dr][sc + dc] = val

    def backtrack(remaining, fid):
        while fid < len(remaining) and remaining[fid] == 0:
            fid += 1

        if fid >= len(remaining):
            return True

        remaining[fid] -= 1

        for orient in all_orients[fid]:
            max_r = max(dr for dr, dc in orient)
            max_c = max(dc for dr, dc in orient)
            for sr in range(R - max_r):
                for sc in range(C - max_c):
                    if can_place(orient, sr, sc):
                        place(orient, sr, sc, True)
                        if backtrack(remaining, fid):
                            return True
                        place(orient, sr, sc, False)

        remaining[fid] += 1
        return False

    return backtrack(list(counts), 0)

def day_12_p1(filename):
    figures, inputs = read_input(filename)
    all_orients = [get_orientations(f) for f in figures]
    sizes = [len(get_cells(f)) for f in figures]

    count = 0
    for (R, C), counts in inputs:
        total_size = sum(sizes[j] * c for j, c in enumerate(counts))
        grid_size = R * C

        if total_size > grid_size:
            pass
        elif total_size * 1.3 < grid_size:
            count += 1
        else:
            if solve(R, C, counts, all_orients):
                count += 1

    return count

def test_day_12_p1():
    result = day_12_p1("test.txt")
    assert result == 2

test_day_12_p1()

p1 = day_12_p1("input.txt")
print("Part 1:", p1)