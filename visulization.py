import matplotlib.pyplot as plt
import numpy as np
from math import pi


def _build_maze_colors(maze, start, goal, path=None):
    height = max(y for y, _ in maze) + 1
    width = max(x for _, x in maze) + 1
    grid = np.ones((height, width), dtype=int)
    path_cells = set(path or [])

    for (y, x), value in maze.items():
        grid[y, x] = value

    colors = np.zeros((height, width, 3))
    for y in range(height):
        for x in range(width):
            cell = (y, x)
            if cell == start:
                colors[y, x] = [0.2, 0.8, 0.2]
            elif cell == goal:
                colors[y, x] = [0.9, 0.2, 0.2]
            elif cell in path_cells:
                colors[y, x] = [0.3, 0.5, 1.0]
            elif grid[y, x] == 0:
                colors[y, x] = [1.0, 1.0, 1.0]
            else:
                colors[y, x] = [0.15, 0.15, 0.15]

    return colors, height, width


def _draw_maze_on_axis(ax, maze, start, goal, path, title):
    colors, height, width = _build_maze_colors(maze, start, goal, path)
    ax.imshow(colors, interpolation="nearest")
    ax.set_xticks(range(width))
    ax.set_yticks(range(height))
    ax.set_xticklabels(range(width))
    ax.set_yticklabels(range(height))
    ax.grid(which="both", color="gray", linewidth=0.5, alpha=0.4)
    ax.set_title(title)


def plot_maze(maze, start, goal, path=None, title="Maze (green=start, red=goal, blue=path)"):
    colors, height, width = _build_maze_colors(maze, start, goal, path)
    fig, ax = plt.subplots(figsize=(max(6, width * 0.5), max(6, height * 0.5)))
    ax.imshow(colors, interpolation="nearest")
    ax.set_xticks(range(width))
    ax.set_yticks(range(height))
    ax.set_xticklabels(range(width))
    ax.set_yticklabels(range(height))
    ax.grid(which="both", color="gray", linewidth=0.5, alpha=0.4)
    ax.set_title(title)
    plt.tight_layout()
    plt.show()


def plot_mazes_side_by_side(maze, start, goal, results):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for ax, result in zip(axes, results):
        title = (
            f"{result['name']} — {result['path_length']} steps | "
            f"{result['time_s'] * 1000:.3f} ms | "
            f"{result['memory_bytes'] / 1024:.2f} KB"
        )
        _draw_maze_on_axis(ax, maze, start, goal, result["path"], title)
    plt.suptitle("Path comparison: BFS vs DFS", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()


def plot_comparison_charts(results):
    names = [r["name"] for r in results]
    time_ms = [r["time_s"] * 1000 for r in results]
    memory_kb = [r["memory_bytes"] / 1024 for r in results]
    path_lengths = [r["path_length"] for r in results]
    colors = ["#4C72B0", "#DD8452"]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    metrics = [
        ("Execution time (ms)", time_ms),
        ("Peak memory (KB)", memory_kb),
        ("Path length (steps)", path_lengths),
    ]

    formats = ["{:.4f}", "{:.2f}", "{}"]
    for ax, (title, values), fmt in zip(axes, metrics, formats):
        bars = ax.bar(names, values, color=colors[: len(names)])
        ax.set_title(title)
        ax.set_ylabel(title)
        ax.grid(axis="y", linestyle="--", alpha=0.6)
        for bar, value in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                fmt.format(value),
                ha="center",
                va="bottom",
                fontsize=10,
            )

    plt.suptitle("BFS vs DFS performance", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()


def plot_step_metrics(df):
    plt.figure(figsize=(12, 6))
    for algo in df['Algorithm'].unique():
        algo_data = df[df['Algorithm'] == algo]
        avg_time = np.mean([steps for steps in algo_data['Step Times']], axis=0)
        avg_memory = np.mean([steps for steps in algo_data['Step Memory']], axis=0)
        plt.plot(avg_memory, linestyle=':', marker='o', mfc='none', label=f'{algo} - Memory')
        plt.plot(avg_time, label=f'{algo} - Time')
    plt.xlabel('Steps')
    plt.ylabel('Time (s) / Memory (KB)')
    plt.title('Step-by-Step Performance')
    plt.legend()
    plt.show()

def plot_radar_chart(df):
    categories = ['Time', 'Memory', 'Path Length']
    num_vars = len(categories)
    df_normalized = df.groupby('Algorithm')[categories].mean()
    max_values = df_normalized.max()
    df_normalized = df_normalized / max_values
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]
    for algorithm in df['Algorithm'].unique():
        if algorithm not in df_normalized.index:
            continue
        values = df_normalized.loc[algorithm].values.tolist()
        values += values[:1]
        ax.plot(angles, values, marker='o', label=algorithm)
        ax.fill(angles, values, alpha=0.25)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)
    plt.xticks(angles[:-1], categories)
    plt.yticks([0, 0.25, 0.5, 0.75, 1], ["0%", "25%", "50%", "75%", "100%"])
    ax.grid(True)
    plt.title('Comparaison des Performances des Algorithmes (Normalisé)')
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.show()

def plot_performance_comparison(stats):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    metrics = ['Time', 'Memory', 'Path Length']
    for i, metric in enumerate(metrics):
        means = stats[(metric, 'mean')]
        stds = stats[(metric, 'std')]
        axes[i].bar(means.index, means, yerr=stds, capsize=5)
        axes[i].set_title(f"{metric} Comparison")
        axes[i].set_ylabel(metric)
        axes[i].set_xlabel('Algorithm')
        axes[i].grid(True)
    plt.tight_layout()
    plt.show()

def plot_boxplots(df):
    import seaborn as sns
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    sns.boxplot(x='Algorithm', y='Time', data=df, ax=axes[0], palette='Set3')
    axes[0].set_title('Boxplot of Time', fontsize=14)
    axes[0].grid(True, linestyle='--', alpha=0.6)
    sns.boxplot(x='Algorithm', y='Memory', data=df, ax=axes[1], palette='Set3')
    axes[1].set_title('Boxplot of Memory', fontsize=14)
    axes[1].grid(True, linestyle='--', alpha=0.6)
    sns.boxplot(x='Algorithm', y='Path Length', data=df, ax=axes[2], palette='Set3')
    axes[2].set_title('Boxplot of Path Length', fontsize=14)
    axes[2].grid(True, linestyle='--', alpha=0.6)
    plt.show()

def plot_pie_charts(stats):
    metrics = ['Time', 'Memory', 'Path Length']
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for i, metric in enumerate(metrics):
        means = stats[(metric, 'mean')]
        axes[i].pie(means, labels=means.index, autopct='%1.1f%%', startangle=140)
        axes[i].set_title(f'{metric} Distribution')
    plt.show()