from config_maze import initialize_maze
from algorithms import BFS, DFS


def print_maze(maze, start, goal, path=None):
    path_cells = set(path or [])
    height = max(y for y, _ in maze) + 1
    width = max(x for _, x in maze) + 1

    for y in range(height):
        row = []
        for x in range(width):
            cell = (y, x)
            if cell == start:
                row.append("S")
            elif cell == goal:
                row.append("G")
            elif cell in path_cells:
                row.append("*")
            elif maze.get(cell, 1) == 0:
                row.append(".")
            else:
                row.append("#")
        print("".join(row))


def run_search(name, search_fn, start, goal, maze):
    path = search_fn(start, goal, maze)
    if path:
        print(f"{name}: path found ({len(path)} steps)")
        print_maze(maze, start, goal, path)
    else:
        print(f"{name}: no path found")
    return path


def main():
    maze, start, goal = initialize_maze()
    print(f"\nStart: {start}  Goal: {goal}\n")

    bfs_path = run_search("BFS", BFS, start, goal, maze)
    print()
    run_search("DFS", DFS, start, goal, maze)

    try:
        show_plot = input("\nShow matplotlib plot for BFS path? (y/n): ").strip().lower()
        if show_plot == "y" and bfs_path:
            from visulization import plot_maze

            plot_maze(maze, start, goal, bfs_path)
    except EOFError:
        pass


if __name__ == "__main__":
    main()
