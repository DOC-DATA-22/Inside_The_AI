"""
fetch_sources.py — Episode 2, Doomsday Prepper AI
Downloads public-domain U.S. government preparedness pages and saves clean text
into sources/web/. Run from the episode-2 folder:  python fetch_sources.py
"""
import os
import re
import time
import requests
from bs4 import BeautifulSoup

OUT_DIR = os.path.join("sources", "web")
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) prepper-ai-dataset-builder"}

# name -> url  (all U.S. federal government = public domain)
SOURCES = {
    # Ready.gov / FEMA
    "ready_water":          "https://www.ready.gov/water",
    "ready_food":           "https://www.ready.gov/food",
    "ready_kit":            "https://www.ready.gov/kit",
    "ready_power_outages":  "https://www.ready.gov/power-outages",
    "ready_evacuation":     "https://www.ready.gov/evacuation",
    "ready_shelter":        "https://www.ready.gov/shelter",
    "ready_plan":           "https://www.ready.gov/plan",
    "ready_hurricanes":     "https://www.ready.gov/hurricanes",
    "ready_winter":         "https://www.ready.gov/winter-weather",
    "ready_extreme_heat":   "https://www.ready.gov/heat",
    "ready_floods":         "https://www.ready.gov/floods",
    "ready_wildfires":      "https://www.ready.gov/wildfires",
    "ready_tornadoes":      "https://www.ready.gov/tornadoes",
    "ready_earthquakes":    "https://www.ready.gov/earthquakes",
    # CDC
    "cdc_water_safe":       "https://www.cdc.gov/water-emergency/about/index.html",
    "cdc_water_storage":    "https://www.cdc.gov/water-emergency/about/how-to-create-and-store-an-emergency-water-supply.html",
    # EPA
    "epa_disinfection":     "https://www.epa.gov/ground-water-and-drinking-water/emergency-disinfection-drinking-water",
    # USDA FSIS / FDA / FoodSafety.gov
    "usda_food_emergencies": "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/emergencies/keep-your-food-safe-during-emergencies",
    "foodsafety_power_outage": "https://www.foodsafety.gov/food-safety-charts/food-safety-during-power-outage",
    "fda_power_floods":     "https://www.fda.gov/food/buy-store-serve-safe-food/food-and-water-safety-during-power-outages-and-floods",
    # NOAA / NWS
    "nws_safety":           "https://www.weather.gov/safety/",
    "nws_heat":             "https://www.weather.gov/safety/heat",
    "nws_cold":             "https://www.weather.gov/safety/cold",
    "nws_lightning":        "https://www.weather.gov/safety/lightning",
    # Department of Energy (home renewable / solar basics)
    "doe_renewable_planning": "https://www.energy.gov/energysaver/planning-home-renewable-energy-systems",
    "doe_solar_planning":   "https://www.energy.gov/energysaver/planning-home-solar-electric-system",
}


def clean_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "noscript"]):
        tag.decompose()
    main = soup.find("main") or soup.find("article") or soup.body or soup
    text = main.get_text("\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def main():
    ok, failed = [], []
    for name, url in SOURCES.items():
        path = os.path.join(OUT_DIR, f"{name}.txt")
        if os.path.exists(path):
            print(f"SKIP  {name:22s} already saved")
            ok.append(name)
            continue
        try:
            r = requests.get(url, headers=HEADERS, timeout=90)
            if r.status_code != 200:
                failed.append((name, url, f"HTTP {r.status_code}"))
                print(f"FAIL  {name:22s} HTTP {r.status_code}")
                continue
            text = clean_text(r.text)
            if len(text) < 500:
                failed.append((name, url, f"only {len(text)} chars"))
                print(f"FAIL  {name:22s} only {len(text)} chars (probably blocked/JS page)")
                continue
            path = os.path.join(OUT_DIR, f"{name}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"SOURCE: {url}\n\n{text}")
            ok.append(name)
            print(f"OK    {name:22s} {len(text):7d} chars")
        except Exception as e:
            failed.append((name, url, str(e)))
            print(f"FAIL  {name:22s} {e}")
        time.sleep(1)  # be polite to .gov servers

    print(f"\nSaved {len(ok)} pages to {OUT_DIR}")
    if failed:
        print(f"{len(failed)} failed:")
        for name, url, why in failed:
            print(f"  - {name}: {why}\n      {url}")


if __name__ == "__main__":
    main()
