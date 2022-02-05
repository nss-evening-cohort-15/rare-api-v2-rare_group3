from dataclasses import fields
from pyexpat import model
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rare_v2api.models import RareUser, Post

class RareUserView(ViewSet):

  def retrieve(self, request, pk=None):
    rareuser = request.auth.user.rare_user
    
    serializer = RareUserSerializer(rareuser, context={'request': request})
    return Response(serializer.data)
  
  def list(self, request):
    rearusers = RareUser.objects.all()
    
    serializer = RareUserSerializer(
      rearusers, many=True, context={'request': request})
    return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ('first_name', 'last_name', 'email','is_superuser', 'username')
        
class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
      model = RareUser
      fields = ('id', 'bio', 'user', 'profile_image_url', 'created_on')
      
      