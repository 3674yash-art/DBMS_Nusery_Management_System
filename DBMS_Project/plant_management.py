import mysql.connector as mycon
from prettytable import PrettyTable
import sys


DB_NAME = "plant_management"

# ------------------------------------------------------------
# DATABASE CONNECTION
# ------------------------------------------------------------

try:
    con = mycon.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD"
    )
    cur = con.cursor()
except Exception as e:
    print("Database connection error:", e)
    sys.exit()


# ------------------------------------------------------------
# CREATE DATABASE AND TABLES
# ------------------------------------------------------------

def create_database():

    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cur.execute(f"USE {DB_NAME}")

    # --------------------------------------------------------
    # ADMIN
    # --------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Admin(
            admin_id VARCHAR(5) PRIMARY KEY,
            username VARCHAR(20) NOT NULL UNIQUE,
            pass VARCHAR(50) NOT NULL
        )
    """)

    # --------------------------------------------------------
    # ADDRESS
    # --------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Address(
            Address_id INT AUTO_INCREMENT PRIMARY KEY,
            City VARCHAR(50) NOT NULL,
            pincode VARCHAR(20) NOT NULL
        )
    """)

    # --------------------------------------------------------
    # CUSTOMER
    # Address_id connects Customer with Address
    # --------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Customer(
            Customer_id INT AUTO_INCREMENT PRIMARY KEY,
            Customer_name VARCHAR(50) NOT NULL,
            Customer_username VARCHAR(30) NOT NULL UNIQUE,
            Customer_password VARCHAR(100) NOT NULL,
            Address_id INT NOT NULL,
            Customer_money DECIMAL(10,2) NOT NULL DEFAULT 0,

            FOREIGN KEY (Address_id)
                REFERENCES Address(Address_id)
        )
    """)

    # --------------------------------------------------------
    # ORDERS
    # Item_id is VARCHAR because IDs are now P001, S001, SP001
    # --------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Orders(
            Order_id INT AUTO_INCREMENT PRIMARY KEY,
            Customer_id INT NOT NULL,
            Item_type VARCHAR(30) NOT NULL,
            Item_id VARCHAR(10) NOT NULL,
            Item_name VARCHAR(50) NOT NULL,
            quantity INT NOT NULL,
            Total_cost DECIMAL(10,2) NOT NULL,
            Order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (Customer_id)
                REFERENCES Customer(Customer_id)
        )
    """)

    # --------------------------------------------------------
    # PLANT
    # --------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Planter(
            Planter_id INT AUTO_INCREMENT PRIMARY KEY,
            Plant_list VARCHAR(100) NOT NULL,
            seed_list VARCHAR(100) NOT NULL,
            capacity INT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Plants(
            plant_id VARCHAR(10) PRIMARY KEY,
            Type_of_Plant VARCHAR(30) NOT NULL,
            Plantname VARCHAR(50) NOT NULL,
            Plant_stock INT NOT NULL DEFAULT 0,
            Plant_cost DECIMAL(10,2) NOT NULL
        )
    """)

    # --------------------------------------------------------
    # SEEDS
    # --------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Seeds(
            seed_id VARCHAR(10) PRIMARY KEY,
            Type_of_seed VARCHAR(30) NOT NULL,
            Seedname VARCHAR(50) NOT NULL,
            seed_cost DECIMAL(10,2) NOT NULL,
            Seed_stock INT NOT NULL DEFAULT 0
        )
    """)

    # --------------------------------------------------------
    # SOIL
    # --------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Soil(
            Soil_id INT AUTO_INCREMENT PRIMARY KEY,
            State VARCHAR(50) NOT NULL UNIQUE,
            N INT,
            P INT,
            K INT,
            pH DECIMAL(4,2)
        )
    """)

    # --------------------------------------------------------
    # WATER SOURCE
    # --------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS WaterSource(
            Water_ID VARCHAR(10) PRIMARY KEY,
            Source_Type VARCHAR(50) NOT NULL,
            Capacity_Litres INT,
            Location VARCHAR(100),
            Water_Quality VARCHAR(30)
        )
    """)

    # --------------------------------------------------------
    # WATER SPRINKLER
    # --------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS WaterSprinkler(
            Sprinkler_ID VARCHAR(10) PRIMARY KEY,
            Sprinkler_Type VARCHAR(50) NOT NULL,
            Capacity_L_per_hr INT,
            Coverage_Area_sqm INT,
            Flow_Rate_L_per_min DECIMAL(6,2),
            Status VARCHAR(30),
            Stock INT NOT NULL DEFAULT 0,
            Cost DECIMAL(10,2) NOT NULL DEFAULT 0
        )
    """)

    # --------------------------------------------------------
    # CROP YIELD
    # --------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS CropYield(
            CropYield_ID INT AUTO_INCREMENT PRIMARY KEY,
            Crop VARCHAR(50),
            Year INT,
            Season VARCHAR(30),
            State VARCHAR(50),
            Area DECIMAL(12,2),
            Production DECIMAL(14,2),
            Fertilizer DECIMAL(14,2),
            Pesticide DECIMAL(14,2),
            Yield DECIMAL(12,4)
        )
    """)

    con.commit()

    insert_sample_data()
    

