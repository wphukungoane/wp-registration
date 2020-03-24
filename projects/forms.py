from django import forms

from .models import ProjectInfo


class NewProjectForm(forms.ModelForm):
    Descriptions = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Describe your project ?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = ProjectInfo
        fields = ['Project_Owner', 'Name','Research_Area','Descriptions',]
