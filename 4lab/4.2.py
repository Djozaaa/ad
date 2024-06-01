import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from scipy.stats import pearsonr, spearmanr

# Шлях до файлу даних
file_path = './adult/adult.data'

# Завантаження даних у DataFrame
data_df = pd.read_csv(file_path, delimiter=', ',  dayfirst=True, na_values='?')

print(data_df)
def normalize(data):
    if data.dtype == 'object':
        print("Column contains non-numeric values and cannot be normalized.")
        return data
    else:
        normalized_data = (data - data.min()) / (data.max() - data.min())
        return normalized_data

# Стандартизація
def standardize(data):
    standardized_data = (data - data.mean()) / data.std()
    return standardized_data

# Вибір атрибутів для графіка
attribute1 = 'age'
attribute2 = 'hours-per-week'

print(data_df.columns)

# Перевірка наявності вибраних атрибутів у даних
if attribute1 not in data_df.columns or attribute2 not in data_df.columns:
    print("One or more selected attributes are not present in the dataset.")
    exit()

# Нормалізація та стандартизація вибраних атрибутів
normalized_attribute1 = normalize(data_df[attribute1])
standardized_attribute2 = standardize(data_df[attribute2])

# Побудова графіка
plt.figure(figsize=(8, 6))
plt.scatter(normalized_attribute1, standardized_attribute2, alpha=0.5)
plt.title('Dependency of {} on {}'.format(attribute2, attribute1))
plt.xlabel('Normalized {}'.format(attribute1))
plt.ylabel('Standardized {}'.format(attribute2))
plt.grid(True)
plt.show()

# Обчислення коефіцієнтів кореляції
pearson_corr, _ = pearsonr(data_df[attribute1], data_df[attribute2])
spearman_corr, _ = spearmanr(data_df[attribute1], data_df[attribute2])
print("Pearson correlation coefficient between {} and {}: {:.2f}".format(attribute1, attribute2, pearson_corr))
print("Spearman correlation coefficient between {} and {}: {:.2f}".format(attribute1, attribute2, spearman_corr))

# One Hot Encoding
categorical_attribute = 'workclass'
one_hot_encoder = OneHotEncoder()
one_hot_encoded = one_hot_encoder.fit_transform(data_df[[categorical_attribute]])
print("One Hot Encoded {}: \n{}".format(categorical_attribute, one_hot_encoded))

# Візуалізація попарних зв'язків між числовими атрибутами
sns.pairplot(data_df)
plt.show()
