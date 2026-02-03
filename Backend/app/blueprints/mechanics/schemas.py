from marshmallow import fields
from app.extensions import ma
from app.models import Mechanics

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    # Add a computed full name field
    name = fields.Method("get_full_name")

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = Mechanics
        load_instance = True
        exclude = ("password",)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
login_mechanic_schema = MechanicSchema(only=['email', 'password'])
