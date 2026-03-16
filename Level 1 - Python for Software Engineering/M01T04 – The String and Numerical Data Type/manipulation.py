str_manip  = input("Please enter a sentence")
print(len(str_manip)) # Prints length of sentence.

# Replacing last letter and other same letters with @.
last_letter = str_manip[-1]
print(last_letter)
str_replace = str_manip.replace(last_letter, "@")
print(str_replace)

# Prints the words last three characters backwards.
print(str_manip[-1:-4:-1])

# Takes first three and last two letters to form a new word.
new_word = str_manip[0:3] + str_manip[-2:]
print(new_word)