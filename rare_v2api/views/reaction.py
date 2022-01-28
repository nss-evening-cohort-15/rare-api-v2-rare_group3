"""View module for handling requests about reactions"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rare_v2api.models import Reaction


class ReactionView(ViewSet):
    """reactions"""

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

class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions

    Arguments:
        serializers
    """
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')
