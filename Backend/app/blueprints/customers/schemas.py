from app.extensions import ma
from app.models import Customers

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    password = ma.String(load_only=True)   

    class Meta:
        model = Customers
        load_instance = True
        include_fk = True
        dump_only = ("id",)               
        
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_customer_schema = CustomerSchema(only=('email', 'password'))