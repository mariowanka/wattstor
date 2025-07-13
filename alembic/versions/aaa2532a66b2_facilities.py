"""facilities

Revision ID: aaa2532a66b2
Revises:
Create Date: 2025-07-13 10:04:20.055268

"""

from typing import Sequence
from typing import Union
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aaa2532a66b2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


UPGRADE = """
CREATE TABLE sites (
    PRIMARY KEY (id),
    id uuid NOT NULL,
    name text NOT NULL,
    description text
);

CREATE INDEX sites_name_idx ON sites (name);

CREATE TABLE devices (
    PRIMARY KEY (id),
    id uuid NOT NULL,
    type text NOT NULL,
    site_id uuid NOT NULL REFERENCES sites (id),
    last_update timestamptz NOT NULL,
    voltage decimal,
    charge decimal,
    wind_speed decimal
);

CREATE INDEX devices_site_id_idx ON devices (site_id);

CREATE TABLE device_history (
    PRIMARY KEY (id),
    id uuid NOT NULL,
    device_id uuid NOT NULL REFERENCES devices (id) ON DELETE CASCADE,
    timestamp timestamptz NOT NULL,
    voltage decimal,
    charge decimal,
    wind_speed decimal
);

CREATE INDEX device_history_device_id_timestamp_idx 
    ON device_history (device_id, timestamp);
"""

DOWNGRADE = """
DROP INDEX device_history_device_id_timestamp_idx;
DROP INDEX devices_site_id_idx;
DROP INDEX sites_name_idx;

DROP TABLE device_history;
DROP TABLE devices;
DROP TABLE sites;
"""


def upgrade():
    op.execute(UPGRADE)


def downgrade():
    op.execute(DOWNGRADE)
