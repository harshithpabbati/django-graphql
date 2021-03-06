import graphene
from django.db.models import Q

from chowkidar.graphql.decorators import resolve_user
from chowkidar.graphql.exceptions import APIException

from ...models import User
from ...utils.auth import generate_username_from_email, generate_password
from ..inputs import UserCreationInput
from ..types.user import PersonalProfile


class AccountCreationResponse(
    graphene.ObjectType,
    description='Response received on account creation mutation'
):
    returning = graphene.Field(PersonalProfile, description='User fields to be returned')
    generatedPassword = graphene.String(description='automatically generated password, if no password was provided')


class AccountCreate(
    graphene.Mutation,
    description='Creates an user account'
):
    class Arguments:
        input = graphene.Argument(
            UserCreationInput,
            required=True,
            description='Fields accepted to create an user account'
        )

    Output = AccountCreationResponse

    @staticmethod
    def mutate(self, info, input):
        try:
            user = User.objects.get(Q(username=input.username) | Q(email=input.email))
            if user.username == input.username:
                raise APIException('Username already taken.', code='USERNAME_TAKEN')
            raise APIException('An account with this email already exist.', code='EMAIL_IN_USE')
        except User.DoesNotExist:
            username = input.username if input.username is not None else generate_username_from_email(input.email)
            password = input.password if input.password is not None else generate_password()
            user = User.objects.create(
                first_name=input.firstName if input.firstName is not None else username,
                last_name=input.lastName if input.lastName is not None else '',
                email=input.email,
                username=username,
            )
            user.set_password(password)
            user.save()
            return AccountCreationResponse(
                returning=user,
                generatedPassword=password if input.password is None else None,
            )


class PasswordChange(
    graphene.Mutation,
    description='Change the password of the logged-in user'
):
    class Arguments:
        oldPassword = graphene.String(
            required=True,
            description='Old password of the user'
        )
        newPassword = graphene.String(
            required=True,
            description='New password of the user'
        )

    Output = graphene.Boolean

    @resolve_user
    def mutate(self, info, oldPassword, newPassword):
        user = info.context.user
        if user.check_password(raw_password=oldPassword):
            user.set_password(raw_password=newPassword)
            user.save()
            return True
        else:
            raise APIException('Invalid old password', code='INVALID_OLD_PASSWORD')


class AccountMutations(graphene.ObjectType):
    accountCreate = AccountCreate.Field()
    passwordChange = PasswordChange.Field()


__all__ = [
    'AccountMutations'
]
