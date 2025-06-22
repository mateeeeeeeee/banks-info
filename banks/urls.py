from rest_framework.routers import DefaultRouter
from .views import BankViewSet, OfferViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'banks', BankViewSet)
router.register(r'offers', OfferViewSet)

urlpatterns = [
    path('', include(router.urls)),
]