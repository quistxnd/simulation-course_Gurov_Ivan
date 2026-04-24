import random

class LCG:
    def __init__(self, seed=42):
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32
        self.state = seed

    def next_val(self):
        """Генерация следующего числа в диапазоне [0, 1)"""
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m

def get_stats(data):
    """Вычисление среднего и дисперсии для выборки"""
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    return mean, variance

# --- Параметры эксперимента ---
N = 100_000
seed_value = 42

# 1. Генерация данных через твой LCG
lcg = LCG(seed=seed_value)
data_lcg = [lcg.next_val() for _ in range(N)]
mean_lcg, var_lcg = get_stats(data_lcg)

# 2. Генерация данных через встроенный random
random.seed(seed_value)
data_builtin = [random.random() for _ in range(N)]
mean_builtin, var_builtin = get_stats(data_builtin)

# 3. Теоретические значения для U(0, 1)
theory_mean = 0.5
theory_var = 1/12

print(f"{'Параметр':<15} | {'Теория':<10} | {'Мой LCG':<10} | {'random.py':<10}")
print("-" * 55)
print(f"{'Среднее':<15} | {theory_mean:<10.5f} | {mean_lcg:<10.5f} | {mean_builtin:<10.5f}")
print(f"{'Дисперсия':<15} | {theory_var:<10.5f} | {var_lcg:<10.5f} | {var_builtin:<10.5f}")

print("\nАнализ точности (разница с теорией):")
print(f"Отклонение LCG:     {abs(theory_mean - mean_lcg):.7f}")
print(f"Отклонение random:  {abs(theory_mean - mean_builtin):.7f}")
