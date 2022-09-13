from argparse import Action
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from mindfuljourneyapi.models import Meditator

# Goal: User can update profile information

# Create a class
class MeditatorProfileView(ViewSet):
    """Meditator profiles list view"""
    def list(self, request):
        """Handles GET requests to get all profiles
        Returns:
            Response -- JSON serialized list of profiles"""
        
        profiles = Meditator.objects.all()

        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handles PUT Requests for a meditator
        Returns:
            Response --JSON serialized for individual profile"""
        try: 
            profile = Meditator.objects.get(pk=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
            #Responds with 404 message - alert - does not exist
        except Meditator.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
    
    # Update profile
    def update(self, request, pk):
        """Handles PUT Requests for Profile
        Returns:
            Response -- 204 Status Code"""

        user = request.auth.user

        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.email = request.data['email']

        user.save()

        meditator = Meditator.objects.get(pk=pk)

        meditator.bio = request.data['bio']
        meditator.location = request.data['location']
        meditator.profile_image_url = request.data['profile_image_url']

        meditator.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')

class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for profile"""
    user = UserProfileSerializer()
    class Meta: 
        model = Meditator
        fields = ('id', 'user', 'bio', 'location', 'profile_image_url')
        depth = 1


