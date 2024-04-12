# Expense Tracker Application

The Expense Tracker Application is a web-based tool designed to help users manage their finances by tracking expenses over time. Built with Flask, this application offers a simple and intuitive interface for adding, editing, and deleting expenses, as well as viewing monthly expense reports.

## Features

- **User Registration and Login**: Secure sign-up and login functionality for personal expense management.
- **Add Expenses**: Users can add expenses by specifying the title, amount, category, and date.
- **View Expenses**: Users can view a list of their expenses on their dashboard.
- **Edit Expenses**: Users have the ability to edit any previously entered expense.
- **Delete Expenses**: Users can delete their expenses.
- **Monthly Expense Reports**: Users can view monthly summaries of their expenses to better understand their spending patterns.

## Technologies

- **Flask**: A micro web framework written in Python.
- **Flask-Login**: For handling user authentication sessions.
- **Flask-SQLAlchemy**: For ORM and database interactions.
- **Flask-WTF**: For form handling.
- **PostgreSQL**: As the database backend.
- **bcrypt**: For hashing user passwords.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.x
- pip
- Virtualenv (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
2. Navigate to the project directory:
   ```bash
   cd expense-tracker
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
4. Activate the virtual environment:
   ```bash
   .\venv\Scripts\activate
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
6. Set up the database:
   - Make sure PostgreSQL is installed and running.
   - Create a new database for the application.
   - Modify the SQLALCHEMY_DATABASE_URI in your application to reflect your PostgreSQL settings.
7. Initialize the database:
   ```bash
   flask shell
   from your application import db
   db.create_all()
   exit()
8. Start the application:
   ```bash
   flask run

## Usage
After starting the application, visit http://127.0.0.1:5000/ in your web browser to access the Expense Tracker Application.
- Register for a new account or login.
- Use the navigation links to add, view, edit, or delete expenses.
- Visit the reports section to view your monthly expense summary.

