import graphene
from graphene_django.debug import DjangoDebug

from chowkidar.graphql import AuthMutations
from user.graphql import UserMutations, UserQueries


class Mutation(
    AuthMutations,
    UserMutations,
):
    pass


class Query(
    UserQueries,
):
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(mutation=Mutation, query=Query)
