from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mindfuljourneyapi.models import Meditator, Category, Post
from mindfuljourneyapi.models.post_category import PostCategory
import uuid, base64
from django.core.files.base import ContentFile

# Goal: User can view a list of posts, create a post, update a post and delete a post
# Create a class
class PostView(ViewSet):
    """Post View"""

    def list(self, request):
        """Handles GET requests for all posts
        Returns:
            Response -- JSON serialized list of posts
        """
        posts = Post.objects.all()
        # Filter through post for specific category
        category = request.query_params.get('category', None)
        user = self.request.query_params.get('user', None)

        if category is not None:
            posts = posts.filter(category=category)
        # Add tags - stretch goals
        # Add user - maybe?

        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handles GET requests for single post
        Returns: 
            Response -- JSON serialized post
        """
        try: 
            post = Post.objects.get(pk=pk)
            user = Meditator.objects.get(user=request.auth.user) #user or meditator? 
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex: 
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    # to create a new post
    def create(self, request):
        """Handles POST operations
        Returns:
            Response -- JSON serialized post instance
        """
        user = Meditator.objects.get(user=request.auth.user)
        category = PostCategory.objects.get(pk=request.data['category'])
    
    # Add header image for post here
        format, imgstr = request.data["post_image_url"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["post_id"]}-{uuid.uuid4()}.{ext}')

        user.post_image_url = data
        user.save()

        post = Post.objects.create(
            user = user,
            category = category
        )



    
#Create class for serializer
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    class Meta:
        model = Post
        fields = ('id', 'meditator', 'category', 'content', 'created_on', "post_image_url")