from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    """
        To create a form from a model, you just need to indicate which model to use to build
        the form in the Meta class of the form. Django introspects the model and builds the
        form dynamically for you.
    """
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

