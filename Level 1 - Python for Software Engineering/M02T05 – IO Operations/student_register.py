student_number = input('How many students are registering today?')
if student_number.isdigit():
    with open("reg_form.txt", "a+") as file: 
        for student in (range(int(student_number))): 
                ID_number = input("What is the student ID?")
                file.write(str(ID_number) + '\n\n\n' + '.........................' + '\n')
else:
    print('Please only enter a number!')
