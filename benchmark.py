import copy
import time
import tracemalloc


def measure_search(name, search_fn, start, goal, maze):
    maze_copy = copy.copy(maze)
    tracemalloc.start()
    start_time = time.perf_counter()
    path = search_fn(start, goal, maze_copy)
    elapsed = time.perf_counter() - start_time
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "name": name,
        "path": path,
        "time_s": elapsed,
        "memory_bytes": peak_memory,
        "path_length": len(path),
    }
