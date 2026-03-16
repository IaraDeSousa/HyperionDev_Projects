birthdate = ''
names = ''

with open("DOB.txt", "r") as file:
    for line in file: 
        line = line.replace("\n", "")
        for i in range(len(line)): 
            if  line[i].isdigit():
                birthdate += line[i:] + '\n'
                names += line[:i] + '\n'
                break

print('Name' + '\n' + names + '\n\n')
print('Birthdate' '\n' + birthdate)      