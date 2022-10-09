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
        posts = Post.objects.all().order_by('-created_on')
        # Filter through post for specific category
        category = request.query_params.get('category', None)
        user = self.request.query_params.get('user', None)

        if category is not None:
            posts = posts.filter(category_id=category)
        if user is not None:
            posts = posts.filter(user_id=user)
        
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handles GET requests for single post
        Returns: 
            Response -- JSON serialized post
        """
        try: 
            post = Post.objects.get(pk=pk)
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
        category = PostCategory.objects.get(pk=request.data['category'])
    
    # Add header image for post here
        format, imgstr = request.data["post_image_url"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')

        post = Post.objects.create(
            meditator = request.auth.user,
            category = category,
            title = request.data['title'],
            content = request.data['content'],
            post_image_url = data,
            created_on = datetime.date.today()
        )

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Update post
    def update(self, request, pk):
        """Handle PUT requests for a post
        Returns:
            Response -- 204 status code"""
        post = Post.objects.get(pk=pk)
        # Need to include info for url
        # Similar to if/else statement, if an image is not updated, it will pass and save without issues
        try:
            format, imgstr = request.data["post_image_url"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')
            post.post_image_url = data
        except:
            pass

        category = PostCategory.objects.get(pk=request.data['category'])
        post.category = category
        post.title = request.data['title']
        post.content = request.data['content']
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
        fields = ('id', 'meditator', 'category', 'title', 'content', 'created_on', 'post_image_url', 'readable_created_on', 'post_comments')
        #Need to leave depth in for react to loop through meditator/user's name
        depth = 3