from controllers.controller import TaskController
from data.repository import TaskRepository

repository = TaskRepository()
controller = TaskController(repository)


# ==== Capturing Task ====
# Defines a new task with title, description, due_date,
# and completion status.
def create_task_input():
    task_title = input(
        "Please enter the task title: ").strip()
    task_description = input(
        "Please enter the task description: ").strip()

    due_day = int(
        input("Please enter this task's due day: "))
    due_month = int(
        input("Please enter this task's due month as a number: "))
    due_year = int(
        input("Please enter this task's due year: "))
    
    controller.create(task_title, task_description, due_year, due_month, due_day)


# ==== Delete Task ====
# Allows user to delete the task with the specified task ID
def delete_task_input():
    task_id = int(input(
        "Please enter the task id you would like to delete: ").strip())
    controller.delete(task_id)


# ==== Edit Task ====
# Allows user to complete the task with the specific task ID
def edit_task():
    task_id = int(input(
        "Please enter the task id of the task you would like to complete: ").strip())
    completed_task = controller.complete(task_id)
    print(f"Task ID: {task_id}")
    print(f"Title: {completed_task.task_title}")
    print(f"Description: {completed_task.task_description}")
    print(f"Entry Date: {completed_task.entry_date}")
    print(f"Due Date: {completed_task.due_date}")
    print(f"Complete: {completed_task.is_complete}\n")


# ==== View all Tasks ====
# Allows the user to view all tasks in the task manager application
def view_all():
    controller.view_all()

