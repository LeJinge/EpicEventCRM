import enum

from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Status(enum.Enum):
    IN_PROGRESS = 'In Progress'
    SIGN = 'Sign'
    FINISH = 'Finish'


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    client_information = relationship('Client', back_populates='contracts')
    commercial_contact = relationship('User', back_populates='contracts')  # Relation entre Contract et User
    events = relationship('Event', back_populates='contract')
    total_amount = Column(Integer, nullable=False)
    rest_to_pay = Column(Integer, nullable=False)
    creation_date = Column(DateTime, nullable=True)
    status = Column(Enum(Status))


