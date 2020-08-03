
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post


from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings


from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required
from .forms import UserCreateForm, ArticleModelForm, UpdateArticleModelForm

# Create your views here.
'''class PostCreateView(CreateView):
    template_name = 'blog/article_create.html'
    form = ArticleModelForm()
    print('hello')
    queryset = Post.objects.all()   
    print('hello')
    def form_valid(self, form):
       print(form.cleaned_data)
       return super().form_valid(form)
       class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'''


def PostList(request):
    posts = Post.objects.filter(status=1).order_by('-updated_on')
    
    return render(request, 'blog/index.html', {'posts': posts } )


def PostDetail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required(login_url="/accounts/login/")
def PostCreateView(request):
    if request.method == 'POST':
        form = ArticleModelForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('home')
    else:
        form = ArticleModelForm()
    return render(request, 'blog/article_create.html', {'form': form})


@login_required(login_url="/accounts/login/")
def PostDeleteView(request, slug):

    context = {}

    post = Post.objects.get(slug=slug)
    user = request.user
    if post.author != user:
        return HttpResponse('You are not the author of that post')

    if request.POST:
        post.delete()
        return redirect('home')

    context = {'post': post}
    return render(request, 'blog/delete.html', context)

@login_required(login_url="/accounts/login/")
def PostUpdateView(request, slug):

    context = {}
  
    blog_post = get_object_or_404(Post, slug=slug)
    user = request.user
    if blog_post.author != user:
        return HttpResponse('You are not the author of that post.')

    if request.POST:
        form = UpdateArticleModelForm(
            request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = " Post Updated "
          
            blog_post = obj
            

    form = UpdateArticleModelForm(
        initial={
            "title": blog_post.title,
            "content": blog_post.content,
            "thumb": blog_post.thumb,
        }
    )

    context['form'] = form
    return render(request, 'blog/article_update.html', context)



def contact_form(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f'Message from {form.cleaned_data["name"]}'
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["email"]
            recipients = ['chamsjlassi2@gmail.com']
            try:
                send_mail(subject, message, sender,
                          recipients, fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return HttpResponse('Success...Your email has been sent')
    return render(request, 'blog/contact.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('home')
    else:
        form = UserCreateForm()
    return render(request, 'registration/signup.html', {'form': form})

