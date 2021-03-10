from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_new", views.create_new, name="create_new"),
    path("bidding", views.bidding, name="bidding"),
    path("watching", views.watching, name="watching"),
    path("comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<str:listing>", views.listing, name="listing"),
    path("categories/<str:category>", views.category, name="category")
]
