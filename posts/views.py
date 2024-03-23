from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostListView(ListView):
  template_name = 'posts/list.html'
  model = Post

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['post_list'] = Post.objects.order_by('created_on').reverse()
    return context

class PostDetailView(DetailView):
  template_name = 'posts/detail.html'
  model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
  template_name = 'posts/new.html'
  model = Post
  fields = ['title', 'subtitle','body']

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  template_name = 'posts/edit.html'
  model = Post
  fields = ['title', 'subtitle','body']

  def test_func(self):
    author = self.get_object().author
    if self.request.user == author:
      return True
    return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  template_name = 'posts/delete.html'
  model = Post
  success_url = reverse_lazy('list')

  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False
