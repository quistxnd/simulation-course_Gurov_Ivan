import customtkinter as ctk
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import chi2, norm


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Цветовая палитра
BG_COLOR = "#121212"
PANEL_BG = "#1E1E1E"
ACCENT_PURPLE = "#BB86FC"
ACCENT_TEAL = "#03DAC6"
TEXT_MUTED = "#888888"


class HorizontalStatCard(ctk.CTkFrame):
    # Карточка для горизонтального размещения под графиком

    def __init__(self, master, title, accent_color):
        super().__init__(master, fg_color=PANEL_BG, corner_radius=10, border_width=1, border_color="#333333")

        top_line = ctk.CTkFrame(self, height=4, fg_color=accent_color, corner_radius=10)
        top_line.pack(fill="x", padx=10, pady=(10, 0))

        self.title_lbl = ctk.CTkLabel(self, text=title.upper(), text_color=TEXT_MUTED, font=("Arial", 11, "bold"))
        self.title_lbl.pack(pady=(5, 0))

        self.value_lbl = ctk.CTkLabel(self, text="0.000", text_color="white", font=("Arial", 24, "bold"))
        self.value_lbl.pack(pady=0)

        self.status_lbl = ctk.CTkLabel(self, text="ОЖИДАНИЕ", text_color=TEXT_MUTED, font=("Arial", 11, "bold"))
        self.status_lbl.pack(pady=(0, 10))

    def update_val(self, value, is_error=True, custom_status=None):
        if custom_status:
            self.value_lbl.configure(text=f"{value:.4f}")
            self.status_lbl.configure(text=custom_status.upper())
            color = ACCENT_TEAL if "ПРОЙДЕН" in custom_status else "#CF6679"
            self.status_lbl.configure(text_color=color)
        elif is_error:
            err_percent = value * 100
            self.value_lbl.configure(text=f"{err_percent:.2f}%")
            if err_percent <= 5.0:
                self.status_lbl.configure(text="НОРМА (<5%)", text_color=ACCENT_TEAL)
            else:
                self.status_lbl.configure(text="ВЫСОКАЯ ПОГРЕШНОСТЬ", text_color="#CF6679")

