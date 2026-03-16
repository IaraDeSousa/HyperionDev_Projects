# Task manager program allowing users to add, view and edit their tasks.
# This program also allows the admin user to register new users, view all
# tasks, view completed tasks, delete tasks, and generate reports on task and
# user statistics.


# ===== Importing external modules ===========
import datetime  # module for formatting dates of tasks
from tabulate import tabulate  # module for formatting tables of tasks and
# statistics


# Creating the task class
# This defines the task class with all the components needed to create a task
class Task:
    def __init__(
            self,
            username,
            task_title,
            task_description,
            entry_date,
            due_date,
            is_complete
    ):
        self.username = username
        self.task_title = task_title
        self.task_description = task_description
        self.entry_date = entry_date
        self.due_date = due_date
        self.is_complete = is_complete


# Task list
# This creates the task list to store all the tasks created within the program.
task_list: list[Task] = []


# Creating the log-in class
# This defines the log-in class with the components needed to create a user for
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


# Username list
# This creates the username list to store the users created within the program.
user_list: list[User] = []


# File Paths Defined
# This defines the file paths for the task file, task overview report,
# user overview report, task tracker, user tracker, and login file for use in
# the program.
task_file_path = (
    "tasks.txt")

task_overview_path = (
    "task_overview.txt")

user_overview_path = (
    "user_overview.txt")

task_tracker_path = (
    "task_tracker.txt")

user_tracker_path = (
    "user_tracker.txt")

login_file_path = (
    "user.txt")


