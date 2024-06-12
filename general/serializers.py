from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class HelpCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpCenter
        fields = '__all__'


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class GetReplySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Reply
        exclude = ['comment']


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'


class GetCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id','user','content','date_commented', 'replies']
    
    def get_replies(self, obj):
        replies = obj.replies.all()
        serializer = GetReplySerializer(replies, many=True)
        return {
            'count': replies.count(),
            'replies': serializer.data
        }
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, attrs):
        user = attrs.get('user')
        news_feed = attrs.get('news_feed')
        if Comment.objects.filter(user=user, news_feed=news_feed).exists():
            raise serializers.ValidationError({'error':'A comment for this user and news_feed already exists'})
        
        return attrs


class NewsFeedSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        comments = obj.comments.all()
        return comments.count()
        # serializer = GetCommentSerializer(comments, many=True)
        # return {
        #     'count': comments.count(),
        #     'comments': serializer.data
        # }
    
    class Meta:
        model = NewsFeed
        fields = '__all__'