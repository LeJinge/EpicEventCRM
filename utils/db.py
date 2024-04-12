from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URI

# Créer l'engine de base de données SQLAlchemy avec l'URI de PostgreSQL
engine = create_engine(DATABASE_URI, echo=True)

# Créer une session de base de données configurée avec l'engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Déclarer une classe de base pour les modèles
Base = declarative_base()


# Fonction pour initier une session, à utiliser au début de vos fonctions d'interaction avec la DB
def init_db_session():
    return SessionLocal()
