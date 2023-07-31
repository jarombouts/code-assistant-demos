from datetime import datetime, timedelta
import requests


from loguru import logger
from dataclasses import dataclass


@dataclass
class config:
    knmi_url = "https://www.daggegevens.knmi.nl/klimatologie/daggegevens"


def _ongewogen_graaddagen(etmaal_gem_temp):
    """Vertaalt gemiddelde etmaaltemperatuur naar ongewogen graaddagen

    Bij de graaddagenberekening wordt de gemiddelde buitentemperatuur van 18° C
    de stookgrens genoemd. Iedere graad die de gemiddelde etmaaltemperatuur van
    de buitenlucht beneden de 18 graden Celsius ligt, is 1 graaddag. Als de
    gemiddelde buitentemperatuur bijvoorbeeld 10°C is, dan hebben we voor die
    dag dus 8 graaddagen. Iedere graad boven de 18°C wordt gesteld op nul, omdat
    er dan van uit wordt gegaan dat er dan niet wordt gestookt.
    """
    if not etmaal_gem_temp:
        return ""
    elif etmaal_gem_temp >= 18:
        return 0
    else:
        return 1018 - (etmaal_gem_temp + 1000)


def _gewogen_graaddagen(etmaal_gem_temp, maand_nr):
    """Vertaalt gemiddelde etmaaltemperatuur naar gewogen graaddagen

    Het is gebleken dat het verband tussen de graaddagen en
    het warmteverbruik van een woning niet geheel lineair is.
    Behalve temperatuur zijn er meer weersinvloeden die invloed
    hebben op het gasverbruik, zoals zoninstraling, luchtvochtigheid,
    windsnelheid etc. Om deze invloeden ook mee te laten wegen in de
    berekeningen is er een empirisch bepaalde seizoen afhankelijke
    weegfactor bepaald voor woonhuizen. Door de ongewogen graaddagen
    te vermenigvuldigen met deze correctiefactoren worden de
    gewogen graaddagen vastgesteld. De weegfactoren zijn:
    - April tot en met September: 0,8
    - Maart en Oktober: 1,0
    - November tot en met Februari: 1,1

    Deze wegingsfactoren zijn alleen van toepassing op woonhuizen.
    Voor bedrijven worden de ongewogen graaddagen gebruikt.
    """

    if not etmaal_gem_temp:
        return ""
    elif int(maand_nr) in (11, 12, 1, 2):
        return _ongewogen_graaddagen(etmaal_gem_temp) * 1.1
    elif int(maand_nr) in (4, 5, 6, 7, 8, 9):
        return _ongewogen_graaddagen(etmaal_gem_temp) * 0.8
    else:
        return _ongewogen_graaddagen(etmaal_gem_temp)


