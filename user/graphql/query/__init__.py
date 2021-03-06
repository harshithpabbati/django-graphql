import graphene
from .user import UserQueries as UQ


class UserQueries(UQ, graphene.ObjectType):
    pass


__all__ = [
    'UserQueries'
]
