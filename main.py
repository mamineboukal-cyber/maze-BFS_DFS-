from config_maze import initialize_maze
from algorithms import BFS

maze , start , goal = initialize_maze()
path = BFS(start,goal,maze)
print(path)