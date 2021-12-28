import random
from faker import Faker
from lis.src.models import Analyzer, Department, Order, LabTest, Patient, lab_orders, db
from lis.src import create_app


LAB_TEST_COUNT = 200
ORDER_COUNT = 400


def truncate_tables():
    """Delete all rows from database tables"""
    db.session.execute(lab_orders.delete())
    Order.query.delete()
    LabTest.query.delete()
    db.session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

# CREATE ORDERS
    last_order = None
    patients = Patient.query.all()
    for _ in range(ORDER_COUNT):
        rand_patient = random.choice(patients)
        last_order = Order(
            patient_id=rand_patient.id
        )
        db.session.add(last_order)

    # insert orders
    db.session.commit()

    # CREATE LAB_TESTS
    last_lab_test = None
    analyzers = Analyzer.query.all()
    for _ in range(LAB_TEST_COUNT):
        rand_analyzer = random.choice(analyzers)
        last_lab_test = LabTest(
            name=fake.word(),
            department_id=rand_analyzer.department_id,
            analyzer_id=rand_analyzer.id
        )
        db.session.add(last_lab_test)

    # insert lab_tests
    db.session.commit()

    lab_test_order_pairs = set()
    while len(lab_test_order_pairs) < ORDER_COUNT:

        candidate = (
            random.randint(last_lab_test.id - LAB_TEST_COUNT +
                           1, last_lab_test.id),   # lab_test range
            random.randint(last_order.id - ORDER_COUNT + 1,
                           last_order.id)  # order_id range
        )

        if candidate in lab_test_order_pairs:
            continue  # pairs must be unique

        lab_test_order_pairs.add(candidate)

    new_orders = [{"lab_test_id": pair[0], "order_id": pair[1]}
                  for pair in list(lab_test_order_pairs)]
    insert_likes_query = lab_orders.insert().values(new_orders)
    db.session.execute(insert_likes_query)

    # insert likes
    db.session.commit()


# run script
main()
