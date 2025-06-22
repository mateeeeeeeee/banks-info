from django.core.management.base import BaseCommand
from banks.models import EconomicIndicator
import requests

class Command(BaseCommand):
    help = "Backfill missing indicator_name fields using World Bank API"

    def handle(self, *args, **kwargs):
        codes = EconomicIndicator.objects.values_list('indicator_code', flat=True).distinct()

        updated = 0
        for code in codes:
            if not code:
                continue
            url = f"https://api.worldbank.org/v2/indicator/{code}?format=json"
            try:
                response = requests.get(url)
                data = response.json()
                name = data[1][0]['name']
                updated += EconomicIndicator.objects.filter(indicator_code=code).update(indicator_name=name)
                self.stdout.write(self.style.SUCCESS(f"✔ Updated '{code}' with name '{name}'"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✖ Failed to fetch name for {code}: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f"Finished. {updated} records updated."))