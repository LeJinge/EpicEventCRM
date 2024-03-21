from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base  # Assurez-vous que ce chemin correspond à votre structure de projet
from models.user import User, UserRole  # Importez vos modèles ici
from config import DATABASE_URI  # Importez votre URI de base de données


def create_database():
    # Crée un moteur de base de données
    engine = create_engine(DATABASE_URI)
    # Crée toutes les tables définies dans les modèles
    Base.metadata.create_all(engine)
    print("Les tables ont été créées.")


def create_initial_users():
    # Crée une session
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crée des utilisateurs initiaux
    admin_user = User(
        name='Admin User',
        email='admin@example.com',
        role=UserRole.SUPERUSER
    )
    # Assurez-vous de hacher le mot de passe dans la pratique réelle
    admin_user.set_password('adminpassword')

    gestion_user = User(
        name='Gestion User',
        email='gestion@example.com',
        role=UserRole.GESTION
    )
    gestion_user.set_password('gestionpassword')  # De même, hachez le mot de passe

    # Ajoute les utilisateurs à la session et les sauvegarde dans la base de données
    session.add(admin_user)
    session.add(gestion_user)
    session.commit()
    print("Les utilisateurs initiaux ont été créés.")


if __name__ == '__main__':
    create_database()
    create_initial_users()
