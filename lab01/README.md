### Моделирование полёта тела в атмосфере

**Задание:**  
- Реализовать приложение для моделирования полёта тела в атмосфере.  
- Предусмотреть возможность ввода шага моделирования и вывода результатов.
- Выполнить моделирование **без очистки предыдущих результатов** для различных шагов моделирования, сравнить траектории и заполнить таблицу:

<details>

<summary>Код Программы</summary>

```
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import math


class FlightSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Моделирование полета тела (Рунге-Кутта)")

        self.g = 9.81
        self.results = {}
        self.animation = None
        self.is_animating = False

        self.colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'cyan']
        self.color_index = 0

        self.legend_lines = []

        self.create_widgets()

    def create_widgets(self):
        left = ttk.LabelFrame(self.root, text="Параметры")
        left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.inputs = {}
        params = [
            ("Начальная скорость (м/с)", "50", "v0"),
            ("Угол (град)", "45", "angle"),
            ("Масса (кг)", "1", "m"),
            ("Коэфф. сопротивления", "0.02", "k"),
            ("Шаг dt (с)", "0.05", "dt")
        ]

        for text, val, key in params:
            frame = ttk.Frame(left)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=text).pack(side=tk.LEFT)
            entry = ttk.Entry(frame, width=10)
            entry.insert(0, val)
            entry.pack(side=tk.RIGHT)
            self.inputs[key] = entry

        ttk.Button(left, text="Запуск", command=self.animate).pack(fill=tk.X, pady=5)
        ttk.Button(left, text="Очистить", command=self.clear).pack(fill=tk.X)

        self.result_text = tk.Text(left, height=15, width=45)
        self.result_text.pack(pady=10)

        self.figure, self.ax = plt.subplots(figsize=(6, 5))
        self.ax.set_title("Траектория полета")
        self.ax.set_xlabel("x (м)")
        self.ax.set_ylabel("y (м)")
        self.ax.grid()
        self.ax.legend(loc='upper right', fontsize=8)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def get_params(self):
        try:
            return {k: float(self.inputs[k].get()) for k in self.inputs}
        except:
            return None

    def simulate(self, v0, angle, m, k, dt):
        rad = math.radians(angle)
        x, y = 0, 0
        vx = v0 * math.cos(rad)
        vy = v0 * math.sin(rad)

        xs, ys = [x], [y]
        max_h = 0

        def derivatives(vx, vy):
            v = math.sqrt(vx ** 2 + vy ** 2)
            ax = -(k / m) * v * vx
            ay = -self.g - (k / m) * v * vy
            return ax, ay

        while y >= 0:
            ax1, ay1 = derivatives(vx, vy)
            k1vx, k1vy = ax1 * dt, ay1 * dt
            k1x, k1y = vx * dt, vy * dt

            ax2, ay2 = derivatives(vx + k1vx / 2, vy + k1vy / 2)
            k2vx, k2vy = ax2 * dt, ay2 * dt
            k2x, k2y = (vx + k1vx / 2) * dt, (vy + k1vy / 2) * dt

            ax3, ay3 = derivatives(vx + k2vx / 2, vy + k2vy / 2)
            k3vx, k3vy = ax3 * dt, ay3 * dt
            k3x, k3y = (vx + k2vx / 2) * dt, (vy + k2vy / 2) * dt

            ax4, ay4 = derivatives(vx + k3vx, vy + k3vy)
            k4vx, k4vy = ax4 * dt, ay4 * dt
            k4x, k4y = (vx + k3vx) * dt, (vy + k3vy) * dt

            vx += (k1vx + 2 * k2vx + 2 * k3vx + k4vx) / 6
            vy += (k1vy + 2 * k2vy + 2 * k3vy + k4vy) / 6
            x += (k1x + 2 * k2x + 2 * k3x + k4x) / 6
            y += (k1y + 2 * k2y + 2 * k3y + k4y) / 6

            if y >= 0:
                xs.append(x)
                ys.append(y)
                max_h = max(max_h, y)

        v_final = math.sqrt(vx ** 2 + vy ** 2)
        return xs, ys, x, max_h, v_final

    def animate(self):
        if self.is_animating:
            return

        params = self.get_params()
        if not params:
            return

        self.is_animating = True

        xs, ys, dist, hmax, vfin = self.simulate(**params)

        color = self.colors[self.color_index % len(self.colors)]
        dt_value = params["dt"]

        label = f"dt = {dt_value:.3f} с"

        self.results[params["dt"]] = (dist, hmax, vfin)
        self.update_table()

        line, = self.ax.plot([], [], lw=2, color=color, label=label)
        point, = self.ax.plot([], [], 'o', color=color, markersize=6)

        self.legend_lines.append(line)

        if len(xs) > 0:
            current_xlim = self.ax.get_xlim()
            current_ylim = self.ax.get_ylim()
            self.ax.set_xlim(0, max(current_xlim[1], max(xs) * 1.1))
            self.ax.set_ylim(0, max(current_ylim[1], max(ys) * 1.1))

        def update(i):
            line.set_data(xs[:i + 1], ys[:i + 1])
            point.set_data([xs[i]], [ys[i]])
            return line, point

        def on_finish():
            self.ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
            self.canvas.draw()
            self.is_animating = False
            self.color_index += 1

        self.animation = FuncAnimation(
            self.figure,
            update,
            frames=len(xs),
            interval=30,
            repeat=False,
            blit=False
        )

        self.canvas.draw()
        self.root.after(len(xs) * 30 + 100, on_finish)
-
    def update_table(self):
        self.result_text.delete(1.0, tk.END)

        if not self.results:
            return

        self.result_text.insert(tk.END, " dt   | Дальность | Макс. высота | Скорость\n")
        self.result_text.insert(tk.END, "-" * 55 + "\n")

        for dt in sorted(self.results):
            d, h, v = self.results[dt]
            self.result_text.insert(
                tk.END,
                f"{dt:4.3f} | {d:9.2f} | {h:12.2f} | {v:8.2f}\n"
            )

    def clear(self):
        if self.animation:
            self.animation.event_source.stop()
            self.animation = None

        self.ax.clear()
        self.ax.set_title("Траектория полета")
        self.ax.set_xlabel("x (м)")
        self.ax.set_ylabel("y (м)")
        self.ax.grid()
        self.ax.legend(loc='upper right', fontsize=8)

        self.results.clear()
        self.result_text.delete(1.0, tk.END)
        self.legend_lines.clear()
        self.color_index = 0

        self.canvas.draw()
        self.is_animating = False


if __name__ == "__main__":
    root = tk.Tk()
    app = FlightSimulatorApp(root)
    root.mainloop()
```
</details>

| Шаг моделирования, с | 1 | 0.1 | 0.01 | 0.001 | 0.0001 |
|----------------------|---|-----|------|-------|--------|
| Дальность полёта, м |  65,08 |   65,01   |   64,46   |   64,44    |    64,43    |
| Максимальная высота, м | 23,77 | 25,60 | 25,61 | 25,61 | 25,61 |
| Скорость в конечной точке, м/с | 19,51 | 18,54 | 18,32 | 18,31 | 18,31 |

### Скриншот:

<img width="990" height="532" alt="image" src="https://github.com/user-attachments/assets/3ec325c0-99e7-461a-b4cf-c784fbec0fa3" />




### Выводы


Реализовано приложения для моделирования полёта тела в атмосфере с изменяемым шагом моделирования. Благодаря этому сделаны выводы:
1. Чем выше шаг модели, тем больше погрешность.
2. При уменьшении шага, проиходит все три величины стабилизируются.




