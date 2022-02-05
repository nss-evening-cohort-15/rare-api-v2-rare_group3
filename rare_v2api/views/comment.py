from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.utils.timezone import make_aware
from datetime import datetime
from rare_v2api.models import Comment, Post, RareUser
from rare_v2api.views.post import PostSerializer


class CommentView(ViewSet):

    def create(self, request):

        author = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["post"])
        # created_on = make_aware(datetime.strptime(request.data["created_on"], '%Y-%m-%d'))

        comment = Comment()
        comment.post = post
        comment.author = author
        comment.content = request.data["content"]
        # comment.created_on = created_on

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        post = Post.objects.get(pk=request.data["post"])
        author = RareUser.objects.get(user=request.auth.user)

        comment = Comment.objects.get(pk=pk)
        comment.post = post
        comment.author = author
        comment.content = request.data["content"]
        comment.created_on = request.data["created_on"]
        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        comments = Comment.objects.all()
        author = RareUser.objects.get(user=request.auth.user)

        post = self.request.query_params.get('post_id', None)
        if post is not None:
            comments = comments.filter(post__id=post)

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

class CommentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CommentRareUserSerializer(serializers.ModelSerializer):

    user = CommentUserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ['user']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'category', 'publication_date', 'image_url', 'content', 'approved', 'comments')


class CommentSerializer(serializers.ModelSerializer):

    author = CommentRareUserSerializer(many=False)
    post = PostSerializer(many=False)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content', 'created_on')