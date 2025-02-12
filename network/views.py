from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import User

@login_required
def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    serialized_posts = []
    for post in page_obj:  # iteramos solo sobre los posts de la página actual
        post_dict = post.serialize()
        post_dict["liked"] = (request.user in post.likes.all())
        serialized_posts.append(post_dict)
    
    return render(request, "network/index.html", {
        "posts": serialized_posts,
        "page_obj": page_obj,
        "current_user": request.user,
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def viewprofile(request, id):
    this_user = User.objects.get(pk=id)
    posts= Post.objects.filter(user=this_user)
    paginator =Paginator(posts, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    serialized_posts = []
    for post in page_obj:
        post_dict = post.serialize()
        # Agregamos la verificación de si el usuario ya dio like
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
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            post = Post(user=request.user, content=content)
            post.save()
            return HttpResponseRedirect(reverse("viewprofile", args=(request.user.id,)))
        
def following(request):
    current_user = request.user
    following = current_user.following.all()
    posts = Post.objects.filter(user__in=following).order_by("-timestamp")
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
    post = Post.objects.get(pk=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        post.save()
        liked = False
    else:
        post.likes.add(user)
        post.save()
        liked = True

    data = {
        "likes_count": post.likes.all().count(),
        "liked": liked
    }
    return JsonResponse(data, status=200)

@csrf_exempt
@login_required
def follow(request, user_id):
    user = User.objects.get(pk=user_id)         
    current_user = request.user                
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


@login_required
def edit_post(request):
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
                "error": "Post no encontrado"
            }, status=404)
    return JsonResponse({
        "success": False,
        "error": "Método no permitido"
    }, status=400)