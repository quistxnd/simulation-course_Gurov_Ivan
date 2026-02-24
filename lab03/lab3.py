import tkinter as tk
import random


class ForestFireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Модель лесного пожара (Клеточный автомат)")

        # Константы
        self.grid_size = 50
        self.cell_pixel = 12
        self.running = False

        # Цветовая схема
        self.colors = {
            0: "#FFFFFF",  # Пусто (Белый)
            1: "#228B22",  # Дерево (Зеленый)
            2: "#FF4500"  # Огонь (Оранжево-красный)
        }

        # Состояния: 0 - Пусто, 1 - Дерево, 2 - Огонь
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Параметры управления
        self.wind = tk.DoubleVar(value=0.2)
        self.humidity = tk.DoubleVar(value=0.1)
        self.rain_chance = tk.DoubleVar(value=0.0)

        self.setup_gui()
        self.reset_forest()

    def setup_gui(self):
        # Левая панель управления
        control_panel = tk.Frame(self.root, padx=15, pady=10, width=200)
        control_panel.pack(side=tk.LEFT, fill=tk.Y)

        # --- СЕКЦИЯ: ЛЕГЕНДА ---
        tk.Label(control_panel, text="ЛЕГЕНДА", font=('Arial', 10, 'bold')).pack(pady=(0, 5))

        legend_frame = tk.Frame(control_panel, relief=tk.RIDGE, borderwidth=2, padx=5, pady=5)
        legend_frame.pack(fill=tk.X, pady=(0, 20))

        self.create_legend_item(legend_frame, self.colors[1], "Дерево")
        self.create_legend_item(legend_frame, self.colors[2], "ПОЖАР (горит)")
        self.create_legend_item(legend_frame, self.colors[0], "Пусто / Пепел")

        # --- СЕКЦИЯ: ПАРАМЕТРЫ ---
        tk.Label(control_panel, text="НАСТРОЙКИ", font=('Arial', 10, 'bold')).pack()

        tk.Label(control_panel, text="Ветер (вправо):").pack(pady=(10, 0))
        tk.Scale(control_panel, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, variable=self.wind).pack()

        tk.Label(control_panel, text="Влажность:").pack(pady=(10, 0))
        tk.Scale(control_panel, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, variable=self.humidity).pack()

        tk.Label(control_panel, text="Интенсивность дождя:").pack(pady=(10, 0))
        tk.Scale(control_panel, from_=0, to=0.5, resolution=0.05, orient=tk.HORIZONTAL,
                 variable=self.rain_chance).pack()

        # Кнопки управления
        self.btn_start = tk.Button(control_panel, text="СТАРТ", command=self.toggle_simulation,
                                   bg="#90EE90", font=('Arial', 10, 'bold'), height=2)
        self.btn_start.pack(fill=tk.X, pady=(20, 5))

        tk.Button(control_panel, text="СБРОС ЛЕСА", command=self.reset_forest).pack(fill=tk.X)

        # Холст для симуляции
        self.canvas = tk.Canvas(self.root, width=self.grid_size * self.cell_pixel,
                                height=self.grid_size * self.cell_pixel, bg="white", highlightthickness=1)
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)

    def create_legend_item(self, parent, color, text):
        """Вспомогательная функция для отрисовки строки в легенде"""
        item_frame = tk.Frame(parent)
        item_frame.pack(fill=tk.X, pady=2)
        canvas = tk.Canvas(item_frame, width=15, height=15, highlightthickness=1)
        canvas.create_rectangle(0, 0, 15, 15, fill=color, outline="gray")
        canvas.pack(side=tk.LEFT)
        tk.Label(item_frame, text=f" — {text}", font=('Arial', 9)).pack(side=tk.LEFT)

    def reset_forest(self):
        self.running = False
        self.btn_start.config(text="СТАРТ", bg="#90EE90")
        # Изначально засаживаем лес деревьями (65%)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid[y][x] = 1 if random.random() < 0.65 else 0
        self.draw_grid()

    def toggle_simulation(self):
        self.running = not self.running
        if self.running:
            self.btn_start.config(text="ПАУЗА", bg="#FFD700")
            self.run_cycle()
        else:
            self.btn_start.config(text="СТАРТ", bg="#90EE90")

    def run_cycle(self):
        if not self.running:
            return


        new_grid = [row[:] for row in self.grid]

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                state = self.grid[y][x]

                if state == 2:  # Огонь
                    new_grid[y][x] = 0  # Превращается в пустоту (пепел)

                elif state == 1:  # Дерево
                    on_fire = False
                    # Проверка соседей (Окрестность фон Неймана)
                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < self.grid_size and 0 <= nx < self.grid_size:
                            if self.grid[ny][nx] == 2:
                                # Вероятность возгорания
                                chance = 0.7 - self.humidity.get()
                                # Модификатор ветра (увеличивает шанс переноса вправо)
                                if dx == 1:
                                    # Базовая вероятность
                                    chance = 0.7 - self.humidity.get()

                                    # Ветер усиливает распространение во всех направлениях
                                    chance *= (1 + self.wind.get())

                                    # Ограничиваем диапазон 0–1
                                    chance = max(0.0, min(1.0, chance))

                                if random.random() < chance:
                                    on_fire = True
                                    break

                    # Случайный удар молнии (очень редкий шанс)
                    if not on_fire and random.random() < 0.0001:
                        on_fire = True

                    if on_fire:
                        # Эффект дождя (спасает дерево от огня)
                        if random.random() < self.rain_chance.get():
                            new_grid[y][x] = 0  # Потушено (но дерево исчезло)
                        else:
                            new_grid[y][x] = 2  # Загорелось



        self.grid = new_grid
        self.draw_grid()
        # Скорость обновления (100 мс = 10 кадров в секунду)
        self.root.after(100, self.run_cycle)

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                val = self.grid[y][x]
                if val != 0:  # Отрисовываем только деревья и огонь
                    x1, y1 = x * self.cell_pixel, y * self.cell_pixel
                    x2, y2 = x1 + self.cell_pixel, y1 + self.cell_pixel
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.colors[val], outline="")


if __name__ == "__main__":
    root = tk.Tk()
    app = ForestFireApp(root)
    root.mainloop()
