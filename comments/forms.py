from django import forms


class CommentForm(forms.Form):
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(widget=forms.Textarea)
