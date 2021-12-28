from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    analyzers = db.relationship('Analyzer', backref='department', lazy=True)
    lab_tests = db.relationship('LabTest', backref='department', lazy=True)

    def __init__(self, name: str):
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Analyzer(db.Model):
    __tablename__ = 'analyzers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'departments.id'), nullable=False)
    lab_tests = db.relationship('LabTest', backref='analyzer', lazy=True)

    def __init__(self, name: str, status: str, department_id: int):
        self.name = name
        self.status = status
        self.department_id = department_id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'department_id': self.department_id
        }


class LabTest(db.Model):
    __tablename__ = 'lab_tests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'departments.id'), nullable=False)
    analyzer_id = db.Column(db.Integer, db.ForeignKey(
        'analyzers.id'), nullable=False)

    def __init__(self, name: str, department_id: int, analyzer_id: int):
        self.name = name
        self.department_id = department_id
        self.analyzer_id = analyzer_id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'department_id': self.department_id,
            'analyzer_id': self.analyzer_id

        }


# Intermediate table for the many-many relationship between orders and lab tests.
lab_orders = db.Table(
    'lab_orders',
    db.Column(
        'lab_test_id', db.Integer,
        db.ForeignKey('lab_tests.id'),
        primary_key=True
    ),

    db.Column(
        'order_id', db.Integer,
        db.ForeignKey('orders.id'),
        primary_key=True
    ),

    db.Column(
        'created_at', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey(
        'patients.id'), nullable=False)
    ordered_lab_tests = db.relationship(
        'LabTest', secondary=lab_orders,
        lazy='subquery',
        backref=db.backref('orders', lazy=True)
    )

    def __init__(self, patient_id: int):
        self.patient_id = patient_id

    def serialize(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id

        }


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, default=None)
    age = db.Column(db.String, default=None)
    gender = db.Column(db.String, default=None)
    orders = db.relationship('Order', backref='patient', lazy=True)

    def __init__(self, first_name: str, last_name: str, age: int, gender: str):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender
        }
