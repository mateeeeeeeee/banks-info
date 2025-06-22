from django.core.management.base import BaseCommand
from banks.models import Bank, Offer, OfferType
import requests

# Example bank API endpoint and mapping logic
BANKS_DATA = [
    {
        "name": "TBC Bank",
        "website": "https://www.tbcbank.ge",
        "logo_url": "https://tbcbank.ge/logo.png",
        "api_url": "https://api.tbcbank.ge/public-offers",  # Example URL
    },
    {
        "name": "Bank of Georgia",
        "website": "https://bankofgeorgia.ge",
        "logo_url": "https://bankofgeorgia.ge/logo.png",
        "api_url": "https://api.bog.ge/public-offers",  # Example URL
    },
    # Add more banks as needed
]

class Command(BaseCommand):
    help = "Import offers from Georgian banks' public APIs"

    def handle(self, *args, **kwargs):
        for bank_data in BANKS_DATA:
            bank, _ = Bank.objects.get_or_create(
                name=bank_data["name"],
                defaults={
                    "website": bank_data["website"],
                    "logo_url": bank_data["logo_url"]
                }
            )

            try:
                response = requests.get(bank_data["api_url"], timeout=10)
                response.raise_for_status()
                offers = response.json()

                for offer_data in offers:
                    Offer.objects.update_or_create(
                        bank=bank,
                        title=offer_data.get("title", "Untitled Offer"),
                        defaults={
                            "offer_type": offer_data.get("type", OfferType.LOAN),
                            "description": offer_data.get("description", ""),
                            "interest_rate": offer_data.get("interest_rate", 0),
                            "term_months": offer_data.get("term_months", 0),
                            "min_amount": offer_data.get("min_amount", 0),
                            "max_amount": offer_data.get("max_amount", 0),
                            "conditions": offer_data.get("conditions", ""),
                        },
                    )
                self.stdout.write(self.style.SUCCESS(f"Imported offers from {bank.name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to fetch offers from {bank.name}: {e}"))