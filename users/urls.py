from django.urls import include, path
from rest_framework import routers
from users.views import UserViewSet

router = routers.DefaultRouter(trailing_slash=True)

router.register(r"users", UserViewSet)
