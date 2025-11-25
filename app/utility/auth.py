from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "supersecretkey"

def encode_token(user_id, role):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1), # Set token expiration.Token expires in 1 hour
        'iat': datetime.now(timezone.utc),  # Issued at time
        'sub': str(user_id), #VERY IMPORTANT, SET YOUR USER ID TO A STRING
        'role': role
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f): #f stands for the function that is getting wrapped. Delete user function from routes is f. 
    @wraps(f)
    def decoration(*args, **kwargs): #The function that runs before the function that we're wrapping  
        
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1] #Bearer <token> 
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            print(data)
            request.logged_in_user_id = data['sub'] 
            request.logged_in_role = data['role']
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(*args, **kwargs)
    
    return decoration

def mechanic_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.logged_in_role != 'mechanic':
            return jsonify({'message': 'Mechanic access required'}), 403
        return f(*args, **kwargs)
    return wrapper

def customer_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.logged_in_role != 'customer':
            return jsonify({'message': 'Customer access required'}), 403
        return f(*args, **kwargs)
    return wrapper