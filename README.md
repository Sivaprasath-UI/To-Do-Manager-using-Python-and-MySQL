# CLI-Based To-Do Manager with MySQL

A beginner-friendly command-line To-Do Manager built using Python and MySQL.

## Features

- Add tasks
- Update tasks
- Delete tasks
- Mark tasks as completed
- View all/pending/completed/today's tasks
- Recurring task support
- Persistent storage using MySQL

---

## Technologies Used

- Python
- MySQL
- mysql-connector-python

---

## MySQL Setup

### Create Database

```sql
CREATE DATABASE todo_app;
```

### Use Database

```sql
USE todo_app;
```

### Create Table

```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'Pending',
    due_date DATE,
    completion_date DATE,
    recurring BOOLEAN DEFAULT FALSE
);
```

---

## Install Dependency

```bash
pip install mysql-connector-python
```

---

##Python Code

```python
import mysql.connector
from datetime import datetime, timedelta


# ---------------- DATABASE CONNECTION ---------------- #
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_PASSWORD_HERE",
            database="todo_app"
        )
        return connection
    except Exception as e:
        print("Database connection error:", e)
        return None


# ---------------- ADD TASK ---------------- #
def add_task(connection):
    title = input("Enter title: ")
    description = input("Enter description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    recurring = input("Is it recurring? (y/n): ").lower() == 'y'

    cursor = connection.cursor()

    query = """
    INSERT INTO tasks (title, description, due_date, recurring)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (title, description, due_date, recurring))
    connection.commit()

    print("Task added successfully!")


# ---------------- VIEW TASKS ---------------- #
def view_tasks(connection, filter_type="all"):
    cursor = connection.cursor()

    if filter_type == "completed":
        query = "SELECT * FROM tasks WHERE status='Completed'"
    elif filter_type == "pending":
        query = "SELECT * FROM tasks WHERE status='Pending'"
    elif filter_type == "today":
        today = datetime.today().date()
        query = f"SELECT * FROM tasks WHERE due_date='{today}'"
    else:
        query = "SELECT * FROM tasks"

    cursor.execute(query)
    tasks = cursor.fetchall()

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(task)


# ---------------- UPDATE TASK ---------------- #
def update_task(connection):
    task_id = input("Enter task ID to update: ")
    new_title = input("Enter new title: ")

    cursor = connection.cursor()
    query = "UPDATE tasks SET title=%s WHERE id=%s"
    cursor.execute(query, (new_title, task_id))
    connection.commit()

    print("Task updated!")


# ---------------- DELETE TASK ---------------- #
def delete_task(connection):
    task_id = input("Enter task ID to delete: ")

    cursor = connection.cursor()
    query = "DELETE FROM tasks WHERE id=%s"
    cursor.execute(query, (task_id,))
    connection.commit()

    print("Task deleted!")


# ---------------- CREATE NEXT RECURRING TASK ---------------- #
def create_next_recurring_task(connection, task):
    old_due_date = task[4]

    if old_due_date:
        next_due_date = old_due_date + timedelta(days=7)
    else:
        next_due_date = datetime.today().date() + timedelta(days=7)

    cursor = connection.cursor()

    query = """
    INSERT INTO tasks (title, description, due_date, recurring)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (task[1], task[2], next_due_date, True))
    connection.commit()

    print("Next recurring task created!")


# ---------------- MARK TASK COMPLETE ---------------- #
def mark_task_completed(connection):
    task_id = input("Enter task ID to mark complete: ")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
    task = cursor.fetchone()

    if not task:
        print("Task not found")
        return

    query = """
    UPDATE tasks
    SET status='Completed', completion_date=%s
    WHERE id=%s
    """
    cursor.execute(query, (datetime.today().date(), task_id))
    connection.commit()

    print("Task marked as completed!")

    if task[6]:  # recurring
        create_next_recurring_task(connection, task)


# ---------------- MAIN MENU ---------------- #
def main():
    connection = connect_db()

    if not connection:
        return

    while True:
        print("\n========== TO-DO MANAGER ==========")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View Completed Tasks")
        print("5. View Today's Tasks")
        print("6. Update Task")
        print("7. Delete Task")
        print("8. Mark Task Completed")
        print("9. Exit")

        choice = input("Enter your choice: ")

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
            mark_task_completed(connection)
        elif choice == '9':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
```


## Run Project

Update database credentials in:

```python
create_connection()
```

Then run:

```bash
python todo_manager.py
```

---

## Resume Description

CLI-Based To-Do Manager using Python and MySQL with CRUD operations, recurring task automation, and persistent database storage.
