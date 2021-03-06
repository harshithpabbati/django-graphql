from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from chowkidar.graphql import GraphQLView
from django.conf import settings
from framework.graphql.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=settings.DEBUG))),
]
