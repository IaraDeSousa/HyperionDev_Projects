# This example program is meant to demonstrate errors.
 
# There are some errors in this program. Run the program, look at the error messages, and find and fix the errors.

print("Welcome to the error program") # Syntax
print("\n") # Syntax

    # Variables declaring the user's age, casting the str to an int, and printing the result
age_Str = "24" # Syntax and runtime.
print("I'm " + age_Str + " years old.")

    # Variables declaring additional years and printing the total years of age
years_from_now = "3" # Removed indentation.
total_years = int(age_Str) + int(years_from_now) # Runtime and syntax.

print("The total number of years: " + str(total_years)) # Runtime error.

# Variable to calculate the total number of months from the given number of years and printing the result
total_months = (total_years * 12) + 6 # Logic error.
print("In 3 years and 6 months, I'll be " + str(total_months) + " months old") # Runtime error.

#HINT, 330 months is the correct answer