# ------------------------------------------------------------
# INSERT SAMPLE RECORDS
# These are added only when the relevant table is empty.
# Add your full datasets here if required.
# ------------------------------------------------------------

def insert_sample_data():

    # ================= PLANTS =================
    cur.execute("SELECT COUNT(*) FROM Plants")

    if cur.fetchone()[0] == 0:

        plants = [
            ("P001", "Cereal", "Rice", 100, 50),
            ("P002", "Cereal", "Wheat", 100, 45),
            ("P003", "Cereal", "Maize", 100, 40),
            ("P004", "Cereal", "Barley", 80, 45),
            ("P005", "Cereal", "Sorghum", 90, 40),
            ("P006", "Cereal", "Millet", 90, 35),
            ("P007", "Cereal", "Ragi", 80, 35),

            ("P008", "Pulse", "Chickpea", 100, 50),
            ("P009", "Pulse", "Pigeon Pea", 90, 55),
            ("P010", "Pulse", "Green Gram", 90, 50),
            ("P011", "Pulse", "Black Gram", 90, 50),
            ("P012", "Pulse", "Lentil", 80, 45),
            ("P013", "Pulse", "Peas", 100, 40),

            ("P014", "Oilseed", "Groundnut", 100, 55),
            ("P015", "Oilseed", "Soybean", 100, 60),
            ("P016", "Oilseed", "Sunflower", 80, 55),
            ("P017", "Oilseed", "Mustard", 100, 50),
            ("P018", "Oilseed", "Sesame", 80, 45),

            ("P019", "Vegetable", "Potato", 120, 35),
            ("P020", "Vegetable", "Onion", 120, 40),
            ("P021", "Vegetable", "Tomato", 120, 45),
            ("P022", "Vegetable", "Brinjal", 100, 40),
            ("P023", "Vegetable", "Cabbage", 100, 35),
            ("P024", "Vegetable", "Cauliflower", 100, 40),
            ("P025", "Vegetable", "Carrot", 100, 35),
            ("P026", "Vegetable", "Radish", 100, 30),
            ("P027", "Vegetable", "Spinach", 100, 25),
            ("P028", "Vegetable", "Lady Finger", 100, 40),
            ("P029", "Vegetable", "Capsicum", 90, 50),
            ("P030", "Vegetable", "Cucumber", 100, 35),

            ("P031", "Fruit", "Mango", 60, 150),
            ("P032", "Fruit", "Banana", 80, 80),
            ("P033", "Fruit", "Papaya", 70, 70),
            ("P034", "Fruit", "Guava", 60, 90),
            ("P035", "Fruit", "Pomegranate", 50, 180),
            ("P036", "Fruit", "Grapes", 70, 120),
            ("P037", "Fruit", "Orange", 60, 100),
            ("P038", "Fruit", "Lemon", 70, 70),
            ("P039", "Fruit", "Watermelon", 100, 50),
            ("P040", "Fruit", "Muskmelon", 100, 45),

            ("P041", "Cash Crop", "Sugarcane", 100, 90),
            ("P042", "Cash Crop", "Cotton", 100, 80),
            ("P043", "Cash Crop", "Jute", 80, 60),
            ("P044", "Cash Crop", "Tea", 60, 120),
            ("P045", "Cash Crop", "Coffee", 60, 150),

            ("P046", "Spice", "Turmeric", 80, 70),
            ("P047", "Spice", "Ginger", 80, 65),
            ("P048", "Spice", "Chilli", 100, 55),
            ("P049", "Spice", "Coriander", 100, 40),
            ("P050", "Spice", "Cardamom", 50, 200)
        ]
        cur.executemany("""
            INSERT INTO Plants
            (plant_id, Type_of_Plant, Plantname, Plant_stock, Plant_cost)
            VALUES (%s, %s, %s, %s, %s)
        """, plants)


    # ================= SEEDS =================
    cur.execute("SELECT COUNT(*) FROM Seeds")

    if cur.fetchone()[0] == 0:

        seeds = [
            ("S001", "Cereal", "Rice Seed", 25, 100),
            ("S002", "Cereal", "Wheat Seed", 22, 100),
            ("S003", "Cereal", "Maize Seed", 20, 100),
            ("S004", "Cereal", "Barley Seed", 22, 80),
            ("S005", "Cereal", "Sorghum Seed", 20, 90),
            ("S006", "Cereal", "Millet Seed", 18, 90),
            ("S007", "Cereal", "Ragi Seed", 18, 80),

            ("S008", "Pulse", "Chickpea Seed", 25, 100),
            ("S009", "Pulse", "Pigeon Pea Seed", 28, 90),
            ("S010", "Pulse", "Green Gram Seed", 25, 90),
            ("S011", "Pulse", "Black Gram Seed", 25, 90),
            ("S012", "Pulse", "Lentil Seed", 22, 80),
            ("S013", "Pulse", "Peas Seed", 20, 100),

            ("S014", "Oilseed", "Groundnut Seed", 30, 100),
            ("S015", "Oilseed", "Soybean Seed", 32, 100),
            ("S016", "Oilseed", "Sunflower Seed", 30, 80),
            ("S017", "Oilseed", "Mustard Seed", 25, 100),
            ("S018", "Oilseed", "Sesame Seed", 22, 80),

            ("S019", "Vegetable", "Potato Seed", 18, 120),
            ("S020", "Vegetable", "Onion Seed", 20, 120),
            ("S021", "Vegetable", "Tomato Seed", 25, 120),
            ("S022", "Vegetable", "Brinjal Seed", 22, 100),
            ("S023", "Vegetable", "Cabbage Seed", 20, 100),
            ("S024", "Vegetable", "Cauliflower Seed", 22, 100),
            ("S025", "Vegetable", "Carrot Seed", 18, 100),
            ("S026", "Vegetable", "Radish Seed", 16, 100),
            ("S027", "Vegetable", "Spinach Seed", 15, 100),
            ("S028", "Vegetable", "Lady Finger Seed", 22, 100),
            ("S029", "Vegetable", "Capsicum Seed", 28, 90),
            ("S030", "Vegetable", "Cucumber Seed", 20, 100),

            ("S031", "Fruit", "Mango Seed", 40, 60),
            ("S032", "Fruit", "Banana Seed", 30, 80),
            ("S033", "Fruit", "Papaya Seed", 25, 70),
            ("S034", "Fruit", "Guava Seed", 28, 60),
            ("S035", "Fruit", "Pomegranate Seed", 50, 50),
            ("S036", "Fruit", "Grapes Seed", 45, 70),
            ("S037", "Fruit", "Orange Seed", 35, 60),
            ("S038", "Fruit", "Lemon Seed", 25, 70),
            ("S039", "Fruit", "Watermelon Seed", 22, 100),
            ("S040", "Fruit", "Muskmelon Seed", 20, 100),

            ("S041", "Cash Crop", "Sugarcane Seed", 35, 100),
            ("S042", "Cash Crop", "Cotton Seed", 30, 100),
            ("S043", "Cash Crop", "Jute Seed", 25, 80),
            ("S044", "Cash Crop", "Tea Seed", 40, 60),
            ("S045", "Cash Crop", "Coffee Seed", 50, 60),

            ("S046", "Spice", "Turmeric Seed", 30, 80),
            ("S047", "Spice", "Ginger Seed", 28, 80),
            ("S048", "Spice", "Chilli Seed", 25, 100),
            ("S049", "Spice", "Coriander Seed", 20, 100),
            ("S050", "Spice", "Cardamom Seed", 55, 50)
        ]

        cur.executemany("""
            INSERT INTO Seeds
            (seed_id, Type_of_seed, Seedname, seed_cost, Seed_stock)
            VALUES (%s, %s, %s, %s, %s)
        """, seeds)

    # ================= CROP YIELD =================

    cur.execute("SELECT COUNT(*) FROM CropYield")

    if cur.fetchone()[0] == 0:

        crop_yield = [
            ("Rice", 2023, "Kharif", "Andhra Pradesh", 1200, 4200, 850, 120, 3.50),
            ("Wheat", 2023, "Rabi", "Punjab", 1500, 6000, 900, 100, 4.00),
            ("Maize", 2023, "Kharif", "Karnataka", 1100, 3850, 700, 90, 3.50),
            ("Sugarcane", 2023, "Annual", "Uttar Pradesh", 1800, 12600, 1100, 150, 7.00),
            ("Cotton", 2023, "Kharif", "Maharashtra", 1400, 2100, 650, 110, 1.50),

            ("Rice", 2024, "Kharif", "West Bengal", 1300, 4550, 880, 125, 3.50),
            ("Wheat", 2024, "Rabi", "Madhya Pradesh", 1250, 4750, 750, 90, 3.80),
            ("Soybean", 2024, "Kharif", "Madhya Pradesh", 1600, 2400, 600, 100, 1.50),
            ("Groundnut", 2024, "Kharif", "Gujarat", 1000, 1800, 500, 80, 1.80),
            ("Mustard", 2024, "Rabi", "Rajasthan", 900, 1350, 450, 70, 1.50),

            ("Potato", 2023, "Rabi", "Uttar Pradesh", 1000, 22000, 700, 140, 22.00),
            ("Onion", 2023, "Rabi", "Maharashtra", 950, 19000, 650, 130, 20.00),
            ("Tomato", 2024, "Kharif", "Karnataka", 800, 17600, 600, 150, 22.00),
            ("Chickpea", 2024, "Rabi", "Madhya Pradesh", 1100, 1650, 500, 75, 1.50),
            ("Lentil", 2024, "Rabi", "Bihar", 700, 840, 350, 50, 1.20),

            ("Mango", 2023, "Summer", "Uttar Pradesh", 600, 7200, 300, 80, 12.00),
            ("Banana", 2024, "Annual", "Tamil Nadu", 500, 12500, 400, 100, 25.00),
            ("Turmeric", 2023, "Kharif", "Telangana", 750, 5250, 450, 90, 7.00),
            ("Chilli", 2024, "Kharif", "Andhra Pradesh", 650, 2600, 400, 80, 4.00),
            ("Tea", 2024, "Annual", "Assam", 900, 2250, 350, 60, 2.50)
        ]

        cur.executemany("""
            INSERT INTO CropYield
            (Crop, Year, Season, State, Area, Production,
             Fertilizer, Pesticide, Yield)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, crop_yield)


    # ================= SOIL =================
    cur.execute("SELECT COUNT(*) FROM Soil")

    if cur.fetchone()[0] == 0:

        soil = [
            ("Andhra Pradesh", 78, 45, 22, 6.8),
            ("Arunachal Pradesh", 55, 15, 35, 5.5),
            ("Assam", 60, 18, 38, 5.8),
            ("Bihar", 85, 30, 25, 7.2),
            ("Karnataka", 72, 42, 25, 6.9),
            ("Kerala", 65, 28, 50, 5.7),
            ("Madhya Pradesh", 70, 40, 20, 7.4),
            ("Maharashtra", 75, 43, 26, 7.1),
            ("Punjab", 150, 50, 40, 8.0),
            ("Tamil Nadu", 80, 38, 30, 6.6),
            ("Uttar Pradesh", 120, 45, 35, 7.6),
            ("West Bengal", 85, 40, 45, 6.2)
        ]

        cur.executemany("""
            INSERT INTO Soil(State, N, P, K, pH)
            VALUES (%s, %s, %s, %s, %s)
        """, soil)


    # ================= WATER SOURCE =================
    cur.execute("SELECT COUNT(*) FROM WaterSource")

    if cur.fetchone()[0] == 0:

        water = [
            ("W001", "Borewell", 10000, "Bhopal Rural MP", "Good"),
            ("W002", "Canal", 50000, "Sehore MP", "Moderate"),
            ("W003", "Pond", 20000, "Raisen MP", "Good"),
            ("W004", "River", 150000, "Vidisha MP", "Excellent"),
            ("W005", "Storage Tank", 15000, "Bhopal Rural MP", "Moderate"),
            ("W006", "Tube Well", 12000, "Hoshangabad MP", "Good"),
            ("W007", "Reservoir", 300000, "Indore MP", "Excellent"),
            ("W008", "Open Well", 8000, "Dewas MP", "Moderate"),
            ("W009", "Check Dam", 60000, "Betul MP", "Good"),
            ("W010", "Lake", 200000, "Bhopal MP", "Good")
        ]

        cur.executemany("""
            INSERT INTO WaterSource
            (Water_ID, Source_Type, Capacity_Litres,
             Location, Water_Quality)
            VALUES (%s, %s, %s, %s, %s)
        """, water)


    # ================= WATER SPRINKLER =================
    cur.execute("SELECT COUNT(*) FROM WaterSprinkler")

    if cur.fetchone()[0] == 0:

        sprinklers = [
            ("SP001", "Rotary", 500, 200, 8.0, "Active", 20, 800),
            ("SP002", "Micro-Sprinkler", 300, 100, 5.0, "Active", 25, 500),
            ("SP003", "Impact Sprinkler", 800, 350, 12.0, "Active", 15, 1200),
            ("SP004", "Drip-Sprinkler Hybrid", 200, 80, 3.0, "Maintenance", 10, 650),
            ("SP005", "Gun Sprinkler", 1200, 500, 18.0, "Active", 10, 2000),
            ("SP006", "Pop-up Spray", 150, 60, 2.5, "Active", 30, 400),
            ("SP007", "Oscillating", 400, 180, 6.0, "Active", 15, 700),
            ("SP008", "Center Pivot", 5000, 4000, 60.0, "Active", 5, 8000),
            ("SP009", "Traveling Gun", 3000, 2000, 45.0, "Active", 5, 6000),
            ("SP010", "Rain Gun", 2500, 1500, 40.0, "Inactive", 8, 4500)
        ]

        cur.executemany("""
            INSERT INTO WaterSprinkler
            (Sprinkler_ID, Sprinkler_Type, Capacity_L_per_hr,
             Coverage_Area_sqm, Flow_Rate_L_per_min,
             Status, Stock, Cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, sprinklers)

    con.commit()

# ------------------------------------------------------------
# GENERIC PRETTY TABLE DISPLAY
# ------------------------------------------------------------

def show_table(table_name):
    allowed = [
        "Admin", "Customer", "Address", "Orders", "Planter",
        "Plants", "Seeds", "Soil", "WaterSource",
        "WaterSprinkler", "CropYield"
    ]

    if table_name not in allowed:
        print("Invalid table.")
        return

    cur.execute(f"SELECT * FROM `{table_name}`")
    rows = cur.fetchall()
    headings = [column[0] for column in cur.description]

    table = PrettyTable()
    table.field_names = headings
    table.align = "l"

    for row in rows:
        table.add_row(row)

    print(f"\n========== {table_name} TABLE ==========")
    print(table)


def show_catalogue():
    for name in ["Plants", "Seeds", "Soil", "WaterSource", "WaterSprinkler"]:
        show_table(name)


def display_all_tables():
    for name in [
        "Admin", "Customer", "Address", "Orders", "Planter",
        "Plants", "Seeds", "Soil", "WaterSource",
        "WaterSprinkler", "CropYield"
    ]:
        show_table(name)


# ------------------------------------------------------------
# CUSTOMER ACCOUNT
# ------------------------------------------------------------

def register_customer():

    print("\n--- Create Customer Account ---")

    name = input("Customer name: ").strip()
    username = input("Create username: ").strip()

    if not name or not username:
        print("Name and username are required.")
        return

    # Check username
    cur.execute("""
        SELECT Customer_id
        FROM Customer
        WHERE Customer_username=%s
    """, (username,))

    if cur.fetchone():
        print("Username already exists.")
        return

    # Address details
    city = input("City: ").strip()
    pincode = input("Pincode: ").strip()

    if not city or not pincode:
        print("City and pincode are required.")
        return

    # Password
    password = input("Create password: ")
    confirm_password = input("Confirm password: ")

    if not password:
        print("Password cannot be empty.")
        return

    if password != confirm_password:
        print("Passwords do not match.")
        return

    try:

        # Create address first
        cur.execute("""
            INSERT INTO Address(City, pincode)
            VALUES (%s, %s)
        """, (city, pincode))

        address_id = cur.lastrowid

        # Create customer using Address_id
        cur.execute("""
            INSERT INTO Customer
            (Customer_name,
             Customer_username,
             Customer_password,
             Address_id,
             Customer_money)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            name,
            username,
            password,
            address_id,
            0
        ))

        con.commit()

        print("\nCustomer account created successfully!")
        print("Customer ID:", cur.lastrowid)
        print("Address ID:", address_id)
        print("Starting balance: ₹0")

    except Exception as e:

        con.rollback()
        print("Error creating account:", e)


def customer_login():
    username = input("Username: ").strip()
    password = input("Password: ")

    cur.execute("""
        SELECT Customer_id, Customer_name
        FROM Customer
        WHERE Customer_username=%s AND Customer_password=%s
    """, (username, password))

    customer = cur.fetchone()

    if customer:
        print("Welcome,", customer[1])
        customer_menu(customer[0])
    else:
        print("Invalid username or password.")


def add_money(customer_id):
    try:
        amount = float(input("Amount to add: ₹"))
        if amount <= 0:
            print("Enter an amount greater than zero.")
            return

        cur.execute("""
            UPDATE Customer
            SET Customer_money = Customer_money + %s
            WHERE Customer_id=%s
        """, (amount, customer_id))
        con.commit()
        print("Money added successfully.")
        show_balance(customer_id)

    except ValueError:
        print("Enter a valid amount.")


def show_balance(customer_id):
    cur.execute("""
        SELECT Customer_name, Customer_username, Customer_money
        FROM Customer WHERE Customer_id=%s
    """, (customer_id,))
    row = cur.fetchone()

    table = PrettyTable(["Customer Name", "Username", "Balance (₹)"])
    if row:
        table.add_row(row)
    print(table)


# ------------------------------------------------------------
# CUSTOMER VIEW OPTIONS
# ------------------------------------------------------------

def view_plants():
    show_table("Plants")


def view_seeds():
    show_table("Seeds")


def view_soil():
    show_table("Soil")


def view_water_sources():
    show_table("WaterSource")


def view_sprinklers():
    show_table("WaterSprinkler")


def view_crop_yield():
    show_table("CropYield")


def view_orders(customer_id):
    cur.execute("""
        SELECT Order_id, Item_type, Item_name, quantity,
               Total_cost, Order_date
        FROM Orders
        WHERE Customer_id=%s
        ORDER BY Order_id DESC
    """, (customer_id,))

    rows = cur.fetchall()
    table = PrettyTable([
        "Order ID", "Item Type", "Item Name",
        "Quantity", "Total Cost (₹)", "Date"
    ])
    for row in rows:
        table.add_row(row)

    print(table)


# ------------------------------------------------------------
# PURCHASE PLANTS, SEEDS, OR SPRINKLERS
# ------------------------------------------------------------

def place_order(customer_id):

    print("\n========== Purchase Menu ==========")
    print("1. Plant")
    print("2. Seed")
    print("3. Water Sprinkler")

    choice = input("Choose item type: ").strip()

    # --------------------------------------------------------
    # PLANT
    # --------------------------------------------------------

    if choice == "1":

        show_table("Plants")

        item_id = input("Enter Plant ID (example P001): ").strip()

        cur.execute("""
            SELECT Plantname, Plant_stock, Plant_cost
            FROM Plants
            WHERE plant_id=%s
        """, (item_id,))

        result = cur.fetchone()

        if not result:
            print("Invalid Plant ID.")
            return

        name, stock, cost = result
        table = "Plants"
        item_type = "Plant"

    # --------------------------------------------------------
    # SEED
    # --------------------------------------------------------

    elif choice == "2":

        show_table("Seeds")

        item_id = input("Enter Seed ID (example S001): ").strip()

        cur.execute("""
            SELECT Seedname, Seed_stock, seed_cost
            FROM Seeds
            WHERE seed_id=%s
        """, (item_id,))

        result = cur.fetchone()

        if not result:
            print("Invalid Seed ID.")
            return

        name, stock, cost = result
        table = "Seeds"
        item_type = "Seed"

    # --------------------------------------------------------
    # WATER SPRINKLER
    # --------------------------------------------------------

    elif choice == "3":

        show_table("WaterSprinkler")

        item_id = input(
            "Enter Sprinkler ID (example SP001): "
        ).strip()

        cur.execute("""
            SELECT Sprinkler_Type, Stock, Cost
            FROM WaterSprinkler
            WHERE Sprinkler_ID=%s
        """, (item_id,))

        result = cur.fetchone()

        if not result:
            print("Invalid Sprinkler ID.")
            return

        name, stock, cost = result
        table = "WaterSprinkler"
        item_type = "Sprinkler"

    else:

        print("Invalid choice.")
        return

    # --------------------------------------------------------
    # QUANTITY
    # --------------------------------------------------------

    try:

        quantity = int(input("Enter quantity: "))

    except ValueError:

        print("Quantity must be a number.")
        return

    if quantity <= 0:

        print("Quantity must be greater than 0.")
        return

    if quantity > stock:

        print("Sorry, insufficient stock.")
        print("Available stock:", stock)
        return

    # --------------------------------------------------------
    # CUSTOMER BALANCE
    # --------------------------------------------------------

    total = quantity * float(cost)

    cur.execute("""
        SELECT Customer_money
        FROM Customer
        WHERE Customer_id=%s
    """, (customer_id,))

    balance_result = cur.fetchone()

    if not balance_result:

        print("Customer not found.")
        return

    balance = float(balance_result[0])

    print("\n--------------------------------")
    print("Item:", name)
    print("Item ID:", item_id)
    print("Quantity:", quantity)
    print("Total Cost: ₹", total)
    print("Your Balance: ₹", balance)
    print("--------------------------------")

    if balance < total:

        print("Insufficient balance.")
        print("Please add money first.")
        return

    # --------------------------------------------------------
    # CONFIRM
    # --------------------------------------------------------

    confirm = input("Confirm purchase? (Y/N): ").strip().upper()

    if confirm != "Y":

        print("Purchase cancelled.")
        return

    # --------------------------------------------------------
    # TRANSACTION
    # --------------------------------------------------------

    try:

        if table == "Plants":

            cur.execute("""
                UPDATE Plants
                SET Plant_stock=Plant_stock-%s
                WHERE plant_id=%s
            """, (quantity, item_id))

        elif table == "Seeds":

            cur.execute("""
                UPDATE Seeds
                SET Seed_stock=Seed_stock-%s
                WHERE seed_id=%s
            """, (quantity, item_id))

        elif table == "WaterSprinkler":

            cur.execute("""
                UPDATE WaterSprinkler
                SET Stock=Stock-%s
                WHERE Sprinkler_ID=%s
            """, (quantity, item_id))

        # Deduct money
        cur.execute("""
            UPDATE Customer
            SET Customer_money=Customer_money-%s
            WHERE Customer_id=%s
        """, (total, customer_id))

        # Store order
        cur.execute("""
            INSERT INTO Orders
            (Customer_id,
             Item_type,
             Item_id,
             Item_name,
             quantity,
             Total_cost)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            customer_id,
            item_type,
            item_id,
            name,
            quantity,
            total
        ))

        con.commit()

        print("\n================================")
        print("     ORDER PLACED SUCCESSFULLY")
        print("================================")
        print("Item:", name)
        print("Item ID:", item_id)
        print("Quantity:", quantity)
        print("Total Cost: ₹", total)
        print("Remaining Balance: ₹", balance - total)

    except Exception as e:

        con.rollback()
        print("Order could not be completed:", e)
        
