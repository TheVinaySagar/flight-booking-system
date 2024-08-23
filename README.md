# Flight Booking System

## Overview

The Flight Booking System is a web-based application designed to manage flight reservations. It allows users to search for flights, book tickets, and manage their bookings. Additionally, there is an admin interface to manage flights, view bookings, and perform administrative tasks.

## Features

### User Features
- **Sign Up / Log In:** Users can create an account and log in to access the system.
- **Search Flights:** Users can search for flights based on date and time.
- **Book Tickets:** Users can book tickets for flights with available seats.
- **My Bookings:** Users can view a list of all their bookings.
- **Log Out:** Users can securely log out of the system.

### Admin Features
- **Admin Log In:** Admins have a separate login to access administrative functions.
- **Add Flights:** Admins can add new flights to the system.
- **Remove Flights:** Admins can remove existing flights from the system.
- **View All Bookings:** Admins can view bookings based on flight number and time.

## Tech Stack

- **Backend Framework:** Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS
- **ORM:** SQLAlchemy (Flask-SQLAlchemy)
- **Python Version:** 3.8+

## Installation

### Prerequisites
- Python 3.8+
- MySQL Server
- Virtual Environment (recommended)

### Setup Instructions

1. **Clone the Repository**
    ```bash
    git clone https://github.com/TheVinaySagar/flight-booking-system.git
    cd flight-booking-system
    ```

2. **Set Up a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure MySQL Database**
    - Create a MySQL database.
    - Update the `Config` class in `config.py` with your database credentials.

5. **Run Migrations**
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

6. **Start the Application**
    ```bash
    python run.py
    ```

7. **Access the Application**
    - Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

### Accessing the Admin Interface
- The admin interface can be accessed by logging in with an admin account.

### Sample Data
- The system is pre-populated with sample flight data for testing purposes. Use the Admin interface to manage these entries.

### Error Handling
- The system handles duplicate entries, and provides meaningful error messages for user input validation.

## Folder Structure

```plaintext
.
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── signup.html
│   │   ├── login.html
│   │   ├── search_flights.html
│   │   ├── my_bookings.html
│   │   ├── admin_login.html
│   │   ├── add_flight.html
│   │   ├── remove_flight.html
│   │   ├── view_bookings.html
│   ├── static/
│       ├── styles/
│           ├── index.css
│           ├── signup.css
│           ├── login.css
│           ├── search_flights.css
│           ├── my_bookings.css
│           ├── admin_login.css
│           ├── add_flight.css
│           ├── remove_flight.css
│           ├── view_bookings.css
├── config.py
├── run.py
├── README.md
├── requirements.txt
