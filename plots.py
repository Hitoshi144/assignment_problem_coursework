import numpy as np
import matplotlib.pyplot as plt


def plot_greedy_vs_optimal(results_5, results_10, filename="fig1_greedy_vs_opt.png"):
    labels = ["n = 5", "n = 10"]
    t_greedy = [results_5["t_greedy"], results_10["t_greedy"]]
    t_opt = [results_5["t_opt"], results_10["t_opt"]]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(x - width / 2, t_greedy, width, label="Жадный алгоритм", color="#f197cc")
    ax.bar(x + width / 2, t_opt, width, label="Точный алгоритм", color="#7ed3e9")
    ax.set_ylabel("Суммарное время, усл. ед.")
    ax.set_title("Сравнение жадного и точного алгоритмов")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)


def plot_scalability(results, filename="fig2_scalability.png"):
    ns = [r["n"] for r in results]
    times = [r["mean_time"] for r in results]

    c = times[0] / (ns[0] ** 3)
    theory = [c * (n ** 3) for n in ns]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.loglog(ns, times, "o-", label="Эксперимент (среднее)", color="#742b2b")
    ax.loglog(ns, theory, "--", label=r"Теоретическая оценка $O(n^3)$", color="#51a77f")
    ax.set_xlabel("Размер задачи n")
    ax.set_ylabel("Время работы, с")
    ax.set_title("Масштабируемость точного алгоритма")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)


def plot_experiment5(results, filename="fig3_stability.png"):
    deltas = [r["delta_pct"] for r in results]
    seeds = [r["seed"] for r in results]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar([str(s) for s in seeds], deltas, color="#ac5ac5")
    ax.set_xlabel("seed")
    ax.set_ylabel("Отклонение жадного, %")
    ax.set_title("Устойчивость преимущества точного алгоритма")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)
    