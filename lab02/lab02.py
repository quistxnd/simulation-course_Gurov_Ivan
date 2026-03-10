import time
import numpy as np
from numba import njit

@njit
def solve(dt, h, t_total=100.0):
    ro = 8960.0
    c = 380.0
    lmd = 460.0

    length = 0.4
    temp_left = 0.0
    temp_right = 300.0

    n_x = int(length / h)
    n_t = int(t_total / dt)

    t_curr = np.zeros(n_x + 1)
    t_curr[0] = temp_left
    t_curr[-1] = temp_right

    alpha = np.zeros(n_x + 1)
    beta = np.zeros(n_x + 1)
    t_new = np.zeros(n_x + 1)
    t_new[-1] = temp_right

    coef_a = lmd / h ** 2
    coef_c = coef_a
    coef_b = 2 * lmd / h ** 2 + ro * c / dt
    coef_f = ro * c / dt

    for i in range(1, n_x):
        denom = coef_b - coef_c * alpha[i - 1]
        alpha[i] = coef_a / denom

    for _ in range(n_t):
        beta[0] = temp_left
        for i in range(1, n_x):
            f_i = -coef_f * t_curr[i]
            denom = coef_b - coef_c * alpha[i - 1]
            beta[i] = (coef_c * beta[i - 1] - f_i) / denom

        for i in range(n_x - 1, 0, -1):
            t_new[i] = alpha[i] * t_new[i + 1] + beta[i]

        for i in range(1, n_x):
            t_curr[i] = t_new[i]

    return t_curr[n_x // 2]


def print_formatted_table(title, row_labels, col_labels, data, fmt_str):
    col_width = 12
    first_col_width = 10
    total_width = first_col_width + 3 + len(col_labels) * (col_width + 3) + 1

    print("=" * total_width)
    print(title.center(total_width))
    print("=" * total_width)

    header = f"| {'dt \\ h':<{first_col_width}} |"
    for label in col_labels:
        header += f" {label:>{col_width}} |"
    print(header)
    print("|" + "-" * (total_width - 2) + "|")

    for i, row_label in enumerate(row_labels):
        row_str = f"| {row_label:<{first_col_width}} |"
        for j in range(len(col_labels)):
            val = data[i, j]
            row_str += f" {val:>{col_width}{fmt_str}} |"
        print(row_str)

    print("=" * total_width + "\n")


if __name__ == "__main__":
    dt_steps = [0.1, 0.01, 0.001, 0.0001]
    h_steps = [0.1, 0.01, 0.001, 0.0001]

    results_temp = np.zeros((4, 4))
    results_time = np.zeros((4, 4))

    for i, dt in enumerate(dt_steps):
        for j, h in enumerate(h_steps):
            start_time = time.time()
            results_temp[i, j] = solve(dt, h, 300.0)
            results_time[i, j] = time.time() - start_time

    print_formatted_table(
        title="Температура в центре (t=300.0с), °C",
        row_labels=dt_steps,
        col_labels=h_steps,
        data=results_temp,
        fmt_str=".4f"
    )

    print_formatted_table(
        title="Время расчёта, сек",
        row_labels=dt_steps,
        col_labels=h_steps,
        data=results_time,
        fmt_str=".4f"
    )