from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    # Add phone_number field as required
    phone_number = serializers.CharField(max_length=20, required=True)

    def get_cleaned_data(self):
        """
        Extend the base cleaned_data with phone_number
        """
        data = super().get_cleaned_data()
        data['phone_number'] = self.validated_data.get('phone_number')
        return data

    def save(self, request):
        """
        Save the user instance, including the phone_number field
        """
        user = super().save(request)
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        return user