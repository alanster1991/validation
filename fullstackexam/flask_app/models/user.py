from flask_app.config.mysqlconenction import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
import re


bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = "fullstackexam"

class User:
    
 
    def __init__(self, data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.confirmed_password = data['confirmed_password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM users;
        """
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))

        return users

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        data = {
            "email": email
        }
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(db).query_db(query, data)

        if len(results) < 1 :
            return False
        print(f"Testing one {results[0]}")
        return cls(results[0])

    @classmethod
    def get_by_id(cls, user_id):
        data = {
            "id" : user_id
        }
        query = """
            SELECT * FROM users WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        print(f"Testing 2 {result[0]}")
        return cls(result[0])
    
    @classmethod
    def login_verification(cls, user_input):
        valid = True
        email_in_db = cls.get_by_email(user_input['email'])
        password_validation = True
        
        if not email_in_db:
            valid = False
        
        else:
            password_validation = bcrypt.check_password_hash(email_in_db.password, user_input['password'])
            
            if not password_validation:
                valid = False
        
        if not valid:
            flash("Invalid email and password")
            return False
        
        return email_in_db

    @classmethod
    def create_valid_user(cls, user):
        if not cls.is_valid(user):
            return False

        pw_hash = bcrypt.generate_password_hash(user['password'])
        user = user.copy()
        user['password'] = pw_hash
        query = """INSERT INTO users (first_name, last_name, email, password) 
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""

        user_id = connectToMySQL(db).query_db(query, user)
        new_user = cls.get_by_id(user_id)
        return new_user
    @classmethod
    def is_valid(cls, user):
        is_valid = True
        email_has_account = User.get_by_email(user['email'])
        if email_has_account:
            flash("email already exists, please log in again")
            return False
        if len(user['first_name']) < 3:
            flash("First name must be at least 2 characters")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("First name must be at least 2 characters")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email address")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long")
            is_valid = False
        if len(user['confirmed_password']) < 8:
            flash("Password must be at least 8 characters long")
            is_valid = False    
        if user['password'] != user['confirmed_password']:
            flash("Password does not match with confirm password")
            is_valid = False
        return is_valid
    