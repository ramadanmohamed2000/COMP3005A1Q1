import psycopg2
from psycopg2 import sql


# Function to insert initial data into the students table
def insert_initial_data(connection):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES
                ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
                ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
                ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02')
                """
            )
            connection.commit()
            print("Initial data added successfully")
        except psycopg2.IntegrityError as e:
            connection.rollback()
            print("Error: Some or all of the initial data already exists.")
            print(e)


# Function to establish a connection to the PostgreSQL database
def connect_to_db():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="Legend_613",
            host="localhost",
            port="5434",
            database="Students",
        )
        return connection
    except psycopg2.Error as e:
        print("Error: Unable to connect to the database")
        print(e)
        return None

# Function to create the students table using the provided schema
def create_students_table(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                enrollment_date DATE
            )
            """
        )
        connection.commit()

# Function to retrieve and display all records from the students table
def get_all_students(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        for student in students:
            print(student)

# Function to add a new student record into the students table
def add_student(connection, first_name, last_name, email, enrollment_date):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                """,
                (first_name, last_name, email, enrollment_date),
            )
            connection.commit()
            print("Student added successfully")
        except psycopg2.IntegrityError as e:
            connection.rollback()
            print("Error: This email address is already in use.")
            print(e)

# Function to update the email address for a student with the specified student_id
def update_student_email(connection, student_id, new_email):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE students
            SET email = %s
            WHERE student_id = %s
            """,
            (new_email, student_id),
        )
        connection.commit()
        print(f"Email address updated for student {student_id}")

# Function to delete the record of the student with the specified student_id
def delete_student(connection, student_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM students
            WHERE student_id = %s
            """,
            (student_id,),
        )
        connection.commit()
        print(f"Student with ID {student_id} deleted")

# Main function to execute the application
def main():
    # Modify the connection parameters according to your PostgreSQL setup
    connection = connect_to_db()

    if connection:
        create_students_table(connection)
        insert_initial_data(connection)

        print("---- All Students ----")
        get_all_students(connection)
        print("----------------------")

        print("\n---- Add New Student ----")
        add_student(connection, "New", "Student", "new.student@example.com", "2023-09-03")
       

        print("-----------------------------")

        print("\n---- All Students (After Update) ----")
        update_student_email(connection, 2, "updated.email@example.com")
        get_all_students(connection)
        print("--------------------------------------")

        print("\n---- Delete Student ----")
        delete_student(connection, 1)  # Assuming 1 is the student_id to delete
        print("---------------------------------")

        print("\n---- All Students (After Delete) ----")
        get_all_students(connection)
        print("--------------------------------------")

        # Close the database connection when done
        connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
