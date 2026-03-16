# Unit tests for task class (Unit Testing Task)
import unittest # module for unit testing the task class
from models.task import Task
from views.view import controller


class TestTask(unittest.TestCase):
    def setUp(self):
        # Creating a sample task to use in the unit tests
        self.sample_task = Task(
            task_title="Test",
            task_description="Test description",
            entry_date="01 Jan 2026",
            due_date="10 Jan 2026",
            is_complete="No"
        )

    # Use case 1 - creating a task and checking that all components are
    # correctly stored in the task object.
    def test_task_creation(self):
        self.assertEqual(self.sample_task.task_title, "Test")
        self.assertEqual(self.sample_task.task_description, "Test description")
        self.assertEqual(self.sample_task.entry_date, "01 Jan 2026")
        self.assertEqual(self.sample_task.due_date, "10 Jan 2026")
        self.assertEqual(self.sample_task.is_complete, "No")
        print("\nTest 1 (creating a task) success!")

    # Use case 2 - validating the default status for is_complete is set to
    # 'No' when a new task is created.
    def test_is_complete_no(self):
        # Your code relies on the string "No" for incomplete tasks
        self.assertEqual(self.sample_task.is_complete, "No")
        self.assertIsInstance(self.sample_task.is_complete, str)
        print("Test 2 (is_completed) success!")

    # Use case 3 - testing that task_description can store a long string
    # without issues
    def test_long_description(self):
        long_desc = "LONG!" * 100  # This creates stress data for testing
        long_task = Task("Test", long_desc, "Entry Date", "Due Date", "No")
        self.assertEqual(len(long_task.task_description), 500)  # 100 words * 5
        # chars - len returned should be 500, testing char limits.
        print("Test 3 (long description) success!")

    # Use case 4 - testing the create_date_input function for valid date input
    def test_create_date_input(self):
        due_year = 2026
        due_month = 1
        due_day = 10
        expected_date = "10 Jan 2026"
        actual_date = controller.create_date_input(due_year, due_month, due_day)
        self.assertEqual(actual_date, expected_date)
        print("Test 4 (create_date_input) success!")


if __name__ == '__main__':
    unittest.main()  # Run the unit tests