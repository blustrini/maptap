"""Script to download geojson for each ISO3 country defined in the maptap app.

Saves data to `data/geojson/XXX.geojson`, where XXX is the ISO3-code.

Also saved a list of bad ISO3 codes for which no geometry was found in 
 `data/geojson/_bad_iso3_codes.txt`
"""
import json
from pathlib import Path
from urllib.request import urlretrieve

from maptap.countries.all_countries import Country

# 10m high-resolution dataset
DATA_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_0_countries.geojson"

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "geojson"
BAD_CODES_FILE = OUTPUT_DIR / "_bad_iso3_codes.txt"


def fetch_and_split_geometries():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Downloading Natural Earth 1:10m high-res dataset (~25MB)...")
    temp_file, _ = urlretrieve(DATA_URL)

    with open(temp_file, "r", encoding="utf-8") as f:
        world_data = json.load(f)

    # Index features by all possible ISO3 keys
    geometry_map = {}
    for feature in world_data.get("features", []):
        props = feature.get("properties", {})

        candidate_codes = [
            props.get("ISO_A3_EH"),  # Extended/Heuristic ISO3 (fixes -99 bug)
            props.get("ADM0_A3"),    # Admin 0 ISO3
            props.get("GU_A3"),      # Governance Unit ISO3
            props.get("ISO_A3"),     # Standard ISO3
            props.get("SOV_A3"),     # Sovereign ISO3
        ]

        for code in candidate_codes:
            if code and code != "-99" and len(code) == 3:
                iso3_upper = code.upper()
                if iso3_upper not in geometry_map:
                    geometry_map[iso3_upper] = feature

    saved_count = 0
    missing_codes = []

    # Iterate strictly over your Country StrEnum
    for country in Country:
        iso3 = country.value.upper()

        if iso3 in geometry_map:
            feature = geometry_map[iso3]
            country_file = OUTPUT_DIR / f"{iso3}.geojson"

            with open(country_file, "w", encoding="utf-8") as out:
                json.dump(feature, out, indent=2)

            saved_count += 1
        else:
            missing_codes.append(iso3)

    # Write missing codes to bad codes file
    sorted_missing = sorted(missing_codes)
    with open(BAD_CODES_FILE, "w", encoding="utf-8") as f:
        for code in sorted_missing:
            f.write(f"{code}\n")

    print(f"\nSaved {saved_count}/{len(Country)} country geometries to '{OUTPUT_DIR}'.")

    if missing_codes:
        print(
            f"Warning: Could not find geometries for {len(missing_codes)} ISO3 codes."
        )
        print(f"Missing codes written to: {BAD_CODES_FILE}")
    else:
        print(f"All ISO3 codes resolved! ({BAD_CODES_FILE} is empty)")


if __name__ == "__main__":
    fetch_and_split_geometries()