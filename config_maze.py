import random
from collections import deque

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
WALL_CHANCE = 0.42


def _has_path(maze, start, goal):
    queue = deque([start])
    seen = {start}
    while queue:
        cell = queue.popleft()
        if cell == goal:
            return True
        y, x = cell
        for dy, dx in DIRECTIONS:
            neighbor = (y + dy, x + dx)
            if neighbor in maze and maze[neighbor] == 0 and neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return False


def _winding_path(start, goal, height, width):
    """Build a guaranteed corridor using all 4 directions (with backtracking)."""
    path = [start]
    current = start
    visited = {start}

    while current != goal:
        y, x = current
        moves = []
        for dy, dx in DIRECTIONS:
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width and (ny, nx) not in visited:
                moves.append((ny, nx))

        if moves:
            moves.sort(key=lambda c: abs(c[0] - goal[0]) + abs(c[1] - goal[1]))
            pick_from = moves[:2] if len(moves) > 1 else moves
            nxt = random.choice(pick_from)
            path.append(nxt)
            visited.add(nxt)
            current = nxt
        elif len(path) > 1:
            path.pop()
            current = path[-1]
        else:
            break

    if current != goal:
        return _shortest_path(start, goal, height, width)

    return path


def _shortest_path(start, goal, height, width):
    queue = deque([start])
    came_from = {start: None}
    while queue:
        cell = queue.popleft()
        if cell == goal:
            break
        y, x = cell
        for dy, dx in DIRECTIONS:
            neighbor = (y + dy, x + dx)
            if 0 <= neighbor[0] < height and 0 <= neighbor[1] < width and neighbor not in came_from:
                came_from[neighbor] = cell
                queue.append(neighbor)

    if goal not in came_from:
        return [start]

    path = []
    cell = goal
    while cell is not None:
        path.append(cell)
        cell = came_from[cell]
    return path[::-1]


def generate_maze(width, height, start, goal):
    maze = {
        (y, x): 1 if random.random() < WALL_CHANCE else 0
        for y in range(height)
        for x in range(width)
    }
    maze[start] = 0
    maze[goal] = 0

    if not _has_path(maze, start, goal):
        for cell in _winding_path(start, goal, height, width):
            maze[cell] = 0

    return maze


def initialize_maze():
    while True:
        try:
            width = int(input("Enter the width of the maze: "))
            height = int(input("Enter the height of the maze: "))
        except ValueError:
            print("Please enter valid integers.")
            continue
        if width > 0 and height > 0:
            break
        print("Width and height must be positive integers.")

    start = (0, 0)
    goal = (height - 1, width - 1)
    maze = generate_maze(width, height, start, goal)
    return maze, start, goal
