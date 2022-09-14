from unicodedata import category
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mindfuljourneyapi.models import Meditator, Post
from mindfuljourneyapi.models.post_category import PostCategory
import uuid, base64
from django.core.files.base import ContentFile
import datetime

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
            posts = posts.filter(category_id=category)
        if user is not None:
            posts = posts.filter(user_id=user)
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
            meditator = Meditator.objects.get(user=request.auth.user) #user
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
        meditator = Meditator.objects.get(user=request.auth.user)
        category = PostCategory.objects.get(pk=request.data['category'])
    
    # Add header image for post here
        format, imgstr = request.data["post_image_url"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')

        post = Post.objects.create(
            meditator = meditator,
            category = category,
            title = request.data['title'],
            content = request.data['content'],
            post_image_url = data,
            created_on = datetime.date.today()
        )

        # Add tags and reactions here later
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Update post
    def update(self, request, pk):
        """Handle PUT requests for a post
        Returns:
            Response -- 204 status code"""
        post = Post.objects.get(pk=pk)
        category = PostCategory.objects.get(pk=request.data['category'])
        post.category = category
        post.title = request.data['title']
        post.content = request.data['content']
        post.post_image_url = request.data['post_image_url']
        post.created_on = datetime.date.today()

        # Save information
        post.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # Delete post
    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        #deletes post
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
#Create class for serializer
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    class Meta:
        model = Post
        fields = ('id', 'meditator', 'category', 'title', 'content', 'created_on', 'post_image_url')
        #Need to leave depth in for react to loop through meditator/user's name
        depth = 2