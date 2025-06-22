import requests
from django.core.management.base import BaseCommand
from banks.models import EconomicIndicator

INDICATORS = {
    "NY.GDP.MKTP.CD": "GDP (current US$)",
    "FP.CPI.TOTL.ZG": "Inflation, consumer prices (annual %)",
    "SL.UEM.TOTL.ZS": "Unemployment rate (% of total labor force)",
    "FR.INR.RINR": "Real interest rate (%)",
    "NE.EXP.GNFS.CD": "Exports of goods and services (current US$)",
    "NE.IMP.GNFS.CD": "Imports of goods and services (current US$)",
    "SP.POP.TOTL": "Population, total",
    "GC.DOD.TOTL.GD.ZS": "Central government debt, total (% of GDP)",
    "FP.RGD.TOTL": "Real GDP growth (annual %)",
    "BX.KLT.DINV.CD.WD": "Foreign direct investment, net inflows (BoP, current US$)"
}

class Command(BaseCommand):
    help = "Import multiple economic indicators from World Bank for all countries"

    def handle(self, *args, **options):
        for code, name in INDICATORS.items():
            self.stdout.write(f"Importing {name} ({code})...")
            url = f"http://api.worldbank.org/v2/country/all/indicator/{code}?format=json&per_page=10000"
            response = requests.get(url)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Failed to fetch {code}"))
                continue

            try:
                data = response.json()[1]  # second item is the actual data
                for entry in data:
                    country = entry.get("country", {}).get("value")
                    year = int(entry.get("date"))
                    value = entry.get("value")
                    if country and year and value is not None:
                        EconomicIndicator.objects.update_or_create(
                            country=country,
                            year=year,
                            indicator_code=code,
                            defaults={
                                "indicator_name": name,
                                "value": value,
                            },
                        )
                self.stdout.write(self.style.SUCCESS(f"Imported {name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing {code}: {e}"))
