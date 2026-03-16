class Course:
    # Class attribute for the course name
    name = "Fundamentals of Computer Science"

    # Class attribute for the contact website
    contact_website = "www.hyperiondev.com"

    # Class attribute for the location
    location = "Cape Town"

    # Method to display contact details
    def contact_details(self):
        print("Please contact us by visiting", self.contact_website)

    # Method to display head office location
    def location(self):
        print("Our head office location is", self.location)

class OOPCourse(Course):

    # Class attribute for the course ID
    course_id = "#12345"
    
    # Class attribute for the description
    description = "OOP Fundamentals"

    # Class attribute for the trainer
    trainer = "Mr Anon A. Mouse"

    # Method to display the trainer details
    def trainer_details(self):
        print("Your trainer is", self.trainer, "and your training is", self.description)

    # Method to display the course ID
    def show_course_id(self):
        print("The course ID is:", self.course_id)


# Creating an instance of the OOPcourse class
course_1 = OOPCourse()

# Call methods needed
course_1.contact_details()
course_1.trainer_details()
course_1.show_course_id()
