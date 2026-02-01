from marshmallow import fields
from app.extensions import ma
from app.models import Service_Tickets
from app.blueprints.mechanics.schemas import MechanicSchema

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.List(
        fields.Nested(MechanicSchema),
        attribute="mechanics_service_tickets"
    )

    class Meta:
        model = Service_Tickets
        include_fk = True
        load_instance = True

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
