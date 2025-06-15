
# Calculates probabilities of not less than n of heads

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# Заданные параметры
n_trials = 40
p_heads = 0.5  # задаём вручную, без оценки

# Симулируем броски монеты
np.random.seed(42)
flips = np.random.choice(['О', 'Р'], size=n_trials, p=[p_heads, 1 - p_heads])
n_heads = np.sum(flips == 'О')

print(f"Броски: {''.join(flips)}")
print(f"Орлов: {n_heads} из {n_trials}")
print(f"Вероятность орла: {p_heads}")

# Расчёт P(X ≥ n) при фиксированном p
x = np.arange(0, n_trials + 1)
tail_probs = binom.sf(x - 1, n_trials, p_heads)  # P(X ≥ x)

# Визуализация
plt.figure(figsize=(10, 5))
plt.plot(x, tail_probs, marker='o', linestyle='-', color='teal', label=r"$P(X \geq n)$ при p = 0.5")
plt.axvline(n_heads, color='red', linestyle='--', label=f'Наблюдение: {n_heads} орлов')
plt.title("Вероятность получить не менее n орлов (без оценки MLE)")
plt.xlabel("n — количество орлов")
plt.ylabel(r"$P(X \geq n)$")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
