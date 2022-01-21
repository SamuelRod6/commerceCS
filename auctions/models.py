from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    category = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=128)
    date = models.DateTimeField(default=timezone.now)
    starting_bid = models.FloatField()
    current_bid = models.FloatField(null=True)
    is_closed = models.BooleanField(default=False)
    picture = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name ="category_listings")
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sellers")
    buyer = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    watchers = models.ManyToManyField(User, blank=True, related_name = "watched_listings")

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):  
        return f"{self.user} place a bid of {self.bid} for {self.item}"
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=256)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} made a comment about {self.item} on {self.date}'