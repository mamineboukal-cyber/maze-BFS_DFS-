import copy
import time
import tracemalloc

from algorithms import BFS, DFS
from config_maze import initialize_maze

ALGOS = (("BFS", BFS), ("DFS", DFS))
SYMBOLS = {0: ".", 1: "#"}


def print_maze(maze, start, goal, path=None):
    path = set(path or [])
    h, w = max(y for y, _ in maze) + 1, max(x for _, x in maze) + 1
    for y in range(h):
        row = []
        for x in range(w):
            c = (y, x)
            row.append(
                "S" if c == start else "G" if c == goal else "*" if c in path else SYMBOLS[maze.get(c, 1)]
            )
        print("".join(row))


def measure(name, fn, start, goal, maze):
    tracemalloc.start()
    t0 = time.perf_counter()
    path = fn(start, goal, copy.copy(maze))
    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "name": name,
        "path": path,
        "path_length": len(path),
        "time_s": elapsed,
        "memory_kb": peak / 1024,
    }


def print_table(results):
    rows = [
        (r["name"], f"{r['time_s']*1000:.4f}", f"{r['memory_kb']:.2f}", str(r["path_length"]))
        for r in results
    ]
    headers = ("Algorithm", "Time (ms)", "Memory (KB)", "Path Length")
    widths = [max(len(h), *(len(row[i]) for row in rows)) for i, h in enumerate(headers)]
    line = lambda cells: "|" + "|".join(f" {c:<{w}} " for c, w in zip(cells, widths)) + "|"
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print("\nPerformance comparison", sep, line(headers), sep, *[line(row) for row in rows], sep, sep="\n")


def main():
    maze, start, goal = initialize_maze()
    print(f"\nStart: {start}  Goal: {goal}\nMaze layout (same for BFS and DFS):")
    print_maze(maze, start, goal)
    print()

    results = []
    for name, fn in ALGOS:
        r = measure(name, fn, start, goal, maze)
        stats = f"{r['time_s']*1000:.4f} ms | {r['memory_kb']:.2f} KB"
        print(f"{name}: {'path found' if r['path'] else 'no path'} ({r['path_length']} steps) | {stats}")
        if r["path"]:
            print_maze(maze, start, goal, r["path"])
        print()
        results.append(r)

    print_table(results)
    try:
        if input("\nShow maze paths and comparison charts? (y/n): ").strip().lower() == "y":
            from visulization import show_results

            show_results(maze, start, goal, results)
    except (EOFError, ImportError):
        print("Install charts deps: .venv\\Scripts\\python.exe -m pip install -r requirements.txt")


if __name__ == "__main__":
    main()
