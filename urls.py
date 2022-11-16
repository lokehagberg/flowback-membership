from django.urls import path

from .views import MembershipPaymentGenerateAPI, MembershipPaymentValidateAPI

membership_patterns = [
    path('generate_payment', MembershipPaymentGenerateAPI.as_view(), name='membership-generate-payment'),
    path('validate_payment', MembershipPaymentValidateAPI.as_view(), name='membership-validate-payment'),
]
