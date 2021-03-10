from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Comment, Watching
from django.db.models import Max, Count

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['listingName', 'listingDesc', 'listingImage', 'listingCategory', 'listingFirstBid']


def index(request):

    ###bids = Bid.objects.order_by('listing','-amount')
    bids = list(Bid.objects.values('listing').annotate(max_amount=Max('amount')).order_by('listing'))
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.filter(listingActive=True),
        "bids" : bids
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_new(request):
    if request.method == "POST":
        f = ListingForm(request.POST)
        new_listing = f.save(commit=False)
        new_listing.listingPoster = request.user
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_new.html", {
            "form": ListingForm()
        })

def listing(request, listing):
    ###get listing
    l = Listing.objects.filter(id=listing)
    ###check if there is a bid
    if Bid.objects.filter(listing=l[0]):
        ###get highest bid
        bids = Bid.objects.filter(listing=l[0]).order_by('-amount').first()
        noOfBids = Bid.objects.values('listing').annotate(num_bids=Count('amount')).filter(listing=listing)
        ###get the number of bids

        currentprice = bids.amount
        ###get highest bidder
        highestBidder = bids.user
        minprice = float(currentprice)+0.01
    else:
        currentprice = l[0].listingFirstBid
        minprice = currentprice

    ### check if being watched by the current user
    
    if Watching.objects.filter(listing=l[0], user=request.user):
        iwatch = True
    else:
        iwatch = False
    

    return render(request, "auctions/listing.html",{
        "listing" : Listing.objects.filter(id=listing),
        "price": currentprice,
        "minprice": minprice,
        "highestBidder": highestBidder,
        "comments": Comment.objects.filter(listingID=listing),
        "noOfBids": noOfBids,
        "iwatch": iwatch
    })

        
@login_required
def bidding(request):
    if request.method == "POST":
        listingID = int(request.POST["listingID"])
        bidAmount = float(request.POST["amount"])
        bidder = request.user
        listing = Listing.objects.filter(id=listingID)

        ### ensure haswon is False and listing is Active

        b = Bid(user=bidder, listing=listing[0], amount=bidAmount)
        b.save()

    return HttpResponseRedirect("/{listing}".format(listing=listingID)
    )

@login_required
def comment(request):
    if request.method == "POST":
        listingID = int(request.POST["listingID"])
        comment_text = request.POST["comment_text"]
        poster = request.user
        listing = Listing.objects.filter(id=listingID)

        c = Comment(comment=comment_text, userID=poster, listingID=listing[0])
        c.save()
    return HttpResponseRedirect("/{listing}".format(listing=listingID))

def categories(request):
    allcategories = list(Listing.CATEGORIES)

    return render(request, "auctions/categories.html",{
        "allcategories": allcategories
    })

def category(request, category):
    bids = list(Bid.objects.values('listing').annotate(max_amount=Max('amount')).order_by('listing'))
    listings = Listing.objects.filter(listingActive=True).filter(listingCategory=category)
    if listings.count() == 0:
        header = f"No item in the {category} category yet"
    else:
        header= category.capitalize()

    return render(request, "auctions/index.html",{
            "listings" : listings,
            "bids" : bids,
            "header": header
        })


@login_required
def watching(request):
    if request.method == "POST":
        listingID = int(request.POST["listingID"])
        watcher = request.user
        listing = Listing.objects.filter(id=listingID)

        ### check if is in the list : add or remove
        if Watching.objects.filter(listing=listing[0], user=request.user):

            ### remove user
            Watching.objects.filter(listing=listing[0], user=request.user).delete()
        else:
            
            ### add user to the watchlist
            w = Watching(user=watcher, listing=listing[0])
            w.save()

    
    if Watching.objects.values('user').annotate(watched_items=Count('listing')).filter(user=request.user):
        wcount = Watching.objects.values('user').annotate(watched_items=Count('listing')).filter(user=request.user)[0]
        noOfW = wcount['watched_items']
    else:
        noOfW = 0

    u = request.user
    u.noOfwatched = noOfW
    u.save()

    return HttpResponseRedirect("/{listing}".format(listing=listingID)
    )
@login_required    
def watchlist(request):
    if Watching.objects.filter(user=request.user):
        wlist = Watching.objects.filter(user=request.user)
        message = "Your watched items:"

    else:
        message = "Your watchlist is empty"
        wlist = None


    
    return render(request, "auctions/watchlist.html",{
        "message": message,
        "wlist": wlist
    })