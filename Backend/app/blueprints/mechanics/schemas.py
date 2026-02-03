from marshmallow import Schema, fields
from app.extensions import ma
from app.models import Mechanics


# ------------------------------------------------------------
#  MAIN MECHANIC SCHEMA
#  - Accepts password on load
#  - Hides password on dump
#  - Adds computed full name
#  - Returns dicts on .load()
# ------------------------------------------------------------

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    # Computed full name for frontend display
    name = fields.Method("get_full_name", dump_only=True)

    # Accept password on load, hide on dump
    password = fields.String(load_only=True, required=True)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = Mechanics
        load_instance = False   # ensures .load() returns dicts
        include_fk = True       # safe + helps with relationships
        exclude = ()            # DO NOT exclude password here


# Exported instances
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


# ------------------------------------------------------------
#  LOGIN SCHEMA
#  - Used ONLY for login
#  - Prevents Marshmallow from expecting extra fields
# ------------------------------------------------------------

class LoginMechanicSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


login_mechanic_schema = LoginMechanicSchema()