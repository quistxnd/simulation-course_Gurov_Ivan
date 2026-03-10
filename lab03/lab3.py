import tkinter as tk
import random

CELL_SIZE = 12
GRID_WIDTH = 60
GRID_HEIGHT = 40

EMPTY = 0
TREE = 1
FIRE = 2
ASH = 3

COLORS = {
    EMPTY: "#d9d9d9",
    TREE: "green",
    FIRE: "red",
    ASH: "black",
    "CLOUD": "#66cc66"
}


class ForestFire:

    def __init__(self, root):

        self.root = root
        self.root.title("Модель лесного пожара")

        self.grid = [[TREE if random.random() < 0.7 else EMPTY
                      for _ in range(GRID_WIDTH)]
                     for _ in range(GRID_HEIGHT)]

        self.canvas = tk.Canvas(
            root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE
        )
        self.canvas.grid(row=0, column=0, rowspan=20)

        control = tk.Frame(root)
        control.grid(row=0, column=1, sticky="n")

        tk.Label(control, text="Направление ветра").pack()

        self.wind = tk.StringVar(value="Нет")

        tk.OptionMenu(control, self.wind,
                      "Нет", "Север", "Юг", "Восток", "Запад").pack()

        tk.Label(control, text="Влажность").pack()

        self.humidity = tk.Scale(control, from_=0, to=100,
                                 orient="horizontal")
        self.humidity.set(30)
        self.humidity.pack()

        tk.Label(control, text="Рост деревьев").pack()

        self.growth = tk.Scale(control, from_=0, to=100,
                               orient="horizontal")
        self.growth.set(2)
        self.growth.pack()

        tk.Label(control, text="Молнии").pack()

        self.lightning = tk.Scale(control, from_=0, to=100,
                                  orient="horizontal")
        self.lightning.set(1)
        self.lightning.pack()

        self.cloud_enabled = tk.BooleanVar()

        tk.Checkbutton(control,
                       text="Дождевое облако",
                       variable=self.cloud_enabled).pack()

        tk.Button(control, text="Случайный пожар",
                  command=self.ignite_random).pack(pady=5)

        tk.Button(control, text="Запуск",
                  command=self.start).pack()

        tk.Button(control, text="Стоп",
                  command=self.stop).pack()

        tk.Button(control, text="Сброс",
                  command=self.reset).pack(pady=5)

        self.running = False

        self.cloud_x = random.randint(1, GRID_WIDTH - 2)
        self.cloud_y = random.randint(1, GRID_HEIGHT - 2)

        self.draw()
        self.create_legend(control)

    def ignite_random(self):

        for _ in range(5):

            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            if self.grid[y][x] == TREE:
                self.grid[y][x] = FIRE

    def neighbors(self, x, y):

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:

                if dx == 0 and dy == 0:
                    continue

                nx = x + dx
                ny = y + dy

                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    yield nx, ny

    def step(self):

        new = [row[:] for row in self.grid]

        humidity_factor = self.humidity.get() / 100
        growth_chance = self.growth.get() / 1000
        lightning_chance = self.lightning.get() / 10000

        wind = self.wind.get()

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):

                cell = self.grid[y][x]

                if cell == FIRE:
                    new[y][x] = ASH

                elif cell == TREE:

                    burning = False

                    for nx, ny in self.neighbors(x, y):

                        if self.grid[ny][nx] == FIRE:

                            prob = 0.6 * (1 - humidity_factor)

                            if wind == "Восток" and nx < x:
                                prob *= 0.5
                            if wind == "Запад" and nx > x:
                                prob *= 0.5
                            if wind == "Север" and ny > y:
                                prob *= 0.5
                            if wind == "Юг" and ny < y:
                                prob *= 0.5

                            if random.random() < prob:
                                burning = True
                                break

                    if burning:
                        new[y][x] = FIRE

                    elif random.random() < lightning_chance:
                        new[y][x] = FIRE

                elif cell == EMPTY:

                    if random.random() < growth_chance:
                        new[y][x] = TREE

        self.grid = new

        if self.cloud_enabled.get():
            self.move_cloud()

    def move_cloud(self):

        self.cloud_x += random.choice([-1, 0, 1])
        self.cloud_y += random.choice([-1, 0, 1])

        self.cloud_x = max(1, min(GRID_WIDTH - 2, self.cloud_x))
        self.cloud_y = max(1, min(GRID_HEIGHT - 2, self.cloud_y))

        for dx in range(-1, 2):
            for dy in range(-1, 2):

                x = self.cloud_x + dx
                y = self.cloud_y + dy

                if self.grid[y][x] == FIRE:
                    self.grid[y][x] = TREE

    def draw(self):

        self.canvas.delete("all")

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):

                color = COLORS[self.grid[y][x]]

                self.canvas.create_rectangle(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    (x + 1) * CELL_SIZE,
                    (y + 1) * CELL_SIZE,
                    fill=color,
                    outline=""
                )

        if self.cloud_enabled.get():

            for dx in range(-1, 2):
                for dy in range(-1, 2):

                    x = self.cloud_x + dx
                    y = self.cloud_y + dy

                    self.canvas.create_rectangle(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        (x + 1) * CELL_SIZE,
                        (y + 1) * CELL_SIZE,
                        fill=COLORS["CLOUD"],
                        outline=""
                    )

    def update(self):

        if self.running:
            self.step()
            self.draw()
            self.root.after(120, self.update)

    def start(self):
        self.running = True
        self.update()

    def stop(self):
        self.running = False

    def reset(self):

        self.running = False

        self.grid = [[TREE if random.random() < 0.7 else EMPTY
                      for _ in range(GRID_WIDTH)]
                     for _ in range(GRID_HEIGHT)]

        self.cloud_x = random.randint(1, GRID_WIDTH - 2)
        self.cloud_y = random.randint(1, GRID_HEIGHT - 2)

        self.draw()

    def create_legend(self, frame):

        legend = tk.LabelFrame(frame, text="Легенда")
        legend.pack(pady=10)

        items = [
            ("Дерево", COLORS[TREE]),
            ("Огонь", COLORS[FIRE]),
            ("Пепел", COLORS[ASH]),
            ("Пусто", COLORS[EMPTY]),
            ("Облако", COLORS["CLOUD"])
        ]

        for name, color in items:

            row = tk.Frame(legend)
            row.pack(anchor="w")

            box = tk.Canvas(row, width=20, height=20)
            box.create_rectangle(0, 0, 20, 20, fill=color)
            box.pack(side="left")

            tk.Label(row, text=name).pack(side="left")


root = tk.Tk()
app = ForestFire(root)
root.mainloop()
