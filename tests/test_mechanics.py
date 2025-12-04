from app import create_app
from app.models import Mechanics, db
from app.utility.auth import encode_token
import unittest
from werkzeug.security import generate_password_hash, check_password_hash

class TestMechanics(unittest.TestCase):

    #STEP 1: set up environment. Similar to constructor. It runs before everything else and ensures other tests have what they need
    def setUp(self): 
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanics(
            first_name="Mech1",
            last_name="Test1",
            email="mech1@email.com",
            password=generate_password_hash("12345"),
            phone="555-555-5555",
            specialty="Engine Repair",
            role="mechanic"
        )
        with self.app.app_context():
            db.drop_all() #Remove any lingering tables
            db.create_all()#Create fresh tables for testing
            db.session.add(self.mechanic)#Adding the mechanic to the session
            db.session.flush()# Flush to assign ID
            self.mechanic_id = self.mechanic.id#Storing the mechanic's ID for later use
            self.token_mechanic = encode_token(self.mechanic.id, "mechanic")#Encoding an auth token for the mechanic
            db.session.commit()#Committing the session to save changes to the database
        self.client = self.app.test_client()#Creating a test client to send requests to the API

    #STEP 2: Writing individual test cases to verify different functionalities
    def test_create_mechanic(self):
        mechanic_payload = {
            "first_name": "New",
            "last_name": "Mechanic",
            "email": "newmech@email.com",
            "password": "1234",
            "phone": "111-222-3333",
            "specialty": "Brakes",
            "role": "mechanic"
            
        }
        #Sending a POST request to create a new mechanic. 
        response = self.client.post('/mechanics', json=mechanic_payload) #sending a test POST request using our test_client and including a JSON body
        self.assertEqual(response.status_code, 201) #this checks if I got a 201 status code
        self.assertEqual(response.json['first_name'], "New") #this checks if the first name in the response matches what we sent
        self.assertEqual(response.json['last_name'], "Mechanic") #this checks if the last name in the response matches what we sent
        self.assertEqual(response.json['email'], "newmech@email.com") #this checks if the email in the response matches what we sent
        self.assertTrue(check_password_hash(response.json['password'], "1234"))
        self.assertEqual(response.json['phone'], "111-222-3333") #this checks if the phone in the response matches what we sent
        self.assertEqual(response.json['specialty'], "Brakes") #this checks if the specialty in the response matches what we sent
        self.assertEqual(response.json['role'], "mechanic") #this checks if the role in the response matches what we sent

    #STEP 3: Create a negative test case to handle invalid input for create_mechanic
    def test_invalid_create_mechanic(self):
        invalid_mechanic_payload = {
            "first_name": "NoEmail",
            "last_name": "Mechanic",
            "password": "abcde",
            "phone": "555-555-5555",
            "specialty": "Brakes",
            "role": "mechanic"
        }
        response = self.client.post('/mechanics', json=invalid_mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json)

    #STEP 4: Test mechanic login functionality
    def test_login_mechanic(self):
        payload = {
            "email": "mech1@email.com",
            "password": "12345"
        }
        response = self.client.post('/mechanics/login', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    #STEP 5: Negative test case for mechanic login with invalid credentials
    def test_invalid_login_mechanic(self):
        payload = {
            "email": "invalid@email.com",
            "password": "wrongpassword"
        }
        response = self.client.post('/mechanics/login', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], "Invalid email or password")
    
    #STEP 6: Test get all mechanics route
    def test_get_mechanics(self):
        headers = {"Authorization": f"Bearer {self.token_mechanic}"}
        response = self.client.get('/mechanics', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['email'], "mech1@email.com")

    #STEP 7: Create negative test for get all mechanics route with invalid token
    def test_get_mechanics_unauthorized(self):
        
        response = self.client.get('/mechanics')
        self.assertEqual(response.status_code, 401)
    
    #STEP 8: Test get single mecahanic with mechnic ID in path
    def test_get_single_mechanic(self):
        headers = {"Authorization": f"Bearer {self.token_mechanic}"}
        response = self.client.get(f'/mechanics/{self.mechanic_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], "mech1@email.com")
    
    #STEP 9: Negative test for get single mechanic with invalid ID
    def test_get_single_mechanic_not_found(self):
        headers = {"Authorization": f"Bearer {self.token_mechanic}"}
        response = self.client.get('/mechanics/9999', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], "Mechanic not found")

     #STEP 10: Update mechanic information.     
    
    def test_update_mechanic(self):
        update_payload = {"first_name": "UpdatedMech", "phone": "000-000-0000"}
        headers = {"Authorization": f"Bearer {self.token_mechanic}"}
        response = self.client.put('/mechanics', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['first_name'], "UpdatedMech")
        self.assertEqual(response.json['phone'], "000-000-0000")
    
    #STEP 11: Negative test for update mechanic with invalid token
    def test_update_mechanic_unauthorized(self):
        update_payload = {"first_name": "UpdatedMech", "phone": "000-000-0000"}
        response = self.client.put('/mechanics', json=update_payload)
        self.assertEqual(response.status_code, 401)
        
    #STEP 12: Test delete mechanic
    def test_delete_mechanic(self):
        headers = {"Authorization": f"Bearer {self.token_mechanic}"}
        response = self.client.delete(f'/mechanics/{self.mechanic_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted", response.json.get('message', '').lower())
     
    #STEP 13: Negative test for delete mechanic with invalid token
    def test_delete_mechanic_unauthorized(self):
        response = self.client.delete(f'/mechanics/{self.mechanic_id}')
        self.assertEqual(response.status_code, 401)
    
    #STEP 14: test get my tickets route       
    def test_get_my_tickets(self):
        headers = {"Authorization": f"Bearer {self.token_mechanic}"}
        response = self.client.get('/mechanics/my_tickets', headers=headers)
        # Adjust expected status code and response as needed
        self.assertIn(response.status_code, (200, 404))
    
    #STEP 15: Negative test for get my tickets with invalid token
    def test_get_my_tickets_unauthorized(self):
        response = self.client.get('/mechanics/my_tickets')
        self.assertEqual(response.status_code, 401)
    
    #STEP 16: Test mechanic logout    
    def test_logout(self):
        headers = {"Authorization": f"Bearer {self.token_mechanic}"}
        response = self.client.post('/mechanics/logout', headers=headers)
        self.assertEqual(response.status_code, 200)
    
    #STEP 17: Negative test for logout with invalid token
    def test_logout_unauthorized(self):
        response = self.client.post('/mechanics/logout')
        self.assertEqual(response.status_code, 401)
