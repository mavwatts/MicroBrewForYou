from django.shortcuts import render, HttpResponseRedirect, reverse, redirect,\
    get_object_or_404  # , HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.base import View
from microbrewforyou_app.models import CustomUser, Posts, BrewTypes, Breweries
from microbrewforyou_app.forms import LoginForm, SignupForm, PostForm,\
    EditUserForm, PicForm

from itertools import chain

# from django.templatetags.static import static  # might cause problem
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
            full_match = False
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
            return HttpResponseRedirect(reverse("homepage"))

        return HttpResponseRedirect(reverse("homepage"))


class IndexView(View):
    def get(self, request):
        words_quote = "They who drink beer, think beer."
        words_author = "Washington Irving"
        all_posts = []
        following_users_list = request.user.users_following.all()
        for user in following_users_list:
            user_posts = Posts.objects.filter(author=user.id)
            for post in user_posts:
                all_posts.append(post)
        user_posts = Posts.objects.filter(
            author=request.user)
        for post in user_posts:
            all_posts.append(post)
        all_posts_sorted = all_posts.sort(
            key=lambda x: x.postTime, reverse=True)
        number_posts = len(Posts.objects.filter(author=request.user))
        if request.user.is_anonymous:
            follow_count = 0
        else:
            follow_count = len(request.user.users_following.all())
        return render(request, 'index.html', {'follow_count': follow_count,
                                              'number_posts': number_posts,
                                              'words_author': words_author,
                                              "words_quote": words_quote,
                                              'all_posts': all_posts})


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
    words_quote = "He was a wise man who invented beer."
    words_author = "Plato"
    return render(request, "login.html", {"form": form,
                                          'words_author': words_author,
                                          "words_quote": words_quote})


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
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
    words_quote = "Beer, it’s the best damn drink in the world."
    words_author = "Jack Nicholson"
    return render(request, "sign_up.html", {"form": form,
                                            'words_author': words_author,
                                            "words_quote": words_quote})


def success(request):
    return HttpResponse('successfully uploaded')


def edit_user_view(request, user_id):
    edit_user = CustomUser.objects.filter(id=user_id).first()
    if edit_user == request.user:
        if request.method == "POST":
            user_form = EditUserForm(request.POST, request.FILES)
            if len(request.FILES) == 0:
                updated_request_files = request.FILES.copy()
                updated_request_files.update(
                    {'user_image': edit_user.user_image}
                )
                user_form = EditUserForm(request.POST, updated_request_files)
            if user_form.is_valid():
                data = user_form.cleaned_data
                edit_user.username = data.get('username')
                edit_user.password = edit_user.password
                edit_user.first_name = data.get('first_name')
                edit_user.bio = data.get('bio')
                edit_user.user_image = data.get('user_image')
                edit_user.address = data.get('address')
                edit_user.city = data.get('city')
                edit_user.state = data.get('state')
                # breakpoint()
                edit_user.save()
                login(request, edit_user)
            return HttpResponseRedirect(reverse("homepage"))
        user_form = EditUserForm(initial={'username': edit_user.username,
                                          'first_name': edit_user.first_name,
                                          'bio': edit_user.bio,
                                          'user_image': edit_user.user_image,
                                          'address': edit_user.address,
                                          'city': edit_user.city,
                                          'state': edit_user.state})
        words_quote = "A man who lies about beer makes enemies."
        words_author = "Stephen King"
        return render(request, "edit_user.html",
                      {"form": user_form,
                       "profile_user": request.user,
                       'words_author': words_author,
                       "words_quote": words_quote})
    else:
        return HttpResponseRedirect(reverse(
            "edit_userview", args=[edit_user.id]))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


