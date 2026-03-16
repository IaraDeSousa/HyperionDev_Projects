import math

# User can choose to calculate a bond or an investment.
calculation_choice = input("Welcome to the finance calculator!\nInvestment - to calculate the amount of interest you'll earn on your investment!\n"
"Bond - to calculate the amount you'll have to pay on a home loan.\n"
"Enter either 'investment' or 'bond' from the menu above to proceed:")

# Making the input all lower case so it can be recognised by the if statement.
calculation_choice = calculation_choice.lower()

# If statement to decide which calculation will be performed.
if calculation_choice == 'bond':
   house_amount = int(input("What is the value of the house?"))
   interest_rate = int(input("What is the interest rate as a percentage number?"))
   month_amount = int(input("How many months do you plan to take to repay the bond?"))
   monthly_interest = (interest_rate/100)/12
   bond_repayment = (monthly_interest * house_amount)/(1 - (1 + monthly_interest)**(-month_amount))
   print(f"The total you will have to repay on your home loan each month is {round(bond_repayment, 2)}") # Rounding to two decimals.
elif calculation_choice == 'investment':
    deposit_amount = int(input("How much are you depositing?"))
    interest_rate = int(input("What is the interest rate as a percentage number?"))
    investment_years = int(input("How many years do you plan on investing?"))
    interest = input("Would you like to perform a simple or compound interest?")
    interest = interest.lower()

    # If statement within investment to determine if simple or compound interest calculation.
    if interest == 'simple':
        simple_interest = deposit_amount * (1 + (interest_rate/100) * investment_years)
        print(f"Your total earned with simple interest is {round(simple_interest, 2)}")
    elif interest == 'compound':
        compound_interest = deposit_amount * math.pow((1+(interest_rate/100)), investment_years)
        print(f"Your total earned with compound interest is {round(compound_interest, 2)}") 
    else: 
        print("Sorry, unable to proceed. Please type simple or compound.") # Program would need to be re-run for this.
else: 
    print("Unable to proceed. You must enter either investment or bond.") # Program would need to be re-run for this.