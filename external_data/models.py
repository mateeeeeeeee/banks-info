from django.db import models

class EconomicIndicator(models.Model):
    country = models.CharField(max_length=100)
    indicator_code = models.CharField(max_length=50)
    indicator_name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    value = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('country', 'indicator_code', 'year')

    def __str__(self):
        return f"{self.country} - {self.indicator_name} ({self.year})"