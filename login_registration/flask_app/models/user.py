from flask_app.config.mysqlconenction import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    
    db = "login_registration"
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
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))

        return users

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1 :
            return False
        print(f"Testing one {results[0]}")
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT * FROM users WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        print(f"Testing 2 {results[0]}")
        return cls(results[0])

    @staticmethod
    def validate_user(user_data):
        is_valid = True
        query ="SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user_data)
        
        if len(results) >= 1:
            flash("Email already existed", "register")
            is_valid = False
        if len(user_data['first_name']) < 3:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(user_data['last_name']) < 3:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user_data['email']):
            flash("Invalid Email address", "register")
            is_valid = False
        if len(user_data['password']) < 8:
            flash("Password must be at least 8 characters long", "register")
            is_valid = False
        if len(user_data['confirmed_password']) < 8:
            flash("Password must be at least 8 characters long", "register")
            is_valid = False    
        if user_data['password'] != user_data['confirmed_password']:
            flash("Password does not match with confirm password", "register")
            is_valid = False
        return is_valid