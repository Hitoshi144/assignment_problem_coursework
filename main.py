import pandas as pd

from experiments import (
    experiment_1, experiment_2, experiment_3,
    experiment_4, experiment_5,
)
from plots import (
    plot_greedy_vs_optimal, plot_scalability, plot_experiment5,
)


def print_experiment_1(res):
    print(f"\nЭксперимент 1 (n={res['n']}, seed={res['seed']})")
    print("Матрица времён:")
    print(res["C"].astype(int))
    print(f"\nЖадный:    назначение {res['greedy_assign'].tolist()}, "
          f"T = {res['t_greedy']:.1f}")
    print(f"Точный:    назначение {res['optimal_assign'].tolist()}, "
          f"T = {res['t_opt']:.1f}")
    print(f"Отклонение: {res['delta']:.1f} "
          f"({res['delta_pct']:.1f}%)")


def print_experiment_2(results):
    print("\nЭксперимент 2. Масштабируемость")
    df = pd.DataFrame(results)
    df["n! (log10)"] = df["factorial"].map(lambda x: f"{x:.1f}")
    print(df[["n", "mean_time", "min_time", "max_time", "n_cubed", "n! (log10)"]]
          .to_string(index=False))


def print_experiment_3(res):
    print(f"\nЭксперимент 3. {res['n_employees']} сотрудников, "
          f"{res['n_tasks']} задач")
    print("Матрица:")
    print(res["C"].astype(int))
    print("\nНазначения (сотрудник -> задача):")
    for i, j in res["assigned"]:
        print(f"  сотрудник {i} -> задача {j} (время {int(res['C'][i, j])})")
    print(f"Свободные сотрудники: {res['free_employees']}")
    print(f"Суммарное время: {res['t_opt']:.1f}")


def print_experiment_4(res):
    print(f"\nЭксперимент 4. Запреты (n={res['n']})")
    print(f"Запрещённые пары: {res['forbidden_pairs']}")
    print("Матрица времён:")
    print(res["C"].astype(int))
    for i in range(0, 5):
        print(f"Сотрудник {res["col_ind"][i]} -> задача {res["row_ind"][i]}")
    print(f"Суммарное время без запретов: {res['t_free']:.1f}")
    print(f"Суммарное время с запретами:  {res['t_forbidden']:.1f}")
    print(f"Нарушенные запреты: {res['violated'] or 'нет'}")


def print_experiment_5(results):
    print("\nЭксперимент 5. Устойчивость")
    df = pd.DataFrame(results)
    print(df[["seed", "t_greedy", "t_opt", "delta_pct"]].to_string(index=False))
    print(f"\nСреднее отклонение: {df['delta_pct'].mean():.1f}%")
    print(f"Мин/макс: {df['delta_pct'].min():.1f}% / {df['delta_pct'].max():.1f}%")


if __name__ == "__main__":
    res1_5 = experiment_1(n=5)
    res1_10 = experiment_1(n=10)
    print_experiment_1(res1_5)
    print_experiment_1(res1_10)

    res2 = experiment_2(sizes=(10, 50, 100, 200, 500), repeats=10)
    print_experiment_2(res2)

    res3 = experiment_3()
    print_experiment_3(res3)

    res4 = experiment_4()
    print_experiment_4(res4)

    res5 = experiment_5(n=10, seeds=tuple(range(10)))
    print_experiment_5(res5)

    plot_greedy_vs_optimal(res1_5, res1_10)
    plot_scalability(res2)
    plot_experiment5(res5)
