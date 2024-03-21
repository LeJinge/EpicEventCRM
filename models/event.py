from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    contract = relationship('Contract', back_populates='events')
    support_contact_id = Column(Integer, ForeignKey('users.id'))
    support_contact = relationship('User', back_populates='events')
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client', back_populates='events')
    location = Column(String(100), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String(1000), nullable=True)
