list = [27, -3, 4, 5, 35, 2, 1, -40, 7, 18, 9, -1, 16, 100]
# A Linear search is the most appropriate as it is an unsorted array.


def search(array, item):
    for i in range(0, len(array)):
        if (array[i] == item):
            return i
    return None


index_search = search(list, 9)
print(index_search)
# It has a good time complexity of O(n), especially as we know the size of the array.


# Insertion Sort
def sort(array):
    n = len(array)  # Get length of array - 1

    for i in range(1, n):
        j = i
        # when index is larger than 0 and previous value is bigger than 
        # the current value.
        while j > 0 and array[j-1] > array[j]: 
            current = array[j]
            previous = array[j-1]
            array[j] = previous 
            array[j-1] = current  # then you swap the two positions!
            j = j - 1  # the new index will be the previous position.

sort(list)
print(list)


# Binary Search algorithm
# You'd use this algorithm when you have a sorted list such as race numbers.
def binary_search(array, target):
    left = 0
    right = len(array) - 1

    while (left <= right):
        mid = (right + left) // 2

        if array[mid] == target:
            return mid
        elif array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

target_index = binary_search(list, 9)
print(target_index)