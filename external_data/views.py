from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import EconomicIndicator
from .serializers import EconomicIndicatorSerializer


class EconomicIndicatorListView(generics.ListAPIView):
    """
    API view to list Economic Indicators with filtering and ordering support.
    """
    queryset = EconomicIndicator.objects.all()
    serializer_class = EconomicIndicatorSerializer

    # Enable filtering by country, indicator_code, and year
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['country', 'indicator_code', 'year']

    # Allow ordering by year and value fields
    ordering_fields = ['year', 'value']