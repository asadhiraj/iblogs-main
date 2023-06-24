from django.http import HttpResponse
from blog.models import Post, Category, Comments
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentsForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category

from .forms import UpdatePostForm


# Create your views here.
from django.core.paginator import Paginator

def home(request):
    # load all the posts from the database
    all_posts = Post.objects.all()

    # create a Paginator object with a desired number of posts per page
    posts_per_page = 5
    paginator = Paginator(all_posts, posts_per_page)

    # get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # get the Page object for the requested page number
    page_obj = paginator.get_page(page_number)

    # retrieve the posts for the current page
    posts = page_obj.object_list

    # get all the categories
    cats = Category.objects.all()

    data = {
        'posts': posts,
        'cats': cats,
        'page_obj': page_obj  # include the Page object in the data for template rendering
    }
    return render(request, 'home.html', data)



def post(request, url):
    post = Post.objects.get(url=url)
    cats = Category.objects.all()
    # print(post)
    return render(request, 'posts.html', {'post': post, 'cats': cats})


def category(request, url):
    cat = Category.objects.get(url=url)
    posts = Post.objects.filter(cat=cat)
    cats = Category.objects.all()
    return render(request, "category.html", {'cats': cats,'cat': cat, 'posts': posts})

def about(request):
    cats = Category.objects.all()
    # print(post)
    return render(request, 'about.html', {'cats': cats})




def catagor(request):
    # load all the post from db(10)
    # print(posts)

    cats = Category.objects.all()

    data = {
        'cats': cats
    }
    return render(request, 'catagor.html', data)


def blog(request):
    # load all the post from db(10)
    posts = Post.objects.all()[:11]
    # print(posts)
    cats = Category.objects.all()

    data = {
        'posts': posts,
        'cats': cats
    }
    return render(request, 'blog.html', data)

def post_details(request, url):
    post = get_object_or_404(Post, url=url)
    comments = post.comments.all()
    cats = Category.objects.all()

    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            author = form.cleaned_data['author']
            content = form.cleaned_data['content']
            comment = Comments(author=author, content=content, post=post)
            comment.save()
            return redirect('post_details', url=url)
    else:
        form = CommentsForm()

    context = {
        'post': post,
        'comments': comments,
        'cats': cats,
        'form': form
    }
    return render(request, 'post_details.html', context)


def search_results(request):
    query = request.GET.get('query')

    # Search in the Post model
    posts = Post.objects.filter(title__icontains=query)

    # Search in the Category model
    categories = Category.objects.filter(title__icontains=query)

    context = {
        'posts': posts,
        'categories': categories,
    }

    return render(request, 'search_results.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import CreateUserForm

def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Get the user object without saving to the database
            password = form.cleaned_data['password']
            hashed_password = make_password(password)  # Create a hashed password
            user.password = hashed_password  # Assign the hashed password to the user object
            user.save()  # Save the user object to the database
            return redirect('acco')
    else:
        form = CreateUserForm()

    return render(request, 'create_user.html', {'form': form})


def acco(request):
    return render(request, 'acco.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to the desired page after successful login
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''

    return render(request, 'login.html', {'error_message': error_message})


from django.shortcuts import render
from .models import Category, Post
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'profile.html', context)




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CreatePostForm

@login_required
@permission_required('blog.add_post', raise_exception=True)
def create_blog_view(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('profile')

    else:
        form = CreatePostForm()

    context = {
        'form': form,
    }
    return render(request, 'create_blog.html', context)


from django.shortcuts import redirect, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import permission_required

@login_required
@permission_required('blog.delete_post', raise_exception=True)
def delete_blog_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id,)
    post.delete()
    return redirect('profile')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import CreatePostForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import UpdatePostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
@login_required
@permission_required('blog.change_post', raise_exception=True)
def update_post_view(request, post_id):
    post = get_object_or_404(Post, post_id=post_id,)

    if request.method == 'POST':
        form = UpdatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdatePostForm(instance=post)

    context = {
        'form': form,
    }
    return render(request, 'update_post.html', context)

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')
