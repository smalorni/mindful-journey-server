from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mindfuljourneyapi.models import Meditator, Event, ActivityLevel
import uuid, base64
from django.core.files.base import ContentFile
from rest_framework.decorators import action
from django.db.models import Q

# Goal: view list of events, create a new event, update and delete an event
# Create class
class EventView(ViewSet): 
    """Mindful Journey Events View"""

    def list(self, request):
        """Handles GET requests for all events
        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all().order_by("start_date")
        user = request.auth.user

        # add search feature for event
        search = self.request.query_params.get('search', None)

        for event in events:
            event.attending = user in event.attendee.all()
        
        #search by location, description
        if search is not None:
            events = events.filter(
                Q(location__contains=search) |
                Q(description__contains=search)
            )

        serializer = EventSerializer(events, many = True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handles GET requests for single event
        Returns: 
            Response -- JSON serialized event
        """
        try: 
            event = Event.objects.get(pk=pk)

            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex: 
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    # to create a new event
    def create(self, request):
        """Handles POST operations
        Returns:
            Response -- JSON serialized post instance
        """
        activity_level = ActivityLevel.objects.get(pk=request.data['activity_level'])
    
    # Add header image for event here
        format, imgstr = request.data["event_image_url"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')


        event = Event.objects.create(
            meditator = request.auth.user,
            name = request.data['name'],
            location = request.data['location'],
            start_date = request.data['start_date'],
            end_date = request.data['end_date'],
            host = request.data['host'],
            description = request.data['description'],
            price = request.data['price'],
            event_image_url = data,
            activity_level = activity_level
        )

        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Update event
    def update(self, request, pk):
        """Handle PUT requests for a event
        Returns:
            Response -- 204 status code"""

        # Need to include info for url
        event = Event.objects.get(pk=pk)
        # Similar to if/else statement, if an image is not updated, it will pass and save without issues
        try:
            format, imgstr = request.data["event_image_url"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')
            event.event_image_url = data #matches above
        except:
            pass
        
        activity_level = ActivityLevel.objects.get(pk=request.data['activity_level'])
        event.name = request.data['name']
        event.location = request.data['location']
        event.start_date = request.data['start_date']
        event.end_date = request.data['end_date']
        event.host = request.data['host']
        event.description = request.data['description']
        event.price = request.data['price']
        
        event.activity_level = activity_level

        # Save information
        event.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # Delete event
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        #deletes event
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # Sign up for event - related to event manager fetch calls - use signup in the url to join event
    @action(methods=['post'], detail=True)
    #The new route is named after function below - add "signup" to fetch call in event manager
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
   
        meditator = request.auth.user
        event = Event.objects.get(pk=pk)
        event.attendee.add(meditator)
        return Response({'message': 'Meditator added'}, status=status.HTTP_201_CREATED)
    # Leave an event - related to event manager fetch calls - use leave in the url for leaving event
    # Action turns a method into a new route
    # Method is 'delete', detail=true returns url with a pk
    @action(methods=['delete'], detail=True)
    # The new route is named after function below - add "leave" to fetch call in event manager
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""
   
        meditator = request.auth.user
        event = Event.objects.get(pk=pk)
        # Removes user
        event.attendee.remove(meditator)
        # Message will show up in Postman
        return Response({'message': 'Meditator removed'}, status=status.HTTP_204_NO_CONTENT)
    
#Create class for serializer
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    class Meta:
        model = Event
        fields = ('id', 'meditator', 'name', 'location', 'start_date', 'end_date', 'host', 'description', 'price', 'event_image_url', 'activity_level', 'readable_start_date', 'readable_end_date', 'attending', 'attendee')
        #depth = 2

