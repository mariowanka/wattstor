from datetime import date
from datetime import datetime
from decimal import Decimal
from operator import methodcaller
from uuid import UUID

from cattrs import Converter
from dateutil.parser import isoparse

converter = Converter(prefer_attrib_converters=True)

converter.register_unstructure_hook(UUID, str)
converter.register_structure_hook(UUID, lambda v, _: UUID(v))

converter.register_unstructure_hook(datetime, methodcaller("isoformat"))
converter.register_structure_hook(datetime, lambda v, _: isoparse(v))

converter.register_unstructure_hook(date, methodcaller("isoformat"))
converter.register_structure_hook(date, lambda v, _: date.fromisoformat(v))

converter.register_unstructure_hook(Decimal, str)
converter.register_structure_hook(Decimal, lambda v, _: Decimal(v))


unstructure = converter.unstructure
structure = converter.structure
