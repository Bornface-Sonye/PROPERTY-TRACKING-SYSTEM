import sqlite3

def setup_database():
    conn = sqlite3.connect("gate_pass.db")
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS laptops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT,
        serial_number TEXT,
        qr_code_data TEXT,
        password TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT,
        number_plate TEXT,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

def register_laptop(member_id, serial, qr_data, password):
    conn = sqlite3.connect("gate_pass.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO laptops (member_id, serial_number, qr_code_data, password)
    VALUES (?, ?, ?, ?)
    """, (member_id, serial, qr_data, password))
    conn.commit()
    conn.close()

def register_car(member_id, number_plate, password):
    conn = sqlite3.connect("gate_pass.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO cars (member_id, number_plate, password)
    VALUES (?, ?, ?)
    """, (member_id, number_plate, password))
    conn.commit()
    conn.close()

def authenticate_laptop(input_data, password):
    conn = sqlite3.connect("gate_pass.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM laptops WHERE qr_code_data=? AND password=?
    """, (input_data, password))
    laptop = cursor.fetchone()
    conn.close()
    return laptop

def authenticate_car(input_data, password):
    conn = sqlite3.connect("gate_pass.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM cars WHERE number_plate=? AND password=?
    """, (input_data, password))
    car = cursor.fetchone()
    conn.close()
    return car
