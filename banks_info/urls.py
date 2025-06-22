"""
URL configuration for banks_info project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from allauth.account.views import confirm_email
from users.views import CustomRegisterView
from rest_framework.routers import DefaultRouter
from external_data.views import EconomicIndicatorListView
from frontend.views import home
from frontend.views import CustomConfirmEmailView, email_confirmed

router = DefaultRouter()

path('api/auth/account-confirm-email/<str:key>/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
path('email-confirmed/', email_confirmed, name='email_confirmed'),

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth URLs
    path('api/auth/', include('dj_rest_auth.urls')),

    # Override registration with your custom one
    path('api/auth/registration/', CustomRegisterView.as_view(), name='rest_register'),

    # Confirm email
    path('api/auth/account-confirm-email/<str:key>/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    path('email-confirmed/', email_confirmed, name='email_confirmed'),

    # Swagger docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('accounts/', include('allauth.urls')),
    path('api/', include('banks.urls')),

    path('api/economic-indicators/', EconomicIndicatorListView.as_view(), name='economic-indicators'),

    # Front
    path('', home, name='home'),
    path('', include('frontend.urls')),
]