# counter for number of stars in each line.
counter = 0

# for loop to create each line of stars.
for i in range(1, 9):
    if i <= 5:
        counter += 1
        print('*' * counter)
    elif i > 5:
        counter -= 1
        print ('*' * counter)