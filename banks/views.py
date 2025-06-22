from rest_framework import viewsets, filters
from .models import Bank, Offer
from .serializers import BankSerializer, OfferSerializer

class BankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['offer_type', 'bank__name', 'title']