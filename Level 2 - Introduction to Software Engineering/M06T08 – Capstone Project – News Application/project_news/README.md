# A Django-based news application.

## Prequisities 
Copy and paste key values in password.txt file into respective key values in
settings.py!

## Running with Docker
1. Start the containers
 ```docker-compose up --build```

2. Setup the database
Open a new terminal window and run:
 ```docker-compose exec web python manage.py migrate```

3. Create an admin account
 ```docker-compose exec web python manage.py createsuperuser``` 

4. Access the site
Website: http://localhost:8000
Admin: http://localhost:8000/admin

## Running with Virtual Environment (Local)

1. Create and activate venv

    **Create:**
    ```python -m venv venv``` 

    **Activate:**
     ```source venv/bin/activate``` 

2. Install requirements
 ```pip install -r requirements.txt```

3. Start MariaDB
Install MariaDB locally, and ensure it is running.
Create the database with this command: ```CREATE DATABASE news_db;```

3. Run migrations and server
Ensure you have a local MariaDB database named news_db created.
 ```python manage.py migrate ```
 ```python manage.py runserver ```