class AddPostView(View):
    def get(self, request):
        words_quote = "For a quart of Ale is a dish for a king."
        words_author = "William Shakespeare"
        form = PostForm()
        return render(
            request, "add_post.html",
            {"form": form, "profile_user": request.user,
                'words_author': words_author, "words_quote": words_quote}
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
        words_quote = (
            "Beer is proof that God loves us and wants us to be happy."
        )
        words_author = "Benjamin Franklin"
        return render(
            request, "add_post.html",
            {"form": form, "profile_user": request.user,
                'words_author': words_author, "words_quote": words_quote}
        )


def post_detail_view(request, post_id):
    my_post = Posts.objects.filter(id=post_id).first()
    words_quote = "Beer, it’s the best damn drink in the world."
    words_author = "Jack Nicholson"
    return render(
        request, "post_detail.html",
        {"post": my_post,
         'words_author': words_author, "words_quote": words_quote}
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
        words_quote = "He was a wise man who invented beer."
        words_author = "Plato"
        return render(request, "edit_post.html",
                      {"form": post_form, "profile_user": request.user,
                       'words_author': words_author,
                       "words_quote": words_quote}
                      )
    else:
        return HttpResponseRedirect(reverse(
            "edit_postview", args=[edit_post.id]))


class UserPostListView(View):
    def get(self, request):
        user_posts = Posts.objects.filter(
            author=request.user).order_by('postTime').reverse()
        return render(
            request, "user_posts.html",
            {"user_posts": user_posts}
        )

    # model = Posts
    # template_name = 'index.html'
    # context_object_name = 'posts'

    # def get_context_data(self, **kwargs):
    #     context = super(UserPostListView, self).get_context_data(**kwargs)
    #     user = get_object_or_404(
    #         CustomUser, username=self.kwargs.get('username'))
    #     liked = [i for i in Posts.objects.filter(
    #         user_name=user) if Like.objects.filter(user=self.request.user, post=i)]
    #     context['liked_post'] = liked
    #     return context

    # def get_queryset(self):
    #     user = get_object_or_404(
    #         CustomUser, username=self.kwargs.get('username'))
    #     return Posts.objects.filter(user_name=user).order_by('-date_posted')


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


class FavoriteBreweryView(View):
    def get(self, request, brewery_id):
        brewery = Breweries.objects.filter(id=brewery_id).first()
        request.user.fav_breweries.add(brewery)
        request.user.save()
        return HttpResponseRedirect(reverse(
            "brewery_detail", args=[brewery.id]))


class UnfavoriteBreweryView(View):
    def get(self, request, brewery_id):
        brewery = Breweries.objects.filter(id=brewery_id).first()
        request.user.fav_breweries.remove(brewery)
        request.user.save()
        return HttpResponseRedirect(reverse(
            "brewery_detail", args=[brewery.id]))


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
        words_quote = "For a quart of Ale is a dish for a king."
        words_author = "William Shakespeare"
        return render(
            request, "user_detail.html",
            {"number_posts": number_posts,
             "selected_user": selected_user,
             "user_posts": user_posts,
             "following_list": following_list,
             "number_following": number_following,
             'words_author': words_author, "words_quote": words_quote}
        )


class BreweryDetailView(View):
    def get(self, request, brewery_id):
        words_quote = "He was a wise man who invented beer."
        words_author = "Plato"
        brewery = Breweries.objects.filter(id=brewery_id).first()
        return render(request,
                      "brewery_detail.html",
                      {"brewery": brewery,
                       'words_author': words_author,
                       "words_quote": words_quote}
                      )


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
            {"brewery": brewery_list_by_city})


# class FavoriteBrewTypesView(View):
#     def get(self, request, favorite_id):
#         brewtypename = BrewTypes.objects.get(id=favorite_id)
#         logged_in_user = request.user
#         logged_in_user.fav_brewtypes.add(brewtypename)
#         logged_in_user.save()
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class FollowingBrewTypesView(View):
    def get(self, request, follow_brew_type_id):
        request.user.fav_brewtypes.add(follow_brew_type_id)
        brewtype = BrewTypes.objects.filter(id=follow_brew_type_id).first()
        brewtype_image = static(f'images/{follow_brew_type_id}.JPG')
        brewtype.img_upload = brewtype_image
        brewtype.save()
        request.user.save()
        return HttpResponseRedirect(reverse(
            "homepage"))


class UnFollowingBrewTypesView(View):
    def get(self, request, unfollow_brew_type_id):
        request.user.fav_brewtypes.remove(unfollow_brew_type_id)
        request.user.save()
        return HttpResponseRedirect(reverse(
            "homepage"))


def pic_form_view(request, brew_type_id):
    edit_brew_type = BrewTypes.objects.filter(id=brew_type_id).first()

    if request.method == 'POST':
        form = PicForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            edit_brew_type.img_upload = data.get(img_upload)
            form.save()
            return redirect('success')
    else:
        form = PicForm()
    breakpoint()
    return render(request, 'favorite_brew_type.html', {'form': form})


def error404view(request, exception):
    return render(request, '404.html')


def error403view(request, exception):
    return render(request, '403.html')


def error500view(request):
    return render(request, '500.html')
