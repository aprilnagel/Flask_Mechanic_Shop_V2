from app import create_app
from app.models import Customers, db, Mechanics
from app.utility.auth import encode_token
import unittest
from werkzeug.security import check_password_hash, generate_password_hash

#Run tests with: python -m unittest discover tests

class TestUsers(unittest.TestCase):

    #Runs before each test_method
    def setUp(self):
        self.app = create_app('TestingConfig') #Create a testing version of my app for these testcases
        self.customer = Customers(
            first_name="Test", 
            last_name="Lasttest", 
            email="test@email.com", 
            password=generate_password_hash("12345"), 
            phone="123-456-7890", 
            address="123 Test St, Test City, TS 12345", 
            role="customer")
        self.mechanic = Mechanics(
            first_name="Mech", 
            last_name="Mechanic", 
            email="mech@email.com", 
            password=generate_password_hash("12345"), 
            phone="987-654-3210", 
            specialty="Engine Repair",
            role="mechanic"
        )
    
        with self.app.app_context():
            db.drop_all() #removing any lingering tables
            db.create_all() #creating fresh tables for another round of testing
            db.session.add(self.customer)
            db.session.add(self.mechanic)
            db.session.flush()  # Flush to assign IDs
            
            self.customer_id = self.customer.id
            self.mechanic_id = self.mechanic.id

            self.token_mechanic = encode_token(self.mechanic.id, "mechanic")
            self.token_customer = encode_token(self.customer.id, "customer")
            db.session.commit()

        self.client = self.app.test_client() #creates a test client that will send requests to our API
    
    def test_create_customer(self):
        customer_payload = {
            "email": "test1@email.com",
            "first_name": "Test2",
            "last_name": "Lasttest2",
            "password": "12345",
            "phone": "555-555-5555",
            "address": "testaddress",
            "role": "customer"
        
        }

        response = self.client.post('/customers', json=customer_payload) #sending a test POST request using our test_client and including a JSON body
        self.assertEqual(response.status_code, 201) #checking if I got a 201 status code
        self.assertEqual(response.json['first_name'], "Test2") #checking to make sure the data that I sent in, is part of the response
        self.assertTrue(check_password_hash(response.json['password'], "12345")) #checking if the password was hashed correctly
        self.assertEqual(response.json['last_name'], "Lasttest2"),
        self.assertEqual(response.json['email'], "test1@email.com")
        self.assertEqual(response.json['phone'], "555-555-5555")
        self.assertEqual(response.json['address'], "testaddress")
        self.assertEqual(response.json['role'], "customer")
        
    #negative check - see what happens when we intentionally send bad data
    
    def test_invalid_create(self):
        customer_payload = {
            "first_name": "Test3",
            "last_name": "Lasttest2",
            "password": "12345",
            "phone": "555-111-5555",
            "address": "testaddress",
            "role": "customer"
        }
        
        response = self.client.post('/customers', json=customer_payload)
        self.assertEqual(response.status_code, 400) #checking if I got a 400 status code
        self.assertIn('email', response.json) #checking to make sure the error message includes 'email' key
        
    def test_get_customers(self):
        response = self.client.get('/customers',
            headers={"Authorization": f"Bearer {self.token_mechanic}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['email'], "test@email.com")

    def test_login_customer(self):
        login_payload = {
            "email": "test@email.com",
            "password": "12345"
        }
        
        response = self.client.post('/customers/login', json=login_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Welcome Test Lasttest")
        self.assertIn('token', response.json) #checking to make sure a token is included in the response
    
    def test_delete_customer(self):
        headers = {"Authorization": f"Bearer {self.token_customer}"}
        response = self.client.delete(f'/customers/{self.customer_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], f"Customer deleted {self.customer_id}")

    def test_unathorized_delete_customer(self):
        response = self.client.delete(f'/customers/{self.customer_id}')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], "Token is missing!")

    def test_update_customer(self):
        update_payload = {"first_name": "UpdatedName", "phone": "000-000-0000"}
        headers = {"Authorization": f"Bearer {self.token_customer}"}
        response = self.client.put(f'/customers/{self.customer_id}', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['first_name'], "UpdatedName")
        self.assertEqual(response.json['phone'], "000-000-0000")
        
            
        