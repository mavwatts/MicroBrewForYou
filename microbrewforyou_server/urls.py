"""microbrewforyou_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns = static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
from microbrewforyou_app.views import login_view, logout_view,\
    signup_view, AddPostView, post_detail_view, IndexView,\
    UserDetailView, edit_post_view, FollowingView, UnfollowingView, \
    BreweriesReloadView, NearbyBreweriesView, BreweryDetailView,\
    FavoriteBreweryView, UnfavoriteBreweryView, brewtypes_view,\
    FollowingBrewTypesView, UnFollowingBrewTypesView, edit_user_view, pic_form_view, success



urlpatterns = [
    path('', IndexView.as_view(), name="homepage"),
    path('post/<int:post_id>/', post_detail_view, name="postview"),
    path('loadbreweries/',
         BreweriesReloadView.as_view(), name="loadbreweriesview"),
    path('nearbybreweries/',
         NearbyBreweriesView.as_view(), name="nearbybreweriesview"),
    path('editpost/<int:post_id>/', edit_post_view, name="edit_postview"),
    path('addpost/', AddPostView.as_view(), name="addpostview"),
    path('user/<int:user_id>/', UserDetailView.as_view(), name="userview"),
    path('edituser/<int:user_id>/',
         edit_user_view, name="edit_userview"),
    path('login/', login_view, name="loginview"),
    path('signup/', signup_view, name="signupview"),
    path('logout/', logout_view, name="logoutview"),
    path('followingbrewtypes/<int:follow_brew_type_id>/', FollowingBrewTypesView.as_view(), name='FollowingBrewTypesView'),
    path('unfollowingbrewtypes/<int:unfollow_brew_type_id>/', UnFollowingBrewTypesView.as_view(), name='UnFollowingBrewTypesView'),
    path('brewtypes/', brewtypes_view, name="brewtypesview"),
    path('image_upload', pic_form_view, name='image_upload'),
    path('success', success, name='success'),
    # path('fav_brewtypes/<int:favorite_id>/',
    #      FavoriteBrewTypesView.as_view(), name="favoritebrewtypes"),
    # path('fav_breweries/<int:favorite_id>/',
    #      FavoriteBreweriesView.as_view(), name="favoritebreweries"),
    path('unfollowing/<int:unfollow_id>/',
         UnfollowingView.as_view(), name="unfollowing"),
    path('following/<int:follow_id>/',
         FollowingView.as_view(), name="following"),
    path('brewery/<int:brewery_id>/',
         BreweryDetailView.as_view(), name="brewery_detail"),
    path('favorite_brewery/<int:brewery_id>/',
         FavoriteBreweryView.as_view(), name="follow_brewery"),
    path('unfavorite_brewery/<int:brewery_id>/',
         UnfavoriteBreweryView.as_view(), name="unfollow_brewery"),
    path('admin/', admin.site.urls),
]

