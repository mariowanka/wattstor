from uuid import uuid4

import pytest
from sqlalchemy import Engine

from app.infrastructure.auth import AuthRepository
from app.model.auth import User
from app.model.exceptions import UserExistsException
from app.model.exceptions import WrongAuthenticationException


class TestAuthRepository:
    @pytest.fixture(scope="class")
    def repository(self, engine: Engine) -> AuthRepository:
        return AuthRepository(engine)

    def test_create_user(self, repository):
        # setup
        user = User(id=uuid4(), username="Foo", is_technician=False)
        password = "bar"

        # run
        repository.create_user(user, password)

        # verify
        assert user == repository.get_user(user.username)

    def test_create_user_already_exists(self, repository):
        # setup
        user = User(id=uuid4(), username="Foo", is_technician=False)
        password = "bar"
        repository.create_user(user, password)

        # run
        with pytest.raises(UserExistsException):
            repository.create_user(user, password)

    def test_login_user(self, repository):
        # setup
        user = User(id=uuid4(), username="Foo", is_technician=False)
        password = "bar"
        repository.create_user(user, password)

        # run
        repository.login_user(user.username, password)

    def test_login_user_wrong_username(self, repository):
        # setup
        user = User(id=uuid4(), username="Foo", is_technician=False)
        password = "bar"
        repository.create_user(user, password)

        # run
        with pytest.raises(WrongAuthenticationException):
            repository.login_user("wrong_name", password)

    def test_login_user_wrong_password(self, repository):
        # setup
        user = User(id=uuid4(), username="Foo", is_technician=False)
        password = "bar"
        repository.create_user(user, password)

        # run
        with pytest.raises(WrongAuthenticationException):
            repository.login_user(user.username, "wrong_password")

    def test_change_password(self, repository):
        # setup
        user = User(id=uuid4(), username="Foo", is_technician=False)
        old_password = "bar"
        new_password = "new"

        repository.create_user(user, old_password)

        # run
        repository.change_password(user.username, old_password, new_password)

        # verify
        repository.login_user(user.username, new_password)

    def test_change_password_wrong_username(self, repository):
        # setup
        user = User(id=uuid4(), username="Foo", is_technician=False)
        old_password = "bar"
        new_password = "new"

        repository.create_user(user, old_password)

        # run
        with pytest.raises(WrongAuthenticationException):
            repository.change_password("wrong_username", old_password, new_password)

    def test_change_password_wrong_password(self, repository):
        # setup
        user = User(id=uuid4(), username="Foo", is_technician=False)
        old_password = "bar"
        new_password = "new"

        repository.create_user(user, old_password)

        # run
        with pytest.raises(WrongAuthenticationException):
            repository.change_password(user.username, "wrong_password", new_password)
