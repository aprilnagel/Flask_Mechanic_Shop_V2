from marshmallow import Schema, fields
from app.extensions import ma
from app.models import Mechanics


# ------------------------------------------------------------
#  MAIN MECHANIC SCHEMA
#  - Used for create, update, get, list
#  - Includes computed full name
#  - Excludes password from output
#  - Does NOT use load_instance=True (so .load() returns dict)
# ------------------------------------------------------------

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    # Computed full name for frontend display
    name = fields.Method("get_full_name", dump_only=True)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = Mechanics
        exclude = ("password",)   # never expose password
        load_instance = False     # ensures .load() returns dicts


# Exported instances
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


# ------------------------------------------------------------
#  LOGIN SCHEMA
#  - Used ONLY for login
#  - Fixes invalid login test
#  - Avoids Marshmallow errors caused by MechanicSchema
# ------------------------------------------------------------

class LoginMechanicSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


login_mechanic_schema = LoginMechanicSchema()