name = input("Think of a person.\nWhat is their name?")
age = int(input("What is their age?"))
hair_colour = input("What is their hair colour?")
eye_colour = input("What is their eye colour?")

# Creating a class
class Adult:

    # Constructor method
    def _init_(self, name, age, hair_colour, eye_colour):
        self.name = name
        self.age = age
        self.hair_colour = hair_colour
        self.eye_colour = eye_colour

    # Creating a method for being old enough to drive
    def can_drive(self):
        print(name, "is old enough to drive!")

class Child(Adult):

    # Creating override method that they are not old enough to drive
    def can_drive(self):
        print(name, "is NOT old enough to drive!")

if age >= 18:
    old_enough = Adult()
    old_enough.can_drive()
else:
    not_old_enough = Child()
    not_old_enough.can_drive()