from django import forms

from .models import Post, Project


class NewTopicForm(forms.ModelForm):
    Descriptions = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Describe your project ?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Project
        fields = ['subject', 'Descriptions']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]
