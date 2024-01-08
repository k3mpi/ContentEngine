from django import forms
from django.utils import timezone

from .models import Idea, Post, Topic, IGPost, Video, Reason, Project, Instagram, Facebook, Pinterest, Youtube


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['idea']



class InstagramPostForm(forms.ModelForm):
    POST_TYPE_CHOICES = [
        ('1', 'Instagram Image'),
        ('2', 'Instagram Video'),
        ('3', 'Instagram Slider'),
    ]

    post_type = forms.ChoiceField(choices=POST_TYPE_CHOICES)

    class Meta:
        model = Post
        fields = ['post_type']
        # Fügen Sie weitere Felder hinzu, falls erforderlich


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'image','slide_mask_first','slide_mask_regular','slide_mask_last', 'watermark', 'youtube_account', 'facebook_account', 'instagram_account', 'wordpress_account', 'pinterest_account']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'slide_mask_first': forms.FileInput(attrs={'class': 'form-control'}),
            'slide_mask_regular': forms.FileInput(attrs={'class': 'form-control'}),
            'slide_mask_last': forms.FileInput(attrs={'class': 'form-control'}),


            'watermark': forms.FileInput(attrs={'class': 'form-control'}),
            # Weitere Widgets für die Konten
        }



    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

class InstagramForm(forms.ModelForm):
    class Meta:
        model = Instagram
        fields = ['username', 'access_token', 'password', 'account_id', 'account_link', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'access_token': forms.TextInput(attrs={'class': 'form-control'}),
            'account_id': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'account_link': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(InstagramForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['access_token'].required = False
        self.fields['password'].required = False
        self.fields['account_id'].required = False
        self.fields['account_link'].required = False

class FacebookForm(forms.ModelForm):
    class Meta:
        model = Facebook
        fields = ['username', 'access_token', 'password', 'account_id', 'account_link', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'access_token': forms.TextInput(attrs={'class': 'form-control'}),
            'account_id': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'account_link': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super(FacebookForm, self).__init__(*args, **kwargs)
            self.fields['username'].required = False
            self.fields['access_token'].required = False
            self.fields['password'].required = False
            self.fields['account_id'].required = False
            self.fields['account_link'].required = False

class PinterestForm(forms.ModelForm):
    class Meta:
        model = Pinterest
        fields = ['username', 'access_token', 'password', 'account_id', 'account_link', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'access_token': forms.TextInput(attrs={'class': 'form-control'}),
            'account_id': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'account_link': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super(PinterestForm, self).__init__(*args, **kwargs)
            self.fields['username'].required = False
            self.fields['access_token'].required = False
            self.fields['password'].required = False
            self.fields['account_id'].required = False
            self.fields['account_link'].required = False

class YoutubeForm(forms.ModelForm):
    class Meta:
        model = Youtube
        fields = ['username', 'access_token', 'password', 'account_id', 'account_link', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'access_token': forms.TextInput(attrs={'class': 'form-control'}),
            'account_id': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'account_link': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(YoutubeForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['access_token'].required = False
        self.fields['password'].required = False
        self.fields['account_id'].required = False
        self.fields['account_link'].required = False
        self.fields['profile_image'].required = False




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['topic', 'IGPost', 'Video']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'IGPost': forms.Select(attrs={'class': 'form-control'}),
            'Video': forms.Select(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        # Dynamisch geladene Fremdschlüssel-Felder
        self.fields['topic'].queryset = Topic.objects.all()
        self.fields['IGPost'].queryset = IGPost.objects.all()
        self.fields['Video'].queryset = Video.objects.all()




class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description', 'date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }



class ReasonForm(forms.ModelForm):
    class Meta:
        model = Reason
        fields = ['name', 'description', 'topic']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
        }