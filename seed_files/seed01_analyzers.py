import random
from faker import Faker
from lis.src.models import Analyzer, Department, Order, LabTest,  db
from lis.src import create_app


def truncate_tables():
    """Delete all rows from database tables"""
    # db.session.execute(lab_orders.delete())
    Analyzer.query.delete()
    db.session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

    # CREATE Analyzers/Dept
    departments = ['Chemistry', 'Hematology', 'Blood Bank', 'Pathology']
    last_analyzer = None  # save last user
    for dept in departments:
        if dept == 'Chemistry':
            chemistry = Department.query.filter_by(name='Chemistry').first()
            dept_analyzers = ['Roche Cobas', 'Architect C8000']
            for name in dept_analyzers:
                last_analyzer = Analyzer(
                    name=name,
                    status='Active',
                    department_id=chemistry.id
                )
                db.session.add(last_analyzer)
        elif dept == 'Hematology':
            hematology = Department.query.filter_by(name='Hematology').first()
            dept_analyzers = ['MindRay', 'Sysmex X30', 'Heme-Microscope']
            for name in dept_analyzers:
                last_analyzer = Analyzer(
                    name=name,
                    status='Active',
                    department_id=hematology.id
                )
                db.session.add(last_analyzer)
        elif dept == 'Blood Bank':
            blood_bank = Department.query.filter_by(name='Blood Bank').first()
            dept_analyzers = ['ORTHO Visions MAX',
                              'ORTHO Workstation', 'Tube Method']
            for name in dept_analyzers:
                last_analyzer = Analyzer(
                    name=name,
                    status='Active',
                    department_id=blood_bank.id
                )
                db.session.add(last_analyzer)

        elif dept == 'Pathology':
            pathology = Department.query.filter_by(name='Pathology').first()
            dept_analyzers = ['Path-scope', 'Microplane']
            for name in dept_analyzers:
                last_analyzer = Analyzer(
                    name=name,
                    status='Active',
                    department_id=pathology.id
                )
                db.session.add(last_analyzer)

     # insert analyzers
    db.session.commit()


# run script
main()
