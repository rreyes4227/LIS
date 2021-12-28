from os import name
from flask import Blueprint, jsonify, abort, request
from sqlalchemy.orm import backref
from ..models import Department, db

bp = Blueprint('departments', __name__, url_prefix='/departments')


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    departments = Department.query.all()  # ORM performs SELECT query
    result = []
    for d in departments:
        # build list of departments as dictionaries
        result.append(d.serialize())
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    d = Department.query.get_or_404(id)
    return jsonify(d.serialize())


@bp.route('/<int:id>/department_analyzers', methods=['GET'])
def department_analyzers(id: int):
    result = []
    d = Department.query.get_or_404(id)
    for analyzer in d.analyzers:
        result.append(analyzer.serialize())
    return jsonify(result)


@bp.route('/<int:id>/department_lab_tests', methods=['GET'])
def department_lab_tests(id: int):
    result = []
    d = Department.query.get_or_404(id)
    for lab_tests in d.lab_tests:
        result.append(lab_tests.serialize())
    return jsonify(result)


@bp.route('', methods=['POST'])
def create():
    if 'name' not in request.json:
        return abort(400)
    # construct Analyzer
    d = Department(
        name=request.json['name']
    )
    db.session.add(d)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(d.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    d = Department.query.get_or_404(id)
    try:
        db.session.delete(d)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    d = Department.query.get_or_404(id)
    try:
        if 'name' in request.json:
            d.name = request.json['name']
            db.session.commit()
            return jsonify(True)
    except:
        return jsonify(False)
