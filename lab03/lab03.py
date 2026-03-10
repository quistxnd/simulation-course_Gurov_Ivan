import tkinter as tk
from tkinter import ttk
import numpy as np
import random

EMPTY = 0
TREE = 1
BURNING = 2

class ForestFireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Моделирование лесного пожара (клеточный автомат)")

        self.size = 60
        self.cell_size = 12
        self.grid = np.zeros((self.size, self.size), dtype=int)

        self.p_growth = tk.DoubleVar(value=0.01)
        self.p_lightning = tk.DoubleVar(value=0.001)
        self.humidity = tk.DoubleVar(value=0.2)
        self.wind_from = tk.StringVar(value="Нет")
        self.burn_duration = tk.StringVar(value="3")

        self.running = False
        self.setup_ui()
        self.reset_grid()

    def setup_ui(self):

        # gui
        control_panel = ttk.Frame(self.root, padding="10")
        control_panel.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(control_panel, text="Вероятность роста дерева:").pack(anchor=tk.W)
        ttk.Scale(control_panel, from_=0, to=0.1, variable=self.p_growth, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 10))

        ttk.Label(control_panel, text="Вероятность молнии:").pack(anchor=tk.W)
        ttk.Scale(control_panel, from_=0, to=0.01, variable=self.p_lightning, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 10))

        ttk.Label(control_panel, text="Влажность (замедляет огонь):").pack(anchor=tk.W)
        ttk.Scale(control_panel, from_=0, to=1, variable=self.humidity, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 10))

        ttk.Label(control_panel, text="Ветер:").pack(anchor=tk.W)
        wind_options = ["Нет", "Северный", "Южный", "Восточный", "Западный"]
        self.wind_menu = ttk.OptionMenu(control_panel, self.wind_from, wind_options[0], *wind_options)
        self.wind_menu.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(control_panel, text="Время горения (циклов):").pack(anchor=tk.W)
        ttk.Entry(control_panel, textvariable=self.burn_duration).pack(fill=tk.X, pady=(0, 10))

        self.btn_start = ttk.Button(control_panel, text="Запустить", command=self.toggle_simulation)
        self.btn_start.pack(pady=5, fill=tk.X)

        ttk.Button(control_panel, text="Сбросить карту", command=self.reset_grid).pack(fill=tk.X)

        ttk.Label(control_panel, text="\nЛегенда:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        ttk.Label(control_panel, text="Зеленый — лес\nКрасный — огонь\nЧерный — пусто", justify=tk.LEFT).pack(
            anchor=tk.W)

        self.canvas = tk.Canvas(self.root, width=self.size * self.cell_size,
                                height=self.size * self.cell_size, bg="black")
        self.canvas.pack(side=tk.RIGHT)

    def reset_grid(self):
        # заполнение карты деревьями
        self.grid = np.random.choice([TREE, EMPTY], size=(self.size, self.size), p=[0.3, 0.7])
        self.draw_grid()

    def toggle_simulation(self):
        # старт / стоп анимации
        self.running = not self.running
        if self.running:
            self.btn_start.config(text="Остановить")
            self.update_step()
        else:
            self.btn_start.config(text="Запустить")

    def get_ignition_chance(self, x, y):
        # загорится ли дерево от соседей с ветром
        wind = self.wind_from.get()
        # 8 соседей
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dx, dy in offsets:
            nx, ny = (x + dx) % self.size, (y + dy) % self.size

            # если сосед горит, он может передать огонь
            if self.grid[nx, ny] >= BURNING:
                # базовый шанс (выше влажность, ниже шанс)
                spread_prob = 1.0 - self.humidity.get()

                # логика ветра
                if wind == "Северный":
                    if dx == -1: spread_prob *= 1.8  # по ветру
                    if dx == 1:  spread_prob *= 0.1  # против ветра
                elif wind == "Южный":
                    if dx == 1:  spread_prob *= 1.8
                    if dx == -1: spread_prob *= 0.1
                elif wind == "Восточный":
                    if dy == 1:  spread_prob *= 1.8
                    if dy == -1: spread_prob *= 0.1
                elif wind == "Западный":
                    if dy == -1: spread_prob *= 1.8
                    if dy == 1:  spread_prob *= 0.1

                if random.random() < spread_prob:
                    return True
        return False

    def update_step(self):
        # один шаг автомата
        if not self.running:
            return

        new_grid = self.grid.copy()

        # время горения из интерфейса
        try:
            max_burn = BURNING + int(self.burn_duration.get())
        except ValueError:
            max_burn = BURNING + 3

        for x in range(self.size):
            for y in range(self.size):
                state = self.grid[x, y]

                if state == EMPTY:
                    # рост деревьев на пустых клетках
                    if random.random() < self.p_growth.get():
                        new_grid[x, y] = TREE

                elif state == TREE:
                    # дерево горит от соседа или молнии
                    ignite = False
                    if self.get_ignition_chance(x, y):
                        ignite = True
                    elif random.random() < self.p_lightning.get():
                        ignite = True

                    if ignite:
                        new_grid[x, y] = BURNING

                elif state >= BURNING:
                    # если дерево горит, увеличиваем стадию горения
                    if state < max_burn:
                        new_grid[x, y] += 1
                    else:
                        new_grid[x, y] = EMPTY  # дерево сгорело

        self.grid = new_grid
        self.draw_grid()
        # скорость обновления 100 мс
        self.root.after(100, self.update_step)

    def draw_grid(self):
        # отрисовка сетки
        self.canvas.delete("all")
        for x in range(self.size):
            for y in range(self.size):
                state = self.grid[x, y]
                if state == TREE:
                    color = "#2E8B57"
                elif state >= BURNING:
                    # эффект затухания огня
                    color = "#FF4500" if state == BURNING else "#800000"
                else:
                    continue

                x1, y1 = y * self.cell_size, x * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")


if __name__ == "__main__":
    root = tk.Tk()
    app = ForestFireGUI(root)
    root.mainloop()