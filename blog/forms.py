from django import forms
from .models import Post
from .models import My_post

class PostForm(forms.ModelForm):
    class Meta:
        model =Post
        fields = ('title', 'text',)

class NameForm(forms.Form):
    product_name = forms.CharField()

