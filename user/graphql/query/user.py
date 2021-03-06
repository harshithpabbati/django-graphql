import graphene
from django.db.models import Q
from chowkidar.graphql.decorators import resolve_user, login_required

from framework.graphql.utils import APIException

from ...models import User
from ..types.user import PersonalProfile, BasicUserProfile


class UserQueries(graphene.ObjectType):
    me = graphene.Field(PersonalProfile)
    user = graphene.Field(
        BasicUserProfile,
        username=graphene.String(required=True),
        description="View a User Profile"
    )
    isUsernameAvailable = graphene.Boolean(
        username=graphene.String(description="username to be checked", required=True),
        description="Check if an username is already in use or if it is available."
    )
    searchUser = graphene.List(
        BasicUserProfile,
        query=graphene.String(required=True),
        description="Search for a user"
    )

    @resolve_user
    def resolve_me(self, info, **kwargs):
        return info.context.user

    @staticmethod
    def resolve_user(self, info, username):
        try:
            return User.objects.get(username=username, is_active=True)
        except User.DoesNotExist:
            raise APIException('User not found', code='USER_NOT_FOUND')

    @staticmethod
    def resolve_isUsernameAvailable(self, info, username, **kwargs):
        if username is not None and len(username) > 0:
            try:
                User.objects.get(username=username)
                return False
            except User.DoesNotExist:
                return True
        else:
            raise APIException("Invalid username provided", code='INVALID_USERNAME')

    @login_required
    def resolve_searchUser(self, info, query, **kwargs):
        return User.objects.filter(
            Q(username__istartswith=query) |
            Q(first_name__istartswith=query) |
            Q(last_name__istartswith=query)
        )[:5]


__all__ = [
    'UserQueries'
]
