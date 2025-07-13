from orjson import loads
from sqlalchemy import Engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from app.model import exceptions
from app.model.auth import User
from app.model.json import structure
from app.model.json import unstructure


class AuthRepository:
    """
    Repository taking care of authentication operation.
    """

    def __init__(self, engine: Engine):
        metadata = MetaData()
        metadata.reflect(
            bind=engine,
            only=["users", "user_site_access"],
        )

        self._users: Table = metadata.tables["users"]
        self._user_site_access: Table = metadata.tables["user_site_access"]

        self._engine = engine

    def get_user(self, username: str) -> User | None:
        query = select(self._users).where(self._users.c.username == username)
        with self._engine.connect() as connection:
            if (row := connection.execute(query).fetchone()) is not None:
                return structure(loads(row.payload), User)
            else:
                return None

    def create_user(self, user: User, password: str):
        with self._engine.connect() as connection:
            check_query = select(self._users).where(
                self._users.c.username == user.username
            )
            if connection.execute(check_query).fetchone() is not None:
                raise exceptions.UserExistsException

            insert_query = insert(self._users).values(
                {
                    **unstructure(user),
                    "password": func.crypt(password, func.gen_salt("md5")),
                }
            )
            connection.execute(insert_query)

    def login_user(self, username: str, password: str):
        query = select(
            self._users.c.password == func.crypt(password, self._users.c.password)
        ).where(self._users.c.username == username)

        with self._engine.connect() as connection:
            result = connection.execute(query).fetchone()
            if result is None or not result.payload:
                raise exceptions.WrongAuthenticationException

    def change_password(self, username: str, old_password: str, new_password: str):
        self.login_user(username, old_password)

        query = (
            update(self._users.c.password)
            .where(self._users.c.username == username)
            .values(password=func.crypt(new_password, func.gen_salt("md5")))
        )
        with self._engine.connect() as connection:
            connection.execute(query)
