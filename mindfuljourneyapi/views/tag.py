from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mindfuljourneyapi.models import Tag

# Goal: Create tag(s) to label event
# Create class

class TagView(ViewSet):
    """Tag View"""

    def list(self, request):
        """Handle GET requests to get all tags

        Returns:
            Response -- JSON serialized list of tags
        """
        tags = Tag.objects.all()
        tag_event = request.query_params.get('event', None)
        if tag_event is not None:
            tags = tags.filter(event_id=tag_event)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single tag
        Returns:
            Response -- JSON serialized tag"""
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    # Create new tag
    def create(self, request):
        """Handle POST operations

        Returns:
            Response --JSON serialized tag instance
            """

        tag = Tag.objects.create(
            label=request.data['label']
        )

        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a tag
        
        Returns:
            Response -- 204 status code
            """
        tag = Tag.objects.get(pk=pk)
        tag.label=request.data['label']

        tag.save()

        return Response(None, status.HTTP_204_NO_CONTENT)

    # Delete tag
    def destroy(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'label')