# ==== Reading the login data ====
# Necessary for user to enter username and password.
def read_login_data():
    user_list.clear()  # Avoid duplicating the login list
    try:
        with open(login_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                username, password = line.split(', ')

                login = User(username, password)
                user_list.append(login)

    except FileNotFoundError:
        print("This file was not found, please try again")
    except ValueError:
        print("The login list doesn't have all the components needed")


# ==== Reading the task data ====
# Necessary for user to view and edit tasks in tasks.txt.
def read_task_data():
    task_list.clear()  # Avoid duplicating the task list
    try:
        with open(task_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                (username, task_title, task_description,
                 entry_date, due_date, is_complete) = line.split(', ')

                task = Task(username, task_title, task_description,
                            entry_date, due_date, is_complete)
                task_list.append(task)

    except FileNotFoundError:
        print("This file was not found, please try again")
    except ValueError:
        print("The task list doesn't have all the components needed")


# ==== Login Section ====
# Login function allowing user to login with correct username and
# password.
def login():
    is_logged_in = False
    while not is_logged_in:
        username = input(
            "Please enter your username to login first: ").strip()
        found_user = None
        for user in user_list:
            if user.username == username:
                found_user = user
                break  # Breaks after correct username found.

        if found_user is None:
            print(
                "Incorrect username. Please try entering your "
                "username again."
            )
            continue
        while not is_logged_in:
            password = input("Please enter your password: ").strip()

            if found_user.password == password:
                # Break while loop and take user back to main menu
                is_logged_in = True
                print("You have successfully logged in!")
                return found_user
            print("Incorrect password. Please try again.")


# ==========Save to Task File Function=============
# Saves changes to the task file for persistence across sessions.
def save_to_file():
    # This will open the file ready for writing.
    with open(task_file_path, 'w') as file:
        for task in task_list:
            # Write each task with updates
            file.write(
                f"{task.username}, {task.task_title}, "
                f"{task.task_description}, {task.entry_date}, "
                f"{task.due_date}, {task.is_complete}\n")


# ==========Increment Tracker Function=============
# Tracks number of tasks added for statistical calculations.
def increment_tracker(filepath: str):
    try:
        with open(filepath, 'r') as file:
            content = file.read().strip()
            number = int(content) if content else 0
    except FileNotFoundError:
        number = 0
    except ValueError:
        print("Value error exception: Number in file is invalid")
        return

    number += 1

    with open(filepath, 'w') as file:
        file.write(str(number))


# ==== New User Function====
# Defines new user by asking for username and password.
def reg_user():
    while True:
        new_username = input("Please enter a new username: ").strip()
        if any(user.username == new_username for user in user_list):
            print('This username already exists. Please try again')
            continue
        else:
            break
    new_password = input("Please enter a new password: ")
    password_match = False
    while not password_match:
        confirm_password = input("Please confirm your new password: ")
        if new_password != confirm_password:
            print("Please ensure that your passwords match!")
        else:
            password_match = True

    with open(login_file_path, 'a') as file:
        file.write(f"\n{new_username}, {new_password}")

    increment_tracker(user_tracker_path)


# ==== Capturing Task ====
# Defines a new task with username, title, description, dates,
# and completion status.
def add_task():
    while True:
        username = input(
            "Please enter the username").strip().lower()
        if any(user.username == username for user in user_list):
            break  # Loop breaks after valid input.
        else:
            print("Please enter a valid username.")

    task_title = input(
        "Please enter the task title").strip()
    task_description = input(
        "Please enter the task description").strip()

    todays_date = datetime.datetime.now()
    entry_date = todays_date.strftime("%d %b %Y")

    due_date = create_date_input()
    is_complete = "No"

    task = Task(
        username, task_title, task_description,
        entry_date, due_date, is_complete
    )

    task_list.append(task)
    save_to_file()
    increment_tracker(task_tracker_path)  # Update tracker
    print("Your task has been successfully added!")


# ==== View all tasks function ====
# View all tasks currently within tasks.txt.
def view_all():
    table_list = []
    headers = ["Username", "Task Title", "Task Description",
               "Entry Date", "Due Date", "Completed?"]
    # Headers for readability
    for task in task_list:
        task_component_list = [
            task.username, task.task_title,
            task.task_description, task.entry_date,
            task.due_date, task.is_complete]
        table_list.append(task_component_list)
    # Column width for readability
    results_table = tabulate(
        table_list, headers=headers,
        colalign=("left", "left", "left", "right", "right",
                  "left"),
        tablefmt='grid', maxcolwidths=[None, 15, 30])
    print(results_table)


# ==== Valid task function ====
# This functions checks that the task number entered by the user in the view_mine function is valid and within bounds of the task list.
def get_valid_task_number(valid_indices):
    try:
        task_number = int(
            input(
                "Please enter the task number to complete or edit the due date"
                " or who it is assigned to, or -1 to return back to the main "
                "menu: "))
        if task_number == -1:
            return -1  # Return -1 to indicate exit 
        
        # Base case: a valid number is entered.
        if task_number in valid_indices:
            return task_number

        print("Invalid task number. That task isn't assigned to you.")
        return get_valid_task_number(valid_indices)  # Recursion

    except ValueError:
        print("Invalid input. Please enter a whole number.")
        return get_valid_task_number(valid_indices)  # Recursion


# ==== View my tasks function ====
# View tasks assigned to the logged in user.
def view_mine(logged_in_user: User):
    table_list = []
    user_task_indices = []  # List to store indices of tasks assigned to the user

    for index, task in enumerate(task_list):
        if task.username == logged_in_user.username:
            user_task_indices.append(index)  # Store the index of the task
            task_component_list = [
                index, task.username, task.task_title,
                task.task_description, task.entry_date,
                task.due_date, task.is_complete]
            table_list.append(task_component_list)

    if not table_list:
        print("This user does not have any tasks assigned to them!")

    headers = ["Index", "Username", "Task Title",
               "Task Description", "Entry Date", "Due Date",
               "Completed?"]  # Headers for readability
    results_table = tabulate(
        table_list, headers=headers,
        tablefmt='grid', maxcolwidths=[None, None, 15, 30])
    print(results_table)

    task_number = get_valid_task_number(user_task_indices)  # Allow user to select a task to edit or complete

    if task_number == -1:
        return  # Exit back to main menu if -1 is returned
    
    task_type = int(input(
        "Type 1 to complete, Type 2 to edit: "))
    
    if task_type == 1:
        task_list[task_number].is_complete = 'Yes'
    elif task_type == 2:
        if task_list[task_number].is_complete == 'Yes':
            print(
                "A completed task cannot be edited. "
                "Returning to main menu...")
            return
        else:
            edit_type = int(
                input(
                    "Type 1 to edit username, "
                    "Type 2 to edit due date: ").strip())
            if edit_type == 1:
                username = input(
                    "Please enter the new username: ")
                task_list[task_number].username = username
                save_to_file()
            elif edit_type == 2:
                due_date = create_date_input()
                task_list[task_number].due_date = due_date
                save_to_file()
            print("Task successfully updated!")

    save_to_file()  # Save any changes to the task file


# ==== View completed tasks function ====
# Allows the user to view which tasks have been completed.
def view_completed():
    table_list = []
    headers = ["Index", "Username", "Task Title",
               "Task Description", "Entry Date", "Due Date",
               "Completed?"]  # Headers for readability
    for index, task in enumerate(task_list):
        if task.is_complete == 'Yes':
            task_component_list = [
                index, task.username, task.task_title,
                task.task_description, task.entry_date,
                task.due_date, task.is_complete]
            table_list.append(task_component_list)
    if not table_list:
        print("No tasks have been completed!")
    else:
        # Specifiying colummn width for task title and task description.
        results_table = tabulate(table_list, headers=headers, colalign=(
            "left", "left", "left", "left", "right", "right", "left"),
            tablefmt='grid', maxcolwidths=[None, None, 15, 30])
        print(results_table)


# ==== Delete tasks function ====
# This function allows for the deletion of tasks no longer needed.
def delete_tasks():
    table_list = []
    headers = ["Index", "Username", "Task Title",
               "Task Description", "Entry Date", "Due Date",
               "Completed?"]  # Headers for readability
    for index, task in enumerate(task_list):
        task_component_list = [
            index, task.username, task.task_title,
            task.task_description, task.entry_date,
            task.due_date, task.is_complete]
        table_list.append(task_component_list)
    if not table_list:
        print("No tasks exist!")
    else:
        # Specifiying colummn width for task title and task description
        results_table = tabulate(table_list, headers=headers, colalign=(
            "left", "left", "left", "left", "right", "right", "left"),
            tablefmt='grid', maxcolwidths=[None, None, 15, 30])
        print(results_table)

    while True:
        try:
            choice = (input(
            "Please provide the index of the task you'd like to "
            "delete, or type -1 to exit: "))
            task_index = int(choice)

            if task_index == -1:
                return
            
            task_list.pop(task_index)
            save_to_file()  # Save changes to the task file after deletion
            print("Task successfully removed! Returning to main menu.")
            return
        
        except ValueError:
            print("Invalid input. Please enter a whole number.")
        except IndexError:
            print("Task index is out of bounds, please try a valid index")


# ==== Generate task report function ====
# This function generates a report on the tasks created, completed,
# incomplete, and overdue for statistical purposes.
def generate_task_report():
    total_tasks_generated = len(task_list)
    
    tasks_completed = 0
    tasks_uncompleted = 0
    tasks_uncompleted_overdue = 0
    current_date = datetime.datetime.now()

    for task in task_list:
        due_date = datetime.datetime.strptime(task.due_date, "%d %b %Y")
        
        if task.is_complete == "Yes":
            tasks_completed += 1
        else:
            tasks_uncompleted += 1
            # If not complete AND the due date is in the past
            if due_date < current_date:
                tasks_uncompleted_overdue += 1

    # Error handling if no tasks have been generated
    if total_tasks_generated > 0:
        percentage_uncompleted = (tasks_uncompleted / len(task_list)) * 100
        percentage_overdue = (tasks_uncompleted_overdue / len(task_list)) * 100
    else:
        percentage_uncompleted = 0
        percentage_overdue = 0

    # Write to task_overview.txt
    with open(task_overview_path, "w") as file:
        file.write(
            f"{total_tasks_generated}, "
            f"{tasks_completed}, "
            f"{tasks_uncompleted}, "
            f"{tasks_uncompleted_overdue}, "
            f"{percentage_uncompleted:.2f}%, "
            f"{percentage_overdue:.2f}%"
        )


# ==== Generate user report function ====
# This function generates a report on the tasks assigned to each user showing
# the percentage completed, incomplete, and overdue for statistical purposes.
def generate_user_report():
    total_users_generated = 0
    total_tasks_generated = len(task_list)

    with open(user_tracker_path, 'r') as file:
        content = file.read().strip()
        try:
            total_users_generated = int(content) if content else 0
        except ValueError:
            total_users_generated = 0

    today = datetime.datetime.now()

    with open(user_overview_path, "w") as file:
        file.write(f"{total_users_generated}, ")
        file.write(f"{total_tasks_generated}\n")

        for user in user_list:
            user_tasks = [t for t in task_list if t.username == user.username]
            num_assigned = len(user_tasks)

            if num_assigned == 0:  # Error handling for users with no tasks 
                # assigned to avoid division by zero
                file.write(f"{user.username}, 0, 0%, 0%, 0%, 0%\n")
                continue

            # Calculating completed and uncompleted tasks for the user
            completed = sum(1 for t in user_tasks if t.is_complete == 'Yes')
            uncompleted = num_assigned - completed
            
            # Calculating overdue tasks for the user
            overdue = 0
            for t in user_tasks:
                due_date_obj = datetime.datetime.strptime(t.due_date, "%d %b %Y")
                if t.is_complete == 'No' and due_date_obj < today:
                    overdue += 1

            # Percentage calculations:
            perc_total = (num_assigned / len(task_list)) * 100 if total_tasks_generated > 0 else 0
            perc_complete = (completed / num_assigned) * 100
            perc_uncompleted = (uncompleted / num_assigned) * 100
            perc_overdue = (overdue / num_assigned) * 100

            # Write the user line (formatted for easy .split(', '))
            file.write(
                f"{user.username}, "
                f"{num_assigned}, "
                f"{perc_total:.2f}%, "
                f"{perc_complete:.2f}%, "
                f"{perc_uncompleted:.2f}%, "
                f"{perc_overdue:.2f}%\n"
            )
    
    print("Reports successfully generated!\nTo view results, please choose display statistics")


# ==== Generate task table function ====
# This function generates a table to display the statistics generated in the
# task report in a friendly manner
def display_task_statistics():
    task_overview = []
    try:
        with open(task_overview_path, 'r') as file:
            for line in file:
                line = line.strip()
                stats_list = line.split(', ')
                task_overview.append(stats_list)  # Append the stats as a new row

    except FileNotFoundError:
        print("This file was not found, please generate the task report first")
        return
    except ValueError:
        print("The task overview list doesn't have all the components needed")
        return
    
    headers = [
        "Total tasks generated", "Tasks completed",
        "Tasks uncomplete", "Task uncomplete and overdue",
        "Percentage tasks uncomplete",
        "Percentage tasks overdue"]
    # Column width for readability
    results_table = tabulate(
        task_overview, headers=headers,
        colalign=("left", "left", "left", "left", "left",
                  "left"),
        tablefmt='grid')
    print("Task Report:")
    print(results_table)


# ==== Generate user table function ====
# This function generates a table to display the statistics generated in the
# user report in a friendly manner
def display_user_statistics():
    user_overview = []
    try:
        with open(user_overview_path, 'r') as file:
            for line in file:
                line = line.strip()
                user_overview.append(line.split(', '))  # Append each user's stats as a new row

    except FileNotFoundError:
        print("This file was not found, please generate the user report first")
        return
    except ValueError:
        print("The user overview list doesn't have all the components needed")
        return
    
    print(f"Total users generated: {user_overview[0][0]}")
    print(f"Total tasks generated: {user_overview[0][1]}")

    headers = [
        "Username", "Total Number of Tasks Assigned", "Percentage of Total Tasks", "Percentage tasks complete", "Percentages tasks uncomplete",
        "Percentage tasks overdue"]
    # Column width for readability
    for user_row in user_overview[1:]:  # Skip the first row which contains totals
        print(f"\nUser: {user_row[0]}")  # Print the username for clarity
        results_table = tabulate(
        [user_row], headers=headers,
        colalign=("left", "left", "left", "left", "left", "left"),
        tablefmt='grid')
        print(results_table)


# ==== Converting due date function ====
# This function captures the due date from the user and converts it to the
# correct format for output and storage.
def create_date_input():
    while True:
        try:
            due_day = int(
                input("Please enter this task's due day"))
            due_month = int(
                input("Please enter this task's due month as a number"))
            due_year = int(
                input("Please enter this task's due year"))
            try:
                due_date = datetime.datetime(
                    due_year, due_month, due_day).strftime(
                    "%d %b %Y")
                return due_date
            except ValueError:
                print("Please enter a valid due date.")
        except ValueError:
            print("Please only input a number")


print("Welcome to the Task Manager program!")  # Welcome message for user
read_login_data()  # Read login data before login
read_task_data()  # Read task data before login
# Login and save logged-in user
logged_in_user: User = login()  # Save the logged-in user for use in the menu
# and report generation


# ==== Menu ====
# This is the menu for the task manager, allowing users to select different
# options to view and edit tasks, and for the admin user to register users,
# generate reports, and delete tasks.
while True:
    admin_menu_string = (
        "Select one of the following options:\n"
        "r - register a user\n"
        "a - add task\n"
        "va - view all tasks\n"
        "vm - view my tasks\n"
        "vc - view completed tasks\n"
        "gr - generate reports\n"
        "ds - display statistics\n"
        "del - delete tasks\n"
        "e - exit\n: "
    )
    menu_string = (
        "Select one of the following options:\n"
        "a - add task\n"
        "va - view all tasks\n"
        "vm - view my tasks\n"
        "e - exit\n: "
    )

    menu = input(
        admin_menu_string
        if logged_in_user.username == "admin"
        else menu_string
    ).lower().strip()

    if menu == 'r' and logged_in_user.username == 'admin':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine(logged_in_user)

    elif menu == 'vc' and logged_in_user.username == 'admin':
        view_completed()

    elif menu == 'del' and logged_in_user.username == 'admin':
        delete_tasks()

    elif menu == 'ds' and logged_in_user.username == 'admin':
        display_task_statistics()
        display_user_statistics()

    elif menu == 'gr' and logged_in_user.username == 'admin':
        generate_task_report()
        generate_user_report()

    elif menu == 'e':
        print('Thank you for using the task manager, goodbye.')
        exit()

    else:
        print("You have entered an invalid input. Please try again")


# Unit tests for task class (Unit Testing Task)
import unittest # module for unit testing the task class

class TestTask(unittest.TestCase):

    def setUp(self):
           # Creating a sample task to use in the unit tests
            self.sample_task = Task(
                username="admin",
                task_title="Test",
                task_description="Test description",
                entry_date="01 Jan 2026",
                due_date="10 Jan 2026",
                is_complete="No"
            )

    # Use case 1 - creating a task and checking that all components are correctly stored in the task object.
        def test_task_creation(self):
            self.assertEqual(self.sample_task.username, "admin")
            self.assertEqual(self.sample_task.task_title, "Test")
            self.assertEqual(self.sample_task.task_description, "Test description")
            self.assertEqual(self.sample_task.entry_date, "01 Jan 2026")
            self.assertEqual(self.sample_task.due_date, "10 Jan 2026")
            self.assertEqual(self.sample_task.is_complete, "No")
            print("\nTest 1 (creating a task) success!")

    # Use case 2 - validating the default status for is_complete is set to 'No' when a new task is created.
        def test_is_complete_no(self):
            # Your code relies on the string "No" for incomplete tasks
            self.assertEqual(self.sample_task.is_complete, "No")
            self.assertIsInstance(self.sample_task.is_complete, str)
            print("Test 2 (is_completed) success!")

    # Use case 3 - testing that task_description can store a long string without issues.
        def test_long_description(self):
            long_desc = "LONG!" * 100  # This creates stress data for testing
            long_task = Task("admin", "Test", long_desc, "Entry Date", "Due Date", "No")
            self.assertEqual(len(long_task.task_description), 500) # 100 words * 5 chars - len returned should be 500, testing char limits.
            print("Test 3 (long description) success!")

    if __name__ == '__main__':
        unittest.main()