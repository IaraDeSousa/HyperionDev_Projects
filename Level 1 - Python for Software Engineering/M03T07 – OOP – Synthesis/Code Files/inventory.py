# This program is a shoe inventory. It allows you to add new shoes, view the current shoes, re-stock the lowest stock shoe, put the highest stock shoe on sale and see the value of a specific shoe's stock.


from tabulate import tabulate


# ========The beginning of the class==========
# This class defines the shoe list, allows you to get the cost and quantity of a specific shoe and print a specific shoe's details.

class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f'Shoe details: {self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}'


# =============Shoe list===========
# This creates the shoe list.
shoe_list: list[Shoe] = []


# =============File Path Defined===========
# This defines the file path for future use.
file_path = (
    "inventory.txt"
)


# ==========Functions to read shoe data==============
# The user must first read the shoe list to update or search it.
def read_shoes_data():
    shoe_list.clear()  # This is to avoid the shoe list being duplicated
    try:
        with open(file_path, 'r') as file:
            for index, line in enumerate(file):
                if index == 0:  # skip header
                    continue

                line = line.strip()
                country, code, product, cost, quantity = line.split(',')

                shoe = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoe)

        print("The shoes have successfully been read from the file")

    except FileNotFoundError:
        print("This file was not found, please try again")
    except ValueError:
        print("The list doesn't have all the components needed")
  

# =============Function to capture new shoe data===========
# This function allows the user to enter a new shoe into the shoe_list.
def capture_shoes():
    country = input("Please enter the shoe's country").strip()
    while True:
        code = input("Please enter the shoe's code").upper().strip()
        if any(shoe.code == code for shoe in shoe_list):
                print("This code already exists. Please type a unique code.")
        else:
            break  # Loop breaks after valid input.
    product = input("Please enter the product name").strip()
    while True:
        try:
            cost = float(input("Please enter the cost of the shoe").strip())
            break  # Loop breaks after valid input.
        except ValueError:
            print("Please only input a number")
    while True: 
        try:
            quantity = int(input("Please enter the quantity of the shoe").strip())
            break  # Loop breaks after valid input
        except ValueError:
            print("Please only input a number")
    shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(shoe)
    save_to_file()
    print("Your shoe has been successfully added!")


# =============Function to view all shoes===========
# This function allows the user to view a list of all the shoes.
def view_all():
    table_list = []
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]       # Printing headers for readability
    for shoe in shoe_list:
        shoe_component_list = [shoe.country, shoe.code,
                               shoe.product, shoe.cost, shoe.quantity]
        table_list.append(shoe_component_list)
    results_table = tabulate(table_list, headers=headers, colalign=("left", "left", "left", "right", "right"))
    print(results_table)


# =============Function to restock shoe with lowest stock===========
def re_stock():
    if not shoe_list:  # The user has to read_shoes prior to restocking.
        print("Please read the file first, no shoes found.")
        return
    
    lowest_quantity = min(shoe_list, key=lambda shoe: shoe.quantity)
    print(f"The shoe with the lowest quantity is the following:\n {lowest_quantity}")

    try:
        user_choice = int(input("""Would you like to update this shoe stock?
            1. Yes
            2. No
            Please enter your selection:"""
            )
        )
        if user_choice == 1:
            while True: 
                try:
                    add_quantity = int(input("Enter the quantity you'd like to restock:"))
                    lowest_quantity.quantity += add_quantity
                    save_to_file()
                    print("The stock has been updated successfully!")
                    break  # Successsful input so loop exits.
                except ValueError:
                    print("Please only input a number")
        elif user_choice == 2:
            print("Shoe stock not updated")
        else:
            print("Error - please enter a valid number")
    except ValueError:
        print("Error - please enter a valid number")  # This is to catch the ValueError if the user doesn't input a number 1 or 2.


# =============Function to search for a specific shoe by code===========
def search_shoe():
    if not shoe_list:  # The user has to read_shoes prior to searching for a shoe.
        print("Please read the file first, no shoes found.")
        return
    shoe_code = input("Please type the shoe code you would like to search by")
    shoe_code = shoe_code.upper().strip()
    for shoe in shoe_list:
        if shoe.code == shoe_code:
            print(shoe)
            return
    
    print("Shoe code not found.") # Error handling if shoe code is incorrect


# =============Function to calculate the value per shoe item===========
def value_per_item():
    if not shoe_list:  # The user has to read_shoes prior to accessing the shoes value.
        print("Please read the file first, no shoes found.")
        return
    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity
        print(f"The stock value for {shoe.product} ({shoe.code}) is £{value:.2f}")
    

# =============Function to put the shoe with the highest stock on sale===========
def highest_qty():
    if not shoe_list:  # The user has to read_shoes prior to restocking.
        print("Please read the file first, no shoes found.")
        return
    highest_quantity = max(shoe_list, key=lambda shoe: shoe.quantity)
    print(f"{highest_quantity}\nThis shoe is now on sale!")


# ==========Save to File Function=============
# This function allows any changes made to be save to file so that upon reopening the file, the changes have been saved.
def save_to_file():
    with open(file_path, 'w') as file:  # This will open the file ready for writing.
        file.write("Country,Code,Product,Cost,Quantity\n")  # Creates the header
        for shoe in shoe_list:
            file.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost:.2f},{shoe.quantity}\n")  # Writes each shoe into the shoe list including any updates and new shoes.


# ==========Main Menu=============
# This menu allows the user to choose what they would like to do in the Shoe Inventory program.
def menu():
    while True:
        print("\n\n\n----Shoe Inventory Menu----\nType the number for what you would like to do!")
        print("1. Read all the shoe data from the file")
        print("2. Add a new shoe to the list")
        print("3. View all shoes")
        print("4. Find the lowest stock shoe and restock this")
        print("5. Search for a specific shoe via the shoe code")
        print("6. Calculate the value of each shoe's stock")
        print("7. Find the shoe with the highest stock and put this on sale!")
        print("0. Exit the application")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            read_shoes_data()

        elif choice == "2":
            capture_shoes()

        elif choice == "3":
            view_all()

        elif choice == "4":
            re_stock()

        elif choice == "5":
            search_shoe()

        elif choice == "6":
            value_per_item()

        elif choice == "7":
            highest_qty()

        elif choice == "0":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Error: Please enter a number from 0 to 7.")

# Calling menu function to boot up the application
menu()