from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from posts.serializers import PostSerializer, CommentSerializer
from posts.models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def partial_update(self, request, pk=None):
        post = Post.objects.get(id=pk)
        if post.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = Post.objects.get(id=pk)
        if self.request.user != post.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, post_id, pk=None):
        comment = Comment.objects.filter(post=post_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def partial_update(self, request, post_id, pk=None):
        comment = Comment.objects.get(id=pk)
        if comment.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, post_id, pk=None):
        comment = Comment.objects.get(id=pk)
        if self.request.user != comment.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
