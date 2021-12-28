from os import name
from flask import Blueprint, jsonify, abort, request
from sqlalchemy.orm import backref
from ..models import Analyzer, db

bp = Blueprint('analyzers', __name__, url_prefix='/analyzers')


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    analyzers = Analyzer.query.all()  # ORM performs SELECT query
    result = []
    for a in analyzers:
        result.append(a.serialize())  # build list of analyzers as dictionaries
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    a = Analyzer.query.get_or_404(id)
    return jsonify(a.serialize())


@bp.route('/<int:id>/analyzer_lab_tests', methods=['GET'])
def analyzer_lab_tests(id: int):
    result = []
    a = Analyzer.query.get_or_404(id)
    for test in a.lab_tests:
        result.append(test.serialize())
    return jsonify(result)


@bp.route('/<int:id>/analyzer_department', methods=['GET'])
def analyzer_department(id: int):
    a = Analyzer.query.get_or_404(id)
    dept = a.department
    result = dept.serialize()
    return jsonify(result)


@bp.route('', methods=['POST'])
def create():
    if 'name' not in request.json and 'department_id' not in request.json and 'status' not in request.json:
        return abort(400)
    # construct Analyzer
    a = Analyzer(
        name=request.json['name'],
        department_id=request.json['department_id'],
        status=request.json['status']
    )
    db.session.add(a)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(a.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    a = Analyzer.query.get_or_404(id)
    try:
        db.session.delete(a)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    a = Analyzer.query.get_or_404(id)
    try:
        if 'name' in request.json:
            a.name = request.json['name']
            db.session.commit()

            if 'department_id' in request.json:
                a.department_id = request.json['department_id']
                db.session.commit()

                if 'status' in request.json:
                    a.status = request.json['status']
                    db.session.commit()
                    return jsonify(True)

                return jsonify(True)

            if 'status' in request.json:
                a.status = request.json['status']
                db.session.commit()
                return jsonify(True)

            return jsonify(True)

        if 'department_id' in request.json:
            a.department_id = request.json['department_id']
            db.session.commit()

            if 'status' in request.json:
                a.status = request.json['status']
                db.session.commit()
                return jsonify(True)

            return jsonify(True)

        if 'status' in request.json:
            a.status = request.json['status']
            db.session.commit()
            return jsonify(True)
    except:
        return jsonify(False)
