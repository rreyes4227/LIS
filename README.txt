Title: Mock Laboratory Information System (LIS)
Description: This is a fully contained backend built on the Flask microframework. It implements 
            a database structure with one to one, one to many, and many to many relationship types created
            using Flask-SQLAlchemy and Alembic. The ORM approach allows the database to be built using 
            Object Oriented Programming and migrations in order to quickly replicate this structure on 
            various databases (PostgreSQL, MySQL, etc).
            This backend also has defined API Endpoints used to access different attributes from the tables.
            There is three seed files attached that will populate the tables that are created with random 
            information using Faker. This data is used for the sole pupose of testing and tables should be 
            trucated prior to implemintation. 
API End Points:
    Analyzers Table 
        /analyzers
            GET request that returns JSON data of every analyzer in the Analyzers table. 
            JSON data includes:
                department_id
                id
                name
                status
        /analyzers/<int:id>
            GET request that returns JSON data of specified analyzer ID 
            JSON data includes:
                department_id
                id
                name
                status
        /analyzers/<int:id>/analyzer_lab_tests
            GET reqeust that returns JSON data of all available lab tests that are linked to a specific analyzer ID
            JSON data includes:
                analyzer_id
                department_id
                id (lab test ID)
                name (lab test name)
        /analyzers/<int:id>/analyzer_department
            GET request that returns JSON data of the department linked to the specified analyzer ID
            JSON data includes:
                id (department id)
                name (department name)
        /analyzers
            POST request that creates a new analyzer record in the Analyzers table. 
            Returns error 400 if request does not include the following required parameters in JSON:
                name
                department_id
                status
        /analyzers/<int:id>
            DELETE request that deletes the specified Analyzer ID. Returns True if successful and False
            if not successful. 
        /analyzers/<int:id>
            PUT request that updates any of the following fields passed in JSON format for a spcified analyzer ID
                name
                department_id
                status

    Departments Table 
        /departments
            GET request that returns JSON data of every department in the Departments table. 
            JSON data includes:
                id
                name
        /departments/<int:id>
            GET request that returns JSON data of specified department ID 
            JSON data includes:
                id
                name
        /departments/<int:id>/department_analyzers
            GET reqeust that returns JSON data of all available analyzers that are linked to a specific department ID
            JSON data includes:
                id
                department_id (analyzer department_id)
                status (analyzer status)
                name (analyzer name)
        /departments/<int:id>/department_lab_tests
            GET request that returns JSON data of all the lab tests linked to the specified department ID
            JSON data includes:
                id (lab test id)
                name (lab test name)
                department_id
                analyzer_id
        /departments
            POST request that creates a new department record in the Departments table. 
            Returns error 400 if request does not include the following required parameters in JSON:
                name
        /departments/<int:id>
            DELETE request that deletes the specified Department ID. Returns True if successful and False
            if not successful. 
        /departments/<int:id>
            PUT request that updates any of the following fields passed in JSON format for a spcified analyzer ID
                name

    Lab Tests Table 
        /lab_tests
            GET request that returns JSON data of every lab test in the lab_tests table. 
            JSON data includes:
                id
                name
                analyzer_id
                department_id
        /lab_tests/<int:id>
            GET request that returns JSON data of specified lab test ID 
            JSON data includes:
                id
                name
                analyzer_id
                department_id
        /lab_tests/<int:id>/lab_test_department
            GET reqeust that returns JSON data of department that is linked to a specific lab test ID
            JSON data includes:
                id (department id)
                name (department name)
        /lab_tests/<int:id>/lab_test_analyzer
            GET request that returns JSON data of the analyzer linked to the specified lab test ID
            JSON data includes:
                id (analyzer id)
                name (analyzer name)
                department_id
                status (analyzer status)
        /lab_tests
            POST request that creates a new lab test record in the lab_tests table. 
            Returns error 400 if request does not include the following required parameters in JSON:
                name
                department_id
                analyzer_id
        /lab_tests/<int:id>
            DELETE request that deletes the specified lab test ID. Returns True if successful and False
            if not successful. 
        /lab_tests/<int:id>
            PUT request that updates any of the following fields passed in JSON format for a spcified lab test ID
                name
                department_id
                analyzer_id

    Orders Table 
        /orders
            GET request that returns JSON data of every order in the Orders table. 
            JSON data includes:
                id
                patient_id
        /orders/<int:id>
            GET request that returns JSON data of specified order ID 
            JSON data includes:
                id
                patient_id
        /orders/<int:id>/order_details
            GET reqeust that returns JSON data of the customer and the lab tests that are linked to a specific order ID
            JSON data includes:
            Index 0 will be the patient information
                id
                first_name
                last_name
                age
                gender
            The rest of the list will be each lab test (1 or more lab tests)
                id (lab test id)
                name (lab test name)
                analyzer_id
                department_id
        /orders
            POST request that creates a order record in the orders table. 
            Returns error 400 if request does not include the following required parameters in JSON:
                patient_id
        /orders/<int:id>
            DELETE request that deletes the specified order ID. Returns True if successful and False
            if not successful. 
        /orders/<int:id>
            PUT request that updates any of the following fields passed in JSON format for a spcified lab test ID
                patient_id
                
    Patients Table 
        /patients
            GET request that returns JSON data of every patient in the lab_tests table. 
            JSON data includes:
                id
                first_name
                last_name
                age
                gender
        /patients/<int:id>
            GET request that returns JSON data of specified patients ID 
            JSON data includes:
                id
                first_name
                last_name
                age
                gender
        /patients/<int:id>/patient_orders
            GET reqeust that returns JSON data of orders that are linked to a specific patient ID
            JSON data includes:
                id (order id)
                patient_id
        /patients
            POST request that creates a new lab test record in the lab_tests table. 
            Returns error 400 if request does not include the following required parameters in JSON:
                first_name
            Optional fields include:
                age
                gender
                last_name
            ALL FIELDS MUST BE INCLUDED IN THE JSON. Pass an empty string for the optional fields if you wish for Null.
        /patients/<int:id>
            DELETE request that deletes the specified patient ID. Returns True if successful and False
            if not successful. 
        /patient/<int:id>
            PUT request that updates any of the following fields passed in JSON format for a spcified patient ID
                first_name
                last_name
                age
                gender

How did the project's design evolve over time?
    Initialy there was no many to many relationship and the database schema was executed using raw SQL. Over time
    I decided to include a many to many relationship as well as create the schema using an ORM approach. 
Did you choose to use an ORM or raw SQL? Why?
    I chose to create this schema using ORM since it is based on using Object Oriented Porgramming which I wanted to practice. 
What future improvements are in store, if any?  
    In the future I want to add additional API support to add speciifc tests to the orders. This is a very simplified version of 
    an LIS so in the future it would be fun to add additional components such as billing, specimen types, collection containers, etc. 
        


        
        