import tkinter as tk
from tkinter import ttk, messagebox
import random

root = tk.Tk()
root.title("Моделирование случайных событий")
root.geometry("600x600")
root.configure(bg="#1e1e2f")
root.resizable(False, False)


predictions_data = {
    "Это точно": 50, "Без сомнений": 50, "Скорее всего да": 50,
    "Перспективы хорошие": 50, "Да": 50, "Пока не ясно": 50,
    "Спроси позже": 50, "Лучше не говорить": 50, "Сконцентрируйся": 50,
    "Не рассчитывай": 50, "Мой ответ — нет": 50, "Очень сомнительно": 50
}


-
def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Настройка вероятностей")
    settings_window.geometry("400x500")
    settings_window.configure(bg="#2a2a40")

    canvas = tk.Canvas(settings_window, bg="#2a2a40", highlightthickness=0)
    scrollbar = ttk.Scrollbar(settings_window, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#2a2a40")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    tk.Label(scroll_frame, text="Установите веса для ответов:", bg="#2a2a40", fg="#00ffcc",
             font=("Arial", 12, "bold")).pack(pady=10)

    scales = {}
    for pred, weight in predictions_data.items():
        frame = tk.Frame(scroll_frame, bg="#2a2a40")
        frame.pack(fill="x", padx=20, pady=5)
        tk.Label(frame, text=pred, bg="#2a2a40", fg="white", width=20, anchor="w").pack(side="left")
        s = tk.Scale(frame, from_=0, to=100, orient="horizontal", bg="#2a2a40", fg="#00ffcc", highlightthickness=0)
        s.set(weight)
        s.pack(side="right")
        scales[pred] = s

    def save_settings():
        for pred in predictions_data:
            predictions_data[pred] = scales[pred].get()
        settings_window.destroy()

    tk.Button(settings_window, text="Сохранить", command=save_settings, bg="#6c63ff", fg="white").pack(pady=10)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")



notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)


frame_yes_no = tk.Frame(notebook, bg="#1e1e2f")
notebook.add(frame_yes_no, text="Да / Нет")


def say_yes_no():
    result = random.choices(["ДА", "НЕТ"], weights=[0.7, 0.3], k=1)[0]
    label_result_yes_no.config(text=result)


tk.Label(frame_yes_no, text="Задайте вопрос", font=("Arial", 18), bg="#1e1e2f", fg="white").pack(pady=40)
tk.Button(frame_yes_no, text="Получить ответ", font=("Arial", 14), bg="#6c63ff", fg="white", command=say_yes_no).pack()
label_result_yes_no = tk.Label(frame_yes_no, text="", font=("Arial", 48, "bold"), bg="#1e1e2f", fg="#00ffcc")
label_result_yes_no.pack(pady=40)


frame_magic = tk.Frame(notebook, bg="#1e1e2f")
notebook.add(frame_magic, text="Шар предсказаний")


btn_settings = tk.Button(frame_magic, text="⚙ Настроить вероятности", font=("Arial", 10), bg="#444466", fg="white",
                         command=open_settings)
btn_settings.pack(pady=10)

entry_question = tk.Entry(frame_magic, width=40, font=("Arial", 12), justify="center")
entry_question.pack(pady=10)

canvas_ball = tk.Canvas(frame_magic, width=300, height=300, bg="#1e1e2f", highlightthickness=0)
canvas_ball.pack(pady=10)

ball = canvas_ball.create_oval(20, 20, 280, 280, fill="black", outline="gray", width=3)
window = canvas_ball.create_oval(90, 90, 210, 210, fill="#1f3fff", outline="#0a1a6b", width=3)
answer_var = tk.StringVar(value="...")
label_answer = tk.Label(frame_magic, textvariable=answer_var, font=("Arial", 10, "bold"), fg="white", bg="#1f3fff",
                        wraplength=100)
label_win = canvas_ball.create_window(150, 150, window=label_answer)

shaking = False


def animate_shake(count=0):
    global shaking
    if count < 20:
        dx, dy = random.randint(-5, 5), random.randint(-5, 5)
        canvas_ball.move(ball, dx, dy);
        canvas_ball.move(window, dx, dy);
        canvas_ball.move(label_win, dx, dy)
        root.after(40, lambda: animate_shake(count + 1))
    else:
        canvas_ball.coords(ball, 20, 20, 280, 280)
        canvas_ball.coords(window, 90, 90, 210, 210)
        canvas_ball.coords(label_win, 150, 150)

        preds = list(predictions_data.keys())
        weights = list(predictions_data.values())

        if sum(weights) == 0: weights = [1] * len(preds)  # Защита от нулевой суммы

        answer_var.set(random.choices(preds, weights=weights, k=1)[0])
        shaking = False


def shake_ball():
    global shaking
    if shaking or not entry_question.get().strip(): return
    shaking = True
    answer_var.set("...")
    animate_shake()


tk.Button(frame_magic, text="Спросить шар", font=("Arial", 14), bg="#6c63ff", fg="white", command=shake_ball).pack(
    pady=20)

root.mainloop()
