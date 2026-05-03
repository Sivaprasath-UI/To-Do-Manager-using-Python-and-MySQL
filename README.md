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
