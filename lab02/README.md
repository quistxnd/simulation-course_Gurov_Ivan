### Метод конечных разностей для уравнения теплопроводности

**Задание:**  
Реализовать моделирование изменения температуры в пластине на основе одномерного уравнения теплопроводности с использованием метода конечных разностей.

Выполнить моделирование с различными шагами по времени и по пространству.  
Заполнить таблицу значений температуры в центральной точке пластины после 2 секунд модельного времени.

<details>
<summary>Код Программы</summary>
 
  ```
import numpy as np
import time


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

    # Коэффициенты матрицы 
    A_i = lam / (dx ** 2)
    C_i = lam / (dx ** 2)
    B_i = (2 * lam / (dx ** 2)) + (rho_c / dt)

    for n in range(steps):
        alpha = np.zeros(N)
        beta = np.zeros(N)

        # Прямая прогонка
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
    return T[N // 2], (end_calc - start_calc)


# --- ПОДГОТОВКА ДАННЫХ ---
steps_vals = [0.1, 0.01, 0.001, 0.0001]
results_temp = {}
results_time = {}

print("Начинаю расчеты. Это займет несколько минут из-за шага 0.0001...")

for dt in steps_vals:
    temp_row = []
    time_row = []
    for dx in steps_vals:
        print(f"Считаю: dt={dt}, dx={dx}...", end="\r")
        center_t, c_time = solve_heat_equation(dx, dt)
        temp_row.append(round(center_t, 2))
        time_row.append(round(c_time, 4))
    results_temp[dt] = temp_row
    results_time[dt] = time_row
    print(f"Завершен расчет для dt={dt}              ")

# --- ИТОГОВЫЙ ВЫВОД В КОНСОЛЬ ---
print("\n" + "="*50)
print(r"ТАБЛИЦА РЕЗУЛЬТАТОВ ТЕМПЕРАТУРЫ (dt \ dx):") # Добавлена r
print(r"dt \ dx | " + " | ".join(f"{str(x):<7}" for x in steps_vals)) # Добавлена r
print("-" * 50)
for dt, row in results_temp.items():
    print(f"{dt:<7} | " + " | ".join(f"{str(x):<7}" for x in row))

print("\n" + "="*50)
print(r"ТАБЛИЦА ВРЕМЕНИ МОДЕЛИРОВАНИЯ (dt \ dx):") # Добавлена r
print(r"dt \ dx | " + " | ".join(f"{str(x):<7}" for x in steps_vals)) # Добавлена r
print("-" * 50)
for dt, row in results_time.items():
    print(f"{dt:<7} | " + " | ".join(f"{str(x):<7}" for x in row))
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




