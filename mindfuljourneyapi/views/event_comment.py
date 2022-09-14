from dataclasses import fields
from multiprocessing import Event
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mindfuljourneyapi.models import EventComment, Event, Meditator, event_comment
import datetime

class EventCommentView(ViewSet):
    """Event Comment View"""

    def list(self, request): 
        """Handles GET requests to get all comments
        Returns:
            Response -- JSON serialized list of event comments"""
    
        eventComments = EventComment.objects.all().order_by("created_on")
        event = request.query_params.get('event', None)
        if event is not None:
            eventComments = eventComments.filter(post_id = event)
        serializer = EventCommentSerializer(eventComments, many = True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single event comment
        Returns:
            Response -- JSON serialized  event comment"""
        try:
            eventComment = EventComment.objects.get(pk=pk)
            serializer = EventCommentSerializer(eventComment)
            return Response(serializer.data)

        except eventComment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handles POST request for event comment"""

        # Foreign Keys
        event = Event.objects.get(pk=request.data["event"]) # Check client's side
        meditator = Meditator.objects.get(user=request.auth.user)
        
        eventComment = EventComment.objects.create(
            #model #client
            event = event,
            meditator = meditator,
            comment = request.data["comment"],
            created_on = datetime.date.today()
        )
        
        serializer = EventCommentSerializer(eventComment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for event comment"""

        meditator = Meditator.objects.get(user=request.auth.user)
        
        eventComment = EventComment.objects.get(pk=pk)
        eventComment.meditator = meditator
        
        eventComment.comment = request.data["comment"]

        eventComment.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete Event Comment"""
        eventComment = EventComment.objects.get(pk=pk)
        eventComment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class EventCommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    class Meta:
        model = EventComment
        fields = ('id', 'meditator', 'event', 'comment','created_on')
        #depth = 2