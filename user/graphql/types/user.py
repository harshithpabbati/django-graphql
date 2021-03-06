import graphene


class BasicUserProfile(graphene.ObjectType, description='Basic profile of a user'):
    id = graphene.String()
    username = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()


class PersonalProfile(BasicUserProfile, graphene.ObjectType, description='Own profile of the requesting user'):
    lastLogin = graphene.DateTime()
    email = graphene.String()
    isEmailVerified = graphene.Boolean()


__all__ = [
    'BasicUserProfile',
    'PersonalProfile'
]
