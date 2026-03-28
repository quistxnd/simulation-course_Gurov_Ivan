class LCG:
    def __init__(self, seed=42):
        # Параметры из Numerical Recipes
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32
        self.state = seed

    def next_val(self):
        """Генерация следующего числа в диапазоне [0, 1)"""
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m

def get_sample_mean(data):
    return sum(data) / len(data)

def get_sample_variance(data, mean):
    return sum((x - mean) ** 2 for x in data) / len(data)

# --- Основной блок выполнения ---

N = 100_000
seed_value = 42

# 1. Генерация выборки
lcg = LCG(seed=seed_value)
data_lcg = [lcg.next_val() for _ in range(N)]

# 2. Расчет статистик
mean_val = get_sample_mean(data_lcg)
var_val = get_sample_variance(data_lcg, mean_val)

# 3. Теоретические значения
theory_mean = 0.5
theory_var = 1/12

# 4. Вывод результатов
print(f"--- Результаты для N = {N} ---")
print(f"Среднее (Mean):     {mean_val:.6f} (Теория: {theory_mean:.6f})")
print(f"Дисперсия (Var):    {var_val:.6f} (Теория: {theory_var:.6f})")
print("-" * 30)
print(f"Отклонение среднего:   {abs(theory_mean - mean_val):.6f}")
print(f"Отклонение дисперсии: {abs(theory_var - var_val):.6f}")
