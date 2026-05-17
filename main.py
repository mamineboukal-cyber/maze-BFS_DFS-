from config_maze import initialize_maze
from algorithms import BFS, DFS
from benchmark import measure_search


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


def print_result(result):
    name = result["name"]
    if result["path"]:
        print(
            f"{name}: path found ({result['path_length']} steps) | "
            f"time: {result['time_s'] * 1000:.4f} ms | "
            f"memory: {result['memory_bytes'] / 1024:.2f} KB"
        )
        print_maze(result["maze"], result["start"], result["goal"], result["path"])
    else:
        print(
            f"{name}: no path found | "
            f"time: {result['time_s'] * 1000:.4f} ms | "
            f"memory: {result['memory_bytes'] / 1024:.2f} KB"
        )


def print_comparison_table(results):
    headers = ("Algorithm", "Time (ms)", "Memory (KB)", "Path Length")
    rows = [
        (
            r["name"],
            f"{r['time_s'] * 1000:.4f}",
            f"{r['memory_bytes'] / 1024:.2f}",
            str(r["path_length"]),
        )
        for r in results
    ]

    widths = [max(len(h), *(len(row[i]) for row in rows)) for i, h in enumerate(headers)]
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    header_line = "|" + "|".join(f" {h:<{w}} " for h, w in zip(headers, widths)) + "|"

    print("\nPerformance comparison")
    print(sep)
    print(header_line)
    print(sep)
    for row in rows:
        print("|" + "|".join(f" {cell:<{w}} " for cell, w in zip(row, widths)) + "|")
    print(sep)


def show_visualizations(maze, start, goal, results):
    try:
        from visulization import plot_comparison_charts, plot_mazes_side_by_side

        plot_mazes_side_by_side(maze, start, goal, results)
        plot_comparison_charts(results)
    except ImportError:
        print(
            "matplotlib is not installed. Run:\n"
            "  .venv\\Scripts\\python.exe -m pip install -r requirements.txt"
        )


def main():
    maze, start, goal = initialize_maze()
    print(f"\nStart: {start}  Goal: {goal}\n")

    algorithms = [("BFS", BFS), ("DFS", DFS)]
    results = []
    for name, search_fn in algorithms:
        result = measure_search(name, search_fn, start, goal, maze)
        result["maze"] = maze
        result["start"] = start
        result["goal"] = goal
        results.append(result)
        print_result(result)
        print()

    print_comparison_table(results)

    try:
        show_plot = input("\nShow maze paths and comparison charts? (y/n): ").strip().lower()
        if show_plot == "y":
            show_visualizations(maze, start, goal, results)
    except EOFError:
        pass


if __name__ == "__main__":
    main()
