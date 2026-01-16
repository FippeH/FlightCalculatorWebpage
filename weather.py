from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup as BS

MET_URL = "https://aro.lfv.se/Links/Link/ViewLink?TorLinkId=314&type=MET&icao="
TAF_URL = "https://aro.lfv.se/Links/Link/ViewLink?TorLinkId=315&type=MET&icao="

def hämta_väder(url):
    try:
        AROweb = urlopen(url)
        HTML = AROweb.read().decode("utf-8")
        soup = BS(HTML, "html.parser")
        rader = soup.find_all("div", class_="tor-link-text-row")
        return [r.get_text().strip().replace("\n", " ") for r in rader]
    except:
        return ["Fel vid hämtning"]

def hämta_MET_TAF(icao):
    icao = icao.upper()
    metar = hämta_väder(MET_URL + icao)
    taf = hämta_väder(TAF_URL + icao)

    m = [rad for rad in metar if rad.startswith(icao)]
    t = [rad for rad in taf if rad.startswith(icao)]

    if not m:
        m = [f"Ingen METAR hittades för {icao}."]
    if not t:
        t = [f"Ingen TAF hittades för {icao}."]

    return "\n".join(["--- METAR ---"] + m + ["", "--- TAF ---"] + t)
