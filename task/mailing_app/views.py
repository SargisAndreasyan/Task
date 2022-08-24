from django.shortcuts import render
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')