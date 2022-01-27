"""View module for handling requests about reactions"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rare_v2api.models import PostReaction


class PostReactionView(ViewSet):
    """post reactions"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post reaction

        Returns:
            Response -- JSON serialized post reaction
        """
        try:
            post_reaction = PostReaction.objects.get(pk=pk)
            serializer = PostReactionSerializer(post_reaction, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all post reactions

        Returns:
            Response -- JSON serialized list of post reactions
        """
        post_reactions = PostReaction.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PostReactionSerializer(
            post_reactions, many=True, context={'request': request})
        return Response(serializer.data)

class PostReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions

    Arguments:
        serializers
    """
    class Meta:
        model = PostReaction
        fields = ('id', 'user', 'post', 'reaction')
