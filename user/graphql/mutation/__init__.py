import graphene
from .account import *
from .profile import *


class UserMutations(ProfileMutations, AccountMutations, graphene.ObjectType):
    pass


__all__ = [
    'UserMutations'
]
