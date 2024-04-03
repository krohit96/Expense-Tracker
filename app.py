import calendar

from flask import Flask, render_template, redirect, url_for, flash, request, get_flashed_messages
from flask import session
from flask_login import logout_user, login_required, current_user, login_user

from extensions import db, bcrypt, login_manager
from forms import ExpenseForm, BudgetForm, RegistrationForm, LoginForm
from models import Expense, Users

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'A\x8e\x185l\xf7mc\\\xd3\t\x00\xcdr\xf6\xc1@\x06v\xb00\xadj)'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost:5432/projects'

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)


def init_db():
    with app.app_context():
        db.create_all()


# ... Other possible configurations and initializations ...

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Create a new user instance (assuming you have a User model defined)
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        session.pop('_flashes', None)

        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        # Inform the user and redirect to the login page
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))  # Assuming you have a 'login' route

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create an instance of the LoginForm

    if form.validate_on_submit():  # Check if form is submitted and validated
        user = Users.query.filter_by(email=form.email.data).first()

        if user:
            # Use bcrypt's check_password_hash function
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)  # Use Flask-Login to handle the user session
                flash('Logged in successfully!')
                return redirect(url_for('home'))
            else:
                flash('Invalid password.')
        else:
            flash('Email not registered.')

    # Always pass the form object to the template
    return render_template('login.html', form=form)


@app.route('/home')
@login_required
def home():
    expenses = Expense.query.filter_by(owner=current_user).all()
    return render_template('home.html', expenses=expenses)


@app.route('/logout')
@login_required
def logout():
    logout_user()  # this function is from flask_login
    session.clear()  # Clear the session
    get_flashed_messages()  # Clear any old messages
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(title=form.title.data, amount=form.amount.data, category=form.category.data,
                          date=form.date.data, user_id=current_user.id)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_expense.html', form=form)


@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    # Ensure that the user is editing their own expense
    if expense.user_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('home'))

    form = ExpenseForm()

    if form.validate_on_submit():
        expense.title = form.title.data
        expense.amount = form.amount.data
        expense.category = form.category.data
        expense.date = form.date.data
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = expense.title
        form.amount.data = expense.amount
        form.category.data = expense.category
        form.date.data = expense.date
    return render_template('edit_expense.html', form=form, expense=expense)


@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    # Ensure that the user is deleting their own expense
    if expense.user_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('home'))

    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/reports')
@login_required
def reports():
    # Use Flask-SQLAlchemy's session to execute raw SQL
    result = db.session.execute("""
        SELECT EXTRACT(MONTH FROM date) as month, SUM(amount) as total
        FROM expense
        WHERE user_id = :user_id
        GROUP BY EXTRACT(MONTH FROM date);
    """, {'user_id': current_user.id})

    # Fetch the results. Flask-SQLAlchemy's execute method returns a ResultProxy which can be directly converted to a
    # list of RowProxy objects.
    monthly_totals = result.fetchall()

    # Convert RowProxy objects to dictionaries and update month numbers to month names
    monthly_totals_dict = []
    for record in monthly_totals:
        record_dict = dict(record)
        record_dict['month'] = calendar.month_name[int(record_dict['month'])]
        monthly_totals_dict.append(record_dict)

    # Render the template and pass the results to it
    return render_template('reports.html', monthly_totals=monthly_totals_dict)


# If this script is executed, run the app
if __name__ == '__main__':
    ## init_db()  # Initialize the database tables
    app.run(debug=True)
