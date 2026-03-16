while True:
    try:
        number_one = int(input("Please input one number"))
        number_two = int(input("Please input one number"))
        break
    except ValueError:
        print("You did not enter a number. Please try again.")

while True:
    operative = input("Please input an operative, such as +, -, * or /")
    if operative in ["+", "-", "*", "/"]:
        break
    else:
        print("You did not enter an operative. Please try again.")


if operative == "+":
    calculation = number_one + number_two
elif operative == "-":
    calculation = number_one - number_two
elif operative == "*":
    calculation = number_one * number_two
elif operative == "/":
    calculation = number_one / number_two


with open("equations.txt", "a+") as file: 
    file.write(f"{number_one} {operative} {number_two} = {calculation}" + "\n")

while True:
    try:
        view_equations = input("Would you like to view previously entered equations? yes/no")
        view_equations = view_equations.lower()
        if view_equations == "yes":
            file = open("equations.txt", "r")
            for line in file:
                print(line)
            break
        elif view_equations == "no":
            break
        else:
            print("You did not enter yes or no. Please try again.")
    except FileNotFoundError as error:
        print("The file you are trying to open does not exist.")
        break
