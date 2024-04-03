from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        from models import Users
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')

    def validate_email(self, email):
        from models import Users
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use. Please choose a different one or log in.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    # Custom Validator for Gmail Address
    def validate_email(form, field):
        if "@gmail.com" not in field.data:
            raise ValidationError('Please enter a valid Gmail address.')


class ExpenseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    amount = FloatField('Amount', validators=[DataRequired()])
    category = SelectField('Category',
                           choices=[('food', 'Food'), ('transport', 'Transport'), ('entertainment', 'Entertainment'),
                                    ('other', 'Other')], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Expense')


class BudgetForm(FlaskForm):
    amount = FloatField('Budget Amount', validators=[DataRequired()])
    submit = SubmitField('Set Budget')
