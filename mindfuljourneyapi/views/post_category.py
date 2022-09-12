from unicodedata import name
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mindfuljourneyapi.models import PostCategory

# Goal: list of categories will appear in a dropdown menu while creating a post, user can select a category
# Create class
class PostCategoryView(ViewSet):
    """Mindful Journey PostCategory View"""
    def list(self, request):
        """Handles GET requests to get all categories for post
        Returns:
            Response -- JSON serialized list of categories"""
        
        post_categories = PostCategory.objects.all()
        serializer = PostCategorySerializer(post_categories, many=True)
        return Response(serializer.data)

#Create class for serializer
class PostCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for post_categories"""
    class Meta:
        model = PostCategory
        fields = ('id', 'name')
