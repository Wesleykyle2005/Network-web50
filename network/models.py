"""Models for the Network social network app."""
# pylint: disable=no-member
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Extended user with followers and following relationships."""
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True)
    def serialize(self):
        """Serialize the user for JSON responses."""
        return {
            "id": self.id,
            "username": self.username,
            "is_authenticated": self.is_authenticated,
            "followers": [{"id": follower.id, "username": follower.username} for follower in self.followers.all()],
            "following": [{"id": following.id, "username": following.username} for following in self.following.all()]
        }
    def __str__(self):
        return f"{self.username} (ID: {self.id}, Followers: {self.followers.count()}, Following: {self.following.count()})"
    
class Post(models.Model):
    """Post model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts")
    def serialize(self):
        """Serialize the post for JSON responses."""
        return {
            "id": self.id,
            "user": self.user,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": [like.username for like in self.likes.all()]
        }
    def __str__(self):
        return f"Post by {self.user.username} (ID: {self.id}, Likes: {self.likes.count()})"
