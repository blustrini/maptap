import dataclasses

from .coords import Coords2D
from .countries import Country


# Need to have a think about how to best represent this.
# Presumably we should check if the coords are actually within the country...?
@dataclasses.dataclass
class City:
    country: Country
    coords: Coords2D