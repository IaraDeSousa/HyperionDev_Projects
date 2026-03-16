# This contains the task class for creating our task management project.


# Creating the task class
# This defines the task class with all the components needed to create a task
class Task:
    def __init__(
            self,
            task_title,
            task_description,
            entry_date,
            due_date,
            is_complete
    ):
        self.task_title = task_title
        self.task_description = task_description
        self.entry_date = entry_date
        self.due_date = due_date
        self.is_complete = is_complete
