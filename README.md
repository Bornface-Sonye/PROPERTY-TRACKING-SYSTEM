# Gate Pass System

## Overview

The **Gate Pass System** is an application designed to efficiently track and manage the movement of members with their belongings, such as laptops, cars, and other properties. This system aims to eliminate manual paperwork by securely recording and tracking all items and their owners electronically. It is built to be used by security officers to verify the movement of items at entry and exit points, ensuring only authorized individuals can take their belongings out.

The system is portable, user-friendly, and designed for seamless operation at any security checkpoint. It integrates secure authentication mechanisms to verify both individuals and their items.

## Key Features

1. **Item Registration**:
   - Register laptops, cars, and other properties with member details, such as member ID, serial number (for laptops), number plate (for cars), and a secure password.
   - Each registered item is assigned a unique identifier (QR code for laptops, number plate for cars) to facilitate authentication at the gate.

2. **Authentication at Gate**:
   - Members can authenticate their exit by scanning their generated QR code (for laptops) or entering the number plate (for cars) along with the associated password.
   - The system verifies the details against the database and ensures that the item is allowed to leave with the member.

3. **Password Protection**:
   - A password is tied to each item during registration and is required for authentication, ensuring that only the authorized member can take the item out.

4. **User Interface (UI)**:
   - The system is equipped with a simple and intuitive graphical user interface (GUI) built using **PyQt5** for easy operation by security officers.
   - The interface includes sections for registering items, generating QR codes, authenticating items, and managing the database.

5. **Portable and User-Friendly**:
   - The system is designed to be deployed on devices such as tablets, laptops, or any other portable devices used at security checkpoints.

6. **Database Integration**:
   - The system uses **SQLite** for local database management to store member information, item details, passwords, and authentication records.

## System Architecture

### 1. **Database Interaction (`database.py`)**:
   - Handles interactions with the SQLite database, including setting up tables, registering new items, and verifying member details.
   - Stores details like member IDs, serial numbers (for laptops), number plates (for cars), passwords, and QR code data.

### 2. **User Interface (`ui.py`)**:
   - Built with PyQt5, the UI allows security officers to enter member details, register items, generate QR codes, and authenticate items.
   - The UI includes input fields for member ID, serial number, number plate, password, and buttons to trigger item registration and authentication.

### 3. **QR Code Generation (`qr_code.py`)**:
   - Dynamically generates QR codes for laptops, which are linked to member IDs, serial numbers, and passwords.
   - These QR codes are used for easy scanning during authentication at the gate.

### 4. **Main Program (`main.py`)**:
   - The entry point for the application that initializes the database, sets up the PyQt5 application, and manages the flow between different UI windows (registration, authentication, etc.).

### 5. **Authentication Logic (`authenticate.py`)**:
   - Verifies the member's details (QR code, number plate, and password) against the records in the database.
   - Ensures that the authentication is successful before allowing the item to be taken out.

## Installation

### Prerequisites

To run this application, ensure you have Python 3.x installed on your machine. You will also need to install the following dependencies:

- **PyQt5**: For building the graphical user interface (GUI).
- **qrcode**: For generating QR codes for laptops.
- **SQLite3**: For local database management.

### Setting Up

1. **Clone or Download the Repository**:
   Clone the repository or download the project folder to your local machine.

   ```bash
   git clone https://github.com/Bornface-Sonye/Gate-Pass-System.git
   cd C:\Users\ADMIN\Desktop\GPS
   move to the project folder and run the command: python main.py to interact with the application
