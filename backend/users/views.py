from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated, IsAdmin,)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
