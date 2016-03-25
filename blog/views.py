
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404#, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Category, Tag
from .forms import PostEditForm

from taskqueue import make_thumbnail


def list_posts(request):
    per_page = 3
    current_page = int(request.GET.get('page', 1)) # page가 있으면 값을 가져오고 없으면 1을 가져온다.

    all_posts = Post.objects.select_related().prefetch_related().all()

    pagi = Paginator(all_posts, per_page)
    try:
        pg = pagi.page(current_page)
    except PageNotAnInteger:
        pg = pagi.page(1)
    except EmptyPage:
        pg = []
        raise Http404("해당 페이지가 존재하지 않습니다.") # 404 에러 페이지로 이동

    return render(request, 'list_posts.html', {
        'posts': pg,
    })

def view_post(request, pk):
    the_post = get_object_or_404(Post, pk=pk)
    the_comment = Comment.objects.filter(post=the_post)

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        new_comment = Comment()
        new_comment.content = request.POST.get('content')
        new_comment.post = the_post

        if new_comment.content == "": # 내용이 없는 댓글은 달리지 않는다. 하지만 스페이스를 입력하면 댓글이 달림..
            pass
        else:
            if request.user is not None:
                new_comment.user = request.user
                new_comment.save()
                return redirect('view_post', pk=the_post.pk)
            else: # request.user is None
                return redirect('login_url')

    return render(request, 'view_post.html', {
        'post': the_post,
        'comment': the_comment,
    })

@login_required
def create_post(request):
    categories = Category.objects.all()

    if request.method == 'GET':
        form = PostEditForm()
    elif request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False) # 커밋을 하지 않은 상태여야지 유저정보를 같이 저장할 수 있다.
            new_post.user = request.user
            new_post.save()
            make_thumbnail.delay(new_post.photo.path, 100, 100)
            return redirect('view_post', pk=new_post.pk)

    return render(request, 'create_post.html', {
        'form': form,
    })

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        post_edit = request.POST
        post.title = post_edit['title']
        post.content = post_edit['content']

        category = get_object_or_404(Category, pk=post_edit['category'])
        post.category = category
        post.save()
        return redirect('view_post', pk=post.pk)

    return render(request, 'edit_post.html', {
        'post': post,
        'categories': categories,
    })

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.user == request.user:
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            post.delete()
            return redirect('list_posts')
    else:
        raise PermissionDenied
        # HttpResponse('error', status_code=405) # 에러를 내고 status code를 바꾸는 명령

    return render(request, 'delete_post.html', {
        'post': post,
    })

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user == request.user:
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            comment.delete()
            return redirect('view_post', pk=comment.post.pk)
    else:
        raise PermissionDenied

    return render(request, 'delete_comment.html',{
        'comment':comment,
    })
