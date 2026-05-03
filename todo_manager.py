import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta


# =========================
# DATABASE CONNECTION
# =========================

def create_connection():
    """
    Create and return MySQL database connection.
    """

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",
            database="todo_app"
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print(f"Database connection error: {e}")
        return None


# =========================
# HELPER FUNCTIONS
# =========================

def validate_date(date_text):
    """
    Validate date format YYYY-MM-DD.
    """

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# =========================
# ADD TASK
# =========================

def add_task(connection):
    """
    Add a new task to database.
    """

    print("\n--- Add New Task ---")

    title = input("Enter task title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    description = input("Enter description: ").strip()

    due_date = input("Enter due date (YYYY-MM-DD): ").strip()

    if not validate_date(due_date):
        print("Invalid date format.")
        return

    recurring_input = input("Is this recurring? (y/n): ").lower()
    recurring = recurring_input == 'y'

    query = """
    INSERT INTO tasks (title, description, due_date, recurring)
    VALUES (%s, %s, %s, %s)
    """

    values = (title, description, due_date, recurring)

    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

    print("Task added successfully.")


# =========================
# VIEW TASKS
# =========================

def view_tasks(connection, filter_type="all"):
    """
    Display tasks based on filter.
    """

    cursor = connection.cursor()

    if filter_type == "completed":
        query = "SELECT * FROM tasks WHERE status='Completed'"

    elif filter_type == "pending":
        query = "SELECT * FROM tasks WHERE status='Pending'"

    elif filter_type == "today":
        today = datetime.today().strftime('%Y-%m-%d')
        query = f"SELECT * FROM tasks WHERE due_date='{today}'"

    else:
        query = "SELECT * FROM tasks"

    cursor.execute(query)
    tasks = cursor.fetchall()

    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n--- TASK LIST ---")

    for task in tasks:
        print(f"""
ID: {task[0]}
Title: {task[1]}
Description: {task[2]}
Status: {task[3]}
Due Date: {task[4]}
Completion Date: {task[5]}
Recurring: {task[6]}
""")


# =========================
# UPDATE TASK
# =========================

def update_task(connection):
    """
    Update task title, description, or due date.
    """

    print("\n--- Update Task ---")

    task_id = input("Enter task ID: ").strip()

    if not task_id.isdigit():
        print("Invalid task ID.")
        return

    title = input("New title: ").strip()
    description = input("New description: ").strip()
    due_date = input("New due date (YYYY-MM-DD): ").strip()

    if not validate_date(due_date):
        print("Invalid date format.")
        return

    query = """
    UPDATE tasks
    SET title=%s, description=%s, due_date=%s
    WHERE id=%s
    """

    values = (title, description, due_date, task_id)

    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

    if cursor.rowcount > 0:
        print("Task updated successfully.")
    else:
        print("Task not found.")


# =========================
# DELETE TASK
# =========================

def delete_task(connection):
    """
    Delete a task.
    """

    print("\n--- Delete Task ---")

    task_id = input("Enter task ID: ").strip()

    if not task_id.isdigit():
        print("Invalid task ID.")
        return

    query = "DELETE FROM tasks WHERE id=%s"

    cursor = connection.cursor()
    cursor.execute(query, (task_id,))
    connection.commit()

    if cursor.rowcount > 0:
        print("Task deleted successfully.")
    else:
        print("Task not found.")


# =========================
# CREATE NEXT RECURRING TASK
# =========================

def create_next_recurring_task(connection, task):
    """
    Create next recurring task automatically.
    """

    old_due_date = task[4]

    if old_due_date:
        next_due_date = old_due_date + timedelta(days=7)
    else:
        next_due_date = datetime.today().date() + timedelta(days=7)

    query = """
    INSERT INTO tasks (title, description, due_date, recurring)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        task[1],
        task[2],
        next_due_date,
        True
    )

    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

    print("Next recurring task created automatically.")


# =========================
# MARK TASK COMPLETE
# =========================

def mark_completed(connection):
    """
    Mark task as completed.
    """

    print("\n--- Mark Task Completed ---")

    task_id = input("Enter task ID: ").strip()

    if not task_id.isdigit():
        print("Invalid task ID.")
        return

    cursor = connection.cursor()

    # Get task details first
    select_query = "SELECT * FROM tasks WHERE id=%s"
    cursor.execute(select_query, (task_id,))

    task = cursor.fetchone()

    if not task:
        print("Task not found.")
        return

    completion_date = datetime.today().strftime('%Y-%m-%d')

    update_query = """
    UPDATE tasks
    SET status='Completed', completion_date=%s
    WHERE id=%s
    """

    cursor.execute(update_query, (completion_date, task_id))
    connection.commit()

    print("Task marked as completed.")

    # If recurring task, create next task automatically
    if task[6]:
        create_next_recurring_task(connection, task)


# =========================
# MENU SYSTEM
# =========================

def show_menu():
    """
    Display application menu.
    """

    print("""
========== TO-DO MANAGER ==========
1. Add Task
2. View All Tasks
3. View Pending Tasks
4. View Completed Tasks
5. View Today's Tasks
6. Update Task
7. Delete Task
8. Mark Task Completed
9. Exit
===================================
""")


# =========================
# MAIN PROGRAM
# =========================

def main():
    connection = create_connection()

    if not connection:
        print("Could not connect to database.")
        return

    while True:
        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_task(connection)

        elif choice == '2':
            view_tasks(connection)

        elif choice == '3':
            view_tasks(connection, "pending")

        elif choice == '4':
            view_tasks(connection, "completed")

        elif choice == '5':
            view_tasks(connection, "today")

        elif choice == '6':
            update_task(connection)

        elif choice == '7':
            delete_task(connection)

        elif choice == '8':
            mark_completed(connection)

        elif choice == '9':
            print("Exiting application...")
            break

        else:
            print("Invalid choice. Please try again.")

    connection.close()


# Run application
if __name__ == "__main__":
    main()
