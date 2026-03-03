import random
import math

# -----------------------------
# 1. Базовый датчик (LCG)
# -----------------------------
class LCG:
    def __init__(self, seed=1):
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32
        self.state = seed

    def random(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m  # нормировка к [0,1)


# -----------------------------
# 2. Функции для вычислений
# -----------------------------
def sample_mean(data):
    return sum(data) / len(data)

def sample_variance(data):
    mean = sample_mean(data)
    return sum((x - mean) ** 2 for x in data) / len(data)


# -----------------------------
# 3. Параметры
# -----------------------------
N = 100_000

# -----------------------------
# 4. Данные от LCG
# -----------------------------
lcg = LCG(seed=42)
data_lcg = [lcg.random() for _ in range(N)]

mean_lcg = sample_mean(data_lcg)
var_lcg = sample_variance(data_lcg)

# -----------------------------
# 5. Данные от встроенного генератора
# -----------------------------
data_builtin = [random.random() for _ in range(N)]

mean_builtin = sample_mean(data_builtin)
var_builtin = sample_variance(data_builtin)

# -----------------------------
# 6. Теоретические значения
# -----------------------------
theoretical_mean = 0.5
theoretical_variance = 1/12

# -----------------------------
# 7. Вывод результатов
# -----------------------------
print("Размер выборки:", N)
print()

print("LCG генератор:")
print("Среднее:", mean_lcg)
print("Дисперсия:", var_lcg)
print()

print("Встроенный генератор:")
print("Среднее:", mean_builtin)
print("Дисперсия:", var_builtin)
print()

print("Теоретические значения:")
print("Среднее:", theoretical_mean)
print("Дисперсия:", theoretical_variance)