import tkinter as tk
from tkinter import ttk
import random

root = tk.Tk()
root.title("Моделирование случайных событий")
root.geometry("600x700")
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


title1 = tk.Label(frame_yes_no, text="Задайте вопрос\nи получите ответ", font=("Arial", 18, "bold"), bg="#1e1e2f",
                  fg="white")
title1.pack(pady=40)

button_yes_no = tk.Button(frame_yes_no, text="Получить ответ", font=("Arial", 14), bg="#6c63ff", fg="white",
                          relief="flat", padx=20, pady=10, command=say_yes_no)
button_yes_no.pack(pady=20)

label_result_yes_no = tk.Label(frame_yes_no, text="", font=("Arial", 48, "bold"), bg="#1e1e2f", fg="#00ffcc")
label_result_yes_no.pack(pady=40)


frame_magic = tk.Frame(notebook, bg="#1e1e2f")
notebook.add(frame_magic, text="Шар предсказаний")


predictions_positive = ["Это точно", "Без сомнений", "Скорее всего да", "Перспективы хорошие", "Да"]
predictions_neutral = ["Пока не ясно", "Спроси позже", "Лучше не говорить", "Сконцентрируйся"]
predictions_negative = ["Не рассчитывай", "Мой ответ — нет", "Очень сомнительно"]

title2 = tk.Label(frame_magic, text="Шар предсказаний", font=("Arial", 16, "bold"), bg="#1e1e2f", fg="white")
title2.pack(pady=5)


frame_probs = tk.Frame(frame_magic, bg="#2a2a40", padx=10, pady=10)
frame_probs.pack(fill="x", padx=20)

tk.Label(frame_probs, text="Настройка шансов (%)", bg="#2a2a40", fg="#00ffcc", font=("Arial", 10, "bold")).grid(row=0,
                                                                                                                column=0,
                                                                                                                columnspan=3)


scale_pos = tk.Scale(frame_probs, from_=0, to=100, orient="horizontal", label="Да", bg="#2a2a40", fg="white",
                     highlightthickness=0)
scale_pos.set(50)
scale_pos.grid(row=1, column=0, padx=5)

scale_neu = tk.Scale(frame_probs, from_=0, to=100, orient="horizontal", label="?", bg="#2a2a40", fg="white",
                     highlightthickness=0)
scale_neu.set(25)
scale_neu.grid(row=1, column=1, padx=5)

scale_neg = tk.Scale(frame_probs, from_=0, to=100, orient="horizontal", label="Нет", bg="#2a2a40", fg="white",
                     highlightthickness=0)
scale_neg.set(25)
scale_neg.grid(row=1, column=2, padx=5)

entry_question = tk.Entry(frame_magic, width=40, font=("Arial", 12), justify="center")
entry_question.pack(pady=10)

canvas = tk.Canvas(frame_magic, width=220, height=220, bg="#1e1e2f", highlightthickness=0)
canvas.pack(pady=5)

ball = canvas.create_oval(10, 10, 210, 210, fill="black", outline="gray", width=3)
window = canvas.create_oval(60, 60, 160, 160, fill="#1f3fff", outline="#0a1a6b", width=3)

answer_text = tk.StringVar()
answer_text.set("...")
label_answer = tk.Label(frame_magic, textvariable=answer_text, font=("Arial", 9, "bold"), fg="white", bg="#1f3fff",
                        wraplength=80, justify="center")
label_window = canvas.create_window(110, 110, window=label_answer)

shaking = False
shake_count = 0


def animate_shake():
    global shake_count, shaking
    if shake_count < 15:
        dx, dy = random.randint(-5, 5), random.randint(-5, 5)
        canvas.move(ball, dx, dy)
        canvas.move(window, dx, dy)
        canvas.move(label_window, dx, dy)
        shake_count += 1
        root.after(40, animate_shake)
    else:
        canvas.coords(ball, 10, 10, 210, 210)
        canvas.coords(window, 60, 60, 160, 160)
        canvas.coords(label_window, 110, 110)


        w_pos = scale_pos.get()
        w_neu = scale_neu.get()
        w_neg = scale_neg.get()

        category = random.choices(
            ['pos', 'neu', 'neg'],
            weights=[w_pos, w_neu, w_neg],
            k=1
        )[0]

        if category == 'pos':
            res = random.choice(predictions_positive)
        elif category == 'neu':
            res = random.choice(predictions_neutral)
        else:
            res = random.choice(predictions_negative)

        answer_text.set(res)
        shake_count = 0
        shaking = False


def shake_ball():
    global shaking
    if shaking: return
    if entry_question.get().strip() == "":
        answer_text.set("Задай вопрос!")
        return
    shaking = True
    answer_text.set("...")
    animate_shake()


button_magic = tk.Button(frame_magic, text="Спросить шар", font=("Arial", 12, "bold"), bg="#6c63ff", fg="white",
                         relief="flat", command=shake_ball)
button_magic.pack(pady=5)

root.mainloop()
