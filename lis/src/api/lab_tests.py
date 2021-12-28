from os import name
from flask import Blueprint, jsonify, abort, request
from sqlalchemy.orm import backref
from ..models import LabTest, db

bp = Blueprint('lab_tests', __name__, url_prefix='/lab_tests')


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    lab_tests = LabTest.query.all()  # ORM performs SELECT query
    result = []
    for l in lab_tests:
        result.append(l.serialize())  # build list of lab_tests as dictionaries
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    l = LabTest.query.get_or_404(id)
    return jsonify(l.serialize())


@bp.route('/<int:id>/lab_test_department', methods=['GET'])
def lab_test_department(id: int):
    l = LabTest.query.get_or_404(id)
    dept = l.department
    result = dept.serialize()
    return jsonify(result)


@bp.route('/<int:id>/lab_test_analyzer', methods=['GET'])
def lab_test_analyzer(id: int):
    l = LabTest.query.get_or_404(id)
    dept = l.analyzer
    result = dept.serialize()
    return jsonify(result)


@bp.route('', methods=['POST'])
def create():
    if 'name' not in request.json and 'department_id' not in request.json and 'analyzer_id' not in request.json:
        return abort(400)
    # construct Analyzer
    l = LabTest(
        name=request.json['name'],
        department_id=request.json['department_id'],
        analyzer_id=request.json['analyzer_id']
    )
    db.session.add(l)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(l.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    l = LabTest.query.get_or_404(id)
    try:
        db.session.delete(l)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    l = LabTest.query.get_or_404(id)
    try:
        if 'name' in request.json:
            l.name = request.json['name']
            db.session.commit()

            if 'department_id' in request.json:
                l.department_id = request.json['department_id']
                db.session.commit()

                if 'analyzer_id' in request.json:
                    l.analyzer_id = request.json['analyzer_id']
                    db.session.commit()
                    return jsonify(True)

                return jsonify(True)

            if 'analyzer_id' in request.json:
                l.analyzer_id = request.json['analyzer_id']
                db.session.commit()
                return jsonify(True)

            return jsonify(True)

        if 'department_id' in request.json:
            l.department_id = request.json['department_id']
            db.session.commit()

            if 'analyzer_id' in request.json:
                l.analyzer_id = request.json['analyzer_id']
                db.session.commit()
                return jsonify(True)

            return jsonify(True)

        if 'analyzer_id' in request.json:
            l.analyzer_id = request.json['analyzer_id']
            db.session.commit()
            return jsonify(True)
    except:
        return jsonify(False)
