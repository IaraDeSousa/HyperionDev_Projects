# This is a book inventory application which allows users to add books, update books, delete books and search for books via the book ID

# Import the sqlite3 library to interact with SQLite databases
import sqlite3

# Establish connection or create a SQLite database file
bookstore_db = 'ebookstore_db.db'  # Store the database name in a variable for easier reference

# ---- Creating book table function ----
# This function creates the book table if it does not already exist and inserts multiple books into the table.
def create_book_table():
    with sqlite3.connect(bookstore_db) as db:
        cursor = db.cursor()  # Get a cursor object to interact with the database

        # Creating the ebookstore table if it does not already exist
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT,
                authorID INTEGER,
                qty INTEGER
            )
            '''
        )

        # Define data for existing books
        book_data = [
            (3001, 'A Tale of Two Cities', 1290, 30),
            (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 2356, 25),
            (3004, 'The Lord of the Rings', 6380, 37),
            (3005, "Alice's Adventures in Wonderland", 5620, 12)
        ]

        # Inserting multiple books into the table
        cursor.executemany(
            '''
            INSERT OR IGNORE INTO book(id, title, authorID, qty)
            VALUES(?, ?, ?, ?)
            ''',
            book_data
        )  # Using INSERT OR IGNORE to avoid duplicate entries if the script is run multiple times
        print('Multiple books inserted.\n')

        db.commit()  # Committing the changes to save the table creation


# ---- Creating author table function ----
# This function creates the author table if it does not already exist and inserts multiple authors into the table.
def create_author_table():
    with sqlite3.connect(bookstore_db) as db:
        cursor = db.cursor()  # Get a cursor object to interact with the database

        # Creating the author table if it does not already exist
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS author (
                id INTEGER PRIMARY KEY,
                name TEXT,
                country TEXT
            )
            '''
        )

        # Define data for existing authors
        authors = [
                    (1290, 'Charles Dickens', 'England'),
                    (8937, 'J.K. Rowling', 'England'),
                    (2356, 'C.S. Lewis', 'Ireland'),
                    (6380, 'J.R.R. Tolkien', 'South Africa'),
                    (5620, 'Lewis Carroll', 'England')
                ]

        # Inserting multiple authors into the author table
        cursor.executemany(
            '''
            INSERT OR IGNORE INTO author(id, name, country)
            VALUES(?, ?, ?)
            ''',
            authors
        )  # Using INSERT OR IGNORE to avoid duplicate entries if the script is run multiple times
        print('Multiple authors inserted.\n')

        db.commit()  # Committing the changes to save the table creation


