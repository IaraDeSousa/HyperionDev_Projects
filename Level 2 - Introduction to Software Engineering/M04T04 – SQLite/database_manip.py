# Create a table

import sqlite3

# Creating the SQLite database file
db = sqlite3.connect('python_programming.db')

# Getting cursor object to interact with the database
cursor = db.cursor()

# Create the python_programming table (if it doesn't already exist)
cursor.execute(
    ''' CREATE TABLE IF NOT EXISTS python_programming (
    id INTEGER PRIMARY KEY,
    name TEXT,
    grade INTEGER
    )
    '''

)

# Committing changes for table creation
db.commit()

# Defining the data for each student and their grades
students_data = [
    (55, 'Carl Davis', 61),
    (66, 'Dennis Fredrickson', 88),
    (77, 'Jane Richards', 78),
    (12, 'Peyton Sawyer', 45),
    (2, 'Lucas Brooke', 99)
]

# Inserting the data into the table
# Used INSERT OR IGNORE to prevent UNIQUE constraint failed when re-running the script.
cursor.executemany(
    ''' 
    INSERT OR IGNORE INTO python_programming(id, name, grade)
    VALUES(?, ?, ?)
    ''',
    students_data
)

# Committing changes for data inserted
db.commit()

# Retrieving student records between 60 and 80
minimum_grade = 60
maximum_grade = 80

# Execute query to fetch the students with grades between the two.
cursor.execute(
    '''
    SELECT * 
    FROM python_programming 
    WHERE grade BETWEEN ? AND ?
    ''', 
    (minimum_grade, maximum_grade)
)

# Fetch all rows matching this query
students = cursor.fetchall()

# Print each student's name and grade if records are found, otherwise output that no students met the criteria
if students:
    print(f'Students with a grade between {minimum_grade} and {maximum_grade}:')
    for student in students:
        print(f'{student[1]}:{student[2]}')
else: 
    print(f'No students found with a grade between {minimum_grade} and {maximum_grade}')

# Updating the grade of student ID=55
grade = 65
id = 55

# UPDATE statement
cursor.execute(
    '''
    UPDATE python_programming SET grade = ? WHERE id = ?
    ''', (grade, id)
)

# Commit changes to data update.
db.commit()

print(f'\nStudent with ID {id} updated with new grade {grade}.\n')

# Delete student with ID=66
id = 66

# Execute DELETE statement
cursor.execute(''' DELETE FROM python_programming WHERE id = ?''', (id,))

# Commit changes to save the deletion
db.commit()

# Change the grade of all students with an id greater than 55 to 80
id = 55
grade = 80

# Execute query to fetch the students with an id greater than 55
cursor.execute(
    '''
    SELECT id, name 
    FROM python_programming 
    WHERE id > ?
    ''', 
    (id,)
)

# Fetch all rows matching this query
students = cursor.fetchall()

# UPDATE each student's grade if records are found, otherwise output that no students met the criteria
if students:
    cursor.execute(
        '''
        UPDATE python_programming SET grade = ? WHERE id > ?
        ''', (grade, id)
    )
    print(f'Students with an id above {id} have been updated to have grade {grade}:')
    for student in students:
        print(f'{student[1]}')
else: 
    print(f'No students found with an id above {id}')

# Commit changes to the updated grades
db.commit()

# Close the database connection
db.close()
print('Connection to database closed.')