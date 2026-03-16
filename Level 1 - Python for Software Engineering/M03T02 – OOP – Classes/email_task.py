"""
Starting template for creating an email simulator program using
classes, methods, and functions.

This template provides a foundational structure to develop your own
email simulator. It includes placeholder functions and conditional statements
with 'pass' statements to prevent crashes due to missing logic.
Replace these 'pass' statements with your implementation once you've added
the required functionality to each conditional statement and function.

Note: Throughout the code, update comments to reflect the changes and logic
you implement for each function and method.
"""

# --- OOP Email Simulator --- #

# --- Email Class --- #
# Create the class, constructor and methods to create a new Email object.

class Email():

# Initialise the instance variables for each email.
    has_been_read = False # Defaults to being not read initially.

    def __init__ (self, email_address, subject_line, email_content):
        self.email_address = email_address
        self.subject_line = subject_line
        self.email_content = email_content

# Create the 'mark_as_read()' method to change the 'has_been_read'
# instance variable for a specific object from False to True.
    def mark_as_read(self):
        self.has_been_read = True        
            
   
# --- Functions --- #
# Build out the required functions for your program.


# Create 3 sample emails and add them to the inbox list.
sale = Email("sales@gmail.com", "Get half price off!", "Click this link to see the deals!")
booking = Email("perubooking@outlook.com", "Booking confirmed", "You're going to the Rainforest!")
package = Email("vinted@google.co.uk", "Parcel is on the way", "Your new top will arrive between 3-5pm")

def populate_inbox(): 
    inbox.append(sale)
    inbox.append(booking)
    inbox.append(package)


 # Create a function that prints each email's subject line
    # alongside its corresponding index number,
    # regardless of whether the email has been read.
def list_emails():
    for i, email in enumerate(inbox):
        print(i, email.subject_line, "\n")       


# Create a function that displays the email_address, subject_line,
    # and email_content attributes for the selected email.
    # After displaying these details, use the 'mark_as_read()' method
    # to set its 'has_been_read' instance variable to True.
def read_email(i: int):
    print(inbox[i].email_address)
    print(inbox[i].subject_line)
    print(inbox[i].email_content)
    inbox[i].mark_as_read()
    print(f"Your email from {inbox[i].email_address} has now been marked as read!")
   
    # Create a function that displays all unread Email object subject lines
    # along with their corresponding index numbers.
    # The list of displayed emails should update as emails are read.    
def view_unread_emails():
    for i, email in enumerate(inbox):
        if email.has_been_read == False:
            print(i, email.subject_line, "\n")

# --- Lists --- #
# Initialise an empty list outside the class to store the email objects.

inbox: list[Email] = []

# --- Email Program --- #

# Call the function to populate the inbox for further use in your program.

populate_inbox()

# Fill in the logic for the various menu operations.
# Display the menu options for each iteration of the loop.
while True:
    user_choice = int(
        input(
            """\nWould you like to:
    1. Read an email
    2. View unread emails
    3. Quit application

    Enter selection: """
        )
    )

    if user_choice == 1:
        i = int(input("What email would you like to read? Please only enter a number."))
        read_email(i)
    elif user_choice == 2:
        print("Here are all your emails!")
        view_unread_emails()
    elif user_choice == 3:
        print("Goodbye! :)")
        break
    else:
        print("Oops - incorrect input.")
