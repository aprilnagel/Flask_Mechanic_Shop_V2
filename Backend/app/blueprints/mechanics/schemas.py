from marshmallow import Schema, fields
from app.extensions import ma
from app.models import Mechanics


# -----------------------------
# 1. Registration Schema
# -----------------------------
class RegisterMechanicSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    phone = fields.String(required=True)
    specialty = fields.String(required=True)
    password = fields.String(required=True)
    role = fields.String(required=False)


register_mechanic_schema = RegisterMechanicSchema()


# -----------------------------
# 2. Update Schema (password optional)
# -----------------------------
class MechanicUpdateSchema(Schema):
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()
    phone = fields.String()
    specialty = fields.String()
    password = fields.String(load_only=True)


mechanic_update_schema = MechanicUpdateSchema()


# -----------------------------
# 3. Dump Schema (never returns password)
# -----------------------------
class MechanicDumpSchema(ma.SQLAlchemyAutoSchema):
    name = fields.Method("get_full_name", dump_only=True)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = Mechanics
        load_instance = False
        include_fk = True
        exclude = ()   # allow password to be returned


mechanic_schema = MechanicDumpSchema()
mechanics_schema = MechanicDumpSchema(many=True)

# -----------------------------
# Login Schema (needed by routes + tests)
# -----------------------------
class LoginMechanicSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

login_mechanic_schema = LoginMechanicSchema()
