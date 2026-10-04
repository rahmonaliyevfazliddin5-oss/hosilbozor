import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.main import app
from app.models.user import User, UserRole
from app.repositories.user_repo import user_repo
from app.schemas.user import UserCreate

# Shared in-memory SQLite with StaticPool so all connections see the same DB
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def farmer_user(db: Session) -> User:
    user = user_repo.create(
        db,
        UserCreate(
            phone="+998901112233",
            full_name="Alisher Dehqon",
            role=UserRole.FARMER,
            language="uz_latn"
        )
    )
    return user


@pytest.fixture
def buyer_user(db: Session) -> User:
    user = user_repo.create(
        db,
        UserCreate(
            phone="+998904445566",
            full_name="Bobur Savdogar",
            role=UserRole.BUYER,
            language="uz_latn"
        )
    )
    return user


@pytest.fixture
def driver_user(db: Session) -> User:
    user = user_repo.create(
        db,
        UserCreate(
            phone="+998907778899",
            full_name="Davron Haydovchi",
            role=UserRole.DRIVER,
            language="uz_latn"
        )
    )
    return user


@pytest.fixture
def farmer_token(farmer_user: User) -> str:
    return create_access_token(
        subject=farmer_user.id,
        extra_claims={"role": farmer_user.role.value, "phone": farmer_user.phone}
    )


@pytest.fixture
def buyer_token(buyer_user: User) -> str:
    return create_access_token(
        subject=buyer_user.id,
        extra_claims={"role": buyer_user.role.value, "phone": buyer_user.phone}
    )


@pytest.fixture
def farmer_headers(farmer_token: str) -> dict:
    return {"Authorization": f"Bearer {farmer_token}"}


@pytest.fixture
def buyer_headers(buyer_token: str) -> dict:
    return {"Authorization": f"Bearer {buyer_token}"}


@pytest.fixture
def driver_token(driver_user: User) -> str:
    return create_access_token(
        subject=driver_user.id,
        extra_claims={"role": driver_user.role.value, "phone": driver_user.phone}
    )


@pytest.fixture
def driver_headers(driver_token: str) -> dict:
    return {"Authorization": f"Bearer {driver_token}"}



@pytest.fixture
def admin_user(db: Session) -> User:
    user = user_repo.create(
        db,
        UserCreate(
            phone="+998900001122",
            full_name="Admin Nazoratchi",
            role=UserRole.ADMIN,
            language="uz_latn"
        )
    )
    return user


@pytest.fixture
def admin_token(admin_user: User) -> str:
    return create_access_token(
        subject=admin_user.id,
        extra_claims={"role": admin_user.role.value, "phone": admin_user.phone}
    )


@pytest.fixture
def admin_headers(admin_token: str) -> dict:
    return {"Authorization": f"Bearer {admin_token}"}

