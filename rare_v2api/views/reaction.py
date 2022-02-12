"""View module for handling requests about reactions"""
from cProfile import label
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rare_v2api.models import Reaction
from rare_v2api.models import RareUser
from django.core.exceptions import ValidationError
from rare_v2api.models import PostReaction


class ReactionView(ViewSet):
    """reactions"""


    def create(self, request):
        reaction = Reaction()
        
        user = RareUser.objects.get(user=request.auth.user)
        label = request.data["label"]
        image_url = request.data["image_url"]
        
        reaction.user = user
        reaction.label = label
        reaction.image_url = image_url
        

        try:
            reaction.save()
            serializer = ReactionSerializer(reaction, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single reaction

        Returns:
            Response -- JSON serialized reaction
        """
        try:
            reaction = Reaction.objects.get(pk=pk)
            serializer = ReactionSerializer(reaction, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all reactions

        Returns:
            Response -- JSON serialized list of reactions
        """
        reactions = Reaction.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = ReactionSerializer(
            reactions, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            reaction = Reaction.objects.get(pk=pk)
            reaction.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions

    Arguments:
        serializers
    """
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')
