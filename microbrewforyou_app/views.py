from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.views.generic.base import View
from microbrewforyou_app.models import CustomUser, Posts, BrewTypes, Breweries
from microbrewforyou_app.forms import LoginForm, SignupForm, PostForm,\
    EditUserForm

import requests


class BreweriesReloadView(View):
    def get(self, request):
        if request.user.is_superuser:
            full_breweries_list = []
            r = requests.get(
                url='https://raw.githubusercontent.com/openbrewerydb/openbrewerydb/master/breweries.json')
            full_breweries_list = r.json()  # populate variable from api
            current_breweries_in_model = Breweries.objects.all()  # in model
            print('Api brewery master list count: ', len(full_breweries_list))
            print('Model Brewery list count start: ',
                  len(current_breweries_in_model))

            for item in full_breweries_list:
                list_item_name = item['name']
                list_item_city = item['city']
                for model_item in current_breweries_in_model:
                    if list_item_name == model_item.name and\
                            list_item_city == model_item.city:
                        full_match = True
                        break  # match found break out of for loop for model
                    else:
                        full_match = False
                        continue

                if full_match is False:
                    new_brewery = Breweries.objects.create(
                        name=item['name'],
                        phone=item['phone'],
                        address=item['street'],
                        city=item['city'],
                        state=item['state'],
                        website=item['website_url']
                    )
                else:
                    continue
            current_breweries_in_model = Breweries.objects.all()
            print('Model Brewery list count end: ',
                  len(current_breweries_in_model))
            return render(request, 'index.html')
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
    return render(request, "login.html", {"form": form})


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
    return render(request, "sign_up.html", {"form": form})


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

# def brewtypes_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("brewtypesview"))


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
        if selected_user.users_following:
            number_following = len(selected_user.users_following.all())
        else:
            number_following = 0
        user_posts = Posts.objects.filter(
            author=user_id).order_by('postTime').reverse()
        number_posts = len(user_posts)
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


class NearbyBreweriesView(View):
    def get(self, request):
        brewery_list_by_city = Breweries.objects.filter(city=request.user.city)

        return render(
            request, "nearby_breweries.html",
            {"brewery_list_by_city": brewery_list_by_city})


class FavoriteBrewTypesView(View):
    def get(self, request, favorite_id):
        brewtypename = BrewTypes.objects.get(id=favorite_id)
        logged_in_user = request.user
        logged_in_user.fav_brewtypes.add(brewtypename)
        logged_in_user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
