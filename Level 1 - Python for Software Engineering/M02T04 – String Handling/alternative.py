user_string = input("Please input a sentence")

# Creates a new string with alternating lower and upper case.
new_string = ''
for i in range(len(user_string)):
    if i % 2 == 0:
        new_string += user_string[i].upper()
    else:
        new_string += user_string[i].lower()
print(new_string)

# Creates a sentence with alternative lower and upper words.
user_list = user_string.split(' ')

upper_lower_list = []
for i, word in enumerate(user_list): # Enumerate uses tuples.
    if i % 2 == 0:
        upper_lower_list.append(word.lower()) # List formatting
    else: 
        upper_lower_list.append(word.upper())
new_word = ' '.join(upper_lower_list) # Joint formatting.
print(new_word)