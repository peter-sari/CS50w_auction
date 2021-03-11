from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    noOfwatched = models.IntegerField(default=0, verbose_name="number of listings watched")

class Listing(models.Model):
    CATEGORIES = (
        ('fashion','fashion'),
        ('electronics','electronics'),
        ('sports','sports'),
        ('home','home'),
        ('motors','motors'),
        ('art','art'),
        ('business','business'),
        ('media','media'),
        ('others','others')
    )

    listingPoster = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Poster")
    listingName = models.CharField(max_length=128, verbose_name="Auction item")
    listingDesc = models.TextField(blank=True, verbose_name="Item description")
    listingActive = models.BooleanField(default=True, verbose_name="Active listing")
    listingImage = models.URLField(blank=True, verbose_name="Link to image")
    listingCategory = models.CharField(max_length=64, choices=CATEGORIES, default='others', verbose_name="Category")
    listingFirstBid = models.DecimalField(max_digits=8, decimal_places=2, default=0.01, verbose_name="Starting bid")
    listingCreated = models.DateTimeField(auto_now_add=True, null=True)
    ### watchers = models.ManyToManyField(Watchers, blank=True, related_name="watched_item", verbose_name="Watchers")
    ### requires the Pillow library to be installed

    def __str__(self):
        return f"{self.listingName} by {self.listingPoster} in {self.listingCategory}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    haswon = models.BooleanField(default=False, verbose_name="Winner bid")

    def __str__(self):
        return f"{self.user} {self.listing} {self.amount}"

class Comment(models.Model):
    comment = models.TextField(blank=True, verbose_name="Comment")
    userID = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="Author")
    listingID = models.ForeignKey(Listing, on_delete=models.CASCADE, verbose_name="Listing item")

    def __str__(self):
        return f"{self.userID} {self.listingID} {self.comment}"

class Watching(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing} wateched by {self.user}"
