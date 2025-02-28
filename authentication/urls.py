from .views import RegistrationView,UsernameValidationView,EmailValidationView,VerificationView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns =[
    path('register/', RegistrationView.as_view(), name='register'),  # Register URL
    path('validate-username',UsernameValidationView.as_view(), name='validate-username'),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()), name='validate-email'), # Email Validation
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),  # Verification URL
]