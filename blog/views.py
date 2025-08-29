from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Post
from .forms import PostForm

# --- FBV for homepage ---
def home(request):
    posts = Post.objects.all()[:5]  # latest 5 posts
    form = None

    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                messages.success(request, "New post created successfully 🎉")
                return redirect("blog:home")
        else:
            form = PostForm()

    return render(request, "blog/home.html", {"posts": posts, "form": form})

# --- CBVs for CRUD ---
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_message = "Post '%(title)s' was created successfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Your post has been created successfully 🎉")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_message = "Post '%(title)s' was updated successfully!"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        messages.success(self.request, "Your post has been updated ✅")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post was deleted ❌")
        return super().delete(request, *args, **kwargs)
