from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Comment, Listing, Bid

class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': "form-control"}))
    description = forms.CharField(label="Description", widget=forms.TextInput(attrs={'class': "form-control"}))
    picture = forms.CharField(label="Image URL", required=False, empty_value="https://i.stack.imgur.com/y9DpT.jpg", widget=forms.TextInput(attrs={'class': "form-control"}))
    starting_bid = forms.FloatField(min_value=1, label="Starting Price", widget=forms.NumberInput(attrs={'class': "form-control"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': "form-control"}))

class NewBidForm(forms.Form):
    new_bid = forms.FloatField(min_value=1, label=False, widget=forms.NumberInput(attrs={'class': "form-control"}))

class NewCommentForm(forms.Form):
    new_comment = forms.CharField(max_length=128, label=False, widget=forms.TextInput(attrs={'class': "form-control"}))



def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def listing_page(request, item_id):
    listing = Listing.objects.get(id=item_id)
    if request.user in listing.watchers.all():
        is_watched = True
    else:
        is_watched = False
    
    if request.method == "POST":
        form = NewBidForm(request.POST)
        if form.is_valid():
            new_bid = form.cleaned_data["new_bid"]
            current_bid = listing.current_bid
            if new_bid > current_bid:
                listing.current_bid = new_bid
                listing.save()
                bid = Bid(item=listing, bid=current_bid, user=request.user)
                bid.save()
            else:
                return render(request, "auctions/listing.html", {
                    "is_watched": is_watched,
                    "listing": listing,
                    "bid_form": form,
                    "comment_form": NewCommentForm(),
                    "message": "New bid has to be higher than the current bid"
                })
    return render(request, "auctions/listing.html", {
                "is_watched": is_watched,
                "listing": listing,
                "bid_form": NewBidForm(),
                "comment_form": NewCommentForm()
            })

@login_required(login_url="login")
def comment(request, item_id):
    listing = Listing.objects.get(id=item_id)
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["new_comment"]
            new_comment = Comment(user=request.user, item=listing, comment=comment)
            new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=[item_id]))



@login_required(login_url="login")
def close(request, item_id):
    listing = Listing.objects.get(id=item_id)
    if request.method == "POST":
        close = request.POST["close"]
        if close == "Close auction":
            listing.is_closed = True
            if listing.starting_bid > listing.current_bid:
                listing.buyer = listing.bids.last().user
            listing.save()
    return HttpResponseRedirect(reverse("listing", args=[item_id]))


@login_required(login_url="login")
def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["description"]
            picture = form.cleaned_data["picture"]
            s_bid = form.cleaned_data["starting_bid"]
            cat = form.cleaned_data["category"]
            username = request.user
        
            new_listing = Listing(title=title, description=desc, picture=picture, starting_bid=s_bid,\
                        current_bid=s_bid, category=cat, seller=username)
            new_listing.save()

            return HttpResponseRedirect(reverse('listing', args=[new_listing.id]))

        else:
            return render(request, "auctions/new.html", {
            "form": form
        })
    else:
        return render(request, "auctions/new.html", {
            "form": NewListingForm()
        })


@login_required(login_url="login")
def watchlist(request):
    watchlist = request.user.watched_listings.all()
    return render(request, "auctions/watchlist.html", {
    "watchlist": watchlist
    })


@login_required(login_url="login")
def watch(request, item_id):
    listing = Listing.objects.get(id=item_id)
    watch = request.POST["watch"]
    if watch == "Remove from watchlist":
        listing.watchers.remove(request.user)
    elif watch == "Add to watchlist":
        listing.watchers.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=[item_id]))

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
    "categories": categories
    })


def category(request, category):
    category_listings = Category.objects.get(category=category).category_listings.all()
    return render(request, "auctions/category.html", {
    "category_name": category,
    "category": category_listings
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



