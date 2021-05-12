from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
# from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm
from posts.models import Post, Group, Comment, Follow

User = get_user_model()

"""
Роман Ли, здравствуй! Хотел поблагодарить Вас за помощь!
Много нового и интересного узнаю благодаря Вашему ревью.
Одни положительные эмоции, спасибо еще раз? словами не передать
Вам свою благодарность =)!
Но тут возникла проблема...
При использовании cache_page ломаются тесты.
Я подумал, что cache_page не стоит использовать в тестах
и в сдаче работы на ревью, так как данные сначала сохраняются,
а затем путь к url и этим данным теряется.
Я пытался найти решение в интернете, но безуспешно.
"""
# @cache_page(20, key_prefix="index_page")


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  'base/index.html',
                  {'page': page})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    count = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'author': author,
                                            'page': page,
                                            'count': count})


def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=(username))
    author = post.author
    count = author.posts.count()
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    if request.method == "POST":
        return add_comment(request, username, post_id)
    return render(request, 'posts/post.html', {'author': author,
                                               'count': count,
                                               'post': post,
                                               'comments': comments,
                                               'form': form})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    return render(request, 'posts/new_post.html', {'form': form})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=(username))
    author = post.author
    if request.user != author:
        return redirect('post', username=author, post_id=post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('post', username=author, post_id=post_id)
    return render(request, 'posts/post_edit.html', {'form': form,
                                                    'author': author,
                                                    'post_id': post_id,
                                                    'post': post})


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=(username))
    author = post.author
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('post', username=author, post_id=post_id)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "posts/follow.html", {'page': page})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        if Follow.objects.filter(user=request.user,
                                 author=author).exists() is False:
            Follow.objects.create(user=request.user, author=author)
    return redirect('profile', username=author)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.get(user=request.user, author=author).delete()
    return redirect('profile', username=author)


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
