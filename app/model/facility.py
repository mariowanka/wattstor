from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from attrs import define


class DeviceType(StrEnum):
    BATTERY = "battery"
    INVERTER = "inverter"
    PV_PANEL = "pv_panel"
    WIND_TURBINE = "wind_turbine"


@define
class Device:
    id: UUID
    type: DeviceType
    site_id: UUID
    last_update: datetime


@define
class Battery(Device):
    voltage: Decimal | None
    charge: Decimal | None
    type: DeviceType = DeviceType.BATTERY


@define
class Inverter(Device):
    voltage: Decimal | None
    type: DeviceType = DeviceType.INVERTER


@define
class PvPanel(Device):
    voltage: Decimal | None
    type: DeviceType = DeviceType.PV_PANEL


@define
class HistoryRecord:
    timestamp: datetime
    voltage: Decimal
    charge: Decimal
    wind_speed: Decimal


@define
class WindTurbine(Device):
    voltage: Decimal | None
    wind_speed: Decimal | None
    type: DeviceType = DeviceType.WIND_TURBINE


def get_device_type(type_name: str) -> type[Device]:
    match type_name:
        case DeviceType.BATTERY:
            return Battery
        case DeviceType.INVERTER:
            return Inverter
        case DeviceType.PV_PANEL:
            return PvPanel
        case DeviceType.WIND_TURBINE:
            return WindTurbine
        case _:
            raise Exception


@define
class Site:
    id: UUID
    name: str
    description: str | None


@define
class SiteResponse:
    site: Site
    devices: dict[DeviceType, list[Device]]


@define
class DeviceResponse:
    device: Device
    history: list[HistoryRecord]