# ---- New book function ----
# This function allows users to add new books to the book database by asking the user to enter the book's ID, title, authorID, and quantity.
def new_book():
    try:
        book_id = book_id_validation()
        title = input("Enter the book's title: ")
        authorID = author_id_validation()
        qty = int(input("Enter the quantity of books: "))

        with sqlite3.connect(bookstore_db) as db:
            cursor = db.cursor()
            sql = "INSERT INTO book (id, title, authorID, qty) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (book_id, title, authorID, qty))
            db.commit()
            print(f"Book '{title}' by author ID {authorID} has been successfully added!")
    except ValueError:
        print("Error: Invalid input. Quantity must be a number. Exiting new book function.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


# ---- Update book information function ----
# This function will default to updating the book quantity, but users can also update the book title and authorID.
def update_book():
    try:
        book_id = book_id_validation()
        check_information(book_id)  # Show the user the current details of the book before they update it.
        with sqlite3.connect(bookstore_db) as db:
            print("\nThe default update action is to update the book's quantity.")  # This is the default action as per requirements.
            print("To update Title or AuthorID instead, type 's' and press enter.")
            user_input = input("Enter new quantity (or 's' to switch): ").lower()
            cursor = db.cursor()
            if user_input == 's':  # Present the user with two other options.
                print("1. Title")
                print("2. Author ID")
                choice = input("Select field (1 or 2): ")

                if choice == "1":
                    new_title = input("Enter new title: ")
                    cursor.execute("UPDATE book SET title = ? WHERE id = ?", (new_title, book_id))
                    print(f"Title updated to '{new_title}'.")
                elif choice == "2":
                    new_author = author_id_validation()
                    cursor.execute("UPDATE book SET authorID = ? WHERE id = ?", (new_author, book_id))
                    print(f"Author ID updated to {new_author}.")
                else:
                    print("Invalid input. Exiting update book function.")
                    return
            else:
                # Execute the default: Quantity update
                new_qty = int(user_input)
                cursor.execute("UPDATE book SET qty = ? WHERE id = ?", (new_qty, book_id))
                print(f"Quantity updated to {new_qty}.")

            db.commit()  # Committing the changes to save the updated data

    except ValueError:
        print("Invalid input. Exiting update book function.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")    


# ---- Delete book by bookID function ----
# This function allows users to delete a book from the database by entering the book's ID.
def delete_book():
    try:
        book_id = book_id_validation()
        with sqlite3.connect(bookstore_db) as db:
            cursor = db.cursor()
            sql = "DELETE FROM book WHERE id = ?"
            cursor.execute(sql, (book_id,))
            db.commit()
            print(f"Book {book_id} has been successfully deleted!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except ValueError:
        print("Error: Invalid input. Exiting delete function.") 


# ---- Search book by bookID function ----
# This function allows users to search for a book by its ID and will return the book's title, authorID and quantity if found.
def search_book_by_id():
    try:
        book_id = book_id_validation()
        with sqlite3.connect(bookstore_db) as db:
            cursor = db.cursor()
            sql = "SELECT * FROM book WHERE id = ?"
            cursor.execute(sql, (book_id,))
            result = cursor.fetchone()
            if result:
                print(f"Book found under ID {result[0]}.\nTitle: {result[1]}, Author ID: {result[2]}, Quantity: {result[3]}")
            else:
                print("No book found with that ID.")

    except ValueError:
        print("Invalid input for book ID. Exiting search book function.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")


# ---- View all books function ----
# This function allows users to view the details of all books in the database, including the book's ID, title, author, authorI, country and quantity.
def view_all_books():
    try:
        with sqlite3.connect(bookstore_db) as db:
            cursor = db.cursor()
            query = '''
                SELECT book.title, author.name, author.country 
                FROM book
                INNER JOIN author ON book.authorID = author.id
            '''
            cursor.execute(query)
            rows = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

    labels = ["Title", "Author's Name", "Author's Country"]

    print("\nDetails")

    for row in rows:
        # zip() pairs each label with the corresponding row.
        for label, value in zip(labels, row):
            print(f"{label}: {value}")  # Prints each book in a user-friendly manner
        
        print("-" * 52)


# ---- Check author and country book information function ----
# This function allows users to check the current author and country information for a specific book before they update it, and then choose whether to update the author, country or neither.
def check_information(book_id: int):
    try:
        with sqlite3.connect(bookstore_db) as db:
            cursor = db.cursor()
            query = '''
                        SELECT author.name, author.country
                        FROM author
                        INNER JOIN book ON author.id = book.authorID
                        WHERE book.id = ?
                    '''
            cursor.execute(query, (book_id,))
            result = cursor.fetchone()
            if result:
                name, country = result
                print(f"\nFor Book ID {book_id}:")
                print(f"Author: {name}")
                print(f"Country: {country}")
                correct_information = int(input("Are the author and country correct for the book you want to update?\nType 1 for yes, Type 2 to update author, Type 3 to update country: "))
                if correct_information == 1:
                    return
                elif correct_information == 2:
                    new_author = input("Please enter the correct author's name: ")
                    query = ''' UPDATE author SET name = ? WHERE id = (SELECT authorID FROM book WHERE id = ?) '''
                    cursor.execute(query, (new_author, book_id))
                    db.commit()
                    print(f"Author name has been updated to {new_author}.")
                elif correct_information == 3:
                    new_country = input("Please enter the correct country: ")
                    query = ''' UPDATE author SET country = ? WHERE id = (SELECT authorID FROM book WHERE id = ?) '''
                    cursor.execute(query, (new_country, book_id))
                    db.commit()
                    print(f"Country has been updated to {new_country}.")
            else:
                print(f"No book found with ID {book_id}.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


# ---- Book ID validation function ----
# This function validates that the user input for book ID is a 4-digit number.
def book_id_validation():
    while True:
        try:
            book_id = int(input("Enter the book's ID: "))
            if (len(str(book_id)) < 4 or len(str(book_id)) > 4):
                print("Error: Book ID must be a 4-digit number. Please try again.")
            else:
                return book_id
        except ValueError:
            print("Error: Invalid input. Book ID must be a 4-digit number. Please try again.")
    

# ---- Author ID validation function ----
# This function validates that the user input for author ID is a 4-digit number.
def author_id_validation():
    while True:
        try:
            author_id = int(input("Enter the authors's ID: "))
            if (len(str(author_id)) < 4 or len(str(author_id)) > 4):
                print("Error: Author ID must be a 4-digit number. Please try again.")
            else:
                return author_id
        except ValueError:
            print("Error: Invalid input. Author ID must be a 4-digit number. Please try again.")
    

# Initialising the databases and two tables.
create_book_table()
create_author_table()

# Welcome message to the user when running the application
print('Welcome to your book inventory!')


# ---- Main Menu ----
# The menu options will keep showing until the user exits the application.
# The user can choose to add new books, update existing books, delete books, search for books by ID, or quit the application.
while True:
    try:
        user_choice = int(
            input(
                '''What would you like to do today? Please choose one of the following options:\n
            1. Add new books to the database?\n
            2. Update a book's information?\n
            3. Delete books from the database?\n
            4. Search the database to find a specific book?\n
            5. View details of all books in the database?\n
            0. Quit the application\n

            Enter selection as a number:'''
            )
        )

        if user_choice == 1:
            new_book()
        elif user_choice == 2:
            update_book()
        elif user_choice == 3:
            delete_book()
        elif user_choice == 4:
            search_book_by_id()
        elif user_choice == 5:
            view_all_books()
        elif user_choice == 0:
            print("Thank you for using the book inventory application, goodbye!")
            exit()
        else:
        print("Error: Please choose one of the five options.")
    except ValueError:
        print("Error: Invalid input. Please enter a number corresponding to the menu options.") 