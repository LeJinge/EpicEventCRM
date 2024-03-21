from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from base import Base  # Importez votre classe de base SQLAlchemy


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    telephone = Column(String(20), nullable=True)
    entreprise = Column(String(100), nullable=True)
    creation_date = Column(DateTime, nullable=True)
    contracts = relationship('Contract', back_populates='client_information')
    events = relationship('Event', back_populates='client')
    commercial_contact = relationship('User', back_populates='clients')  # Relation entre Client et User

    def __repr__(self):
        return f"<Client(nom='{self.nom}', email='{self.email}', entreprise='{self.entreprise}')>"