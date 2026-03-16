from datetime import datetime
from data.repository import TaskRepository
from models.task import Task


# ==== Task Controller ====
# This is the task controller, which contains all the functions needed to
# create, view, update, and delete tasks within the program. It uses the task
#  repository to read and write task data to the file, and the task model to
# create a list of tasks.
class TaskController:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
        self.task_list: list[Task] = task_repository.read_task_data()
        
    # This creates a date input for the due date, allowing us to create a due
    # date for the task.
    def create_date_input(self, due_year, due_month, due_day):
        due_date = datetime(
            due_year, due_month, due_day).strftime(
            "%d %b %Y")
        return due_date

    # This creates a new task with the given title, description, and due date,
    # and saves it to the task list and file.
    def create(self, task_title, task_description, due_year, due_month, due_day):
        try:
            due_date = self.create_date_input(due_year, due_month, due_day)
            task = Task(task_title, task_description,  
                        datetime.now().strftime("%d %b %Y"),
                        due_date, "No")
            self.task_list.append(task)
            self.task_repository.save(self.task_list)
        except ValueError:
            print("Exiting! Please enter a valid due date.")

    # This deletes a task with the given task id, and saves the updated task
    # list to the file.
    def delete(self, task_id: int):
        try:
            del self.task_list[task_id]
            self.task_repository.save(self.task_list)
        except IndexError:
            print("Please enter a valid task id.")  

    # This views a specific task with the given task id, printing the task
    # details to the console.
    def view_all(self):
        for index, task in enumerate(self.task_list):
            print(f"Task ID: {index}")
            print(f"Title: {task.task_title}")
            print(f"Description: {task.task_description}")
            print(f"Entry Date: {task.entry_date}")
            print(f"Due Date: {task.due_date}")
            print(f"Completed: {task.is_complete}\n")

    # This views a specific task with the given task id, printing the task
    # details to the console.
    def complete(self, task_id: int):
        try:
            self.task_list[task_id].is_complete = "Yes"
            self.task_repository.save(self.task_list)
            print("Task successfully completed!")
            return self.task_list[task_id]
        except IndexError:
            print("Please enter a valid task id.")