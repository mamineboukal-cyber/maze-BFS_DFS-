import random


def generate_maze(width, height, path, start, goal):
    maze = {}
    for y in range(height):
        for x in range(width):
            maze[(y, x)] = random.choice([0, 1])

    maze[start] = 0
    maze[goal] = 0
    for coord in path:
        maze[coord] = 0

    return maze


def _random_path(height, width):
    y, x = 0, 0
    path = [(y, x)]
    while (y, x) != (height - 1, width - 1):
        moves = []
        if y < height - 1:
            moves.append("down")
        if x < width - 1:
            moves.append("right")
        choice = random.choice(moves)
        if choice == "down":
            y += 1
        else:
            x += 1
        path.append((y, x))
    return path


def initialize_maze():
    while True:
        width = int(input("Enter the width of the maze: "))
        height = int(input("Enter the height of the maze: "))
        if width > 0 and height > 0:
            break
        print("Width and height must be positive integers.")

    start = (0, 0)
    goal = (height - 1, width - 1)
    path = _random_path(height, width)
    maze = generate_maze(width, height, path, start, goal)
    return maze, start, goal
