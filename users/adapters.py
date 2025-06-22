from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from django.core.exceptions import PermissionDenied

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.phone_number = form.cleaned_data.get('phone_number')
        if commit:
            user.save()
        return user

    def login(self, request, user):
        email_address = EmailAddress.objects.filter(user=user, email=user.email).first()
        if email_address and not email_address.verified:
            raise PermissionDenied("Email address not verified.")
        return super().login(request, user)