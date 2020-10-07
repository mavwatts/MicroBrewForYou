from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.views.generic.base import View

from microbrewforyou_app.models import CustomUser, Posts
from microbrewforyou_app.forms import LoginForm, SignupForm, PostForm
# Create your views here.


def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))
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
