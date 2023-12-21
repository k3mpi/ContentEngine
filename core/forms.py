from django import forms
from .models import Idea, Post, Topic, IGPost, Video, Reason


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['idea']




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