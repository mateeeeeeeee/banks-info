import requests
from django.core.management.base import BaseCommand
from external_data.models import EconomicIndicator

class Command(BaseCommand):
    help = 'Fetches World Bank economic data for selected indicators'

    def handle(self, *args, **options):
        countries = ['US', 'GE', 'CN', 'DE', 'FR']
        indicators = {
            'NY.GDP.MKTP.CD': 'GDP (current US$)',
            'FP.CPI.TOTL.ZG': 'Inflation (CPI)',
            'SL.UEM.TOTL.ZS': 'Unemployment rate',
            'FB.BNK.CAPA.ZS': 'Bank capital to assets ratio (%)',
        }

        for code, name in indicators.items():
            for country in countries:
                url = f'https://api.worldbank.org/v2/country/{country}/indicator/{code}?format=json&per_page=100'
                response = requests.get(url)
                data = response.json()

                if not isinstance(data, list) or len(data) < 2:
                    self.stdout.write(f"❌ Failed to get data for {country} {code}")
                    continue

                for entry in data[1]:
                    year = entry['date']
                    value = entry['value']
                    if value is None:
                        continue

                    EconomicIndicator.objects.update_or_create(
                        country=entry['country']['value'],
                        indicator_code=code,
                        year=int(year),
                        defaults={
                            'indicator_name': name,
                            'value': float(value)
                        }
                    )
        self.stdout.write(self.style.SUCCESS("✅ Economic data fetched successfully."))