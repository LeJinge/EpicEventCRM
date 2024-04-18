from datetime import datetime

from models.models import User, UserRole, Client, Contract, ContractStatus, Event


def test_user_creation(session):
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com", role=UserRole.SUPERUSER)
    user.set_password("safe_password123")
    session.add(user)
    session.commit()

    retrieved_user = session.query(User).one()
    assert retrieved_user.first_name == "John"
    assert retrieved_user.last_name == "Doe"
    assert retrieved_user.email == "john.doe@example.com"
    assert retrieved_user.role == UserRole.SUPERUSER
    assert retrieved_user.verify_password("safe_password123")


def test_client_creation(session):
    client = Client(first_name="Alice", last_name="Smith", email="alice@example.com", phone_number="1234567890", company_name="Alice Co.")
    session.add(client)
    session.commit()

    retrieved_client = session.query(Client).one()
    assert retrieved_client.first_name == "Alice"
    assert retrieved_client.last_name == "Smith"
    assert retrieved_client.email == "alice@example.com"


def test_contract_creation(session):
    client = Client(first_name="Bob", last_name="Builder", email="bob@example.com")
    session.add(client)
    session.commit()

    contract = Contract(client_id=client.id, status=ContractStatus.IN_PROGRESS, total_amount=10000,
                        remaining_amount=5000)
    session.add(contract)
    session.commit()

    retrieved_contract = session.query(Contract).one()
    assert retrieved_contract.client_id == client.id
    assert retrieved_contract.status == ContractStatus.IN_PROGRESS
    assert retrieved_contract.total_amount == 10000
    assert retrieved_contract.remaining_amount == 5000


def test_event_creation(session):
    event = Event(
        title="Annual Meeting",
        start_date=datetime.strptime("2022-01-01", "%Y-%m-%d"),
        end_date=datetime.strptime("2022-01-02", "%Y-%m-%d"),
        location="Conference Room",
        attendees=50,
        notes="Annual general meeting"
    )
    session.add(event)
    session.commit()

    added_event = session.query(Event).filter_by(title="Annual Meeting").first()
    assert added_event is not None
    assert added_event.start_date == datetime(2022, 1, 1)
    assert added_event.end_date == datetime(2022, 1, 2)
