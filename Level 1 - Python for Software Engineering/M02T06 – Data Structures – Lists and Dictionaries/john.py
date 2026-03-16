name_list = []
name = ''

while name != 'john':
    name = str(input("Enter your name: "))
    name = name.lower()
    name_list.append(name)

del name_list[-1]
print("Incorrect names: " + str(name_list))
