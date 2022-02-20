from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import PaginationLimit
from api.serializers import FollowSerializer
from constants.types import MessageTexts, MessageTypes

from .models import Follow

User = get_user_model()


class FoodgramUserViewSet(UserViewSet):
    pagination_class = PaginationLimit

    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({
                MessageTypes.Error: MessageTexts.SelfSubscribing
            }, status=status.HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(user=user, author=author).exists():
            return Response({
                MessageTypes.Error: MessageTexts.AllReadySubscribed
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(user=user, author=author)
        serializer = FollowSerializer(follow, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({
                MessageTypes.Error: MessageTexts.SelfUnsubscribing
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.filter(user=user, author=author)

        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            MessageTypes.Error: MessageTexts.AllReadyUnsubscribed
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
