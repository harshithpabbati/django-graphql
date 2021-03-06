from datetime import datetime

import graphene
from chowkidar.graphql.decorators import resolve_user
from framework.graphql.utils import APIException

from ..inputs import UserProfileInput
from ..types.user import PersonalProfile


class AccountUpdationResponse(
    graphene.ObjectType,
    description='Response received on account updation mutation'
):
    returning = graphene.Field(
        PersonalProfile,
        description='User fields to be returned'
    )


class ProfileUpdate(
    graphene.Mutation,
    description='Updates the account of the logged-in user'
):
    class Arguments:
        input = graphene.Argument(
            UserProfileInput,
            required=True,
            description='Fields accepted for updation of the user profile'
        )

    Output = AccountUpdationResponse

    @resolve_user
    def mutate(self, info, input):
        user = info.context.user
        if hasattr(input, "firstName") and input.firstName is not None:
            user.first_name = input.firstName
        if hasattr(input, "lastName") and input.lastName is not None:
            user.last_name = input.lastName
        if hasattr(input, "state") and input.state is not None:
            user.state = input.state
        if hasattr(input, "dateOfBirth") and input.dateOfBirth is not None:
            user.dateOfBirth = datetime.fromisoformat(input.dateOfBirth)
        if hasattr(input, "bio") and input.bio is not None:
            user.bio = input.bio
        if hasattr(input, "url") and input.url is not None:
            user.url = input.url

        user.save()
        return AccountUpdationResponse(returning=user)

#
# class ProfileMediaUpload(graphene.Mutation):
#     Output = graphene.Boolean
#
#     @resolve_user
#     def mutate(self, info):
#         user = info.context.user
#         if info.context.FILES:
#             if 'userAvatar' in info.context.FILES:
#                 user.avatar = info.context.FILES['userAvatar']
#             if 'userCover' in info.context.FILES:
#                 user.cover = info.context.FILES['userCover']
#             user.save()
#             return True
#         else:
#             raise APIException("File not attached", code="FILE_NOT_ATTACHED")


class ProfileMutations(graphene.ObjectType):
    profileUpdate = ProfileUpdate.Field()
    # profileMediaUpload = ProfileMediaUpload.Field()


__all__ = [
    'ProfileMutations'
]
