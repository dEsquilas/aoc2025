import time

def read_input(filename):
    lines = [line.strip() for line in open(filename, "r")]

    figures = []
    inputs = []
    current_grid = []

    for line in lines:
        if not line:
            continue
        if "x" in line:
            parts = line.split(": ")
            dims = tuple(map(int, parts[0].split("x")))
            nums = [int(n) for n in parts[1].split()]
            inputs.append((dims, nums))
        elif ":" in line:
            if current_grid:
                figures.append(current_grid)
            current_grid = []
        else:
            current_grid.append(list(line))

    if current_grid:
        figures.append(current_grid)

    return figures, inputs

def rotate_90(grid):
    rows = len(grid)
    cols = len(grid[0])
    return [[grid[rows - 1 - j][i] for j in range(rows)] for i in range(cols)]

def flip_horizontal(grid):
    return [row[::-1] for row in grid]

def get_all_orientations(grid):
    orientations = set()
    current = grid

    for _ in range(4):
        orientations.add(tuple(tuple(row) for row in current))
        orientations.add(tuple(tuple(row) for row in flip_horizontal(current)))
        current = rotate_90(current)

    return list(orientations)

from functools import cache

ALL_ORIENTATIONS = []
FIGURE_AREAS = []

def get_figure_area(figure):
    return sum(1 for row in figure for c in row if c == '#')

def find_first_empty(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if not board[row][col]:
                return row, col
    return None

def covers_cell(figure, start_row, start_col, target_row, target_col):
    r = target_row - start_row
    c = target_col - start_col
    return 0 <= r < 3 and 0 <= c < 3 and figure[r][c] == '#'

def flood_fill_size(board, start_row, start_col, visited):
    rows, cols = len(board), len(board[0])
    stack = [(start_row, start_col)]
    size = 0
    while stack:
        r, c = stack.pop()
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or board[r][c]:
            continue
        visited.add((r, c))
        size += 1
        stack.extend([(r-1, c), (r+1, c), (r, c-1), (r, c+1)])
    return size

def has_small_gaps(board, min_area):
    visited = set()
    for row in range(len(board)):
        for col in range(len(board[0])):
            if not board[row][col] and (row, col) not in visited:
                region_size = flood_fill_size(board, row, col, visited)
                if region_size < min_area:
                    return True
    return False

def can_place(board, figure, start_row, start_col):
    for r in range(3):
        for c in range(3):
            if figure[r][c] == '#' and board[start_row + r][start_col + c]:
                return False
    return True

def place(board, figure, start_row, start_col):
    result = []
    for row in range(len(board)):
        new_row = []
        for col in range(len(board[0])):
            r = row - start_row
            c = col - start_col
            if 0 <= r < 3 and 0 <= c < 3 and figure[r][c] == '#':
                new_row.append(True)
            else:
                new_row.append(board[row][col])
        result.append(tuple(new_row))
    return tuple(result)

MIN_FIGURE_AREA = 0

@cache
def solve_recursive(board, remaining_counts):
    empty_cell = find_first_empty(board)

    if empty_cell is None:
        return all(c == 0 for c in remaining_counts)

    if all(c == 0 for c in remaining_counts):
        return False

    total_figure_area = sum(FIGURE_AREAS[i] * c for i, c in enumerate(remaining_counts))
    empty_count = sum(1 for row in board for cell in row if not cell)
    if total_figure_area != empty_count:
        return False

    if has_small_gaps(board, MIN_FIGURE_AREA):
        return False

    target_row, target_col = empty_cell

    for figure_id, count in enumerate(remaining_counts):
        if count == 0:
            continue

        new_counts = list(remaining_counts)
        new_counts[figure_id] -= 1
        new_counts = tuple(new_counts)

        for orientation in ALL_ORIENTATIONS[figure_id]:
            for start_row in range(max(0, target_row - 2), min(len(board) - 2, target_row + 1)):
                for start_col in range(max(0, target_col - 2), min(len(board[0]) - 2, target_col + 1)):
                    if covers_cell(orientation, start_row, start_col, target_row, target_col):
                        if can_place(board, orientation, start_row, start_col):
                            new_board = place(board, orientation, start_row, start_col)
                            if solve_recursive(new_board, new_counts):
                                return True

    return False

def solve_box(dims, figure_counts):
    rows, cols = dims
    board = tuple(tuple(False for _ in range(cols)) for _ in range(rows))
    return solve_recursive(board, tuple(figure_counts))

def day_12(filename):
    global ALL_ORIENTATIONS, FIGURE_AREAS, MIN_FIGURE_AREA
    solve_recursive.cache_clear()

    figures, inputs = read_input(filename)

    ALL_ORIENTATIONS = []
    FIGURE_AREAS = []
    for figure in figures:
        ALL_ORIENTATIONS.append(get_all_orientations(figure))
        FIGURE_AREAS.append(get_figure_area(figure))

    MIN_FIGURE_AREA = min(FIGURE_AREAS)

    count = 0
    for i, (dims, figure_counts) in enumerate(inputs):
        print(f"Caja {i+1}/{len(inputs)}: {dims} - {figure_counts}")
        start = time.time()
        solved = solve_box(dims, figure_counts)
        elapsed = time.time() - start
        if solved:
            print(f"  -> Resuelta! ({elapsed:.3f}s)")
            count += 1
        else:
            print(f"  -> No tiene solución ({elapsed:.3f}s)")

    return count, 0


def test_day_12():
     assert day_12("test.txt") == (2, 0)

test_day_12()

p1, p2 = day_12("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
