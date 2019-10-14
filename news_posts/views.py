from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)
from django.shortcuts import get_object_or_404
from .models import NewsPost
from .forms import NewsPostForm
from django.views.generic.edit import FormMixin
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from comments.forms import CommentForm
from comments.models import Comment
from .tasks import send_mail_notification_task


class NewsPostListView(ListView):
    """
    News post list
    """
    model = NewsPost
    template_name = 'news_post_list.html'
    context_object_name = 'news_post_list'
    paginate_by = 5


class NewsPostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create a news post
    """
    form_class = NewsPostForm
    template_name = 'news_post_create.html'
    success_message = 'News post was successfully created.'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewsPostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    """
    Update a news post
    """
    form_class = NewsPostForm
    model = NewsPost
    template_name = 'news_post_update.html'
    success_message = 'News post was successfully updated.'

    def get_object(self):
        slug = self.kwargs.get("slug")
        return get_object_or_404(NewsPost, slug=slug)

    def get_success_url(self):
        return self.object.get_absolute_url()

    def test_func(self):
        news_post = self.get_object()
        if self.request.user == news_post.author:
            return True
        return False


class NewsPostDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a news post
    """
    model = NewsPost
    template_name = 'news_post_delete.html'
    success_url = reverse_lazy('post_list')
    success_message = 'Post was successfully removed.'

    def get_object(self):
        slug = self.kwargs.get("slug")
        return get_object_or_404(NewsPost, slug=slug)

    def test_func(self):
        news_post = self.get_object()
        if self.request.user == news_post.author:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class NewsPostDetailView(SuccessMessageMixin, FormMixin, DetailView):
    template_name = 'news_post_detail.html'
    form_class = CommentForm
    success_url = "."
    success_message = 'Your comment was successfully added.'

    def get_object(self):
        slug = self.kwargs.get("slug")
        return get_object_or_404(NewsPost, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(self.request.POST)
        context['comment_form'] = form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        form = context['comment_form']

        if form.is_valid():
            content_data = form.cleaned_data.get('content')
            parent_obj = None
            try:
                parent_id = request.POST['parent_id']
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()

            new_comment = Comment.objects.create(
                author=self.request.user,
                content=content_data,
                parent=parent_obj,
                post=self.object
            )

            mail_subject = 'New comment'
            current_site = get_current_site(request)
            message = render_to_string('new_comment.html', {
                'post': new_comment.post,
                'domain': current_site.domain,
            })
            to_email = new_comment.post.author.email

            send_mail_notification_task.delay(mail_subject, message, to_email)
        return self.form_valid(form)
