"""
Populate lis Department and Patient data using faker. 
"""

import random
from faker import Faker
from lis.src.models import Department, Patient, db
from lis.src import create_app

PATIENT_COUNT = 150


def truncate_tables():
    """Delete all rows from database tables"""
    # db.session.execute()
    Department.query.delete()
    Patient.query.delete()
    db.session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

    # CREATE DEPARTMENTS
    departments = ['Chemistry', 'Hematology', 'Blood Bank', 'Pathology']
    last_department = None  # save last user
    for dept in departments:
        last_department = Department(
            name=dept
        )
        db.session.add(last_department)

    # CREATE PATIENTS
    last_patient = None  # save last tweet
    genders = ['male', 'female', 'non-binary', 'other']
    for _ in range(PATIENT_COUNT):
        last_patient = Patient(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            age=random.randint(0, 100),
            gender=random.choice(genders)
        )
        db.session.add(last_patient)

    # insert tweets
    db.session.commit()


# run script
main()
