from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.utils.timezone import make_aware
from datetime import datetime
from rare_v2api.models import Post, RareUser, Category, Comment, PostReaction, postreaction



class PostView(ViewSet):

    def create(self, request):

        user = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])
        # publication_date = make_aware(datetime.strptime(request.data["publication_date"], '%Y-%m-%d'))

        post = Post()
        post.user = user
        post.title = request.data["title"]
        post.category = category
        # post.publication_date = publication_date
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        user = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])

        post = Post.objects.get(pk=pk)
        post.user = user
        post.title = request.data["title"]
        post.category = category
        # post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        posts = Post.objects.all()
        user = RareUser.objects.get(user=request.auth.user)

        # for post in posts:
        #     post.joined = user in post.posts.all()

        category = self.request.query_params.get('catergory_id', None)
        if category is not None:
            posts = posts.filter(category__id=type)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)


class PostUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PostRareUserSerializer(serializers.ModelSerializer):

    user = PostUserSerializer(many=False)
    class Meta:
        model = RareUser
        fields = ['id', 'user', 'bio']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'label')


class CommentSerializer(serializers.ModelSerializer):

    author = PostRareUserSerializer(many=False)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_on')

class PostReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions

    Arguments:
        serializers
    """
    class Meta:
        model = PostReaction
        fields = ('id', 'user', 'post', 'reaction')
class PostSerializer(serializers.ModelSerializer):

    user = PostRareUserSerializer(many=False)
    category = CategorySerializer(many=False)
    comments = CommentSerializer(many=True)
    post_reactions = PostReactionSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'category', 'publication_date', 'image_url', 'content', 'approved', 'comments', 'post_reactions')
