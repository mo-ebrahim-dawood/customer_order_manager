# Customer Order Manager

A simple command-line application built with Python to manage customer orders and keep track of sales.

I built this project in two versions to practice different ways of storing and managing data: JSON and SQLite.

## Project Versions

### 1. JSON Version
The first version uses a JSON file to store order information.

It allows users to:
- Add new orders.
- View all orders.
- Search for orders by customer name.
- Cancel orders.
- Calculate total sales.

Data is saved in a JSON file, so it remains available when the program is closed.

**File:** `customer_order_manager_json.py`

### 2. SQLite Version
The second version uses an SQLite database instead of a JSON file.

It includes the previous features, with additional functionality:
- Update existing orders.
- Search for orders directly through SQL queries.
- Delete orders using their IDs.
- Calculate total sales using SQL.
- Store data in a structured database.

The database and its table are created automatically when the application runs.

**File:** `customer_order_manager.py`

## Technologies Used

- Python 3
- SQLite
- JSON
- Python's built-in `sqlite3` module

## How to Run

Make sure Python 3 is installed.

**Run the JSON version:**

```bash
python customer_order_manager_json.py
```

**Run the SQLite version:**

```bash
python customer_order_manager.py
```

## What I Practiced

- Writing and organizing Python functions.
- Working with lists and dictionaries.
- Handling user input and exceptions.
- Reading and writing JSON files.
- Connecting Python with SQLite.
- Using SQL commands to insert, retrieve, update, and delete records.
- Validating data and working with database constraints.

## Author

Mohamed Dawood

GitHub: [mo-ebrahim-dawood](https://github.com/mo-ebrahim-dawood)
