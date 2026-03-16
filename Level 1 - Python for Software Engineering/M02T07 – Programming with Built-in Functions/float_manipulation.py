import statistics as sta
import math as m 

# Creating a list of integers
number_input = input('Please input 10 numbers')
number_input = number_input.strip()
number_list = number_input.split(' ')
int_number = []
for number in number_list:
    int_number.append(float(number))
print(int_number)

# Adding these together
print(sum(int_number))

# Max and min index
max_index = int_number.index(max(int_number))
print(max_index)

min_index = int_number.index(min(int_number))
print(min_index)

# Mean and median of list
mean_list = round(sta.mean(int_number), 2)
print(mean_list)

print(sta.median(int_number))