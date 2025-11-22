from app.extensions import ma
from app.models import Parts

class PartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Parts
        

part_schema = PartSchema()
parts_schema = PartSchema(many=True)

