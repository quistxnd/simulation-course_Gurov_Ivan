import sys
import numpy as np
from scipy.stats import poisson

import matplotlib


matplotlib.use('qtagg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QDoubleSpinBox, QSpinBox, QTextEdit
)
from PyQt6.QtCore import Qt

STYLE_SHEET = """
QWidget { background-color: #F5F7FA; font-family: 'Segoe UI', Arial, sans-serif; color: #2C3E50; }
QLabel { font-weight: bold; font-size: 13px; margin-top: 5px; }
QPushButton { 
    background-color: #3498DB; color: white; border: none; 
    border-radius: 5px; padding: 12px; font-size: 14px; font-weight: bold;
}
QPushButton:hover { background-color: #2980B9; }
QPushButton:pressed { background-color: #1F618D; }
QSpinBox, QDoubleSpinBox { 
    background-color: white; border: 1px solid #BDC3C7; 
    border-radius: 4px; padding: 6px; font-size: 14px;
}
QTextEdit { 
    background-color: white; border: 1px solid #BDC3C7; 
    border-radius: 5px; padding: 10px; font-size: 14px; color: #273746;
}
"""


class CleanPoissonSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ Пуассоновского потока")
        self.resize(1000, 650)
        self.setStyleSheet(STYLE_SHEET)


        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)


        control_panel = QWidget()
        control_panel.setFixedWidth(300)
        v_layout = QVBoxLayout(control_panel)


        self.lam_input = self.create_spinbox(QDoubleSpinBox, "Интенсивность λ (заявок/сек):", 0.1, 50.0, 5.0, v_layout)
        self.t_input = self.create_spinbox(QDoubleSpinBox, "Интервал времени T (сек):", 0.1, 20.0, 2.0, v_layout)
        self.n_input = self.create_spinbox(QSpinBox, "Количество экспериментов N:", 100, 100000, 5000, v_layout)
        self.n_input.setSingleStep(1000)


        self.btn_run = QPushButton("СМОДЕЛИРОВАТЬ ПОТОК")
        self.btn_run.clicked.connect(self.run_simulation)
        v_layout.addWidget(self.btn_run)


        v_layout.addWidget(QLabel("Результаты и Вывод:"))
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        v_layout.addWidget(self.text_output)

        main_layout.addWidget(control_panel)


        self.figure, self.ax = plt.subplots(facecolor='#F5F7FA')
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)


        self.run_simulation()

    def create_spinbox(self, widget_type, label_text, min_val, max_val, default_val, layout):
        """создание однотипных элементов интерфейса"""
        layout.addWidget(QLabel(label_text))
        spinbox = widget_type()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default_val)
        layout.addWidget(spinbox)
        return spinbox

    def run_simulation(self):
        lam = self.lam_input.value()
        T = self.t_input.value()
        N = self.n_input.value()
        expected_mu = lam * T

        # генерация числа заявок через экспоненциальные интервалы времени
        results = np.zeros(N, dtype=int)
        for i in range(N):
            current_time = 0.0
            requests_count = 0
            # пока время не вышло, прибавляем случайный шаг и считаем заявки
            while (current_time := current_time + np.random.exponential(1.0 / lam)) <= T:
                requests_count += 1
            results[i] = requests_count

        # расчет среднего и дисперсии
        mean_val = np.mean(results)
        var_val = np.var(results)

        # очистка и базовая настройка графика
        self.ax.clear()
        self.ax.set_facecolor('white')
        self.ax.grid(color='#E5E8E8', linestyle='--', linewidth=1)

        # построение эмпирической гистограммы
        max_k = max(results) if len(results) > 0 else int(expected_mu * 2)
        bins = np.arange(-0.5, max_k + 1.5, 1)
        self.ax.hist(results, bins=bins, density=True, color='#85C1E9', edgecolor='#2980B9',
                     alpha=0.8, label='Модель (Гистограмма)')

        # наложение точной функции пуассона
        x_vals = np.arange(0, max_k + 1)
        y_vals = poisson.pmf(x_vals, expected_mu)
        self.ax.plot(x_vals, y_vals, 'o-', color='#E74C3C', linewidth=2.5, markersize=6,
                     label=f'Теория Пуассона (λT = {expected_mu:.1f})')

        self.ax.set_title(f"Распределение числа заявок за T={T}с", fontsize=14, color='#2C3E50')
        self.ax.set_xlabel("Число заявок", fontsize=12)
        self.ax.set_ylabel("Вероятность", fontsize=12)
        self.ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()

        # анализ данных для формирования вывода
        diff = abs(mean_val - var_val)

        report = (
            f"Ожидаемое число заявок (λT): {expected_mu:.3f}\n"
            f"Среднее (M): {mean_val:.3f}\n"
            f"Дисперсия (D): {var_val:.3f}\n\n"
            f"ВЫВОД:\n"
        )

        # проверка свойства равенства матожидания и дисперсии
        if diff < max(0.5, expected_mu * 0.1):
            report += ("Эмпирическое распределение совпадает с теоретическим. " )
        else:
            report += ("⚠️ Замечено отклонение. Возможно, число экспериментов N слишком мало " )

        self.text_output.setText(report)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CleanPoissonSimulator()
    window.show()
    sys.exit(app.exec())