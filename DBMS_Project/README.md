# Plant Management System

A Python and MySQL based Plant Management System for managing plants, seeds, soil information, water sources, sprinklers, customers, orders and crop-yield data.

## Technologies Used

- Python
- MySQL
- MySQL Connector/Python
- PrettyTable

## Features

### Admin

- Admin account creation
- Admin login
- View plants
- View seeds
- View soil information
- View water sources
- View water sprinklers
- View crop yield
- Increase stock
- View all database tables

### Customer

- Customer registration
- Customer login
- View plants
- View seeds
- View soil information
- View water sources
- View sprinklers
- View crop yield
- Add money to account
- Check account balance
- Purchase plants, seeds and sprinklers
- View previous orders

## Database Tables

The system contains the following tables:

1. Admin
2. Address
3. Customer
4. Orders
5. Planter
6. Plants
7. Seeds
8. Soil
9. WaterSource
10. WaterSprinkler
11. CropYield

## Database Relationships

- Address → Customer
- Customer → Orders
- Orders logically references Plants, Seeds or WaterSprinkler through Item_type and Item_id

Admin, Planter, Soil, WaterSource and CropYield are currently independent tables.

## Project Structure

```text
Plant-Management-Database/
│
├── plant_management.py
├── README.md
├── requirements.txt
├── .gitignore
└── screenshots/
```

## Requirements

- Python 3.x
- MySQL Server
- MySQL Connector/Python
- PrettyTable

## Installation

Install the required Python packages:

```bash
pip install mysql-connector-python prettytable
```

Or install via `requirements.txt`:

```bash
pip install -r requirements.txt
```

## MySQL Configuration

The program connects to MySQL using:

```python
host="localhost"
user="root"
password="YOUR_MYSQL_PASSWORD"
```

Change the password according to your local MySQL installation.

The database is automatically created as:

`plant_management`

## How to Run

Run the Python program:

```bash
python plant_management.py
```

The main menu provides:

1. Admin
2. Customer
3. Exit
4. Delete and Recreate Database

## Database Initialization

When the program starts, it:

1. Creates the database if it does not exist.
2. Creates the required tables.
3. Inserts sample catalogue data if the tables are empty.
4. Starts the main menu.

## ER Diagram

Add the ER diagram image here:

![ER Diagram](screenshots/er_diagram.png)

## Security Note

This project is created for educational purposes.

Passwords are currently stored directly in the database.
For a production system, passwords should be securely hashed.

## Author

Developed as a database management project using Python and MySQL.
