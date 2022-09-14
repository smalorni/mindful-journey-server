from dataclasses import fields
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mindfuljourneyapi.models import PostComment, Post, Meditator
import datetime

class PostCommentView(ViewSet):
    """Post Comment View"""

    def list(self, request): 
        """Handles GET requests to get all comments
        Returns:
            Response -- JSON serialized list of post comments"""
    
        postComments = PostComment.objects.all().order_by("created_on")
        post = request.query_params.get('post', None)
        if post is not None:
            postComments = postComments.filter(post_id = post)
        serializer = PostCommentSerializer(postComments, many = True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single post comment
        Returns:
            Response -- JSON serialized  post comment"""
        try:
            postComment = PostComment.objects.get(pk=pk)
            serializer = PostCommentSerializer(postComment)
            return Response(serializer.data)

        except postComment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handles POST request for post comment"""

        # Foreign Keys
        post = Post.objects.get(pk=request.data["post"]) # Check client's side
        meditator = Meditator.objects.get(user=request.auth.user)
        
        postComment = PostComment.objects.create(
            #model #client
            post = post,
            meditator = meditator,
            comment = request.data["comment"],
            created_on = datetime.date.today()
        )
        
        serializer = PostCommentSerializer(postComment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for post comment"""

        meditator = Meditator.objects.get(user=request.auth.user)
        
        postComment = PostComment.objects.get(pk=pk)
        postComment.meditator = meditator
        
        postComment.comment = request.data["comment"]

        postComment.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete Post Comment"""
        postComment = PostComment.objects.get(pk=pk)
        postComment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class PostCommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    class Meta:
        model = PostComment
        fields = ('id', 'meditator', 'post', 'comment','created_on')
        #depth = 2