from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Catogary
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/index.html', context)


# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/index.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = 5

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['cats'] = Catogary.objects.all()
    # And so on for more models
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, id = self.kwargs['pk'])
        total_likes = post.total_likes()
        is_liked = False
        if post.likes.filter(id= self.request.user.id).exists():
            is_liked=True
        context['total_likes'] = total_likes
        context['is_liked'] = is_liked
    # And so on for more models
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','catogary', 'image', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','catogary', 'image', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def CatogaryView(request, cats):
    context = {
        'cats': cats,
        'catogary_posts': Post.objects.filter(catogary__name=cats)
    }
    return render(request, 'blog/catogaries.html', context)

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked=False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def search(request):
    query = request.GET['search_query']
    if len(query)>20:
        all_posts = []
    else:
        context = {
            'all_posts': Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query) ,
            'query' : query
        }
    return render(request, 'blog/search.html' , context)