def api_scraper(
    start=datetime.now().date() - timedelta(days=31),
    end=datetime.now().date() - timedelta(days=1),
    stations=None,
    normalize=True,
):
    """
    Haalt voor de gevraagde stations en datumbereik de volgende velden op via de KNMI API:

            DDVEC    = Vectorgemiddelde windrichting in graden (360=noord, 90=oost, 180=zuid, 270=west, 0=windstil/variabel)
            FG       = Etmaalgemiddelde windsnelheid (in 0.1 m/s)
            TG       = Etmaalgemiddelde temperatuur (in 0.1 graden Celsius)
            TN       = Minimum temperatuur (in 0.1 graden Celsius)
            TX       = Maximum temperatuur (in 0.1 graden Celsius)
            T10N     = Minimum temperatuur op 10 cm hoogte (in 0.1 graden Celsius)
            SQ       = Zonneschijnduur (in 0.1 uur) berekend uit de globale straling (-1 voor <0.05 uur)
            RH       = Etmaalsom van de neerslag (in 0.1 mm) (-1 voor <0.05 mm)
            PG       = Etmaalgemiddelde luchtdruk herleid tot zeeniveau (in 0.1 hPa) berekend uit 24 uurwaarden
            NG       = Etmaalgemiddelde bewolking (bedekkingsgraad van de bovenlucht in achtsten, 9=bovenlucht onzichtbaar)
            UG       = Etmaalgemiddelde relatieve vochtigheid (in procenten)

    Params
        start:    begindatum als datetime of string ('YYYYMMDD'); default gisteren - 31 dagen
        end:      einddatum als datetime of string ('YYYYMMDD'); default gisteren
        stations: list of int; default [260] (De Bilt)
        normalize: waarden worden geconverteerd naar eenheden die gebruikt worden binnen Eneco (e.g. hele graden Celsius ipv 0.1 graden)

    Uitvoerformaat: list of dicts

    API docs: https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script

    Uitvoerformaat van API:

    Header, regels 1 t/m NSTN+NVAR+11, beginnend met een '#':
    1 t/m 5                  disclaimer
    8 t/m 7+NSTN             stationslijst: nummer, longitude, lattitude, hoogte en naam
    9+NSTN t/m 8+NSTN+NVAR   geselecteerde variabelen met hun omschrijving
    10+NSTN+NVAR             kolomaanduidingen

    Data, regel NSTN+NVAR+12 en verder.
    Achtereenvolgens stationsnummer, 8-cijferige datum (YYYYMMDD) en de waarden van
    gekozen variabelen in komma-gescheiden kolommen.
    """

    if stations is None:
        stations = [260]

    knmi_map = {
        "STN": "STN",
        "YYYYMMDD": "YYYYMMDD",
        "DDVEC": "WINDRICHTING",
        "FG": "WINDSNELHEID",
        "TG": "TEMP_GEM",
        "TN": "TEMP_MIN",
        "TX": "TEMP_MAX",
        "T10N": "GRONDTEMP_MIN",
        "SQ": "ZONUREN",
        "RH": "NEERSLAG",
        "PG": "LUCHTDRUK",
        "NG": "BEWOLKING",
        "UG": "LUCHTVOCHTIGHEID",
    }

    assert isinstance(stations, list)
    _stations = ":".join(str(x) for x in stations)

    if isinstance(start, str):
        _start = start
    elif isinstance(start, int):
        _start = str(start)
    else:
        _start = start.strftime("%Y%m%d")

    if isinstance(end, str):
        _end = end
    elif isinstance(end, int):
        _end = str(end)
    else:
        _end = end.strftime("%Y%m%d")

    url = config.knmi_url
    post_data = {
        "start": _start,
        "end": _end,
        "stns": _stations,
        "vars": ":".join(
            [key for key in knmi_map.keys() if key not in ["STN", "YYYYMMDD"]]
        ),
    }

    logger.debug(post_data)
    logger.info("Getting measurements from knmi...")
    resp = requests.post(url, data=post_data)
    resp.raise_for_status()

    logger.debug("Got measurements from knmi, mapping values...")
    measurements = []
    to_normalize = [
        "WINDSNELHEID",
        "TEMP_GEM",
        "TEMP_MIN",
        "TEMP_MAX",
        "GRONDTEMP_MIN",
        "ZONUREN",
        "NEERSLAG",
        "LUCHTDRUK",
    ]
    for line in resp.text.split("\n"):
        if not line.lstrip().startswith("#"):
            knmi_values = [el.strip() for el in line.split(",")]

            if len(knmi_values) == len(knmi_map.keys()):
                rec = dict(zip(knmi_map.values(), knmi_values))

                for k, v in rec.items():
                    if normalize and k in to_normalize and v:
                        rec[k] = float(v) / 10

                rec["ONGEWOGEN_GRAADDAGEN"] = _ongewogen_graaddagen(rec.get("TEMP_GEM"))
                rec["GEWOGEN_GRAADDAGEN"] = _gewogen_graaddagen(
                    rec.get("TEMP_GEM"), rec.get("YYYYMMDD")[4:6]
                )
                measurements.append(rec)

    return measurements
