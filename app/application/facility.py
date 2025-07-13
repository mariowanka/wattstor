from datetime import datetime
from uuid import UUID
from uuid import uuid4

from app.infrastructure.facility import FacilityRepository
from app.model.facility import Device
from app.model.facility import DeviceResponse
from app.model.facility import DeviceType
from app.model.facility import Site
from app.model.facility import SiteResponse


class FacilityService:
    """
    Service taking care of facility operations
    """

    def __init__(self, repository: FacilityRepository):
        self._repository = repository

    def list_sites(self) -> list[Site]:
        return self._repository.list_sites()

    def load_site(self, site_id: UUID) -> SiteResponse | None:
        if (site := self._repository.get_site(site_id)) is None:
            return None

        site_devices = self._repository.get_site_devices(site_id)

        return SiteResponse(site=site, devices=site_devices)

    def load_device(self, device_id: UUID) -> DeviceResponse | None:
        if (device := self._repository.get_device(device_id)) is None:
            return None

        device_history = self._repository.get_device_history(device_id)

        return DeviceResponse(device=device, history=device_history)

    def create_device(self, device_type: DeviceType, site_id: UUID) -> UUID:
        new_device = Device(
            id=uuid4(),
            type=device_type,
            site_id=site_id,
            last_update=datetime.now(),
        )
        self._repository.create_device(new_device)
        return new_device.id

    def delete_device(self, device_id: UUID):
        self._repository.delete_device(device_id)
