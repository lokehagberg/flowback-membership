from django.utils import timezone
from rest_framework.permissions import BasePermission

from flowback.common.services import get_object
from flowback.membership.models import MembershipUser


class UserIsMember(BasePermission):
    message = 'User is not a member'

    def has_permission(self, request, view):
        membership = get_object(MembershipUser, user=request.user, raise_exception=False)

        if membership and membership.valid_until > timezone.now():
            return True

        return False
