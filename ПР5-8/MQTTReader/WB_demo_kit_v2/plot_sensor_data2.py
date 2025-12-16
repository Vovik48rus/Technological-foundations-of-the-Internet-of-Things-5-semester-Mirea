import pandas as pd
import matplotlib.pyplot as plt
from WB_demo_kit_v2.SensorReading2 import SensorReading
import json
from rich.pretty import pprint

with open("../data-10-11-2025-ver2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

sensor_r_lst = [SensorReading.model_validate(d) for d in data]

df = pd.DataFrame([r.model_dump() for r in sensor_r_lst])

#  Преобразуем столбец времени в datetime
df["time"] = pd.to_datetime(df["time"])

#  Список метрик, где 0 считается недопустимым
metrics = ["illuminance", "voltage", "noise"]

#  Удаляем строки, где хотя бы одна из метрик равна 0
df_filtered = df[~(df[metrics] == 0).any(axis=1)]

#  Устанавливаем 'time' как индекс
df_filtered = df_filtered.set_index("time")

#  Ресемплинг с усреднением за каждые 2 секунды
# df_resampled = df_filtered.resample("2s").mean().reset_index()

#  Выводим примеры
pprint(df.head())
pprint(df_filtered.head())
# pprint(df_resampled.head())

#  Используем отфильтрованный DataFrame с временным индексом
df = df_filtered.copy()

#  Убедимся, что индекс действительно datetime
df.index = pd.to_datetime(df.index)

metrics = {
    "illuminance": "Освещённость (lux)",
    "voltage": "Напряжение (V)",
    "noise": "Шумность дБ"
}

for metric, label in metrics.items():
    plt.figure(figsize=(8, 5))

    # Строим гистограмму вручную, чтобы получить counts и bins
    counts, bins, patches = plt.hist(
        df[metric],
        bins=20,
        edgecolor="black",
        alpha=0.7
    )

    # Добавляем подписи над каждым столбцом
    for count, bin_left, bin_right in zip(counts, bins[:-1], bins[1:]):
        if count > 0:  # только если есть данные
            x = (bin_left + bin_right) / 2
            plt.text(
                x, count,               # координаты подписи
                f"{int(count)}",        # текст
                ha="center", va="bottom",
                fontsize=9, fontweight="bold"
            )

    plt.title(f"Распределение значений: {label}")
    plt.xlabel(label)
    plt.ylabel("Частота")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

for metric, label in zip(
        ["illuminance", "voltage", "noise"],
        ["Освещённость (lux)", "Напряжение (V)", "Шумность (дБ)"]
):
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df[metric], label=label, linewidth=1.5)
    plt.title(f"{label} во времени")
    plt.xlabel("Время")
    plt.ylabel("Значение")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

metrics_labels = {
    "illuminance": "Освещённость (lux)",
    "voltage": "Напряжение (V)",
    "noise": "Шумность дБ"
}

for metric, metric_label in metrics_labels.items():
    bins = 3
    counts, bin_edges = pd.cut(df[metric], bins=bins, retbins=True)
    grouped = counts.value_counts().sort_index()

    labels = [f"{round(bin_edges[i], 3)}–{round(bin_edges[i + 1], 3)}"
              for i in range(len(bin_edges) - 1)]

    plt.figure(figsize=(8, 8))

    wedges, texts, autotexts = plt.pie(
        grouped.values,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 11, 'weight': 'bold'}
    )

    for autotext in autotexts:
        autotext.set_color('white')

    plt.legend(wedges, labels, title="Диапазоны", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title(f"Распределение значений: {metric_label}", pad=20)
    plt.tight_layout()
    plt.show()
