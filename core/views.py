from django.shortcuts import render, redirect, get_object_or_404
from .models import Idea, Post, Topic, Reason
from .forms import IdeaForm, PostForm, TopicForm, ReasonForm  # Sie müssen diese Form erstellen
from django.core.paginator import Paginator
def dashboard(request):
    pass
def overview(request):
    pass
def settings(request):
    pass

############################################################################################################## IDEAS ###
########################################################################################################################
def list_ideas(request):
    ideas_list = Idea.objects.all()
    paginator = Paginator(ideas_list, 10)  # Zeigt 25 Ideen pro Seite

    page_number = request.GET.get('page')
    ideas = paginator.get_page(page_number)

    return render(request, 'core/idea_list.html', {'ideas': ideas})

def create_idea(request):
    form = IdeaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_ideas')
    return render(request, 'core/idea_form.html', {'form': form})

def update_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    form = IdeaForm(request.POST or None, instance=idea)
    if form.is_valid():
        form.save()
        return redirect('list_ideas')
    return render(request, 'core/idea_form.html', {'form': form})

def delete_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        idea.delete()
        return redirect('list_ideas')
    return render(request, 'meineapp/idea_confirm_delete.html', {'object': idea})

############################################################################################################## POSTS ###
########################################################################################################################

def list_posts(request):
    posts = Post.objects.all()
    return render(request, 'core/post_list.html', {'posts': posts})

def create_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_posts')
    return render(request, 'core/post_form.html', {'form': form})

def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('list_ideas')
    return render(request, 'core/post_form.html', {'form': form})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('list_posts')
    return render(request, 'core/post_confirm_delete.html', {'object': post})

############################################################################################################# Topics ###
########################################################################################################################

def list_topics(request):
    topics = Topic.objects.all()
    return render(request, 'core/topic_list.html', {'topics': topics})

def create_topic(request):
    form = TopicForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_topics')
    return render(request, 'core/topic_form.html', {'form': form})

def update_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    form = TopicForm(request.POST or None, instance=topic)
    if form.is_valid():
        form.save()
        return redirect('list_topics')
    return render(request, 'core/topic_form.html', {'form': form})

def delete_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        topic.delete()
        return redirect('list_topics')
    return render(request, 'core/topic_confirm_delete.html', {'object': topic})

############################################################################################################ Reasons ###
########################################################################################################################

def list_reasons(request):
    reasons = Reason.objects.all()
    return render(request, 'core/reason_list.html', {'reasons': reasons})

def create_reason(request):
    form = ReasonForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_reasons')
    return render(request, 'core/reason_form.html', {'form': form})

def update_reason(request, pk):
    reason = get_object_or_404(Reason, pk=pk)
    form = ReasonForm(request.POST or None, instance=reason)
    if form.is_valid():
        form.save()
        return redirect('list_reasons')
    return render(request, 'core/reason_form.html', {'form': form})

def delete_reason(request, pk):
    reason = get_object_or_404(Reason, pk=pk)
    if request.method == 'POST':
        reason.delete()
        return redirect('list_reasons')
    return render(request, 'core/reason_confirm_delete.html', {'object': reason})
