def largest_number(number_list):
    # Base case: if the list has only one element, return it
    if len(number_list) == 1:
        return number_list[0]

    # Recursive case: compare first element with the largest of the rest
    sub_max = largest_number(number_list[1:])
    return number_list[0] if number_list[0] > sub_max else sub_max

print(largest_number([3, 1, 99, 6]))