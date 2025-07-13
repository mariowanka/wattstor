from collections import defaultdict
from uuid import UUID

from orjson import loads
from sqlalchemy import Engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select

from app.model import exceptions
from app.model.facility import Device
from app.model.facility import DeviceType
from app.model.facility import HistoryRecord
from app.model.facility import Site
from app.model.facility import get_device_type
from app.model.json import structure
from app.model.json import unstructure


class FacilityRepository:
    def __init__(self, engine: Engine):
        metadata = MetaData()
        metadata.reflect(
            bind=engine,
            only=["sites", "devices", "device_history"],
        )

        self._sites: Table = metadata.tables["sites"]
        self._devices: Table = metadata.tables["devices"]
        self._device_history: Table = metadata.tables["device_history"]

        self._engine = engine

    def list_sites(self) -> list[Site]:
        query = select(self._sites).order_by(self._sites.c.name)
        with self._engine.connect() as connection:
            return [
                structure(row.payload, Site)
                for row in connection.execute(query).fetchall()
            ]

    def get_site(self, site_id: UUID) -> Site | None:
        """
        Load site from database
        """
        query = select(self._sites).where(self._sites.c.site_id == site_id)
        with self._engine.connect() as connection:
            if (row := connection.execute(query).fetchone()) is not None:
                return structure(loads(row.payload), Site)
            else:
                return None

    def get_site_devices(self, site_id: UUID) -> dict[DeviceType, list[Device]]:
        """
        Load devices for given site
        """
        query = select(self._devices).where(self._devices.c.site_id == site_id)

        result: dict[DeviceType, list[Device]] = defaultdict(list)
        with self._engine.connect() as connection:
            for row in connection.execute(query).fetchall():
                data = loads(row.payload)
                try:
                    device_type = get_device_type(data["type"])
                except exceptions.WrongDeviceTypeException:
                    # TODO send this to sentry
                    continue

                device = structure(data, device_type)
                result[device.type].append(device)

        return result

    def get_device(self, device_id: UUID) -> Device | None:
        query = select(self._devices).where(self._devices.c.id == device_id)
        with self._engine.connect() as connection:
            if (row := connection.execute(query).fetchone()) is not None:
                data = loads(row.payload)
                return structure(data, get_device_type(data["type"]))
            else:
                return None

    def get_device_history(self, device_id: UUID) -> list[HistoryRecord]:
        query = (
            select(self._device_history)
            .where(self._device_history.c.device_id == device_id)
            .order_by(self._device_history.c.timestamp)
        )
        with self._engine.connect() as connection:
            return [
                structure(row.payload, HistoryRecord)
                for row in connection.execute(query).fetchall()
            ]

    def create_device(self, device: Device):
        query = insert(self._devices).values(unstructure(device))
        with self._engine.connect() as connection:
            connection.execute(query)

    def delete_device(self, device_id: UUID):
        query = delete(self._devices).where(self._devices.c.device_id == device_id)
        with self._engine.connect() as connection:
            connection.execute(query)
