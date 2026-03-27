import time
import math
import random


class LCG:
    # линейный конгруэнтный генератор
    # X_{n+1} = (a * X_n + c) mod m


    def __init__(self, seed=1):
        # константы кнута
        self.m = 2 ** 64
        self.a = 6364136223846793005
        self.c = 1442695040888963407
        self.state = seed

    def get_value(self):
        # возвращение числа [0, 1)
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m

    def generate_batch(self, size):
        # создание массива случайных чисел
        return [self.get_value() for _ in range(size)]


def analyze_distribution(data):
    # вычисление основных статистических показателей выборки
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / (n - 1)
    return mean, variance


def check_correlation(data):
    # оценка коэффициента автокорреляции между соседними элементами
    n = len(data)
    x = data[:-1]
    y = data[1:]

    mean_x, mean_y = sum(x) / len(x), sum(y) / len(y)

    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den = (sum((xi - mean_x) ** 2 for xi in x) * sum((yi - mean_y) ** 2 for yi in y)) ** 0.5
    return num / den


def main():
    N = 100000
    seed_value = int(time.time())

    my_rng = LCG(seed=seed_value)

    # сбор данных
    t0 = time.perf_counter()
    my_sample = my_rng.generate_batch(N)
    t1 = time.perf_counter()

    builtin_sample = [random.random() for _ in range(N)]

    m_mean, m_var = analyze_distribution(my_sample)
    b_mean, b_var = analyze_distribution(builtin_sample)
    corr = check_correlation(my_sample)

    print(f"--- Сравнение ГСЧ на выборке {N} элементов ---")
    print(f"{'Показатель':<15} | {'Теория':<10} | {'LCG':<10} | {'Встроенный'}")
    print("-" * 60)
    print(f"{'Мат. ожидание':<15} | {0.5:<10.5f} | {m_mean:<10.5f} | {b_mean:.5f}")
    print(f"{'Дисперсия':<15} | {1 / 12:<10.5f} | {m_var:<10.5f} | {b_var:.5f}")

    print(f"\n--- Качественный анализ собственного датчика ---")
    print(f"Автокорреляция:   {corr:.6f} (идеал: 0)")
    print(f"Время генерации:  {t1 - t0:.4f} сек")
    print(f"Воспроизводимость: {my_sample[:3] == LCG(seed_value).generate_batch(3)}")


if __name__ == "__main__":
    main()