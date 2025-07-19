"""Views for the Network social network app."""
# pylint: disable=no-member
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import Post, User

@login_required
def index(request):
    """Main view: shows all paginated posts."""
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    serialized_posts = []
    for post in page_obj:
        post_dict = post.serialize()
        post_dict["liked"] = (request.user in post.likes.all())
        serialized_posts.append(post_dict)
    return render(request, "network/index.html", {
        "posts": serialized_posts,
        "page_obj": page_obj,
        "current_user": request.user,
    })


def login_view(request):
    """User login view."""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return render(request, "network/login.html", {
            "message": "Invalid username and/or password."
        })
    return render(request, "network/login.html")


def logout_view(request):
    """User logout view."""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """User registration view."""
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/register.html")

@login_required
def viewprofile(request, user_id):
    """User profile view."""
    this_user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=this_user)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    serialized_posts = []
    for post in page_obj:
        post_dict = post.serialize()
        post_dict["liked"] = (request.user in post.likes.all())
        serialized_posts.append(post_dict)
    current_user = request.user
    is_following = current_user in this_user.followers.all()
    followers_count = this_user.followers.all().count()
    following_count = this_user.following.all().count()
    return render(request, "network/viewprofile.html", {
        "user": this_user,
        "posts": serialized_posts,
        "current_user": current_user,
        "is_following": is_following,
        "followers_count": followers_count,
        "following_count": following_count,
        "page_obj": page_obj
    })

@login_required
def new_post(request):
    """View to create a new post."""
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            post = Post(user=request.user, content=content)
            post.save()
            return HttpResponseRedirect(reverse("viewprofile", args=(request.user.id,)))
    return HttpResponseRedirect(reverse("index"))

def following(request):
    """View for posts from followed users."""
    current_user = request.user
    following_users = current_user.following.all()
    posts = Post.objects.filter(user__in=following_users).order_by("-timestamp")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    serialized_posts = []
    for post in page_obj:
        post_dict = post.serialize()
        post_dict["liked"] = (request.user in post.likes.all())
        serialized_posts.append(post_dict)
    return render(request, "network/following.html", {
        "posts": serialized_posts,
        "current_user": current_user,
        "page_obj": page_obj
    })

@csrf_exempt
@login_required
def like(request, post_id):
    """View to like or unlike a post."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        post = Post.objects.get(pk=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        data = {
            "likes_count": post.likes.all().count(),
            "liked": liked
        }
        return JsonResponse(data, status=200)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@login_required
def follow(request, user_id):
    """View to follow or unfollow a user."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        user = User.objects.get(pk=user_id)
        current_user = request.user
        if user == current_user:
            return JsonResponse({"error": "You cannot follow yourself"}, status=400)
        if user in current_user.following.all():
            current_user.following.remove(user)
            following = False
        else:
            current_user.following.add(user)
            following = True
        data = {
            "message": "Action completed",
            "following": following,
            "followers_count": user.followers.all().count(),
            "following_count": user.following.all().count(),
            "followers_this": list(user.followers.values("id", "username")),
            "following_this": list(user.following.values("id", "username"))
        }
        return JsonResponse(data, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def edit_post(request):
    """View to edit your own post."""
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        content = request.POST.get("content")
        try:
            post = Post.objects.get(pk=post_id, user=request.user)
            post.content = content
            post.save()
            return JsonResponse({
                "success": True,
                "post_id": post_id,
                "new_content": content,
            }, status=200)
        except Post.DoesNotExist:
            return JsonResponse({
                "success": False,
                "error": "Post not found"
            }, status=404)
    return JsonResponse({
        "success": False,
        "error": "Method not allowed"
    }, status=400)
