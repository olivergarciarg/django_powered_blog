from django.shortcuts import render, get_object_or_404, redirect
# from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import User, Post, Comment
from .models import Post, Comment
# from .forms import UserForm, PostForm, CommentForm, UserForm2
from .forms import PostForm, CommentForm, UserForm2


# Create your views here.
class SignUp(CreateView):
    form_class = UserForm2
    template_name = 'auth/user_form.html'

    # login_url = '/login/'
    #redirect_field_name = 'blog/about.html'
    # template_name = 'blog/signup.html'
    # form_class = PostForm
    # model = Post
    #form_class = UserForm
    #model = User
    def get_success_url(self):
        return reverse_lazy('about')
        # return reverse('lawyer_detail', kwargs={'lawyer_slug': self.object.lawyer_slug})

# class Register(CreateView):
#    form_class = UserForm2
#    template_name = 'auth/user_form.html'


# class CreatePostView2(CreateView):
    # login_url = '/login/'
    # redirect_field_name = 'blog/about.html'
    # template_name = 'blog/signup.html'
    # form_class = PostForm
    # model = Post
    # form_class = UserForm
    # model = User


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    model = Post

    # uses django ORM, this executes an SQL query. '__lte' below means less than or equal to.
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=False).order_by('-published_date')
        # return Post.objects.order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


# class DraftListView(LoginRequiredMixin, ListView):
class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'blog/post_draft_list.html'
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')
        # return Post.objects.order_by('created_date')


# Comments views
@login_required()
def post_publish(request, pk):
    # request is needed to redirect after login
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required()
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required()
# def comment_approve(request, pk):
def comment_approve(request, pk):
    # request is needed to redirect after login
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required()
def comment_remove(request, pk):
    # request is needed to redirect after login
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
