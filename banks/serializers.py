from rest_framework import serializers
from .models import Bank, Offer

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class OfferSerializer(serializers.ModelSerializer):
    bank = BankSerializer()

    class Meta:
        model = Offer
        fields = '__all__'