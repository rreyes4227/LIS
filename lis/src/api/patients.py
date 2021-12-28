from os import name
from flask import Blueprint, jsonify, abort, request
from sqlalchemy.orm import backref
from ..models import Patient, db

bp = Blueprint('patients', __name__, url_prefix='/patients')


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    patients = Patient.query.all()  # ORM performs SELECT query
    result = []
    for p in patients:
        result.append(p.serialize())  # build list of orders as dictionaries
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    p = Patient.query.get_or_404(id)
    return jsonify(p.serialize())


@bp.route('/<int:id>/patient_orders', methods=['GET'])
def patient_orders(id: int):
    p = Patient.query.get_or_404(id)
    result = []
    orders = p.orders
    for order in orders:
        result.append(order.serialize())
    return jsonify(result)


@bp.route('', methods=['POST'])
def create():
    if 'first_name' not in request.json:
        return abort(400)
    p = Patient(
        first_name=request.json['first_name'],
        last_name=request.json['last_name'],
        age=request.json['age'],
        gender=request.json['gender']
    )
    db.session.add(p)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(p.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    p = Patient.query.get_or_404(id)
    try:
        db.session.delete(p)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    p = Patient.query.get_or_404(id)
    try:
        if 'first_name' in request.json:
            p.first_name = request.json['first_name']
            db.session.commit()

            if 'last_name' in request.json:
                p.first_name = request.json['last_name']
                db.session.commit()

                if 'age' in request.json:
                    p.age = request.json['age']
                    db.session.commit()

                    if 'gender' in request.json:
                        p.gender = request.json['gender']
                        db.session.commit()
                        return jsonify(True)

                    return jsonify(True)

                return jsonify(True)

            return jsonify(True)

        if 'last_name' in request.json:
            p.first_name = request.json['last_name']
            db.session.commit()

            if 'age' in request.json:
                p.age = request.json['age']
                db.session.commit()

                if 'gender' in request.json:
                    p.gender = request.json['gender']
                    db.session.commit()
                    return jsonify(True)

                return jsonify(True)

            return jsonify(True)

        if 'age' in request.json:
            p.age = request.json['age']
            db.session.commit()

            if 'gender' in request.json:
                p.gender = request.json['gender']
                db.session.commit()
                return jsonify(True)

            return jsonify(True)

        if 'gender' in request.json:
            p.gender = request.json['gender']
            db.session.commit()
            return jsonify(True)
    except:
        return jsonify(False)
