from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from flowback.membership.services import membership_stripe_generate, membership_stripe_validate


class MembershipPaymentGenerateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        link = membership_stripe_generate(user=request.user)
        return Response(data=link, status=status.HTTP_200_OK)


class MembershipPaymentValidateAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.headers.get('stripe-signature'))
        link = membership_stripe_validate(body=request.body, signature=request.headers.get('stripe-signature'))
        return Response(data=link, status=status.HTTP_200_OK)
