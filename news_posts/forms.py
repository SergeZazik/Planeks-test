from django import forms
from .models import NewsPost
from ckeditor.widgets import CKEditorWidget


class NewsPostForm(forms.ModelForm):
    """
    Form for News post model
    """
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = NewsPost
        fields = [
            'title',
            'content',
            'attachment',
        ]

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = NewsPost.objects.filter(title__iexact=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This title has already been used. Please try again.")
        return title
