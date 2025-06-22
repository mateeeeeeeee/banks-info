from django.core.management.base import BaseCommand
from banks.models import EconomicIndicator
import requests

class Command(BaseCommand):
    help = 'Import GDP data from World Bank API for all countries'

    def handle(self, *args, **kwargs):
        indicator_code = 'NY.GDP.MKTP.CD'  # GDP (current US$)
        page = 1
        total_pages = 1

        self.stdout.write("Fetching GDP data for all countries...")

        while page <= total_pages:
            url = f'https://api.worldbank.org/v2/country/all/indicator/{indicator_code}?format=json&per_page=100&page={page}'
            try:
                response = requests.get(url)
                response.raise_for_status()
                result = response.json()

                if page == 1:
                    total_pages = result[0]['pages']

                data = result[1]

                for item in data:
                    country = item['country']['value']
                    year = int(item['date'])
                    value = item['value']
                    indicator_name = item['indicator']['value']

                    if value is None:
                        continue

                    EconomicIndicator.objects.update_or_create(
                        country=country,
                        indicator_code=indicator_code,
                        indicator_name=indicator_name,
                        year=year,
                        defaults={'value': value}
                    )

                self.stdout.write(self.style.SUCCESS(f"Page {page}/{total_pages} imported."))
                page += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error on page {page}: {e}"))
                break

        self.stdout.write(self.style.SUCCESS("Finished importing global GDP data."))