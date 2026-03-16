def adding_up_to(number_list, index):
    # Base case
    if index < 0:
        return 0
    else:
        # Recursive case
        return number_list[index] + adding_up_to(number_list, index - 1)

my_list = [1, 2, 3, 4]
print(f"Your list total is {adding_up_to(my_list, 3)}")
