from os import name
from flask import Blueprint, jsonify, abort, request
from sqlalchemy.orm import backref
from ..models import Order, db

bp = Blueprint('orders', __name__, url_prefix='/orders')


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    orders = Order.query.all()  # ORM performs SELECT query
    result = []
    for o in orders:
        result.append(o.serialize())  # build list of orders as dictionaries
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    o = Order.query.get_or_404(id)
    return jsonify(o.serialize())


@bp.route('/<int:id>/order_details', methods=['GET'])
def order_details(id: int):
    o = Order.query.get_or_404(id)
    result = []
    result.append(o.patient.serialize())
    lab_tests = o.ordered_lab_tests
    for test in lab_tests:
        result.append(test.serialize())
    return jsonify(result)


@bp.route('', methods=['POST'])
def create():
    if 'patient_id' not in request.json:
        return abort(400)
    # construct Analyzer
    o = Order(
        patient_id=request.json['patient_id']
    )
    db.session.add(o)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(o.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    o = Order.query.get_or_404(id)
    try:
        db.session.delete(o)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    o = Order.query.get_or_404(id)
    try:
        if 'patient_id' in request.json:
            o.name = request.json['name']
            db.session.commit()
            return jsonify(True)
    except:
        return jsonify(False)
