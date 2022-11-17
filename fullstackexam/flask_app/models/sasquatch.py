from flask_app.config.mysqlconenction import connectToMySQL
from flask import flash
from flask_app.models import user

db = "fullstackexam"

class Sasquatch:
    
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.siting_date = data['siting_date']
        self.sasquatch = data['sasquatch']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def create_valid_report(cls, report):
        if not cls.is_valid(report):
            return False
        print(f"printing report{report}")
        query = """
            INSERT INTO sasquatches (location, description, siting_date, sasquatch, user_id) 
            VALUES (%(location)s, %(description)s, %(siting_date)s, %(sasquatch)s, %(user_id)s);
        """
        report_id = connectToMySQL(db).query_db(query, report)
        
        print(f"Printing report_id {report_id}")

        report = cls.get_by_id(report_id)

        return report
    
    @classmethod
    def get_by_id(cls, report_id):
        print(f"get report by id {report_id}")
        data = { 'id' : report_id}
        query = """
            SELECT sasquatches.id, sasquatches.created_at, sasquatches.updated_at, location, description, siting_date, sasquatch,
            users.id as user_id, first_name, last_name, email, users.created_at as UC, users.updated_at as UU
            FROM sasquatches JOIN users on users.id = sasquatches.user_id
            WHERE sasquatches.id = %(id)s;
        """

        result = connectToMySQL(db).query_db(query,data)
        print(f"PRINTING ID {result}")
        if len(result) < 0:
            return False
        result = result[0]

        report = cls(result)

        report.user = user.User(
            {
                "id" : result['user_id'],
                "first_name" : result['first_name'],
                "last_name" : result['last_name'],
                "email" : result['email'],
                "password": "",
                "confirmed_password" : "",
                "created_at" : result['UC'],
                "updated_at" : result['UU']
            }
        )
        return report

    @classmethod
    def delete_report_by_id(cls, report_id):
        data = {
            "id": report_id
        }
        query = """
            DELETE FROM sasquatches WHERE id = %(id)s;
        """
        connectToMySQL(db).query_db(query, data)
        return report_id

    @classmethod
    def update_report(cls, report, session_id):
        report = cls.get_by_id(report['id'])
        if report.user.id != session_id:
            flash("You must be the person who reported it.")
            return False
        if not cls.is_valid(report):
            return False
        query = """
            UPDATE sasquatches SET location = %(location)s, description = %(description), siting_date = %(siting_date)s, sasquatch = %(sasquatch)s
            WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, report)
        report = cls.get_by_id(report['id'])
        return report

    @classmethod
    def get_all(cls):
        query = """
            SELECT sasquatches.id, sasquatches.created_at, sasquatches.updated_at, location, description, siting_date, sasquatch,
            users.id as user_id, first_name, last_name, email, users.created_at as UC, users.updated_at as UU
            from sasquatches JOIN users on users.id = sasquatches.user_id;
        """
        results = connectToMySQL(db).query_db(query)
        reports = []

        for report in results:

            report_instance = cls(report)

            report_instance.user = user.User(
                {
                    "id" : report['user_id'],
                "first_name" : report['first_name'],
                "last_name" : report['last_name'],
                "email" : report['email'],
                "password" : "",
                "confirmed_password" : "",
                "created_at" : report['UC'],
                "updated_at" : report['UU']
                }
            )
            reports.append(report_instance)
        return reports

    @staticmethod
    def is_valid(report):
        valid = True
        flash_error = "is required and must be at least 2 characters."

        if len(report['location']) < 3:
            flash("location" + flash_error)
            valid = False
        if len(report['description']) < 3:
            flash("Description" + flash_error)
            valid = False
        if len(report['siting_date']) <= 0:
            flash("Date is required")
            valid = False
        if len(report['sasquatch']) < 0:
            flash("Numbes of sasquatch must be at least 1.")
            valid = False

        return valid



    
        