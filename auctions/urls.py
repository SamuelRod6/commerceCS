from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:item_id>", views.listing_page, name="listing"),
    path("watch/<int:item_id>", views.watch, name="watch"),
    path("close/<int:item_id>", views.close, name="close"),
    path("comment/<int:item_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("<str:category>", views.category, name="category"),
]
