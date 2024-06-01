import numpy as np
from datetime import datetime


file_path = './VHI/household_power_consumption.txt'

dtype = [('Date', 'U12'), ('Time', 'U12'),('Global_active_power', 'float'), ('Global_reactive_power', 'float'), ('Voltage', 'float'), ('Global_intensity', 'float'), ('Sub_metering_1', 'float'),
         ('Sub_metering_2', 'float'), ('Sub_metering_3', 'float')]

data_str = np.genfromtxt(file_path, delimiter=';', names=True, dtype=dtype)

# 1. Відібрати домогосподарства, де загальне споживання електроенергії перевищує 5 кВт.
domestic_consumers = data_str[(data_str['Sub_metering_1'] + data_str['Sub_metering_2'] + data_str['Sub_metering_3']) > 5]

# 2. Обрати всі домогосподарства, у яких вольтаж перевищую 235 В.
domestic_consumers_voltage = data_str[data_str['Voltage'] > 235] 
# 3. Виберіть домогосподарства, де струм становить від 19 до 20 А, і де пральна машина і холодильник споживають більше, ніж котел і кондиціонер.
domestic_consumers_current = data_str[(data_str['Global_intensity'] >= 19) & 
                                      (data_str['Global_intensity'] <= 20) &
                                      (data_str['Sub_metering_1'] > data_str['Sub_metering_2']) &
                                      (data_str['Sub_metering_2'] > data_str['Sub_metering_3'])]
# 4. Випадковим чином відберіть 500000 домогосподарств і обчисліть середнє споживання для кожної субгрупи обліку.
random_indices = np.random.choice(len(data_str), size=min(500000, len(data_str)), replace=False)
random_sample = data_str[random_indices]

average_sub_metering_1 = np.nanmean(random_sample['Sub_metering_1'])
average_sub_metering_2 = np.nanmean(random_sample['Sub_metering_2'])
average_sub_metering_3 = np.nanmean(random_sample['Sub_metering_3'])

# 5 Відібрати домогосподарства, які споживають більше 6 кВт на хвилину в середньому після 18:00, і серед них ті, у яких основне споживання електроенергії в цей період припадає на пральну машину, сушарку, холодильник та освітлення (група 2 є найбільшою)
times = np.array([datetime.strptime(time_str, '%H:%M:%S') for time_str in data_str['Time']])

data_with_time = np.array([(date, time, g_active, g_reactive, voltage, g_intensity, sub_1, sub_2, sub_3)
                           for (date, time, g_active, g_reactive, voltage, g_intensity, sub_1, sub_2, sub_3), time_str in zip(data_str, times)],
                          dtype=dtype)
times = np.array(times)  # Перетворення списку часових рядків у нерозбірливий масив об'єктів datetime
above_six_kw = data_with_time[(times >= datetime.strptime('18:00:00', '%H:%M:%S')) & 
                               ((data_with_time['Sub_metering_1'] + data_with_time['Sub_metering_2'] +
                                 data_with_time['Sub_metering_3']) > 6)]
# 6. Виберіть кожен третій результат з першої половини і кожен четвертий результат з другої половини.
first_half = above_six_kw[:len(above_six_kw)//2:3]
second_half = above_six_kw[len(above_six_kw)//2::4]

print("Households with electricity consumption exceeding 5 kW:")
print(domestic_consumers)
print("\nHouseholds with voltage exceeding 235 V:")
print(domestic_consumers_voltage)  
print("\nHouseholds with current between 19-20 A, where washing machine and refrigerator consume more than boiler and air conditioner:")
print(domestic_consumers_current)

print("\nAverage electricity consumption for Sub_metering_1:", average_sub_metering_1)
print("Average electricity consumption for Sub_metering_2:", average_sub_metering_2)
print("Average electricity consumption for Sub_metering_3:", average_sub_metering_3)
print("\nHouseholds consuming more than 6 kW per minute on average after 18:00:" , above_six_kw)

print("\nHouseholds with main electricity consumption attributed to specific appliances after 18:00:")
print(above_six_kw)
print("\nEvery third result from the first half:")
print(first_half)
print("\nEvery fourth result from the second half:")
print(second_half)

