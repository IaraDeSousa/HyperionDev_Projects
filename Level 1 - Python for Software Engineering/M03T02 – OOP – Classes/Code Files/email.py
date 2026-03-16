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


class Email:
    def __init__(self, address, subject, content):
        self.address = address
        self.subject = subject
        self.content = content
        self.has_read = False


# Initialise the instance variables for each email.

# Create the 'mark_as_read()' method to change the 'has_been_read'
# instance variable for a specific object from False to True.


    def mark_as_read(self):
        self.has_read = True

# --- Functions --- #
# Build out the required functions for your program.


def populate_inbox():
    email = Email("10 Avenue", "House Letter", "Dear John...")
    emailSecond = Email("15 Avenue", "Deliveroo Order", "Dear John...")
    emailThird = Email("25 Avenue", "Bank details", "Dear John...")
    inbox.append(email)
    inbox.append(emailSecond)
    inbox.append(emailThird)

    # Create 3 sample emails and add them to the inbox list.


def list_emails():
    # Create a function that prints each email's subject line
    # alongside its corresponding index number,
    # regardless of whether the email has been read.
    for index, email in enumerate(inbox):
        print(index, email.subject)


def read_email(index):
    # Create a function that displays the email_address, subject_line,
    # and email_content attributes for the selected email.
    # After displaying these details, use the 'mark_as_read()' method
    # to set its 'has_been_read' instance variable to True.
    inbox[index].mark_as_read()


def view_unread_emails():
    # Create a function that displays all unread Email object subject lines
    # along with their corresponding index numbers.
    # The list of displayed emails should update as emails are read.
    for index, email in enumerate(inbox):
        if (not email.has_read):
            print(index, email.subject)


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
        email_selection_index = int(
            input( """\n Please select an index: """  )
        )
        try:
            read_email(email_selection_index)
            print("\n", inbox[email_selection_index].address, "\n",
                inbox[email_selection_index].subject, "\n", inbox[email_selection_index].content + "\n")
        except IndexError:
            print("\n Email not valid!")

    elif user_choice == 2:
        view_unread_emails()

    elif user_choice == 3:
        break

    else:
        print("Oops - incorrect input.")
