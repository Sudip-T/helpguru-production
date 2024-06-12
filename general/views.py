from .models import *
from .serializers import *
from rest_framework import status
from rest_framework import viewsets
from core.permissions import IsObjectOwner
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


#Maniip02172014,5665
class FAQView(viewsets.ReadOnlyModelViewSet):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()
    # pagination_class = CustomPagination

    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS:
    #         permission_classes = [IsAuthenticated]
    #     elif self.action in ['create', 'update', 'destroy']:
    #         permission_classes = [IsAuthenticated, IsAdminUser]
    #     else:
    #         raise MethodNotAllowed(self.action)

    #     return [permission() for permission in permission_classes]


class HelpCenterView(viewsets.ReadOnlyModelViewSet):
    serializer_class = HelpCenterSerializer
    queryset = HelpCenter.objects.all()

    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS:
    #         permission_classes = [IsAuthenticated]
    #     elif self.action in ['create', 'update', 'destroy']:
    #         permission_classes = [IsAuthenticated, IsAdminUser]
    #     else:
    #         raise MethodNotAllowed(self.action)

    #     return [permission() for permission in permission_classes]
    
    # def create(self, request, *args, **kwargs):
    #     try:
    #         serializer = HelpCenterSerializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         error = str(e).strip("'[]'")
    #         return Response({'error':error}, status=status.HTTP_400_BAD_REQUEST)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer


class NewsFeedView(viewsets.ReadOnlyModelViewSet):
    serializer_class = NewsFeedSerializer
    queryset = NewsFeed.objects.all()


# from django.db.models import Count          

# class NewsFeedView(viewsets.ReadOnlyModelViewSet):
#     serializer_class = NewsFeedSerializer
#     queryset = NewsFeed.objects.annotate(
#         likes_count=Count('likes'),
#         comments_count=Count('comments')
#     )
    

class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.action in ['list','retrieve','create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update','destroy']:
            permission_classes = [IsAuthenticated, IsObjectOwner]
        else:
            raise MethodNotAllowed(self.action)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetCommentSerializer
        return CommentSerializer
    
    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
        else:
            try:
                data = request.data.copy()
                data['user'] = request.user.id
                serializer = self.get_serializer(data=data)
            except Exception as e:
                return Response({
                    'error':str(e) }, status=status.HTTP_400_BAD_REQUEST)
            
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReplyView(viewsets.ModelViewSet):
    queryset = Reply.objects.all()

    def get_permissions(self):
        if self.action in ['list','retrieve','create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update','destroy']:
            permission_classes = [IsAuthenticated, IsObjectOwner]
        else:
            raise MethodNotAllowed(self.action)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetReplySerializer
        return ReplySerializer
    
    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
        else:
            try:
                data = request.data.copy()
                data['user'] = request.user.id
                serializer = self.get_serializer(data=data)
            except Exception as e:
                return Response({
                    'error':str(e) }, status=status.HTTP_400_BAD_REQUEST)
            
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)