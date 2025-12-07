from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Post, Comment
from .forms import UserRegisterForm, PostForm, CommentForm

# ----------------------
# User Authentication
# ----------------------
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post-list')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'blog/profile.html')

# ----------------------
# Blog Posts (CRUD)
# ----------------------
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# ----------------------
# Posts by Tag
# ----------------------
class PostByTagListView(ListView):
    """
    Shows posts that have the tag with slug `tag_slug`.
    URL pattern should be: path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), ...)
    """
    model = Post
    template_name = 'blog/post_list_by_tag.html'  # you can reuse post_list.html if preferred
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        # django-taggit stores tag names and slugs depending on usage; this filters by slug first,
        # fallback to name if slug doesn't match anything.
        qs = Post.objects.filter(tags__slug=tag_slug).distinct()
        if not qs.exists():
            qs = Post.objects.filter(tags__name__iexact=tag_slug).distinct()
        return qs.order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_slug'] = self.kwargs.get('tag_slug')
        return context

# ----------------------
# Comments
# ----------------------
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

# ----------------------
# Search
# ----------------------
def search_posts(request):
    query = request.GET.get('q', '')
    results = Post.objects.none()
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})
