from views.view import view_all, edit_task, create_task_input, delete_task_input

# ==== Menu ====
# This is the menu for the task manager, allowing users to select different
# options to create, view, update, and delete tasks, as well as exit the 
# program.
while True:
    menu_string = (
        "Select one of the following options:\n"
        "c - Create task\n"
        "v - View all tasks\n"
        "vs - View specific task\n"
        "d - Delete task\n"
        "e - exit\n: "
    )

    menu = input(menu_string).lower().strip()

    if menu == 'c':
        create_task_input()

    elif menu == 'v':
        view_all()

    elif menu == 'vs':
        edit_task()

    elif menu == 'd':
        delete_task_input()

    elif menu == 'e':
        print('Thank you for using the task manager, goodbye.')
        exit()

    else:
        print("You have entered an invalid input. Please try again")
