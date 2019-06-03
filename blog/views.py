
from django.shortcuts                       import render, get_object_or_404, redirect
from django.urls                            import reverse
from django.contrib.auth.decorators         import login_required
from django.contrib.auth.models             import User
from django.http                            import HttpResponse, HttpResponseRedirect, JsonResponse, Http404 #new
from datetime                               import datetime
from .forms                                 import *
from .models                                import Post, Profile, Images
from django.contrib.auth                    import authenticate, login, logout
from django.db.models                       import Q
from django.core.paginator                  import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader                 import render_to_string
from django.forms                           import modelformset_factory
# Create your views here.

# def index(request):
#     return HttpResponse("hello django")

def post_list(request):
    post_list = Post.published.all().order_by('-id')
    query = request.GET.get('q')
    if query:
        post_list = Post.published.filter(
            Q(title__icontains=query)|
            Q(author__username=query)|
            Q(body__icontains=query)
            )
    
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if page is None:
        start_index = 0
        end_index = 7
    else:
        (start_index, end_index) = proper_pagination(posts, index=4)

    page_range = list(paginator.page_range)[start_index:end_index]
    
    context = {
        'posts': posts,
        'page_range': page_range,
    }
    return render(request, 'blog/post_list.html', context)


def proper_pagination(posts, index):
    start_index = 0
    end_index = 7
    if posts.number > index:
        start_index = posts.number - index
        end_index = start_index + end_index
    return (start_index, end_index)

def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    is_liked = False;
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    context ={
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes()
    }
    return render(request, 'blog/post_detail.html', context)

def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False;
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context ={
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes()
    }
    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form': html})
        

def post_create(request):
    ImageFormset = modelformset_factory(Images, fields=('image',), extra=4)
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            for f in formset:
                try:
                    photo = Images(post=post, image=f.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    break
            return redirect('post_list')



    else:
        form = PostCreateForm()
        formset = ImageFormset(queryset=Images.objects.none())
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'blog/post_create.html', context)


def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.author:
        raise Http404()
    if request.method == "POST":
        form = PostEditForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'blog/post_edit.html', context)





def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('post_list'))
                else:
                    return HttpResponse("User is not activate")
            else:
                return HttpResponse("User in None")
    else:
        form = UserLoginForm()

    context = {
            'form': form,
        }
    return render(request, 'blog/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('post_list')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('post_list')

    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }

    return render(request, 'registration/register.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse("blog:edit_profile"))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'blog/edit_profile.html', context)


