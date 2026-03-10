import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QLineEdit, QTabWidget, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

# --- ЛЕГКИЙ ДИЗАЙН ---
STYLE = """
QMainWindow { background-color: #ffffff; }
QTabWidget::pane { border: none; background-color: #ffffff; }
QTabBar::tab {
    background: #f0f0f0; color: #555; padding: 12px 40px;
    border-radius: 10px; margin: 5px; font-weight: bold;
}
QTabBar::tab:selected { background: #007AFF; color: #fff; }

QLineEdit {
    border: 2px solid #eee; border-radius: 12px; padding: 12px;
    font-size: 14px; background: #f9f9f9; color: #333;
}
QLineEdit:focus { border: 2px solid #007AFF; }

QPushButton {
    background-color: #007AFF; color: white; border-radius: 12px;
    padding: 14px; font-weight: bold; font-size: 14px;
}
QPushButton:hover { background-color: #0063CC; }

#MagicBall {
    background-color: qradialgradient(cx:0.4, cy:0.4, radius: 1, fx:0.3, fy:0.3, stop:0 #444, stop:1 #000);
    color: white; border-radius: 90px; font-weight: bold; font-size: 14px; padding: 20px;
}
"""

class WhiteMinimalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oracle")
        self.setFixedSize(380, 500)
        self.setStyleSheet(STYLE)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(self.create_yes_no(), "Да/Нет")
        self.tabs.addTab(self.create_ball(), "Шар")

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        widget.setGraphicsEffect(shadow)

    def create_yes_no(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        inp = QLineEdit()
        inp.setPlaceholderText("Введите ваш вопрос...")

        res = QLabel("?")
        res.setAlignment(Qt.AlignmentFlag.AlignCenter)
        res.setStyleSheet("font-size: 60px; font-weight: bold; color: #ddd;")

        btn = QPushButton("ПОЛУЧИТЬ ОТВЕТ")

        def logic():
            if inp.text():
                ans = random.choice(["ДА", "НЕТ"])
                res.setText(ans)
                res.setStyleSheet(
                    f"font-size: 60px; font-weight: bold; color: {'#28C76F' if ans == 'ДА' else '#EA5455'};")

        btn.clicked.connect(logic)

        layout.addWidget(inp)
        layout.addStretch()
        layout.addWidget(res)
        layout.addStretch()
        layout.addWidget(btn)
        return page

    def create_ball(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        inp = QLineEdit()
        inp.setPlaceholderText("Спросите магический шар...")

        ball = QLabel("8")
        ball.setObjectName("MagicBall")
        ball.setFixedSize(180, 180)
        ball.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ball.setWordWrap(True)
        self.add_shadow(ball)  # Добавляем тень для красоты

        btn = QPushButton("ПОТРЯСТИ ШАР")

        def logic():
            if inp.text():
                answers = ["Бесспорно", "Предрешено", "Никаких сомнений", "Определённо да", "Да",
                           "Пока неясно", "Спроси позже", "Лучше не знать",
                           "Даже не думай", "Мой ответ — нет", "Весьма сомнительно"]
                ball.setText(random.choice(answers))

        btn.clicked.connect(logic)

        layout.addWidget(inp)
        layout.addStretch()
        layout.addWidget(ball, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        layout.addWidget(btn)
        return page

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WhiteMinimalApp()
    window.show()
    sys.exit(app.exec())