# ------------------------------------------------------------
# CUSTOMER MENU
# ------------------------------------------------------------

def customer_menu(customer_id):
    while True:
        print("\n========== CUSTOMER AREA ==========")
        print("1. View Plants")
        print("2. View Seeds")
        print("3. View Soil Information")
        print("4. View Water Sources")
        print("5. View Water Sprinklers")
        print("6. View Crop Yield")
        print("7. Add Money to Account")
        print("8. Check Account Balance")
        print("9. Purchase Plant, Seed, or Sprinkler")
        print("10. View My Orders")
        print("11. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            view_plants()
        elif choice == "2":
            view_seeds()
        elif choice == "3":
            view_soil()
        elif choice == "4":
            view_water_sources()
        elif choice == "5":
            view_sprinklers()
        elif choice == "6":
            view_crop_yield()
        elif choice == "7":
            add_money(customer_id)
        elif choice == "8":
            show_balance(customer_id)
        elif choice == "9":
            place_order(customer_id)
        elif choice == "10":
            view_orders(customer_id)
        elif choice == "11":
            break
        else:
            print("Invalid choice.")


# ------------------------------------------------------------
# ADMIN ACCOUNT AND LOGIN
# ------------------------------------------------------------

def create_admin():

    admin_id = input("Admin ID: ").strip()
    username = input("Create admin username: ").strip()

    password = input("Create password: ")
    confirm = input("Confirm password: ")

    if not admin_id or not username or not password:
        print("All fields are required.")
        return

    if password != confirm:
        print("Passwords do not match.")
        return

    try:

        cur.execute("""
            INSERT INTO Admin(admin_id, username, pass)
            VALUES (%s,%s,%s)
        """, (admin_id, username, password))

        con.commit()

        print("Admin account created successfully.")

    except mycon.Error as e:

        con.rollback()
        print("Could not create admin:", e)

        


def admin_login():
    username = input("Admin username: ").strip()
    password = input("Admin password: ")

    cur.execute("""
        SELECT admin_id FROM Admin
        WHERE username=%s AND pass=%s
    """, (username, password))

    if cur.fetchone():
        print("Admin login successful.")
        admin_menu()
    else:
        print("Invalid admin username or password.")


def admin_access():
    while True:
        print("\n========== ADMIN SPACE ==========")
        print("1. Existing Admin Login")
        print("2. Create Admin Account")
        print("3. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            admin_login()
        elif choice == "2":
            create_admin()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


# ------------------------------------------------------------
# ADMIN STOCK MANAGEMENT
# ------------------------------------------------------------

def increase_stock():
    print("\n--- Increase Stock ---")
    print("1. Plant")
    print("2. Seed")
    print("3. Water Sprinkler")

    choice = input("Choose category: ")

    try:
        if choice == "1":
            show_table("Plants")
            item_id = input("Plant ID: ").strip()
            quantity = int(input("Quantity to add: "))

            if quantity <= 0:
                print("Enter a positive quantity.")
                return

            cur.execute("""
                UPDATE Plants
                SET Plant_stock=Plant_stock+%s
                WHERE plant_id=%s
            """, (quantity, item_id))

        elif choice == "2":
            show_table("Seeds")
            item_id = input("Seed ID: ").strip()
            quantity = int(input("Quantity to add: "))

            if quantity <= 0:
                print("Enter a positive quantity.")
                return

            cur.execute("""
                UPDATE Seeds
                SET Seed_stock=Seed_stock+%s
                WHERE seed_id=%s
            """, (quantity, item_id))

        elif choice == "3":
            show_table("WaterSprinkler")
            item_id = input("Sprinkler ID: ").strip()
            quantity = int(input("Quantity to add: "))

            if quantity <= 0:
                print("Enter a positive quantity.")
                return

            cur.execute("""
                UPDATE WaterSprinkler
                SET Stock=Stock+%s
                WHERE Sprinkler_ID=%s
            """, (quantity, item_id))

        else:
            print("Invalid choice.")
            return

        if cur.rowcount == 0:
            con.rollback()
            print("Item ID not found.")
        else:
            con.commit()
            print("Stock updated successfully.")

    except ValueError:
        con.rollback()
        print("Enter a valid quantity.")
    except mycon.Error as e:
        con.rollback()
        print("Stock update failed:", e)


# ------------------------------------------------------------
# ADMIN TABLE VIEW
# ------------------------------------------------------------

def admin_menu():
    while True:
        print("\n========== ADMIN MENU ==========")
        print("1. View Plants")
        print("2. View Seeds")
        print("3. View Soil")
        print("4. View Water Sources")
        print("5. View Water Sprinklers")
        print("6. View Crop Yield")
        print("7. Increase Stock")
        print("8. View All Database Tables")
        print("9. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            show_table("Plants")
        elif choice == "2":
            show_table("Seeds")
        elif choice == "3":
            show_table("Soil")
        elif choice == "4":
            show_table("WaterSource")
        elif choice == "5":
            show_table("WaterSprinkler")
        elif choice == "6":
            show_table("CropYield")
        elif choice == "7":
            increase_stock()
        elif choice == "8":
            display_all_tables()
        elif choice == "9":
            break
        else:
            print("Invalid choice.")


# ------------------------------------------------------------
# RESET DATABASE
# ------------------------------------------------------------

def reset_database():
    print("\nWARNING: This will permanently delete all saved data.")
    print("This includes accounts, balances, orders, and stock changes.")

    confirm = input(
        "Type DELETE to remove and recreate the database: "
    ).strip()

    if confirm != "DELETE":
        print("Database reset cancelled.")
        return

    try:
        cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        con.commit()

        create_database()

        print("\nDatabase deleted and recreated successfully.")
        print("The new database contains the table structure")
        print("and the sample catalogue records.")
        print("Create a new admin and customer account to continue.")

    except mycon.Error as e:
        con.rollback()
        print("Database reset failed:", e)


# ------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------

def main_menu():
    while True:
        print("\n===================================")
        print("      PLANT MANAGEMENT SYSTEM")
        print("===================================")
        print("1. Admin")
        print("2. Customer")
        print("3. Exit")
        print("4. Delete and Recreate Database")

        choice = input("Enter choice: ")

        if choice == "1":
            admin_access()

        elif choice == "2":
            print("\n1. Existing Customer Login")
            print("2. Create New Customer Account")
            print("3. Back")

            customer_choice = input("Enter choice: ")

            if customer_choice == "1":
                customer_login()
            elif customer_choice == "2":
                register_customer()

        elif choice == "3":
            print("Thank you for using the system.")
            break

        elif choice == "4":
            reset_database()

        else:
            print("Invalid choice.")


# ------------------------------------------------------------
# START PROGRAM
# ------------------------------------------------------------

create_database()
main_menu()

cur.close()
con.close()
