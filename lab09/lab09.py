import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QDoubleSpinBox,
    QSpinBox, QTextEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

STYLE_SHEET = """
QMainWindow { 
    background-color: #F3F4F6; /* Светло-серый фон окна */
}
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    color: #374151; /* Темно-серый текст */
}
QLabel { 
    font-weight: bold; 
    margin-top: 5px;
}
QPushButton { 
    background-color: #3B82F6; /* Приятный синий цвет */
    color: white; 
    border: none; 
    padding: 12px; 
    border-radius: 6px; 
    font-weight: bold;
    font-size: 14px;
}
QPushButton:hover { 
    background-color: #2563EB; /* Цвет чуть темнее при наведении */
}
QPushButton:pressed {
    background-color: #1D4ED8;
}
QDoubleSpinBox, QSpinBox { 
    background-color: #FFFFFF; 
    color: #1F2937; 
    border: 1px solid #D1D5DB; 
    border-radius: 4px;
    padding: 5px;
}
QDoubleSpinBox:focus, QSpinBox:focus {
    border: 1px solid #3B82F6;
}
QTextEdit { 
    background-color: #FFFFFF; 
    color: #1F2937; 
    border: 1px solid #D1D5DB; 
    border-radius: 6px;
    padding: 10px;
    font-family: 'Consolas', 'Courier New', monospace; /* Моноширинный для ровных цифр */
    font-size: 13px; 
}
"""


class MM1LossEngine:
    @staticmethod
    def simulate(lam, mu, n_requests):
        accepted = 0
        rejected = 0
        inter_arrivals = np.random.exponential(1.0 / lam, n_requests)
        service_times = np.random.exponential(1.0 / mu, n_requests)

        arrival_times = np.cumsum(inter_arrivals)

        server_free_time = 0.0

        for i in range(n_requests):
            arrival = arrival_times[i]
            if arrival >= server_free_time:
                accepted += 1
                server_free_time = arrival + service_times[i]
            else:
                rejected += 1

        p0_emp = accepted / n_requests
        p1_emp = rejected / n_requests

        return p0_emp, p1_emp


class QueuingLabWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Моделирование СМО M/M/1")
        self.resize(1100, 700)
        self.setStyleSheet(STYLE_SHEET)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        control_panel = QVBoxLayout()
        control_panel.setSpacing(10)

        control_panel.addWidget(QLabel("Интенсивность поступления λ (заявок/ед.вр):"))
        self.sb_lambda = QDoubleSpinBox()
        self.sb_lambda.setRange(0.1, 100.0)
        self.sb_lambda.setValue(5.0)
        self.sb_lambda.setSingleStep(0.5)
        control_panel.addWidget(self.sb_lambda)

        control_panel.addWidget(QLabel("Интенсивность обслуживания μ (заявок/ед.вр):"))
        self.sb_mu = QDoubleSpinBox()
        self.sb_mu.setRange(0.1, 100.0)
        self.sb_mu.setValue(6.0)
        self.sb_mu.setSingleStep(0.5)
        control_panel.addWidget(self.sb_mu)

        control_panel.addWidget(QLabel("Количество заявок для симуляции (N):"))
        self.sb_n = QSpinBox()
        self.sb_n.setRange(1, 1000000)
        self.sb_n.setValue(10000)
        self.sb_n.setSingleStep(1000)
        control_panel.addWidget(self.sb_n)

        control_panel.addSpacing(10)

        self.btn_run = QPushButton("Запустить симуляцию")
        self.btn_run.clicked.connect(self.process)
        control_panel.addWidget(self.btn_run)

        control_panel.addSpacing(10)
        control_panel.addWidget(QLabel("Результаты (Статистика):"))

        self.results_log = QTextEdit()
        self.results_log.setReadOnly(True)
        control_panel.addWidget(self.results_log)
        layout.addLayout(control_panel, 1)
        self.canvas = FigureCanvas(plt.Figure(figsize=(7, 5), facecolor='#F3F4F6'))
        layout.addWidget(self.canvas, 3)

        self.process()

    def process(self):
        lam = self.sb_lambda.value()
        mu = self.sb_mu.value()
        n = self.sb_n.value()

        p0_emp, p1_emp = MM1LossEngine.simulate(lam, mu, n)

        rho = lam / mu
        p0_theor = 1.0 / (1.0 + rho)
        p1_theor = rho / (1.0 + rho)

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.set_facecolor('#FFFFFF')

        labels = ['Свободен (P0)', 'Занят / Отказ (P1)']
        emp_vals = [p0_emp, p1_emp]
        theor_vals = [p0_theor, p1_theor]

        x = np.arange(len(labels))
        width = 0.35

        ax.bar(x - width / 2, emp_vals, width, label='Эмпирика (симуляция)', color='#3B82F6', edgecolor='#2563EB',
               zorder=3)
        ax.bar(x + width / 2, theor_vals, width, label='Теория (формулы)', color='#F59E0B', edgecolor='#D97706',
               alpha=0.9, zorder=3)

        ax.set_title(f"Вероятности состояний СМО (Нагрузка ρ = {rho:.2f})", color='#1F2937', pad=15, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, color='#374151', fontsize=11)
        ax.tick_params(axis='y', colors='#374151')

        legend = ax.legend(facecolor='#FFFFFF', edgecolor='#D1D5DB')
        plt.setp(legend.get_texts(), color='#374151')

        ax.grid(color='#E5E7EB', linestyle='-', linewidth=1, zorder=0, axis='y')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#D1D5DB')
        ax.spines['left'].set_color('#D1D5DB')

        self.canvas.figure.tight_layout()
        self.canvas.draw()

        report = (
            f"--- СТАТИСТИКА СМО ---\n"
            f"Заявок обработано: {n}\n"
            f"Нагрузка (ρ = λ/μ): {rho:.3f}\n\n"

            f"[ВЕРОЯТНОСТЬ P0 (Канал свободен)]\n"
            f"  Теоретическая:   {p0_theor:.4f}\n"
            f"  Эмпирическая: {p0_emp:.4f}\n"
            f"  Разница:  {abs(p0_theor - p0_emp):.4f}\n\n"

            f"[ВЕРОЯТНОСТЬ P1 (Канал занят / Отказ)]\n"
            f"  Теоретическая:   {p1_theor:.4f}\n"
            f"  Эмпирическая: {p1_emp:.4f}\n"
            f"  Разница:  {abs(p1_theor - p1_emp):.4f}\n\n"

            f"[АБСОЛЮТНАЯ ПРОПУСКНАЯ СПОСОБНОСТЬ (A)]\n"
            f"  Эмпирическая: {(lam * p0_emp):.3f} заяв/ед.вр"
        )
        self.results_log.setText(report)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if hasattr(sys, 'frozen'):
        QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    w = QueuingLabWindow()
    w.show()
    sys.exit(app.exec())