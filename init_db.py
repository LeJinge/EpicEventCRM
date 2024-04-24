import typer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
from models.models import Base, User, UserRole, pwd_context


def drop_database():
    engine = create_engine(DATABASE_URI)
    Base.metadata.drop_all(engine)
    typer.echo("Toutes les tables ont été supprimées.")


def create_database():
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)
    typer.echo("Les tables ont été créées.")


def create_initial_users():
    Session = sessionmaker(bind=engine)
    session = Session()

    admin_user = User(
        first_name='Jérémy',
        last_name='Carmona',
        email='jeremy.carmona@exemple.com',
        role=UserRole.SUPERUSER,
        password=pwd_context.hash('adminpassword')
    )

    gestion_user = User(
        first_name='Matthias',
        last_name='Carmona',
        email='gestion@exemple.com',
        role=UserRole.GESTION,
        password=pwd_context.hash('gestionpassword')
    )

    session.add(admin_user)
    session.add(gestion_user)
    session.commit()
    typer.echo("Les utilisateurs initiaux ont été créés.")
    session.close()


def create_fictitious_users():
    Session = sessionmaker(bind=engine)
    session = Session()

    # Commerciaux
    for i in range(1, 16):
        commercial_user = User(
            first_name=f"Commercial{i}",
            last_name=f"User{i}",
            email=f"commercial.user{i}@example.com",
            role=UserRole.COMMERCIALE,
            password=pwd_context.hash('password')
        )
        session.add(commercial_user)

    # Support
    for i in range(1, 16):
        support_user = User(
            first_name=f"Support{i}",
            last_name=f"User{i}",
            email=f"support.user{i}@example.com",
            role=UserRole.SUPPORT,
            password=pwd_context.hash('password')
        )
        session.add(support_user)

    session.commit()
    typer.echo("Les utilisateurs fictifs commerciaux et support ont été créés.")
    session.close()


engine = create_engine(DATABASE_URI)
drop_database()
create_database()
create_initial_users()
create_fictitious_users()
