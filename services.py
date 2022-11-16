import json
import os
from pathlib import Path

import environ
import stripe
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from flowback.common.services import get_object
from flowback.user.models import User
from flowback.membership.models import MembershipRegistrationPayment, MembershipUser

env = environ.Env(STRIPE_KEY=str,
                  STRIPE_REGISTRATION_PRODUCT=str,
                  STRIPE_SUCCESS_URL=str,
                  STRIPE_FAILURE_URL=str,
                  STRIPE_WEBHOOK_SECRET=str)

base_dir = Path(__file__).resolve().parent.parent.parent
env.read_env(os.path.join(base_dir, ".env"))

stripe.api_key = env('STRIPE_KEY')


def membership_stripe_generate(*, user: User):
    print(env("STRIPE_REGISTRATION_PRODUCT"))
    session = stripe.checkout.Session.create(
        line_items=[{
          'price': env("STRIPE_REGISTRATION_PRODUCT"),
          'quantity': 1,
        }],
        mode='payment',
        success_url=env('STRIPE_SUCCESS_URL'),
        cancel_url=env('STRIPE_FAILURE_URL')
      )

    MembershipRegistrationPayment.objects.create(platform='stripe',
                                                 payment_id=session.payment_intent,
                                                 user=user,
                                                 status=session.status,
                                                 currency=session.currency)

    return session.url


def membership_stripe_validate(*, body: dict, signature: str):
    try:
        data = stripe.Webhook.construct_event(body, signature, env('STRIPE_WEBHOOK_SECRET'))
        pobj = data.data.object
    except Exception as e:
        raise ValidationError('Signature verification failed')

    if not (pobj.object == 'payment_intent' and pobj.status == 'succeeded'):
        return

    payment = get_object(MembershipRegistrationPayment, payment_id=pobj.id)
    payment.amount_received = pobj.amount_received
    payment.status = pobj.status
    payment.save()

    member, created = MembershipUser.objects.get_or_create(user=payment.user)
    if (member.valid_until and member.valid_until < timezone.now()) or created:
        member.valid_until = timezone.now() + timezone.timedelta(days=365)

    else:
        member.valid_until += timezone.timedelta(days=365)

    member.save()
