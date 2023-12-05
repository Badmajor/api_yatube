from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response

from rest_framework.permissions import BasePermission, SAFE_METHODS

from posts.models import Comment, Group, Post
from rest_framework.viewsets import GenericViewSet

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class CustomPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [CustomPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'post', 'delete'])
    def comments(self, request, *args, **kwargs):
        post = self.get_object()
        if request.method == 'GET':
            data = Comment.objects.filter(post=post)
            serializer = CommentSerializer(data, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(post=post, author=request.user)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [CustomPermission]

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentView(GenericViewSet, RetrieveModelMixin,
                  UpdateModelMixin, DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CustomPermission]
