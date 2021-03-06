import graphene


class UserCreationInput(graphene.InputObjectType):
    email = graphene.String(required=True, description='Email address of the user')
    password = graphene.String(description='Login password for the user')
    username = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()


class UserProfileInput(graphene.InputObjectType):
    username = graphene.String(description='Valid username for the user')
    firstName = graphene.String(description='First name of the user')
    lastName = graphene.String(description='Last name of the user')
    bio = graphene.String(description='Bio of the user')
    url = graphene.String(description='Link to website/blog etc. of the user')
    state = graphene.String(description='State of Residence of the user')
    dateOfBirth = graphene.String(description='Date of birth of the user')


__all__ = [
    'UserCreationInput',
    'UserProfileInput'
]
