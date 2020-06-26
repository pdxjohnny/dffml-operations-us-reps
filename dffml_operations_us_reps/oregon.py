import json

import aiohttp

from dffml import op, Definition, Stage

# Not sure what this is, maybe an API key? Funny thing is its posted to both
# arcgis API and Oregon's API
WKID = 102100

OR_ADDRESS_TO_CORDS_URL = (
    "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find"
)
OR_ADDRESS_TO_CORDS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.oregonlegislature.gov",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://www.oregonlegislature.gov/FindYourLegislator/leg-districts.html",
}


@op(
    imp_enter={
        "session": (lambda self: aiohttp.ClientSession(trust_env=True))
    },
)
async def or_address_to_cords(self, address: str) -> dict:
    """
    Given an address, use geocode.arcgis.com API to find it.

    https://developers.arcgis.com/labs/rest/search-for-an-address/
    """

    params = (
        ("text", address),
        ("outSR", str(WKID)),
        ("f", "json"),
        ("outFields", "*"),
        ("maxLocations", "6"),
    )

    async with self.parent.session.get(
        OR_ADDRESS_TO_CORDS_URL,
        headers=OR_ADDRESS_TO_CORDS_HEADERS,
        params=params,
    ) as resp:
        data = await resp.json()
        if not data["locations"]:
            return
        first = data["locations"][0]
        return {
            "x_y": first["feature"]["geometry"],
            "x_y_min_max": first["extent"],
            "lat_lng": {
                "lat": first["feature"]["attributes"]["Y"],
                "lng": first["feature"]["attributes"]["X"],
            },
        }


OR_FIND_REPS_URL = "https://navigator.state.or.us/arcgis/rest/services/Projects/FYL_Districts/MapServer/identify"
OR_FIND_REPS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.oregonlegislature.gov",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://www.oregonlegislature.gov/FindYourLegislator/leg-districts.html",
    "TE": "Trailers",
}


@op(
    inputs={"cords": or_address_to_cords.op.outputs["result"]},
    imp_enter={
        "session": (lambda self: aiohttp.ClientSession(trust_env=True))
    },
)
async def or_find_reps(self, cords: dict) -> dict:
    params = (
        ("f", "json"),
        (
            "geometry",
            json.dumps(
                {
                    "spatialReference": {"wkid": WKID},
                    # "x": -13671302.36492608,
                    # "y": 5703668.310709929,
                    **cords["x_y"],
                }
            ),
        ),
        ("tolerance", "0"),
        ("returnGeometry", "true"),
        (
            "mapExtent",
            json.dumps(
                {
                    # "xmin": -13734366.837631756,
                    # "ymin": 5666986.848049702,
                    # "xmax": -13588524.987663837,
                    # "ymax": 5741589.387655934,
                    "spatialReference": {"wkid": WKID},
                    **cords["x_y_min_max"],
                }
            ),
        ),
        ("imageDisplay", "400,400,96"),
        ("maxAllowableOffset", "0"),
        ("geometryType", "esriGeometryPoint"),
        ("sr", str(WKID)),
        ("layers", "all:0,1,2"),
    )

    async with self.parent.session.get(
        OR_FIND_REPS_URL, headers=OR_FIND_REPS_HEADERS, params=params
    ) as resp:  # skipcq: BAN-B310
        return {
            person["attributes"]["Name"]: person["attributes"]["Email"]
            for person in (await resp.json())["results"]
            if person["attributes"]["Email"] not in [None, "Not Available"]
        }
