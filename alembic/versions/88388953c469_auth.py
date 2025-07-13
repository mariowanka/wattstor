"""auth

Revision ID: 88388953c469
Revises: aaa2532a66b2
Create Date: 2025-07-13 14:01:39.204203

"""

from typing import Sequence
from typing import Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "88388953c469"
down_revision: Union[str, None] = "aaa2532a66b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


UPGRADE = """
CREATE EXTENSION pgcrypto;

CREATE TABLE users (
    PRIMARY KEY (id),
    id uuid NOT NULL,
    username text UNIQUE NOT NULL,
    password text NOT NULL,
    is_technician bool NOT NULL
);

CREATE INDEX users_username_idx ON users (username);

CREATE TABLE user_site_access (
    PRIMARY KEY (id),
    user_id uuid NOT NULL REFERENCES users (id),
    site_id uuid NOT NULL REFERENCES sites (id)
);

CREATE INDEX user_site_access_idx ON user_site_access (user_id, site_id);
"""

DOWNGRADE = """
DROP INDEX users_username_idx;
DROP TABLE users;
"""


def upgrade() -> None:
    op.execute(UPGRADE)


def downgrade() -> None:
    op.execute(DOWNGRADE)
