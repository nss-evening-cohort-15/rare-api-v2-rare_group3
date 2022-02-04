from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rare_v2api.models import RareUser, Post

class ProfileView(ViewSet):
  def list(self, request):    # sourcery skip: merge-dict-assign
    user = RareUser.objects.get(user=request.auth.user)
    posts = Post.objects.filter(user=user) 
    posts = PostSerializer(
      posts, many=True, context={'request' : request}
    )
    user = RareUserSerializer(
      user, context={'request': request})
    
    profile = {}
    profile["user"] = user.data
    profile["posts"] = posts.data
    
    return Response(profile)
  
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('first_name', 'last_name' )
    
class RareUserSerializer(serializers.ModelSerializer):
  user = UserSerializer(many=False)
  class Meta:
    model = RareUser
    fields = ('profile_image_url', 'created_on', 'user')
    
class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ('id', 'title', 'image_url', 'content', 'publication_date' )