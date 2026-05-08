import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import csv
import threading
import time
import os


class WeatherSimulationModel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Моделирование погоды (Марковские цепи)")
        self.geometry("1300x800")

        # Применяем более современный стандартный стиль
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        # Системные переменные
        self.is_simulating = False
        self.time_step = 0
        self.state_sequence = []

        # 0: Ясно, 1: Облачно, 2: Пасмурно
        self.state_names = ["Ясно (1)", "Облачно (2)", "Пасмурно (3)"]
        self.current_idx = 0

        self.output_file = "weather_log.csv"
        self.init_csv()

        self.build_interface()

    def init_csv(self):
        # Создаем файл с заголовками, если начинаем заново
        with open(self.output_file, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["День", "Код_Состояния", "Описание"])

    def build_interface(self):
        # Основные фреймы (Графики слева, Настройки справа)
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.control_frame = ttk.Frame(self, width=300)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # --- Блок управления ---
        lbl_title = ttk.Label(self.control_frame, text="Панель управления", font=("Helvetica", 16, "bold"))
        lbl_title.pack(pady=(0, 20))

        # Матрица
        matrix_group = ttk.LabelFrame(self.control_frame, text="Матрица вероятностей переходов")
        matrix_group.pack(fill=tk.X, pady=10, ipadx=5, ipady=5)

        default_matrix = [
            [0.6, 0.3, 0.1],
            [0.2, 0.5, 0.3],
            [0.1, 0.4, 0.5]
        ]

        self.entries = []
        for row in range(3):
            row_entries = []
            row_frame = ttk.Frame(matrix_group)
            row_frame.pack(pady=2)
            for col in range(3):
                ent = ttk.Entry(row_frame, width=6, justify="center")
                ent.insert(0, str(default_matrix[row][col]))
                ent.pack(side=tk.LEFT, padx=3)
                row_entries.append(ent)
            self.entries.append(row_entries)

        # Скорость
        speed_group = ttk.LabelFrame(self.control_frame, text="Скорость симуляции (сек/день)")
        speed_group.pack(fill=tk.X, pady=10, ipadx=5, ipady=5)

        self.delay_var = tk.DoubleVar(value=0.1)
        speed_scale = ttk.Scale(speed_group, from_=0.01, to=1.0, variable=self.delay_var, orient=tk.HORIZONTAL)
        speed_scale.pack(fill=tk.X, padx=10, pady=5)

        # Кнопки
        self.btn_action = ttk.Button(self.control_frame, text="▶ Старт", command=self.switch_simulation)
        self.btn_action.pack(fill=tk.X, pady=10, ipady=5)

        btn_clear = ttk.Button(self.control_frame, text="⟳ Очистить данные", command=self.clear_data)
        btn_clear.pack(fill=tk.X, pady=5, ipady=5)

        # Информационное табло
        info_group = ttk.LabelFrame(self.control_frame, text="Текущее состояние")
        info_group.pack(fill=tk.X, pady=20, ipadx=5, ipady=15)

        self.lbl_day = ttk.Label(info_group, text="День: 0", font=("Helvetica", 14))
        self.lbl_day.pack(pady=5)

        self.lbl_weather = ttk.Label(info_group, text="Ожидание запуска", font=("Helvetica", 16, "bold"),
                                     foreground="gray")
        self.lbl_weather.pack(pady=5)

        # --- Блок графиков ---
        self.figure = plt.Figure(figsize=(8, 7), dpi=100)
        self.figure.subplots_adjust(hspace=0.4)

        self.ax_history = self.figure.add_subplot(211)
        self.ax_dist = self.figure.add_subplot(212)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.refresh_plots([0.33, 0.33, 0.34])

    def get_transition_matrix(self):
        try:
            mat = np.array([[float(e.get()) for e in row] for row in self.entries])
            # Проверка стохастичности матрицы
            if not np.allclose(mat.sum(axis=1), 1.0):
                messagebox.showerror("Ошибка", "Сумма вероятностей в каждой строке должна равняться 1.")
                return None
            return mat
        except ValueError:
            messagebox.showerror("Ошибка", "Матрица должна содержать только числа.")
            return None

    def find_theoretical_probs(self, P):
        """Решение уравнения (P^T - I) * pi = 0 при сумме pi = 1"""
        size = P.shape[0]
        matrix_eq = np.transpose(P) - np.identity(size)
        # Заменяем последнее уравнение на условие нормировки
        matrix_eq[-1, :] = 1.0
        rhs = np.zeros(size)
        rhs[-1] = 1.0
        try:
            return np.linalg.solve(matrix_eq, rhs)
        except np.linalg.LinAlgError:
            return np.array([1 / 3, 1 / 3, 1 / 3])  # Fallback если матрица вырождена

    def switch_simulation(self):
        if self.is_simulating:
            self.is_simulating = False
            self.btn_action.config(text="▶ Продолжить")
        else:
            trans_matrix = self.get_transition_matrix()
            if trans_matrix is not None:
                self.is_simulating = True
                self.btn_action.config(text="⏸ Пауза")
                # Запуск отдельного потока
                thread = threading.Thread(target=self.run_process, args=(trans_matrix,), daemon=True)
                thread.start()

    def run_process(self, matrix):
        theoretical = self.find_theoretical_probs(matrix)

        while self.is_simulating:
            self.time_step += 1
            self.state_sequence.append(self.current_idx)

            # Обновление UI
            self.lbl_day.config(text=f"День: {self.time_step}")
            self.lbl_weather.config(text=self.state_names[self.current_idx])

            # Смена цвета текста в зависимости от погоды
            colors = ["#f39c12", "#7f8c8d", "#2c3e50"]
            self.lbl_weather.config(foreground=colors[self.current_idx])

            # Запись в CSV
            with open(self.output_file, 'a', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([self.time_step, self.current_idx + 1, self.state_names[self.current_idx]])

            # Перерисовка графиков
            self.refresh_plots(theoretical)

            # Вычисление следующего состояния
            probabilities = matrix[self.current_idx]
            self.current_idx = np.random.choice([0, 1, 2], p=probabilities)

            time.sleep(self.delay_var.get())

    def refresh_plots(self, theo_probs):
        # 1. График истории (ступенчатый)
        self.ax_history.clear()
        self.ax_history.set_title("Динамика изменения погоды (последние 50 дней)", fontsize=12)

        # ИСПРАВЛЕННЫЙ БЛОК КОДА:
        if not self.state_sequence:
            display_data = [0]  # Значение по умолчанию для Y
            x_data = [0]  # Значение по умолчанию для X
        else:
            display_data = self.state_sequence[-50:]
            x_data = range(self.time_step - len(display_data) + 1, self.time_step + 1)

        self.ax_history.plot(x_data, display_data, drawstyle='steps-mid', color='#2980b9', linewidth=2)
        self.ax_history.set_yticks([0, 1, 2])
        self.ax_history.set_yticklabels(["Ясно", "Облачно", "Пасмурно"])
        self.ax_history.grid(True, linestyle='--', alpha=0.6)

        # 2. Гистограмма распределений
        self.ax_dist.clear()
        self.ax_dist.set_title(f"Сравнение вероятностей (Выборка: {self.time_step} дн.)", fontsize=12)

        labels = ["Ясно", "Облачно", "Пасмурно"]
        x_pos = np.arange(len(labels))
        bar_width = 0.35

        if self.time_step > 0:
            empirical_probs = [self.state_sequence.count(i) / self.time_step for i in range(3)]
        else:
            empirical_probs = [0, 0, 0]

        bars1 = self.ax_dist.bar(x_pos - bar_width / 2, empirical_probs, bar_width, label='Эмпирическое (Практика)',
                                 color='#2ecc71')
        bars2 = self.ax_dist.bar(x_pos + bar_width / 2, theo_probs, bar_width, label='Теоретическое (Стационарное)',
                                 color='#e74c3c')

        self.ax_dist.set_xticks(x_pos)
        self.ax_dist.set_xticklabels(labels)
        self.ax_dist.set_ylim(0, 1.0)
        self.ax_dist.legend(loc="upper right")

        # Подписи значений над столбцами
        self.ax_dist.bar_label(bars1, fmt='%.3f', padding=3, fontsize=9)
        self.ax_dist.bar_label(bars2, fmt='%.3f', padding=3, fontsize=9)

        self.canvas.draw()

    def clear_data(self):
        self.is_simulating = False
        self.btn_action.config(text="▶ Старт")

        self.time_step = 0
        self.state_sequence.clear()
        self.current_idx = 0

        self.lbl_day.config(text="День: 0")
        self.lbl_weather.config(text="Сброшено", foreground="gray")

        self.init_csv()  # Перезапись файла
        self.refresh_plots([0.33, 0.33, 0.34])


if __name__ == "__main__":
    app = WeatherSimulationModel()
    app.mainloop()