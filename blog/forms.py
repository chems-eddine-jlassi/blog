from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


def should_be_empty(value):
    if value:
        raise forms.ValidationError('Field is not empty')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=80)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    forcefield = forms.CharField(
        required=False, widget=forms.HiddenInput, label="Leave empty", validators=[should_be_empty])

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', error_messages={'exists': 'This already exists'})
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    def cleaned_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =[
            'title',
            'slug',
            'content',
            'thumb',
            'status'
        ]
class UpdateArticleModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =[
            'title',
            
            'content',
            'thumb'  
        ]
    def save(self, commit=True):
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
       
        blog_post.content = self.cleaned_data['content']
        if self.cleaned_data['thumb']:
            blog_post.thumb = self.cleaned_data['thumb']
        if commit:
            blog_post.save()
        return blog_post