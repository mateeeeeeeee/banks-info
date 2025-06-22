from django.db import models

class Bank(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class OfferType(models.TextChoices):
    LOAN = 'loan', 'Loan'
    DEPOSIT = 'deposit', 'Deposit'
    CREDIT_CARD = 'credit_card', 'Credit Card'


class Offer(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='offers')
    offer_type = models.CharField(max_length=20, choices=OfferType.choices)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # e.g., 7.50%
    term_months = models.PositiveIntegerField(null=True, blank=True)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    conditions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.bank.name} - {self.title}"


class EconomicIndicator(models.Model):
    country = models.CharField(max_length=100, db_index=True)
    indicator_code = models.CharField(max_length=50, db_index=True)
    indicator_name = models.CharField(max_length=255)
    year = models.PositiveIntegerField(db_index=True)
    value = models.FloatField()

    def __str__(self):
        return f"{self.country} - {self.indicator_name} ({self.year})"