import random
from algorithms import DIRS, reachable, _search

WALL_CHANCE = 0.42


def _winding_path(start, goal, height, width):
    path, cur, seen = [start], start, {start}
    while cur != goal:
        y, x = cur
        moves = [
            (y + dy, x + dx)
            for dy, dx in DIRS
            if 0 <= y + dy < height
            and 0 <= x + dx < width
            and (y + dy, x + dx) not in seen
        ]
        if moves:
            moves.sort(key=lambda c: abs(c[0] - goal[0]) + abs(c[1] - goal[1]))
            cur = random.choice(moves[:2] if len(moves) > 1 else moves)
            path.append(cur)
            seen.add(cur)
        elif len(path) > 1:
            path.pop()
            cur = path[-1]
        else:
            break
    return path if cur == goal else _search(
        start, goal, {(y, x): 0 for y in range(height) for x in range(width)}
    )


def generate_maze(width, height, start, goal):
    maze = {
        (y, x): int(random.random() < WALL_CHANCE)
        for y in range(height)
        for x in range(width)
    }
    maze[start] = maze[goal] = 0
    if not reachable(start, goal, maze):
        for cell in _winding_path(start, goal, height, width):
            maze[cell] = 0
    return maze


def initialize_maze():
    while True:
        try:
            width, height = int(input("Enter the width of the maze: ")), int(
                input("Enter the height of the maze: ")
            )
        except ValueError:
            print("Please enter valid integers.")
            continue
        if width > 0 and height > 0:
            break
        print("Width and height must be positive integers.")
    start, goal = (0, 0), (height - 1, width - 1)
    return generate_maze(width, height, start, goal), start, goal
