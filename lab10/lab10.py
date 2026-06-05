import sys
import math
import heapq
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QFormLayout, QPushButton,
    QDoubleSpinBox, QSpinBox, QTextEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class QueueModel:
    def __init__(self, l, m, c, q, n):
        self.l = l
        self.m = m
        self.c = c
        self.q = q
        self.cap = c + q
        self.n = n

    def run_sim(self):
        events = []
        arrivals = np.random.exponential(1.0 / self.l, self.n)
        arr_times = np.cumsum(arrivals)

        for t in arr_times:
            heapq.heappush(events, (t, 0))

        t_curr = 0.0
        sys_cnt = 0
        states = {i: 0.0 for i in range(self.cap + 1)}
        rej = 0

        while events:
            t_prev = t_curr
            t_curr, e_type = heapq.heappop(events)

            if sys_cnt <= self.cap:
                states[sys_cnt] += (t_curr - t_prev)

            if e_type == 0:
                if sys_cnt < self.cap:
                    sys_cnt += 1
                    if sys_cnt <= self.c:
                        dt = np.random.exponential(1.0 / self.m)
                        heapq.heappush(events, (t_curr + dt, 1))
                else:
                    rej += 1
            else:
                sys_cnt -= 1
                if sys_cnt >= self.c:
                    dt = np.random.exponential(1.0 / self.m)
                    heapq.heappush(events, (t_curr + dt, 1))

        p_emp = {k: v / t_curr for k, v in states.items()}
        return p_emp, rej / self.n

    def get_theory(self):
        a = self.l / self.m
        p = {}

        s0 = sum((a ** k) / math.factorial(k) for k in range(self.c + 1))
        s1 = sum((a ** (self.c + i)) / (math.factorial(self.c) * (self.c ** i)) for i in range(1, self.q + 1))

        p0 = 1.0 / (s0 + s1)
        p[0] = p0

        for k in range(1, self.c + 1):
            p[k] = (a ** k / math.factorial(k)) * p0

        for i in range(1, self.q + 1):
            p[self.c + i] = (a ** (self.c + i) / (math.factorial(self.c) * (self.c ** i))) * p0

        return p, p.get(self.cap, 0.0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("СМО M/M/c/m")
        self.resize(1000, 650)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        left_pane = QVBoxLayout()
        form = QFormLayout()

        self.inp_l = QDoubleSpinBox()
        self.inp_l.setRange(0.1, 100.0)
        self.inp_l.setValue(10.0)
        form.addRow("λ (приход):", self.inp_l)

        self.inp_m = QDoubleSpinBox()
        self.inp_m.setRange(0.1, 100.0)
        self.inp_m.setValue(3.0)
        form.addRow("μ (обслуживание):", self.inp_m)

        self.inp_c = QSpinBox()
        self.inp_c.setRange(1, 20)
        self.inp_c.setValue(3)
        form.addRow("Каналы (c):", self.inp_c)

        self.inp_q = QSpinBox()
        self.inp_q.setRange(0, 50)
        self.inp_q.setValue(10)
        form.addRow("Очередь (m):", self.inp_q)

        self.inp_n = QSpinBox()
        self.inp_n.setRange(100, 1000000)
        self.inp_n.setValue(20000)
        self.inp_n.setSingleStep(1000)
        form.addRow("Кол-во заявок:", self.inp_n)

        left_pane.addLayout(form)

        self.btn = QPushButton("Рассчитать")
        self.btn.clicked.connect(self.run_calc)
        left_pane.addWidget(self.btn)

        self.text_out = QTextEdit()
        self.text_out.setReadOnly(True)
        left_pane.addWidget(self.text_out)

        right_pane = QVBoxLayout()
        self.fig, self.ax = plt.subplots(tight_layout=True)
        self.canvas = FigureCanvas(self.fig)
        right_pane.addWidget(self.canvas)

        main_layout.addLayout(left_pane, 1)
        main_layout.addLayout(right_pane, 2)

    def run_calc(self):
        l = self.inp_l.value()
        m = self.inp_m.value()
        c = self.inp_c.value()
        q = self.inp_q.value()
        n = self.inp_n.value()

        model = QueueModel(l, m, c, q, n)
        p_emp, rej_emp = model.run_sim()
        p_th, rej_th = model.get_theory()

        cap = c + q
        x = np.arange(cap + 1)
        y_emp = [p_emp.get(i, 0.0) for i in range(cap + 1)]
        y_th = [p_th.get(i, 0.0) for i in range(cap + 1)]

        self.ax.clear()
        self.ax.plot(x, y_emp, marker='o', label='Имитация')
        self.ax.plot(x, y_th, linestyle='--', label='Теория')
        self.ax.set_xlabel('Заявок в системе')
        self.ax.set_ylabel('Вероятность')
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

        rho = l / m
        res = (
            f"--- Результаты моделирования ---\n"
            f"Загрузка (ρ) = {rho:.3f}\n\n"
            f"Вероятность простоя:\n"
            f"Теория: {p_th.get(0, 0):.4f}\n"
            f"Практика: {p_emp.get(0, 0):.4f}\n\n"
            f"Вероятность отказа:\n"
            f"Теория: {rej_th:.4f}\n"
            f"Практика: {rej_emp:.4f}\n\n"
            f"Относительная пропускная способность:\n"
            f"Теория: {(1 - rej_th):.4f}\n"
            f"Практика: {(1 - rej_emp):.4f}\n\n"
            f"Абсолютная пропускная способность:\n"
            f"A = {l * (1 - rej_emp):.3f}\n"
        )
        self.text_out.setText(res)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())