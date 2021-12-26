# What does the overall distribution look like when 
# just base it on the min, max function with randomness?
import random
import numpy as np

min = 19.3
max = 45.67

number_list = []
for i in range(1000):
    f = min + (max - min)*random.random()
    number_list.append(f)

sum_total = sum(number_list)
length_nl = len(number_list)

avg = sum_total/length_nl

perc50 = np.percentile(number_list, 50)
perc95 = np.percentile(number_list, 95)
perc99 = np.percentile(number_list, 99)

print(f'''
        Min: {min},
        Avg: {avg},
        Perc50: {perc50},
        Perc95: {perc95},
        Perc99: {perc99},
        Max: {max}
        ''')
