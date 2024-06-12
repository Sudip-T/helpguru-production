from .views import *
from django.urls import path, include
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register(r'faqs', FAQView, basename='faqs')
router.register(r'reply', ReplyView, basename='reply')
router.register(r'comment', CommentView, basename='comment')
router.register(r'newsfeed', NewsFeedView, basename='newsfeed')
router.register(r'help-center', HelpCenterView, basename='help-center')
router.register(r'events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls))
]