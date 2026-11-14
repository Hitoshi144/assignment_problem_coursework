import time
import numpy as np

from assignment import (
    generate_matrix,
    add_forbidden,
    greedy_assignment,
    optimal_assignment,
)

def experiment_1(n=5, low=1, high=100, seed=143):
    C = generate_matrix(n, low=low, high=high, seed=seed)

    greedy_assign, t_greedy = greedy_assignment(C)
    _, col_ind, t_opt = optimal_assignment(C)

    delta = t_greedy - t_opt
    delta_pct = delta / t_opt * 100 if t_opt > 0 else 0.0

    return {
        "C": C,
        "greedy_assign": greedy_assign,
        "t_greedy": t_greedy,
        "optimal_assign": col_ind,
        "t_opt": t_opt,
        "delta": delta,
        "delta_pct": delta_pct,
        "n": n,
        "seed": seed,
    }

def experiment_2(sizes=(10, 50, 100, 200, 500),
                 repeats=10, low=1, high=100, seed=143):
    results = []
    for n in sizes:
        times = []
        C = generate_matrix(n, low=low, high=high, seed=seed + n)

        optimal_assignment(C)

        for _ in range(repeats):
            t0 = time.perf_counter()
            optimal_assignment(C)
            t1 = time.perf_counter()
            times.append(t1 - t0)

        times = np.array(times)
        results.append({
            "n": n,
            "mean_time": float(times.mean()),
            "min_time": float(times.min()),
            "max_time": float(times.max()),
            "std_time": float(times.std()),
            "n_cubed": n ** 3,
            "factorial": _factorial_log10(n),
        })
    return results


def _factorial_log10(n):
    if n <= 1:
        return 0.0
    return float(sum(np.log10(k) for k in range(2, n + 1)))

def experiment_3(n_employees=7, n_tasks=5, low=1, high=100, seed=143):
    C = generate_matrix(n_employees, m=n_tasks, low=low, high=high, seed=seed)
    row_ind, col_ind, t_opt = optimal_assignment(C)

    assigned_employees = set(int(i) for i in row_ind)
    free_employees = [i for i in range(n_employees)
                      if i not in assigned_employees]

    return {
        "C": C,
        "row_ind": row_ind,
        "col_ind": col_ind,
        "t_opt": t_opt,
        "assigned": list(zip(row_ind.tolist(), col_ind.tolist())),
        "free_employees": free_employees,
        "n_employees": n_employees,
        "n_tasks": n_tasks,
    }

def experiment_4(n=5, forbidden_pairs=((4, 0), (3, 1), (2, 2)),
                 low=1, high=100, seed=143, M=1e6):
    C = generate_matrix(n, low=low, high=high, seed=seed)
    C_forbidden = add_forbidden(C, forbidden_pairs, M=M)

    _, _, t_free = optimal_assignment(C)

    row_ind, col_ind, t_forbidden = optimal_assignment(C_forbidden)

    forbidden_set = set(forbidden_pairs)
    chosen_pairs = set(zip(row_ind.tolist(), col_ind.tolist()))
    violated = chosen_pairs & forbidden_set

    return {
        "C": C,
        "C_forbidden": C_forbidden,
        "forbidden_pairs": forbidden_pairs,
        "row_ind": row_ind,
        "col_ind": col_ind,
        "t_free": t_free,
        "t_forbidden": t_forbidden,
        "violated": violated,
        "M": M,
        "n": n,
    }

def experiment_5(n=10, seeds=tuple(range(10)), low=1, high=100):
    results = []
    for seed in seeds:
        C = generate_matrix(n, low=low, high=high, seed=seed)
        _, t_greedy = greedy_assignment(C)
        _, _, t_opt = optimal_assignment(C)
        delta = t_greedy - t_opt
        delta_pct = delta / t_opt * 100 if t_opt > 0 else 0.0
        results.append({
            "seed": seed,
            "t_greedy": t_greedy,
            "t_opt": t_opt,
            "delta": delta,
            "delta_pct": delta_pct,
            "n": n,
            "range": (low, high),
        })
    return results
