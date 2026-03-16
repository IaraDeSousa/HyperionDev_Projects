number_list = []
number = 0

# Creating list of numbers, to continue until -1 is entered.
while True:
    number = int(input("Please enter a number"))
    if number == 0:
        print("0 is not a valid input, please try again")
    elif number == -1:
        break
    else:
        number_list.append(number)

# Adding numbers in the list together.
total_numbers = 0
for num in number_list:
    total_numbers = total_numbers + num

# Finding average of the numbers.
length_list = len(number_list)
average_numbers = total_numbers / length_list
print(average_numbers)