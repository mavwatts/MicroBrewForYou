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
# if settings.DEBUG:
#     urlpatterns = static(settings.MEDIA_URL,
#                          document_root=settings.MEDIA_ROOT)

from microbrewforyou_app.views import login_view, logout_view, signup_view
from microbrewforyou_app.views import AddPostView, post_detail_view, IndexView
from microbrewforyou_app.views import UserDetailView, FavoriteBreweriesView
from microbrewforyou_app.views import edit_post_view, FollowingView
from microbrewforyou_app.views import UnfollowingView, edit_user_view
from microbrewforyou_app.views import BreweriesReloadView, NearbyBreweriesView
from microbrewforyou_app.views import BreweryDetailView, FavoriteBreweryView
from microbrewforyou_app.views import UnfavoriteBreweryView, success
from microbrewforyou_app.views import pic_form_view, FollowingBrewTypesView
from microbrewforyou_app.views import UnFollowingBrewTypesView
from microbrewforyou_app.views import UserPostListView, brewtypes_view


urlpatterns = [
     path('', IndexView.as_view(), name="homepage"),
     path('login/', login_view, name="loginview"),
     path('signup/', signup_view, name="signupview"),
     path('logout/', logout_view, name="logoutview"),
     path('user/<int:user_id>/', UserDetailView.as_view(), name="userview"),
     path('user/<int:user_id>/edit',
          edit_user_view, name="edit_userview"),
     path('user/<int:favorite_id>/favorite_breweries',
          FavoriteBreweriesView.as_view(), name="favoritebreweries"),
     path('userposts/',
          UserPostListView.as_view(), name='userposts'),
     path('post/add', AddPostView.as_view(), name="addpostview"),
     path('post/<int:post_id>/', post_detail_view, name="postview"),
     path('post/<int:post_id>/edit', edit_post_view, name="edit_postview"),
     path('loadbreweries/',
          BreweriesReloadView.as_view(), name="loadbreweriesview"),
     path('brewery/<int:brewery_id>/',
          BreweryDetailView.as_view(), name="brewery_detail"),
     path('brewery/<int:follow_id>/follow',
          FollowingView.as_view(), name="following"),
     path('brewery/<int:unfollow_id>/unfollow/',
          UnfollowingView.as_view(), name="unfollowing"),
     path('brewery/<int:brewery_id>/favorite',
          FavoriteBreweryView.as_view(), name="favorite_brewery"),
     path('brewery/<int:brewery_id>/unfavorite',
          UnfavoriteBreweryView.as_view(), name="unfavorite_brewery"),
     path('nearbybreweries/',
          NearbyBreweriesView.as_view(), name="nearbybreweriesview"),
     path('brewtypes/', brewtypes_view, name="brewtypesview"),
     path('brewtypes/<int:follow_brew_type_id>/follow',
          FollowingBrewTypesView.as_view(), name='FollowingBrewTypesView'),
     path('brewtypes/<int:unfollow_brew_type_id>/unfollow',
          UnFollowingBrewTypesView.as_view(), name='UnFollowingBrewTypesView'),
     path('image_upload', pic_form_view, name='image_upload'),
     path('success', success, name='success'),
     path('success', success, name='success'),
     path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = 'microbrewforyou_app.views.error404view'

handler403 = 'microbrewforyou_app.views.error403view'

handler500 = 'microbrewforyou_app.views.error500view'
