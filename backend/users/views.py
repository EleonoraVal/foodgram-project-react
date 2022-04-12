from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import LimitPageSizePagination
from api.permissions import AllowAny
from api.serializers import FollowSerializer, SubscriptionSerializer
from recipes.models import Follow

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    pagination_class = LimitPageSizePagination

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True,
            methods=('post', 'delete'),
            permission_classes=(IsAuthenticated, ))
    def subscribe(self, request, pk):
        author = get_object_or_404(User, id=pk)
        user = self.request.user
        is_already_follow = Follow.objects.filter(
            user=user, author=author).exists()
        data = {
            'user': user.pk,
            'author': author.pk,
        }
        serializer = SubscriptionSerializer(data=data,
                                            context={'request': request})
        if request.method == 'POST':
            if not is_already_follow:
                new_following = Follow.objects.create(
                    user=user,
                    author=author
                )
                recipes_limit = self.request.query_params.get('recipes_limit')
                serializer = FollowSerializer(
                    new_following,
                    context={'request': request,
                             'recipes_limit': recipes_limit}
                )
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response('Подписка уже была оформлена '
                            f'{author.username} (id - {pk})',
                            status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            if is_already_follow:
                Follow.objects.filter(user=user, author=author).delete()
                return Response('Подписка удалена',
                                status=status.HTTP_204_NO_CONTENT)
            return Response('Подписки на этого автора не было!'
                            f'{author.username} (id - {pk})',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
