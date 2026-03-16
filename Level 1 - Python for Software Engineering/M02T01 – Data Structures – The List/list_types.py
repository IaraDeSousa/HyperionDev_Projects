friends_names = ['Nesta', 'Aaliyah', 'Ben']
print(friends_names[0]) # prints first name
print(friends_names[-1]) # prints last name

friends_ages = [25, 24, 26]

# for loop for going through the list friends_names
# if statement to add friends' ages if it equals the corresponding name
for name in friends_names:
    if name == 'Nesta': 
        print(f"{name} is {friends_ages[0]} years old")
    elif name == 'Aaliyah':
        print(f"{name} is {friends_ages[1]} years old")
    else:
        print(f"{name} is {friends_ages[2]} years old")
