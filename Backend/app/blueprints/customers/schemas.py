from app.extensions import ma
from app.models import Customers

class CustomerSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    password = ma.String(load_only=True)

    class Meta:
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "role",
            "password"
        )
        
         
        
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_customer_schema = CustomerSchema(only=('email', 'password'))