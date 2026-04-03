import tkinter as tk
from tkinter import ttk
import random

root = tk.Tk()
root.title("Моделирование случайных событий")
root.geometry("600x550")
root.configure(bg="#1e1e2f")
root.resizable(False, False)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

style = ttk.Style()
style.theme_use("clam")


frame_yes_no = tk.Frame(notebook, bg="#1e1e2f")
notebook.add(frame_yes_no, text="Да / Нет")


def say_yes_no():
    result = random.choices(["ДА", "НЕТ"], weights=[0.7, 0.3], k=1)[0]
    label_result_yes_no.config(text=result)


title1 = tk.Label(frame_yes_no,
                  text="Задайте вопрос\nи получите ответ",
                  font=("Arial", 18, "bold"),
                  bg="#1e1e2f",
                  fg="white")
title1.pack(pady=40)

button_yes_no = tk.Button(frame_yes_no,
                          text="Получить ответ",
                          font=("Arial", 14),
                          bg="#6c63ff",
                          fg="white",
                          relief="flat",
                          padx=20,
                          pady=10,
                          command=say_yes_no)
button_yes_no.pack(pady=20)

label_result_yes_no = tk.Label(frame_yes_no,
                               text="",
                               font=("Arial", 48, "bold"),
                               bg="#1e1e2f",
                               fg="#00ffcc")
label_result_yes_no.pack(pady=40)



frame_magic = tk.Frame(notebook, bg="#1e1e2f")
notebook.add(frame_magic, text="Шар предсказаний")

predictions = [
    "Это точно",
    "Без сомнений",
    "Скорее всего да",
    "Перспективы хорошие",
    "Да",
    "Пока не ясно",
    "Спроси позже",
    "Лучше не говорить",
    "Сконцентрируйся и спроси снова",
    "Не рассчитывай на это",
    "Мой ответ — нет",
    "Очень сомнительно"
]

title2 = tk.Label(frame_magic,
                  text="Шар предсказаний",
                  font=("Arial", 20, "bold"),
                  bg="#1e1e2f",
                  fg="white")
title2.pack(pady=10)

entry_question = tk.Entry(frame_magic,
                          width=40,
                          font=("Arial", 12),
                          justify="center")
entry_question.pack(pady=10)


canvas = tk.Canvas(frame_magic,
                   width=300,
                   height=300,
                   bg="#1e1e2f",
                   highlightthickness=0)
canvas.pack(pady=20)

ball = canvas.create_oval(20, 20, 280, 280,
                          fill="black", outline="gray", width=3)

window = canvas.create_oval(90, 90, 210, 210,
                            fill="#1f3fff", outline="#0a1a6b", width=3)

answer_text = tk.StringVar()
answer_text.set("...")

label_answer = tk.Label(frame_magic,
                        textvariable=answer_text,
                        font=("Arial", 11, "bold"),
                        fg="white",
                        bg="#1f3fff",
                        wraplength=100,
                        justify="center")

label_window = canvas.create_window(150, 150, window=label_answer)



shaking = False
shake_count = 0


def animate_shake():
    global shake_count, shaking

    if shake_count < 20:
        dx = random.randint(-5, 5)
        dy = random.randint(-5, 5)
        canvas.move(ball, dx, dy)
        canvas.move(window, dx, dy)
        canvas.move(label_window, dx, dy)

        shake_count += 1
        root.after(40, animate_shake)
    else:
        # возвращаем шар в центр
        canvas.coords(ball, 20, 20, 280, 280)
        canvas.coords(window, 90, 90, 210, 210)
        canvas.coords(label_window, 150, 150)

        answer = random.choice(predictions)
        answer_text.set(answer)

        shake_count = 0
        shaking = False


def shake_ball():
    global shaking

    if shaking:
        return

    question = entry_question.get()
    if question.strip() == "":
        answer_text.set("Введите вопрос")
        return

    shaking = True
    answer_text.set("...")
    animate_shake()


button_magic = tk.Button(frame_magic,
                         text="Спросить шар",
                         font=("Arial", 14),
                         bg="#6c63ff",
                         fg="white",
                         relief="flat",
                         padx=20,
                         pady=10,
                         command=shake_ball)
button_magic.pack(pady=10)

root.mainloop()
