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

def initialize_maze():
    #1-geting the width and the height from the user
    width = int(input("Enter the width of the maze: "))
    height = int(input("Enter the height of the maze: "))
    #2-defining start and goal
    start = (0, 0)
    goal = (height - 1, width - 1)
    #3-generating random path
    H = w = 0
    path = [(0,0)]
    while H != height - 1 or w != width - 1: 
        R = random.choice(['H', 'V'])
        if R == 'H' and H < height - 1:
            H += 1
            path.append((H, w))
        elif R == 'V' and w < width - 1:
            w += 1
            path.append((H, w))
        elif H == height - 1 :
            w += 1 
            path.append((H,w))
        elif  w == width - 1 :
            H += 1 
            path.append((H,w))
    #4-generating the maze
    maze = generate_maze(width, height, path , start , goal )

    return maze ,start ,goal