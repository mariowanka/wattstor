from uuid import UUID

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for

from app.application.facility import FacilityService
from app.model.facility import DeviceType


class FacilityController:
    """
    Controller defining api for sites and devices
    """

    blueprint = Blueprint("facility", __name__, url_prefix="/facility")

    def __init__(self, service: FacilityService):
        self._service = service

    @blueprint.get("/")
    def index(self):
        sites = self._service.list_sites()
        return render_template("site_list.html", sites=sites)

    @blueprint.get("/site/<uuid:site_id>")
    def site(self, site_id: UUID):
        site = self._service.load_site(site_id)
        return render_template("site_detail.html", site=site)

    @blueprint.get("/device/<uuid:device_id>")
    def device(self, device_id: UUID):
        device = self._service.load_device(device_id)
        return render_template("device_detail.html", device=device)

    @blueprint.post("/device")
    def create_device(self):
        form = DeviceForm()
        if form.validate_on_submit():
            device_id = self._service.create_device(
                device_type=DeviceType(form.device_type), site_id=form.site_id
            )

        return redirect(url_for("facility.device", device_id=device_id))

    @blueprint.delete("/device/<uuid:device_id>")
    def delete_device(self, device_id: UUID):
        self._service.delete_device(device_id)
        return redirect(url_for("facility.index"))
