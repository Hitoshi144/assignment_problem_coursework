import numpy as np
from scipy.optimize import linear_sum_assignment

def generate_matrix(n, m=None, low=1, high=100, seed=143):
    if m is None:
        m = n
    rng = np.random.default_rng(seed)

    C = rng.integers(low, high + 1, size=(n, m)).astype(float)
    return C


def add_forbidden(C, forbidden_pairs, M=1e6):
    C_new = C.copy()
    for i, j in forbidden_pairs:
        C_new[i, j] = M
    return C_new

def greedy_assignment(C):
    n, m = C.shape
    assigned = np.zeros(n, dtype=bool)
    assignment = np.full(m, -1, dtype=int)

    for j in range(m):
        column = C[:, j].copy()
        column[assigned] = np.inf

        if np.all(np.isinf(column)):
            break

        i = int(np.argmin(column))
        assignment[j] = i
        assigned[i] = True

    total_time = sum(C[assignment[j], j] for j in range(m)
                     if assignment[j] != -1)
    return assignment, float(total_time)

def optimal_assignment(C):
    row_ind, col_ind = linear_sum_assignment(C)
    total_time = float(C[row_ind, col_ind].sum())
    return row_ind, col_ind, total_time


def assignment_to_dict(row_ind, col_ind):
    return {int(i): int(j) for i, j in zip(row_ind, col_ind)}
