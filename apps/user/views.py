from rest_framework import viewsets

from apps.user.models import User, Visitor
from apps.user.serializers import UserSerializer, VisitorSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

