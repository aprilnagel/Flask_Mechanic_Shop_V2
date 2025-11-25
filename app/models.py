
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Table
from datetime import date

#Base Class
class Base(DeclarativeBase):
    pass

#instantiate the databases
db = SQLAlchemy(model_class=Base) 
#I dont really understand this line of code.

#junction table object
#many to many relationship between mechanics and service tickets
mechanic_service_ticket = Table(
    "mechanic_service_ticket", 
    Base.metadata,
    Column("mechanic_id", Integer, ForeignKey("mechanics.id")),
    Column("service_ticket_id", Integer, ForeignKey("service_tickets.id"))
)
#___________________________CUSTOMERS_____________________________

class Customers(Base):
    __tablename__ = "customers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(300), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="customer")
    
    #--------RELATIONSHIPS---------
    
    #one to many with service tickets
    service_tickets_customer: Mapped[list["Service_Tickets"]] = relationship("Service_Tickets", back_populates="customer")

#___________________________SERVICE TICKETS_____________________________

class Service_Tickets(Base):
    __tablename__ = "service_tickets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column (Integer, ForeignKey("customers.id"), nullable=False)
    vehicle_make: Mapped[str] = mapped_column(String(100), nullable=False)
    vehicle_model: Mapped[str] = mapped_column(String(100), nullable=False)
    vehicle_year: Mapped[int] = mapped_column(nullable=False)
    service_description: Mapped[str] = mapped_column(String(500), nullable=False)
    date_created: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    price: Mapped[float] = mapped_column(Float, default=0.0, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Pending")
    parts: Mapped[str] = mapped_column(String(500), nullable=True)
    completion_date: Mapped[date] = mapped_column(Date, nullable=True)

    
    
    #--------RELATIONSHIPS---------
    
    #many to one with customers
    customer: Mapped[list["Customers"]] = relationship("Customers", back_populates="service_tickets_customer")
    
    #many to many with mechanics
    mechanics_service_tickets: Mapped[list["Mechanics"]] = relationship("Mechanics", secondary=mechanic_service_ticket, back_populates="service_tickets_mechanics")
    
    #many to many with parts through service_ticket_parts association table
    parts_service_tickets: Mapped[list["Service_Ticket_Parts"]] = relationship("Service_Ticket_Parts", back_populates="service_ticket")

#___________________________MECHANICS_____________________________

class Mechanics(Base):
    __tablename__ = "mechanics"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    specialty: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="mechanic")
    
    #--------RELATIONSHIPS---------
    
    #many to many with service tickets through mechanic_service_ticket table object
    service_tickets_mechanics: Mapped[list["Service_Tickets"]] = relationship("Service_Tickets", secondary=mechanic_service_ticket, back_populates="mechanics_service_tickets")

#___________________________PARTS_____________________________

class Parts(Base):
    __tablename__ = "parts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    part_name: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    
    #--------RELATIONSHIPS---------
    
    #many to many with service tickets through service_ticket_parts
    service_tickets_parts: Mapped[list["Service_Ticket_Parts"]] = relationship("Service_Ticket_Parts", back_populates="part")

#__________________SERVICE TICKET PARTS(ASSOCIATION TABLE)_____________________

class Service_Ticket_Parts(Base): #association table to show the many to many relationship between service tickets and parts
    __tablename__ = "service_ticket_parts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    service_ticket_id: Mapped[int] = mapped_column(Integer, ForeignKey("service_tickets.id"), nullable=True)
    part_id: Mapped[int] = mapped_column(Integer, ForeignKey("parts.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    #--------RELATIONSHIPS---------
    #many to one with service tickets
    service_ticket: Mapped["Service_Tickets"] = relationship("Service_Tickets", back_populates="parts_service_tickets")
    
    #many to one with parts
    part: Mapped["Parts"] = relationship("Parts", back_populates="service_tickets_parts")


