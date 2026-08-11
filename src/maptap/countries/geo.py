from .all_countries import Country


class CountryGeo:
    """Some class representing the geometry of country. 

    Replace me with something better!
    """
    ...


# Somehow load in the geojsons in data/geojsons
def country_to_geometry(country: Country) -> CountryGeo:
    """Get geometry associated with country.

    Args:
        country: Query country.

    Returns:
        CountryGeo: THe geometry representing the country.
    """
    ...