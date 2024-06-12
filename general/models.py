from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()


class FAQ(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(unique=True)

    def __str__(self):
        return self.title
    

class HelpCenter(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    
    def clean(self):
        if HelpCenter.objects.exists() and not self.pk:
            raise ValidationError("The help center banner text and description already exist")
                               
    def save(self, *args, **kwargs):
        self.id = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Events(models.Model):
    event_img = models.ImageField(upload_to='events/')

    class Meta:
        ordering = ['-id']


class NewsFeed(models.Model):
    title = models.CharField(max_length=5600)
    description = models.TextField()
    photo = models.ImageField(upload_to='newsfeed')
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_newsfeed_likes')
    news_feed = models.ForeignKey(NewsFeed, on_delete=models.CASCADE, related_name='likes')
    liked = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'news_feed')

    def __str__(self):
        return self.news_feed.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_newsfeed_comment')
    news_feed = models.ForeignKey(NewsFeed, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commnet {self.id} - NewsFeed {self.news_feed.id} - User {self.user.phone_number}'
    
    # class Meta:
    #     unique_together = ('user', 'news_feed')
    

class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies',  on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replies')
    date_replied = models.DateTimeField(auto_now_add=True)
    reply = models.TextField()

    def __str__(self):
        return self.user.phone_number

    # @property
    # def get_replies(self):
    #     return self.replies.all()



class SeeResult(models.Model):
    passed_year = models.IntegerField()
    symbol_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 