from django.utils import timezone

from django.db import models
from flowback.common.models import BaseModel
from flowback.user.models import User


class MembershipRegistrationPayment(BaseModel):
    platform = models.TextField()
    payment_id = models.TextField(unique=True)
    currency = models.TextField()
    amount_received = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.TextField()


class MembershipUser(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    valid_until = models.DateTimeField(default=timezone.now)
