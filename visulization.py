import matplotlib.pyplot as plt
import numpy as np


def _colors(maze, start, goal, path=()):
    h, w = max(y for y, _ in maze) + 1, max(x for _, x in maze) + 1
    path = set(path)
    palette = {
        "start": [0.2, 0.8, 0.2],
        "goal": [0.9, 0.2, 0.2],
        "path": [0.3, 0.5, 1.0],
        "open": [1.0, 1.0, 1.0],
        "wall": [0.15, 0.15, 0.15],
    }
    img = np.zeros((h, w, 3))
    for y in range(h):
        for x in range(w):
            cell = (y, x)
            key = (
                "start"
                if cell == start
                else "goal"
                if cell == goal
                else "path"
                if cell in path
                else "open"
                if maze.get(cell, 1) == 0
                else "wall"
            )
            img[y, x] = palette[key]
    return img, h, w


def _draw(ax, maze, start, goal, path, title):
    img, h, w = _colors(maze, start, goal, path)
    ax.imshow(img, interpolation="nearest")
    ax.set_xticks(range(w))
    ax.set_yticks(range(h))
    ax.grid(color="gray", linewidth=0.5, alpha=0.4)
    ax.set_title(title)


def show_results(maze, start, goal, results):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for ax, r in zip(axes, results):
        _draw(
            ax,
            maze,
            start,
            goal,
            r["path"],
            f"{r['name']} — {r['path_length']} steps | {r['time_s']*1000:.3f} ms | {r['memory_kb']:.2f} KB",
        )
    fig.suptitle("Path comparison: BFS vs DFS", fontsize=14)
    plt.tight_layout()
    plt.show()

    names = [r["name"] for r in results]
    metrics = [
        ("Time (ms)", [r["time_s"] * 1000 for r in results], "{:.4f}"),
        ("Memory (KB)", [r["memory_kb"] for r in results], "{:.2f}"),
        ("Path length", [r["path_length"] for r in results], "{}"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, (title, values, fmt) in zip(axes, metrics):
        bars = ax.bar(names, values, color=["#4C72B0", "#DD8452"])
        ax.set_title(title)
        ax.grid(axis="y", linestyle="--", alpha=0.6)
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), fmt.format(value), ha="center", va="bottom")
    fig.suptitle("BFS vs DFS performance", fontsize=14)
    plt.tight_layout()
    plt.show()
