import enum
from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from base import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(enum.Enum):
    SUPERUSER = 'Superuser'
    GESTION = 'Gestion'
    COMMERCIALE = 'Commerciale'
    SUPPORT = 'Support'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(Enum(UserRole))
    contracts = relationship('Contract', back_populates='commercial_contact')  # Relation entre User et Contract
    events = relationship('Event', back_populates='support_contact')  # Relation entre User et Event
    clients = relationship('Client', back_populates='commercial_contact')  # Relation entre User et Client

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def is_superuser(self):
        return self.role == UserRole.SUPERUSER

    def is_gestion(self):
        return self.role == UserRole.GESTION

    def is_commerciale(self):
        return self.role == UserRole.COMMERCIALE

    def is_support(self):
        return self.role == UserRole.SUPPORT
