from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.views.generic.base import View
from microbrewforyou_app.models import CustomUser, Posts, BrewTypes, Breweries
from microbrewforyou_app.forms import LoginForm, SignupForm, PostForm,\
    EditUserForm

import requests


class CitySearchView(View):
    def get(self, request, search_city):
        city_breweries_list = []
        r = requests.get(
            url=f'https://api.openbrewerydb.org/breweries?by_city={search_city}')
        # breakpoint()
        for brewery in r.json():
            # if search_city.lower() == single_brewery.city.lower() and search_state.lower() == single_brewery.state.lower():
            city_breweries_list.append(brewery)
        print(len(city_breweries_list))
        for item in city_breweries_list:
            print(item['name'])
            print(item['street'])
            print(item['city'])
            print(item['state'])
            print(item['phone'])
            print(item['website_url'])
        return render(request, 'index.html')


class IndexView(View):
    def get(self, request):
        if request.user.is_anonymous:
            follow_count = 0
        else:
            follow_count = len(request.user.users_following.all())
        return render(request, 'index.html', {'follow_count': follow_count})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get(
                    'next', reverse("homepage")))
    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = CustomUser.objects.create_user(
                username=data.get("username"), password=data.get(
                    "password"), first_name=data.get(
                        "first_name"), bio=data.get(
                            "bio"), user_image=data.get(
                                "user_image"), address=data.get(
                                    "address"), city=data.get(
                                        "city"), state=data.get("state"))
            login(request, new_user)
            return HttpResponseRedirect(reverse("homepage"))

    form = SignupForm()
    return render(request, "generic_form.html", {"form": form})


def edit_user_view(request, user_id):
    edit_user = CustomUser.objects.filter(id=user_id).first()
    if edit_user == request.user:
        if request.method == "POST":
            user_form = EditUserForm(request.POST)
            if user_form.is_valid():
                data = user_form.cleaned_data
                edit_user.username = data.get('username')
                edit_user.password = edit_user.password
                edit_user.first_name = data.get('first_name')
                edit_user.bio = data.get('bio')
                edit_user.address = data.get('address')
                edit_user.city = data.get('city')
                edit_user.state = data.get('state')
                edit_user.save()
                login(request, edit_user)
            return HttpResponseRedirect(reverse("homepage"))
        user_form = EditUserForm(initial={'username': edit_user.username,
                                          'first_name': edit_user.first_name,
                                          'bio': edit_user.bio,
                                          'address': edit_user.address,
                                          'city': edit_user.city,
                                          'state': edit_user.state})
        return render(request, "edit_user.html",
                      {"form": user_form, "profile_user": request.user})
    else:
        return HttpResponseRedirect(reverse(
            "edit_userview", args=[edit_user.id]))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


class AddPostView(View):
    def get(self, request):
        form = PostForm()
        return render(
            request, "add_post.html",
            {"form": form, "profile_user": request.user}
        )

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_post = Posts.objects.create(
                body=data.get('body'),
                author=request.user
            )
            return HttpResponseRedirect(
                reverse("postview", args=[new_post.id])
            )
        return render(
            request, "add_post.html",
            {"form": form, "profile_user": request.user}
        )


def post_detail_view(request, post_id):
    my_post = Posts.objects.filter(id=post_id).first()
    return render(
        request, "post_detail.html",
        {"post": my_post}
    )


def edit_post_view(request, post_id):
    edit_post = Posts.objects.filter(id=post_id).first()
    if edit_post.author == request.user:
        if request.method == "POST":
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                data = post_form.cleaned_data
                edit_post.body = data.get('body')
                edit_post.save()
            return HttpResponseRedirect(
                reverse("postview", args=[edit_post.id]))
        post_form = PostForm(initial={'body': edit_post.body})
        return render(request, "edit_post.html",
                      {"form": post_form, "profile_user": request.user})
    else:
        return HttpResponseRedirect(reverse(
            "edit_postview", args=[edit_post.id]))


class FollowingView(View):
    def get(self, request, follow_id):
        add_user = CustomUser.objects.filter(id=follow_id).first()
        request.user.users_following.add(add_user)
        request.user.save()
        return HttpResponseRedirect(reverse(
            "userview", args=[add_user.id]))


class UnfollowingView(View):
    def get(self, request, unfollow_id):
        remove_user = CustomUser.objects.filter(id=unfollow_id).first()
        logged_in_user = request.user
        logged_in_user.users_following.remove(remove_user)
        logged_in_user.save()
        return HttpResponseRedirect(reverse(
            "userview", args=[remove_user.id]))


class UserDetailView(View):
    def get(self, request, user_id):
        selected_user = CustomUser.objects.filter(id=user_id).first()
        following_list = request.user.users_following.all()
        number_following = len(selected_user.users_following.all())
        user_posts = Posts.objects.filter(
            author=user_id).order_by('postTime').reverse()
        number_posts = len(user_posts)
        # breakpoint()
        return render(
            request, "user_detail.html",
            {"number_posts": number_posts,
             "selected_user": selected_user,
             "user_posts": user_posts,
             "following_list": following_list,
             "number_following": number_following})


class FavoriteBreweriesView(View):
    def get(self, request, favorite_id):
        breweriesname = Breweries.objects.get(id=favorite_id)
        logged_in_user = request.user
        logged_in_user.fav_breweries.add(breweriesname)
        logged_in_user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class FavoriteBrewTypesView(View):
    def get(self, request, favorite_id):
        brewtypename = BrewTypes.objects.get(id=favorite_id)
        logged_in_user = request.user
        logged_in_user.fav_brewtypes.add(brewtypename)
        logged_in_user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