# Класс приложения и инициалищации
class SimulationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Анализ случайных величин (Лабораторная 6)")
        self.geometry("1150x750")
        self.configure(fg_color=BG_COLOR)

        self.tabview = ctk.CTkTabview(self, fg_color=PANEL_BG, segmented_button_selected_color=ACCENT_PURPLE)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)

        self.tab_discrete = self.tabview.add("Дискретное распределение")
        self.tab_normal = self.tabview.add("Нормальное распределение")

        self.init_discrete_tab()
        self.init_normal_tab()

    
    # Интерфейс Дискретная
    def init_discrete_tab(self):
        left_panel = ctk.CTkFrame(self.tab_discrete, width=300, fg_color=BG_COLOR, corner_radius=10)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(left_panel, text="НАСТРОЙКИ", text_color=ACCENT_PURPLE, font=("Arial", 14, "bold")).pack(
            anchor="w", padx=15, pady=(15, 5))

        ctk.CTkLabel(left_panel, text="Объем выборки (N):", text_color=TEXT_MUTED).pack(anchor="w", padx=15)
        self.n_discrete_combo = ctk.CTkComboBox(left_panel, values=["10", "100", "1000", "10000"],
                                                button_color=ACCENT_PURPLE)
        self.n_discrete_combo.set("1000")
        self.n_discrete_combo.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(left_panel, text="ТАБЛИЦА ВЕРОЯТНОСТЕЙ", text_color=ACCENT_PURPLE,
                     font=("Arial", 12, "bold")).pack(anchor="w", padx=15, pady=(10, 5))

        self.table_frame = ctk.CTkScrollableFrame(left_panel, height=220, fg_color=PANEL_BG)
        self.table_frame.pack(fill="x", padx=15, pady=5)

        self.table_rows = []
        for i in range(1, 6):
            self.add_table_row(i, 0.2)

        btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(btn_frame, text="+", width=40, fg_color="#333333",
                      command=lambda: self.add_table_row("", "")).pack(side="left")
        ctk.CTkButton(btn_frame, text="-", width=40, fg_color="#333333", command=self.remove_last_row).pack(
            side="right")

        self.error_lbl_disc = ctk.CTkLabel(left_panel, text="", text_color="#CF6679", font=("Arial", 12))
        self.error_lbl_disc.pack(pady=5)

        ctk.CTkButton(left_panel, text="ГЕНЕРИРОВАТЬ", height=45, fg_color=ACCENT_PURPLE, hover_color="#9C27B0",
                      font=("Arial", 14, "bold"), command=self.run_discrete).pack(fill="x", side="bottom", padx=15,
                                                                                  pady=15)

      
        right_panel = ctk.CTkFrame(self.tab_discrete, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

     
        plot_container = ctk.CTkFrame(right_panel, fg_color=BG_COLOR, corner_radius=10)
        plot_container.pack(side="top", fill="both", expand=True, pady=(0, 10))

        self.fig_disc, self.ax_disc = plt.subplots(figsize=(6, 4), facecolor=BG_COLOR)
        self.ax_disc.set_facecolor(BG_COLOR)
        self.ax_disc.tick_params(colors='white')
        for spine in self.ax_disc.spines.values():
            spine.set_edgecolor('#444444')

        self.canvas_disc = FigureCanvasTkAgg(self.fig_disc, master=plot_container)
        self.canvas_disc.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        
        cards_container = ctk.CTkFrame(right_panel, fg_color="transparent", height=120)
        cards_container.pack(side="bottom", fill="x")

        self.card_chi_disc = HorizontalStatCard(cards_container, "Критерий χ²", ACCENT_PURPLE)
        self.card_chi_disc.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.card_m_disc = HorizontalStatCard(cards_container, "Погрешность (M)", ACCENT_TEAL)
        self.card_m_disc.pack(side="left", fill="x", expand=True, padx=5)

        self.card_d_disc = HorizontalStatCard(cards_container, "Погрешность (D)", ACCENT_TEAL)
        self.card_d_disc.pack(side="left", fill="x", expand=True, padx=(5, 0))

    # Управление строками таблиц
    
    def add_table_row(self, x_val, p_val):
        row_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=2)

        ent_x = ctk.CTkEntry(row_frame, width=100, height=28, placeholder_text="X")
        ent_x.insert(0, str(x_val))
        ent_x.pack(side="left", padx=2)

        ent_p = ctk.CTkEntry(row_frame, width=100, height=28, placeholder_text="P")
        ent_p.insert(0, str(p_val))
        ent_p.pack(side="right", padx=2)

        self.table_rows.append({'frame': row_frame, 'x': ent_x, 'p': ent_p})

    def remove_last_row(self):
        if len(self.table_rows) > 1:
            row = self.table_rows.pop()
            row['frame'].destroy()
    # Логика дискретного распределения 
    # Считывание значений из таблицы
    def run_discrete(self):
        try:
            x_th = [float(row['x'].get().replace(',', '.')) for row in self.table_rows]
            p_th = [float(row['p'].get().replace(',', '.')) for row in self.table_rows]
            N = int(self.n_discrete_combo.get())

            p_sum = sum(p_th)
            if abs(p_sum - 1.0) > 1e-4:
                self.error_lbl_disc.configure(text=f"Сумма P = {p_sum:.4f} (нужно 1.0)")
                return
            self.error_lbl_disc.configure(text="")
            # Сравнение числа с накопленной вероятностью
            samples = []
            cdf = np.cumsum(p_th)
            for _ in range(N):
                u = random.random()
                for i, c in enumerate(cdf):
                    if u <= c:
                        samples.append(x_th[i])
                        break
            # Вычисления эмпирических параметров и теоретических
            m_th = sum(x * p for x, p in zip(x_th, p_th))
            d_th = sum((x ** 2) * p for x, p in zip(x_th, p_th)) - m_th ** 2
            m_emp = np.mean(samples)
            d_emp = np.var(samples)

            err_m = abs(m_th - m_emp) / abs(m_th) if m_th != 0 else abs(m_emp)
            err_d = abs(d_th - d_emp) / d_th if d_th != 0 else abs(d_emp)

            # Хи-квадрат
            unique, counts = np.unique(samples, return_counts=True)
            freq_map = dict(zip(unique, counts))
            chi_val = 0
            for i in range(len(x_th)):
                e_i = N * p_th[i]
                o_i = freq_map.get(x_th[i], 0)
                if e_i > 0: chi_val += ((o_i - e_i) ** 2) / e_i

            df = len(x_th) - 1
            chi_crit = chi2.ppf(0.95, df if df > 0 else 1)
            chi_status = f"ПРОЙДЕН (КР: {chi_crit:.2f})" if chi_val < chi_crit else f"ОТКЛОНЕН (КР: {chi_crit:.2f})"

            self.card_chi_disc.update_val(chi_val, custom_status=chi_status)
            self.card_m_disc.update_val(err_m)
            self.card_d_disc.update_val(err_d)

            self.ax_disc.clear()
            self.ax_disc.hist(samples, bins=np.arange(min(x_th) - 0.5, max(x_th) + 1.5, 1),
                              color=ACCENT_PURPLE, alpha=0.8, rwidth=0.7)
            self.ax_disc.set_title(f"Эмпирическое распределение (N={N})", color="white", pad=10)
            self.canvas_disc.draw()

        except ValueError:
            self.error_lbl_disc.configure(text="Ошибка: проверьте ввод")

   
    #  Интерфейс Нормальная

    
    def init_normal_tab(self):
        left_panel = ctk.CTkFrame(self.tab_normal, width=300, fg_color=BG_COLOR, corner_radius=10)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(left_panel, text="МЕТОД BOX-MULLER", text_color=ACCENT_TEAL, font=("Arial", 14, "bold")).pack(
            anchor="w", padx=15, pady=(15, 5))

        ctk.CTkLabel(left_panel, text="Объем выборки (N):", text_color=TEXT_MUTED).pack(anchor="w", padx=15,
                                                                                        pady=(10, 0))
        self.n_normal_combo = ctk.CTkComboBox(left_panel, values=["10", "100", "1000", "10000"],
                                              button_color=ACCENT_TEAL)
        self.n_normal_combo.set("1000")
        self.n_normal_combo.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(left_panel, text="Интервалы (K):", text_color=TEXT_MUTED).pack(anchor="w", padx=15)
        self.entry_k = ctk.CTkEntry(left_panel)
        self.entry_k.insert(0, "15")
        self.entry_k.pack(fill="x", padx=15, pady=5)

        self.error_lbl_norm = ctk.CTkLabel(left_panel, text="", text_color="#CF6679", font=("Arial", 12))
        self.error_lbl_norm.pack(pady=5)

        ctk.CTkButton(left_panel, text="ГЕНЕРИРОВАТЬ", height=45, fg_color=ACCENT_TEAL, hover_color="#00B3A6",
                      font=("Arial", 14, "bold"), text_color="black", command=self.run_normal).pack(fill="x",
                                                                                                    side="bottom",
                                                                                                    padx=15, pady=15)

        right_panel = ctk.CTkFrame(self.tab_normal, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        plot_container = ctk.CTkFrame(right_panel, fg_color=BG_COLOR, corner_radius=10)
        plot_container.pack(side="top", fill="both", expand=True, pady=(0, 10))

        self.fig_norm, self.ax_norm = plt.subplots(figsize=(6, 4), facecolor=BG_COLOR)
        self.ax_norm.set_facecolor(BG_COLOR)
        self.ax_norm.tick_params(colors='white')
        for spine in self.ax_norm.spines.values():
            spine.set_edgecolor('#444444')

        self.canvas_norm = FigureCanvasTkAgg(self.fig_norm, master=plot_container)
        self.canvas_norm.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        cards_container = ctk.CTkFrame(right_panel, fg_color="transparent", height=120)
        cards_container.pack(side="bottom", fill="x")

        self.card_chi_norm = HorizontalStatCard(cards_container, "Критерий χ²", ACCENT_TEAL)
        self.card_chi_norm.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.card_m_norm = HorizontalStatCard(cards_container, "Отклонение (M)", ACCENT_PURPLE)
        self.card_m_norm.pack(side="left", fill="x", expand=True, padx=5)

        self.card_d_norm = HorizontalStatCard(cards_container, "Погрешность (D)", ACCENT_PURPLE)
        self.card_d_norm.pack(side="left", fill="x", expand=True, padx=(5, 0))

    # Метод Бокса-Мюллера
        
    def run_normal(self):
        try:
            self.error_lbl_norm.configure(text="")
            N = int(self.n_normal_combo.get())
            K = int(self.entry_k.get())

            samples = []
            for _ in range((N + 1) // 2):
                u1, u2 = random.random(), random.random()
                z0 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
                z1 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)
                samples.extend([z0, z1])

            samples = np.array(samples[:N])
            m_emp, d_emp = np.mean(samples), np.var(samples)

            err_m = abs(0 - m_emp)
            err_d = abs(1 - d_emp) / 1.0
    # Хи-квадрат 
            observed_freq, bin_edges = np.histogram(samples, bins=K)
            chi_val = 0
            for i in range(K):
                p_i = norm.cdf(bin_edges[i + 1]) - norm.cdf(bin_edges[i])
                expected_freq = N * p_i
                if expected_freq > 0:
                    chi_val += ((observed_freq[i] - expected_freq) ** 2) / expected_freq

            df = K - 3
            chi_crit = chi2.ppf(0.95, df if df > 0 else 1)
            chi_status = f"ПРОЙДЕН (КР: {chi_crit:.2f})" if chi_val < chi_crit else f"ОТКЛОНЕН (КР: {chi_crit:.2f})"

            self.card_chi_norm.update_val(chi_val, custom_status=chi_status)
            self.card_m_norm.update_val(err_m)
            self.card_d_norm.update_val(err_d)

            self.ax_norm.clear()
            _, bins, _ = self.ax_norm.hist(samples, bins=K, density=True, color=ACCENT_TEAL, alpha=0.7)

            x = np.linspace(min(bins), max(bins), 100)
            y = norm.pdf(x, 0, 1)
            self.ax_norm.plot(x, y, color=ACCENT_PURPLE, linewidth=2.5, label='Теория N(0,1)')
            self.ax_norm.set_title(f"Нормальное распределение (N={N})", color="white", pad=10)
            self.ax_norm.legend(facecolor=BG_COLOR, edgecolor='#444444', labelcolor='white')
            self.canvas_norm.draw()

        except ValueError:
            self.error_lbl_norm.configure(text="Ошибка ввода!")


if __name__ == "__main__":
    app = SimulationApp()
    app.mainloop()
