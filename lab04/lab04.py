import random
import statistics


class lcg_random: # линейный конгруэнтный генератор

    def __init__(self, seed=42):
        self.m = 2 ** 32
        self.a = 1664525
        self.c = 1013904223
        self.state = seed

    def random(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m


def main():
    N = 100_000

    # генерация выборок
    custom_rng = lcg_random(seed=123)
    custom_sample = [custom_rng.random() for _ in range(N)]
    builtin_sample = [random.random() for _ in range(N)]

    # статистика
    custom_mean, custom_var = statistics.mean(custom_sample), statistics.variance(custom_sample)
    builtin_mean, builtin_var = statistics.mean(builtin_sample), statistics.variance(builtin_sample)

    # теоретические значения
    th_mean = 0.5
    th_var = 1 / 12

    # Вывод результатов
    print(f"Размер выборки: {N}\n")
    print(f"{'Датчик':<20} | {'Среднее':<10} | {'Дисперсия'}")
    print("-" * 46)
    print(f"{'Теоретический':<20} | {th_mean:<10.6f} | {th_var:.6f}")
    print(f"{'Свой (LCG)':<20} | {custom_mean:<10.6f} | {custom_var:.6f}")
    print(f"{'Встроенный (Python)':<20} | {builtin_mean:<10.6f} | {builtin_var:.6f}")


if __name__ == "__main__":
    main()