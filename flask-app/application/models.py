from application import db 
from flask_login import UserMixin
import bcrypt

# User Table
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Integer, nullable=False, default=0)
    record = db.relationship('Record', backref='record_user_br')
    request = db.relationship('Request', backref='request_user_br')
    review = db.relationship('Review', backref='review_user_br')
    transaction = db.relationship('Transaction', backref='transaction_user_br')

# User Record Table
class Record(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    num_books_hired = db.Column(db.Integer)
    num_books_returned = db.Column(db.Integer)
    current_num_books = db.Column(db.Integer)

# Books Table
class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    num_of_copies = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    review = db.relationship('Review', backref='review_book_br')
    transaction = db.relationship('Transaction', backref='transaction_book_br')

# Request Table
class Request(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)

# Review Table
class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    review = db.Column(db.String(200), nullable=False)

# Transaction Table
class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    issue_date = db.Column(db.Date(), nullable=False)
    return_date = db.Column(db.Date(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
    
# create database tables and relationships 
db.create_all()

# create an admin account, would be in a .gitignore file, but is left here for testing purposes
# first we need to check if the admin account exists because we only want to create the account once
user = User.query.filter_by(email="Admin@gmail.com").first()

if user:
    # do nothing
    pass 
else:
    # generate a salt
    salt = bcrypt.gensalt()
    # encode the string (password)
    encoded_pass = "Password123".encode('UTF-8')
    # hash the password 
    hashed_password = bcrypt.hashpw(encoded_pass, salt)
    # create a new user object
    new_user = User(
        first_name = "Admin",
        last_name = "User",
        email = "Admin@gmail.com",
        address = "Admin HQ, LAX",
        password = hashed_password,
        is_admin = 1
    )
    # add and commit user to database
    db.session.add(new_user)
    db.session.commit()
    

