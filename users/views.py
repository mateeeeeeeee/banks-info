from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    request=CustomRegisterSerializer,
    responses={201: None},
)
class CustomRegisterView(RegisterView):
    """
    Custom user registration view that uses a custom serializer.
    Extended schema for API documentation.
    """
    serializer_class = CustomRegisterSerializer