import enum

from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(enum.Enum):
    SUPERUSER = 'Superuser'
    GESTION = 'Gestion'
    COMMERCIALE = 'Commerciale'
    SUPPORT = 'Support'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)  # Ajout du prénom
    last_name = Column(String)  # Ajout du nom
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(Enum(UserRole))

    contracts = relationship("Contract", back_populates="commercial_contact")
    events = relationship("Event", back_populates="support_contact")
    clients = relationship("Client", back_populates="commercial_contact")

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)  # Ajout du prénom
    last_name = Column(String)  # Ajout du nom
    email = Column(String)
    phone_number = Column(String)
    company_name = Column(String)
    creation_date = Column(DateTime)

    commercial_contact_id = Column(Integer, ForeignKey('users.id'))
    commercial_contact = relationship("User", back_populates="clients")
    contracts = relationship("Contract", back_populates="client")
    events = relationship("Event", back_populates="client")


class ContractStatus(enum.Enum):
    IN_PROGRESS = 'In Progress'
    SIGNED = 'Signed'
    FINISHED = 'Finished'


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    commercial_contact_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Enum(ContractStatus))
    total_amount = Column(Integer)
    remaining_amount = Column(Integer)
    creation_date = Column(DateTime)

    client = relationship("Client", back_populates="contracts")
    commercial_contact = relationship("User", back_populates="contracts")
    events = relationship("Event", back_populates="contract")


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    location = Column(String)
    attendees = Column(Integer)
    notes = Column(String)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    support_contact_id = Column(Integer, ForeignKey('users.id'))

    contract = relationship("Contract", back_populates="events")
    client = relationship("Client", back_populates="events")
    support_contact = relationship("User", back_populates="events")
