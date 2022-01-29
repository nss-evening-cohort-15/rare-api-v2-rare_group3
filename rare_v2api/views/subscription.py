"""View module for handling requests about subscription types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rare_v2api.models import (Subscription,RareUser)



class SubscriptionView(ViewSet):
    """Level up subscription types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single subscription type

        Returns:
            Response -- JSON serialized subscription type
        """
        try:
            subscription = Subscription.objects.get(pk=pk)
            serializer = SubscriptionSerializer(
                subscription, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all subscription types

        Returns:
            Response -- JSON serialized list of subscription types
        """
        subscriptions = Subscription.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = SubscriptionSerializer(
            subscriptions, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized subscription instance
        """
        # Uses the token passed in the `Authorization` header
        user = RareUser.objects.get(user=request.auth.user)
        author=RareUser.objects.get(pk=request.data["author"])
        # Create a new Python instance of the subscription class
        # and set its properties from what was sent in the
        # body of the request from the client.
        subscription = Subscription()
        subscription.follower = user
        subscription.author = author
        
        # Try to save the new subscription to the database, then
        # serialize the subscription instance as JSON, and send the
        # JSON as a response to the client request
            
        try:
            subscription.save()
            serializer = SubscriptionSerializer(subscription, context={'request': request})
            return Response(serializer.data)
        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            subscription = Subscription.objects.get(pk=pk)
            subscription.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for subscription types

        Arguments:
            serializers
    """
    class Meta:
        model = Subscription
        fields = ('id','follower','author','created_on','ended_on')
        
