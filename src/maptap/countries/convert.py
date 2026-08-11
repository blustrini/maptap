from maptap.errors import MapTapError

from .all_countries import Country


class UnrecognisedCountryError(MapTapError):
    """Country is not recognised by this application"""


def convert_str_to_iso2(country_str: str) -> Country:
    """Convert arbitrary string to country.
    
    Args:
        country_str: String representing the country
    
    Returns:
        Country: Country object
        

    Raises:
        UnrecognisedCountryError: Input string was not recognised as a country
    """
    ...
