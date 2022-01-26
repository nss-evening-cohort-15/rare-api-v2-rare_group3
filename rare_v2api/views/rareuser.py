from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rare_v2api.models import RareUser
from rare_v2api.views.post import PostUserSerializer

@api_view(['GET'])
def get_rareuser_profile(request):
  rareuser = request.auth.user
  
  serializer = RareUserSerializer(rareuser)
  return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ('first_name', 'last_name', 'email')
      
class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    
    posts = PostUserSerializer(many = True)
    class Meta:
      model = RareUser
      fields = ('id', 'posts', 'bio', 'user')
    