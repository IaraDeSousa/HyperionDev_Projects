from models.task import Task
import os
# File Paths Defined
# This defines the file paths for the task file, task overview report,
# user overview report, task tracker, user tracker, and login file for use in
# the program.


# ==== Task Repository ====
# Task repository will read and write from the tasks text file, allowing us to
# save and view tasks created within the program.
class TaskRepository:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_dir, "..", "data", "tasks.txt")

# This reads the task data from the file, creating a list of task objects to
# be used within the program.
    def read_task_data(self):
        tasks = []
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    (task_title, task_description,
                     entry_date, due_date, is_complete) = line.split(', ')

                    task = Task(task_title, task_description,
                                entry_date, due_date, is_complete)
                    tasks.append(task)
            return tasks
        except FileNotFoundError:
            print("This file was not found, please try again")
        except ValueError:
            print("The task list doesn't have all the components needed")

# This saves the task data to the file, allowing us to save tasks created 
# within the program and view them later.
    def save(self, task_list: list[Task]):
        # This will open the file ready for writing.
        with open(self.file_path, 'w') as file:
            for task in task_list:
                # Write each task with updates
                file.write(
                    f"{task.task_title}, "
                    f"{task.task_description}, {task.entry_date}, "
                    f"{task.due_date}, {task.is_complete}\n")