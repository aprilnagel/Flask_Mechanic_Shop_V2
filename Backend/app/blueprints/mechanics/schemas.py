from marshmallow import Schema, fields
from app.extensions import ma
from app.models import Mechanics


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    name = fields.Method("get_full_name", dump_only=True)

    # Accept AND return password (required for tests)
    password = fields.String(required=True)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = Mechanics
        load_instance = False
        include_fk = True
        exclude = ()   # do NOT exclude password


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


class LoginMechanicSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


login_mechanic_schema = LoginMechanicSchema()