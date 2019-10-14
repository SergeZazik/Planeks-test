# from django.views.generic import DetailView, DeleteView
# from django.views.generic.edit import FormMixin
# from django.core.exceptions import PermissionDenied
# from django.shortcuts import get_object_or_404
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib import messages
# from django.urls import reverse_lazy
#
#
# from .models import Comment
# from .forms import CommentForm
#
#
# class CommentDetailView(FormMixin, DetailView):
#     form_class = CommentForm
#     template_name = 'comment_detail.html'
#     success_url = '.'
#
#     def get_queryset(self):
#         return Comment.objects.filter(id=self.kwargs['pk'], parent=None)
#
#     def get_context_data(self, **kwargs):
#         context = super(CommentDetailView, self).get_context_data(**kwargs)
#         initial_data = {
#             "object_id": self.object.pk
#         }
#
#         form = CommentForm(self.request.POST or None, initial=initial_data)
#
#         context['comment_form'] = form
#
#         return context
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         context = self.get_context_data(**kwargs)
#         form = context['comment_form']
#
#         if form.is_valid():
#             c_type = form.cleaned_data.get('content_type')
#             obj_id = form.cleaned_data.get('object_id')
#             content_data = form.cleaned_data.get('content')
#             parent_obj = None
#
#             try:
#                 parent_id = int(request.POST.get('parent_id'))
#             except:
#                 parent_id = None
#
#             if parent_id:
#                 parent_qs = Comment.objects.filter(id=parent_id)
#                 if parent_qs.exists() and parent_qs.count() == 1:
#                     parent_obj = parent_qs.first()
#
#             new_comment, created = Comment.objects.get_or_create(
#                                         author=self.request.user,
#                                         content=content_data,
#                                         parent=parent_obj,
#                                     )
#
#         return self.form_valid(form)
#
#
# class CommentDeleteView(SuccessMessageMixin, DeleteView):
#     model = Comment
#     template_name = 'comment_delete.djhtml'
#     success_url = '.'
#     success_message = 'Comment was successfully removed.'
#
#     def get_success_url(self, **kwargs):
#         return self.get_object().post.get_absolute_url()
#
#     def dispatch(self, request, *args, **kwargs):
#         if (
#             not self.request.user.is_staff
#             and not self.request.user.is_superuser
#             and self.request.user != self.get_object().author
#         ):
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)