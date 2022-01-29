"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import ValidationError
from rare_v2api.models import Category
from rest_framework import status


class CategoryView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(
                category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        categories = Category.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized category instance
        """
        # Uses the token passed in the `Authorization` header
        # Create a new Python instance of the subscription class
        # and set its properties from what was sent in the
        # body of the request from the client.
        label=Category.objects.get(label=request.data["label"])
        category = Category()
        category.label = label
        # Try to save the new category to the database, then
        # serialize the category instance as JSON, and send the
        # JSON as a response to the client request
            
        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for game types

        Arguments:
            serializers
    """
    class Meta:
        model = Category
        fields = ('id','label')
