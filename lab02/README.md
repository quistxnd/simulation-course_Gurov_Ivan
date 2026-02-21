### Метод конечных разностей для уравнения теплопроводности

**Задание:**  
Реализовать моделирование изменения температуры в пластине на основе одномерного уравнения теплопроводности с использованием метода конечных разностей.

Выполнить моделирование с различными шагами по времени и по пространству.  
Заполнить таблицу значений температуры в центральной точке пластины после 2 секунд модельного времени.

<details>
<summary>Код Программы</summary>
 
  ```
  import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import Tk, Label, Button, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def solve_heat_equation(dx, dt, total_time=2.0):

    L = 1.0  # Длина пластины
    rho_c = 1.2e5  # Скорректированная теплоемкость для прогрева
    lam = 500.0  # Теплопроводность

    start_calc = time.time()

    N = int(L / dx) + 1
    steps = int(total_time / dt)

    # Начальные и граничные условия
    T = np.full(N, 20.0)
    T_left, T_right = 100.0, 100.0
    T[0], T[-1] = T_left, T_right

    # Коэффициенты матрицы (согласно мат. модели на скринах)
    # A_i = lam/h^2, C_i = lam/h^2, B_i = 2*lam/h^2 + rho*c/tau
    A_i = lam / (dx ** 2)
    C_i = lam / (dx ** 2)
    B_i = (2 * lam / (dx ** 2)) + (rho_c / dt)

    for n in range(steps):
        alpha = np.zeros(N)
        beta = np.zeros(N)

        # Прямая прогонка (формулы из мат. модели)
        beta[1] = T_left
        for i in range(1, N - 1):
            F_i = -(rho_c / dt) * T[i]
            denom = B_i - C_i * alpha[i]
            alpha[i + 1] = A_i / denom
            beta[i + 1] = (C_i * beta[i] - F_i) / denom

        # Обратная прогонка
        T_new = np.zeros(N)
        T_new[-1] = T_right
        for i in range(N - 2, 0, -1):
            T_new[i] = alpha[i + 1] * T_new[i + 1] + beta[i + 1]

        T_new[0] = T_left
        T = T_new

    end_calc = time.time()
    calc_time = end_calc - start_calc

    return np.linspace(0, L, N), T, T[N // 2], calc_time


# --- ПОДГОТОВКА ДАННЫХ ---
steps_vals = [0.1, 0.01, 0.001, 0.0001]
results_temp = {}
results_time = {}

print("Выполняется расчет... Пожалуйста, подождите.")

for dt in steps_vals:
    temp_row = []
    time_row = []
    for dx in steps_vals:
        # Для dx=0.0001 расчет может быть долгим, выводим прогресс
        _, _, center_t, c_time = solve_heat_equation(dx, dt)
        temp_row.append(round(center_t, 2))
        time_row.append(round(c_time, 4))
    results_temp[dt] = temp_row
    results_time[dt] = time_row

# --- ВЫВОД В КОНСОЛЬ ---
print(r"Таблица результатов (dt \ dx):")
for dt, row in results_temp.items():
    print(f"{dt:<7} | {' | '.join(map(str, row))}")

print(r"\nТаблица времени моделирования (dt \ dx):")
for dt, row in results_time.items():
    print(f"{dt:<7} | {' | '.join(map(str, row))}")


# --- GUI (ИНТЕРФЕЙС) ---
def show_gui():
    root = Tk()
    root.title("Прототип приложения")
    root.geometry("700x500")

    # Зеленая панель (Скрин 3)
    top_panel = Frame(root, bg="#a3d3c3", padx=10, pady=10)
    top_panel.pack(fill="x", padx=10, pady=10)

    # Расчет для визуализации (красивый изгиб)
    x, T, center, _ = solve_heat_equation(0.01, 0.01)

    Label(top_panel, text=f"Исходные данные:\nL=1.0m\nT0=20C, BC=100C", bg="#a3d3c3", justify="left").pack(side="left")
    Label(top_panel, text=f"Температура в центре: {center:.2f} °C\nВремя симуляции: 2.000 с", bg="#a3d3c3",
          font=("Arial", 10, "bold")).pack(side="right")
    Button(top_panel, text="Запуск", bg="#48cae4", width=10).pack(side="top", pady=5)

    # График
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x, T, color='red', linewidth=2)
    ax.set_title("Распределение T(x)")
    ax.set_xlabel("x, м")
    ax.set_ylabel("T, °C")
    ax.grid(True, alpha=0.3)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    show_gui()
  ```
</details>


| Шаг по времени, с \ Шаг по пространству, м | 0.1 | 0.01 | 0.001 | 0.0001 |
|-------------------------------------------|-----|------|-------|--------|
| **0.1** | 20.19 | 20.04 | 20.04 | 20.04 |
| **0.01** | 20.15 | 20.02 | 20.02 | 20.02 |
| **0.001** | 20.15 | 20.02 | 20.02 | 20.02 |
| **0.0001** | 20.15 | 20.02 | 20.02 | 20.02 |

#### Таблица времен моделирования

| Шаг по времени ($dt$), с \ Шаг по пространству ($h$), м | 0.1 | 0.01 | 0.001 | 0.0001 |
|:-------------------------------------------|:-----:|:------:|:-------:|:--------:|
| **0.1** | 0.0002 | 0.0019 | 0.0198 | 0.1914 |
| **0.01** | 0.002 | 0.0188 | 0.1916 | 1.9037 |
| **0.001** | 0.0193 | 0.1869 | 1.8945 | 19.0808 |
| **0.0001** | 0.1919 | 1.8634 | 19.0311 | 190.8414 |

**Сделать вывод.**


