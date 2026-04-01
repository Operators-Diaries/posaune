from __future__ import annotations

import requests

BASE_URL = "http://widgets.vvo-online.de/abfahrtsmonitor"


def _resolve_stop_id(
    session: requests.Session,
    stop_name: str,
    city: str = "Dresden",
) -> str:
    resp = session.get(
        f"{BASE_URL}/Haltestelle.do",
        params={"ort": city, "hst": stop_name},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    stops = data[1] if isinstance(data, list) and len(data) > 1 else []

    if not stops:
        raise ValueError(f"Keine Haltestelle gefunden für {stop_name!r}")

    for name, stop_city, stop_id in stops:
        if name.strip().lower() == stop_name.lower() and stop_city.lower() == city.lower():
            return str(stop_id)

    return str(stops[0][2])


def _fetch_departures(
    session: requests.Session,
    stop_id: str,
    limit: int = 10,
) -> dict[str] | list:
    resp = session.get(
        f"{BASE_URL}/Abfahrten.do",
        params={"hst": stop_id, "lim": limit},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def get_next_departures_by_line_and_direction(
    stop_names: list[str] = ["St. Benno Gymnasium", "Straßburger Platz", "Sachsenallee"],
    city: str = "Dresden",
    limit: int = 20,
) -> dict[str, dict[tuple[str, str], int]]:
    """
    Rückgabeformat:
    ```
    {
        "Haltestelle": {
            ("Linie", "Ziel"): Minuten
        }
    }
    ```
    """

    result: dict[str, dict[tuple[str, str], int]] = {}

    with requests.Session() as session:
        for stop_name in stop_names:
            stop_id = _resolve_stop_id(session, stop_name, city)
            departures = _fetch_departures(session, stop_id, limit)

            per_line_direction: dict[tuple[str, str], int] = {}

            for entry in departures:
                if not isinstance(entry, list) or len(entry) != 3:
                    continue

                line, destination, minutes = entry

                try:
                    minute_value = int(minutes)
                except (TypeError, ValueError):
                    continue

                key = (str(line), str(destination))

                current = per_line_direction.get(key)
                if current is None or minute_value < current:
                    per_line_direction[key] = minute_value

            result[stop_name] = per_line_direction

    return result