import io
import os
from datetime import date
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.http import HttpResponse
import pytrends
from PIL import ImageDraw, ImageFont
from PIL.Image import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from pytrends.request import TrendReq

from ContentEngine.settings import MEDIA_ROOT
from . import util, ai
from .ai import ai_response
from .models import Idea, Post, Topic, Reason, IGPost, IGSlide, Video, Hashtag, Keyword, Article, AudioComment, \
    Category, Theme, Mode, Project, Pinterest, Instagram, Youtube, SocialMedia, PostType
from .forms import IdeaForm, PostForm, TopicForm, ReasonForm, ProjectForm, \
    InstagramPostForm, PinterestForm, YoutubeForm, InstagramForm, FacebookForm  # Sie müssen diese Form erstellen
from django.core.paginator import Paginator

from .util import extract_topic_and_reasons, create_ig_post_images, create_post_video


def dashboard(request):
    pass
def overview(request):
    pass
def settings(request):
    pass

############################################################################################################## IDEAS ###
########################################################################################################################

def list_ideas(request):
    # Sortierparameter aus dem Request holen
    sort_order = request.GET.get('sort', 'desc')  # Standardmäßig nach Datum absteigend sortieren

    # Initialisieren des Querysets und Anwenden der Sortierung
    if sort_order == 'asc':
        ideas_list = Idea.objects.all().order_by('datetime')
    else:  # 'desc' und andere Fälle
        ideas_list = Idea.objects.all().order_by('-datetime')

    paginator = Paginator(ideas_list, 10)  # Zeigt 10 Ideen pro Seite

    page_number = request.GET.get('page')
    ideas = paginator.get_page(page_number)

    pytrends = TrendReq(hl='de-DE', tz=60)
    trending_searches_df = pytrends.trending_searches(pn='germany')
    trending_keywords = trending_searches_df.iloc[:, 0].head(100).tolist()

    return render(request, 'core/idea_list.html', {
        'ideas': ideas,
        'trending_keywords': trending_keywords,
        'sort_order': sort_order  # Fügen Sie den Sortierparameter hinzu, um ihn im Template zu verwenden
    })

def get_ideas(request):
    if request.method == 'POST':
        # Verarbeiten der Auswahl und Speichern der ausgewählten Ideen
        selected_ideas = request.POST.getlist('selected_ideas')
        for idea_text in selected_ideas:
            Idea(idea=idea_text, datetime= timezone.now()).save()
        return render(request, 'core/idea_saved_confirmation.html')
    else:
        # Abrufen und Verarbeiten der Trenddaten
        pytrends = TrendReq(hl='de-DE', tz=60)
        trending_searches_df = pytrends.trending_searches(pn='germany')
        trending_keywords_string = ', '.join(trending_searches_df.iloc[:, 0].head(100))
        response = ai.ideas_from_trends(trending_keywords_string)
        xml_string = response
        print(xml_string)
        ideas = util.extract_ideas(xml_string)


        # Senden der Ideen an das Template
        return render(request, 'partials/idea_selection.html', {'ideas': ideas})

def create_idea(request):
    form = IdeaForm(request.POST or None)
    if form.is_valid():
        # Erstellen Sie eine neue Idea-Instanz, speichern Sie sie aber noch nicht in der Datenbank
        new_idea = form.save(commit=False)

        # Setzen Sie das datetime-Feld auf den aktuellen Zeitpunkt
        new_idea.datetime = timezone.now()

        # Speichern Sie die vollständige Instanz in der Datenbank
        new_idea.save()

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
    return render(request, 'core/idea_confirm_delete.html', {'object': idea})

############################################################################################################## POSTS ###
########################################################################################################################
def list_posts(request):
    # Filterparameter und Sortierparameter aus dem Request holen
    project_id = request.GET.get('project')
    category_id = request.GET.get('category')
    sort_order = request.GET.get('sort', 'datetime_desc')  # Standardmäßig nach Datum absteigend sortieren

    # Initialisieren des Querysets
    posts_query = Post.objects.all()

    # Filtern der Posts nach Kategorie, wenn eine Kategorie angegeben ist
    if category_id:
        posts_query = posts_query.filter(category_id=category_id)
    if project_id:
        posts_query = posts_query.filter(project_id=project_id)


    # Sortieren der Posts
    if sort_order == 'datetime_asc':
        posts_query = posts_query.order_by('datetime')
    elif sort_order == 'datetime_desc':
        posts_query = posts_query.order_by('-datetime')

    # Paginierung
    paginator = Paginator(posts_query, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # Zusätzliche Informationen für das Template
    categories = Category.objects.all()
    projects = Project.objects.all()

    return render(request, 'core/post_list.html', {
        'posts': posts,
        'categories': categories,
        'projects': projects,
        'selected_category': category_id,
        'sort_order': sort_order
    })

def view_post(request, post_id):
    post = Post.objects.get(id=post_id)
    topic = post.topic
    reasons = Reason.objects.filter(topic=topic)
    ig_post = post.IGPost
    ig_slides = IGSlide.objects.filter(ig_post=ig_post)
    video = post.Video

    return render(request, 'core/post_view.html', {
        'post': post,
        'topic': topic,
        'reasons': reasons,
        'ig_slides': ig_slides,
        'video': video
    })

def create_post(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_selector')
        idea_id = request.POST.get('idea_selector')
        category_id = request.POST.get('category')
        post_Type_id = request.POST.get('type_selector')
        theme_id = request.POST.get('theme')
        mode_id = request.POST.get('mode')

        project = Project.objects.get(id=project_id)
        post_type = PostType.objects.get(id=post_Type_id)
        idea = Idea.objects.get(id=idea_id)
        category = Category.objects.get(id=category_id)
        theme = Theme.objects.get(id=theme_id)
        mode = Mode.objects.get(id=mode_id)
        if(post_type.name == 'Top 10 Liste'):
            response = ai.ai_response_top10(idea.idea)
            xml_string = response
        elif(post_type.name == '10 Unterpunkte und Paragraphen zu einem Thema'):
            response = ai.ai_response_10paragraphs(idea.idea)
            xml_string = response
        elif (post_type.name == '10 Fakten zu einem Thema'):
            response = ai.ai_response_10facts(idea.idea)
            xml_string = response
        elif (post_type.name == '10 Gründe zu einem Thema'):
            response = ai.ai_response_10reasons(idea.idea)
            xml_string = response
        extracted_topic, extracted_reasons, extracted_descriptions = extract_topic_and_reasons(xml_string)
        # Erstellen des Topic-Objekts
        topic = Topic(name=extracted_topic, description="", date=date.today())
        topic.save()

        # Erstellen des Reason-Objekts
        for reason, description in zip(extracted_reasons, extracted_descriptions):
            Reason(name=reason, description=description, topic=topic).save()

        # Erstellen des Post-Objekts
        post = Post(topic=topic, category=category, theme=theme, mode=mode, project=project, post_type=post_type)

        # Setzen des datetime-Felds auf den aktuellen Zeitpunkt
        post.datetime = timezone.now()

        # Speichern des Post-Objekts
        post.save()

        # Optional: Weiterleitung
        return HttpResponseRedirect(reverse('list_posts'))
    else:
        ideas = Idea.objects.all()
        post_types = PostType.objects.all()
        categories = Category.objects.all()
        projects = Project.objects.all()
        themes = Theme.objects.all()
        modes = Mode.objects.all()

        return render(request, 'core/post_form.html', {
            'ideas': ideas,
            'categories': categories,
            'projects': projects,
            'post_types': post_types,
            'themes': themes,
            'modes': modes
        })

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

############################################################################################################# PROJECTS ###
########################################################################################################################
def update_project(request, pk):
    reason = get_object_or_404(Reason, pk=pk)
    form = ReasonForm(request.POST or None, instance=reason)
    if form.is_valid():
        form.save()
        return redirect('list_reasons')
    return render(request, 'core/reason_form.html', {'form': form})

def delete_project(request, pk):
    reason = get_object_or_404(Reason, pk=pk)
    if request.method == 'POST':
        reason.delete()
        return redirect('list_reasons')
    return render(request, 'core/reason_confirm_delete.html', {'object': reason})

def list_projects(request):
    # Filterparameter und Sortierparameter aus dem Request holen
    sort_order = request.GET.get('sort', 'datetime_desc')  # Standardmäßig nach Datum absteigend sortieren

    # Initialisieren des Querysets
    projects = Project.objects.all()

    # Paginierung
    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)



    return render(request, 'core/project_list.html', {
        'projects': projects,
    })

def view_project(request, project_id):
    project = Project.objects.get(id=project_id)



    return render(request, 'core/project_view.html', {
        'project': project,


    })

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            # Optional: Weiterleitung oder zusätzliche Logik
            return redirect(reverse('list_projects'))
    else:
        form = ProjectForm()


    return render(request, 'core/project_form.html', {'form': form})

def update_project(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('list_ideas')
    return render(request, 'core/post_form.html', {'form': form})

def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('list_projects')
    return render(request, 'core/project_confirm_delete.html', {'object': project})

def create_seo(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)

        xml_string = ai.hashtag_data(post)

        hashtags, keywords, meta = util.extract_hashtags(xml_string)

        for name in hashtags:
            hashtag, created = Hashtag.objects.get_or_create(name=name)
            post.hashtags.add(hashtag)

        for name in keywords:
            keyword, created = Keyword.objects.get_or_create(name=name)
            post.keywords.add(keyword)

        post.meta = meta
        post.save()

        # Optional: Rückkehr zur Liste der Posts oder zu einer Erfolgsmeldung
        return HttpResponseRedirect(reverse('list_posts'))
    except Exception as e:
        print("Error in create_ig_video:", e)
        return HttpResponse("Error occurred", status=500)

def list_publish_posts(request):
    # Filterparameter und Sortierparameter aus dem Request holen
    category_id = request.GET.get('category')
    project_id = request.GET.get('project')
    sort_order = request.GET.get('sort', 'datetime_desc')  # Standardmäßig nach Datum absteigend sortieren

    # Initialisieren des Querysets
    posts_query = Post.objects.all()

    # Filtern der Posts nach Kategorie, wenn eine Kategorie angegeben ist
    if category_id:
        posts_query = posts_query.filter(category_id=category_id)
    if project_id:
        posts_query = posts_query.filter(project_id=project_id)

    # Sortieren der Posts
    if sort_order == 'datetime_asc':
        posts_query = posts_query.order_by('datetime')
    elif sort_order == 'datetime_desc':
        posts_query = posts_query.order_by('-datetime')

    # Paginierung
    paginator = Paginator(posts_query, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # Zusätzliche Informationen für das Template
    categories = Category.objects.all()
    projects = Project.objects.all()

    return render(request, 'core/post_publish_list.html', {
        'posts': posts,
        'categories': categories,
        'projects': projects,
        'selected_category': category_id,
        'selected_project': project_id,
        'sort_order': sort_order
    })



############################################################################################################ Publications ###
#############################################################################################################################
def view_post_publications(request, post_id):
    post = Post.objects.get(id=post_id)
    topic = post.topic
    reasons = Reason.objects.filter(topic=topic)
    ig_post = post.IGPost
    ig_slides = IGSlide.objects.filter(ig_post=ig_post)
    video = post.Video

    return render(request, 'core/post_publications_view.html', {
        'post': post,
        'topic': topic,
        'reasons': reasons,
        'ig_slides': ig_slides,
        'video': video
    })


def publish_youtube_post(request, post_id):
    # Erhalte das Post-Objekt oder gebe einen 404-Fehler zurück, falls es nicht existiert
    post = get_object_or_404(Post, id=post_id)

    # Stelle sicher, dass das Post-Objekt ein Video hat
    if post.Video:
        # Pfad zur Videodatei (wenn MEDIA_ROOT definiert ist, verwenden Sie os.path.join)
        video_file_path = os.path.join(MEDIA_ROOT, post.Video.videoPath)

        # Titel und Beschreibung aus dem Post-Objekt
        title = post.topic.name  # Oder ein anderes Feld, das den Titel darstellt
        description = post.topic.description  # Oder ein anderes Feld für die Beschreibung

        # Kategorie-ID, Schlüsselwörter und Datenschutzeinstellungen - Beispielwerte
        category_id = "22"  # Kategorie-ID für YouTube (z.B. 22 für 'People & Blogs')
        keywords = [hashtag.name for hashtag in post.hashtags.all()]  # Liste der Hashtags
        privacy_status = "public"  # 'public', 'private' oder 'unlisted'

        # Rufe die Upload-Funktion auf
        util.upload_youtube_video(video_file_path, title, description, category_id, keywords, privacy_status)

        return HttpResponseRedirect(reverse('list_posts'))
    else:
        print("Dieser Post hat kein Video zum Hochladen.")

        return HttpResponseRedirect(reverse('list_posts'))

def publish_pinterest_post(request, post_id):
    pass
def publish_facebook_post(request, post_id):
    pass

def publish_instagram_post(request, post_id):
    post = Post.objects.get(id=post_id)
    topic = post.topic
    reasons = Reason.objects.filter(topic=topic)
    ig_post = post.IGPost
    ig_slides = IGSlide.objects.filter(ig_post=ig_post)
    video = post.Video

    if request.method == 'POST':
        form = InstagramPostForm(request.POST, request.FILES)
        if form.is_valid():
            selected_post_type_value = form.cleaned_data.get('post_type')

            # Konvertieren Sie den Wert in ein PostType-Objekt
            selected_post_type = PostType.objects.get(id=selected_post_type_value)

            # Übergeben Sie das PostType-Objekt an Ihre Funktionen
            if selected_post_type_value == '1':
                util.publish_instagram_image(post)
            elif selected_post_type_value == '2':
                util.publish_instagram_video(post, selected_post_type)
            elif selected_post_type_value == '3':
                util.publish_instagram_slider(post, selected_post_type)

            return redirect(reverse('list_posts'))
    else:
        form = InstagramPostForm()
    return render(request, 'core/publish_instagram_post.html', {'form': form, 'post': post,
        'topic': topic,
        'reasons': reasons,
        'ig_slides': ig_slides,
        'video': video})



############################################################################################################## IG POST ###
##########################################################################################################################

def create_ig_post(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        topic = post.topic
        reasons = Reason.objects.filter(topic=topic)

        ig_post = IGPost.objects.create(title=f"Post for {topic.name}", description=topic.description, datetime= timezone.now())
        print("ig_post created")
        slides_paths = create_ig_post_images(topic, reasons, post)

        for i, slide_path in enumerate(slides_paths):
            slide = IGSlide(ig_post=ig_post, number=i)
            slide.png = slide_path  # Speichern des Pfads im ImageField
            slide.save()

        # Aktualisieren des Post-Objekts mit dem neuen IGPost
        post.IGPost = ig_post
        post.save()

        return HttpResponseRedirect(reverse('list_posts'))
    except Exception as e:
        print("Error in create_ig_post:", e)
        return HttpResponse("Error occurred", status=500)


def list_slides(request):
    # Filter- und Sortierparameter aus dem Request holen
    category_id = request.GET.get('category')
    sort_order = request.GET.get('sort', 'datetime_desc')  # Standardmäßig nach Datum absteigend sortieren

    # Filtern der IGPosts nach Kategorie
    if category_id:
        posts_query = Post.objects.filter(category_id=category_id)
    else:
        posts_query = Post.objects.all()

    # Holen der IGPosts IDs basierend auf dem gefilterten Post Queryset
    ig_post_ids = posts_query.values_list('IGPost', flat=True).distinct()

    # Holen der IGPosts basierend auf den IDs
    ig_posts_query = IGPost.objects.filter(id__in=ig_post_ids)

    # Sortieren der IGPosts
    if sort_order == 'datetime_asc':
        ig_posts_query = ig_posts_query.order_by('datetime')
    elif sort_order == 'datetime_desc':
        ig_posts_query = ig_posts_query.order_by('-datetime')

    # Paginierung
    paginator = Paginator(ig_posts_query, 24)  # 24 IGPosts pro Seite
    page_number = request.GET.get('page')
    ig_posts = paginator.get_page(page_number)

    # Zusätzliche Informationen für das Template
    categories = Category.objects.all()

    return render(request, 'core/slide_list.html', {
        'ig_posts': ig_posts,
        'categories': categories,
        'selected_category': category_id,
        'sort_order': sort_order
    })
############################################################################################################## Video ###
##########################################################################################################################
def create_ig_video(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        topic = post.topic
        reasons_list = Reason.objects.filter(topic=topic)

        # Extrahieren der Gründe als Liste von Strings
        reasons = [reason.name for reason in reasons_list]
        reason_desc = [reason.description for reason in reasons_list]

        # Erstellen des Videos und Speichern des Pfads
        video_path = create_post_video(topic.name, reasons, reason_desc,  post.mode, post.theme, post.category)

        # Erstellen des Video-Objekts in der Datenbank
        video = Video.objects.create(videoPath=video_path, datetime= timezone.now())
        video.save()
        post.Video = video
        post.save()
        print("Video object created with path:", video.videoPath)

        # Optional: Rückkehr zur Liste der Posts oder zu einer Erfolgsmeldung
        return HttpResponseRedirect(reverse('list_posts'))
    except Exception as e:
        print("Error in create_ig_video:", e)
        return HttpResponse("Error occurred", status=500)

def create_long_video(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        topic = post.topic
        reasons_list = Reason.objects.filter(topic=topic)

        # Extrahieren der Gründe als Liste von Strings
        reasons = [reason.name for reason in reasons_list]
        reason_desc = [reason.description for reason in reasons_list]

        # Erstellen des Videos und Speichern des Pfads
        video_path = util.create_long_video(topic.name, reasons, post.mode, post.theme,post, post.category)

        # Erstellen des Video-Objekts in der Datenbank
        video = Video.objects.create(videoPath=video_path, datetime= timezone.now())
        video.save()
        post.Video = video
        post.save()
        print("Video object created with path:", video.videoPath)

        # Optional: Rückkehr zur Liste der Posts oder zu einer Erfolgsmeldung
        return HttpResponseRedirect(reverse('list_posts'))
    except Exception as e:
        print("Error in create_ig_video:", e)
        return HttpResponse("Error occurred", status=500)

############################################################################################################## Audio Comment ###
##########################################################################################################################


def create_audio(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)

        xml_string = ai.create_audio_skript(post)
        skript = util.extract_audio_skript(xml_string)
        audio_path = ai.text_to_speech(skript, post.topic.name)

        # Erstellen und Speichern des AudioComment-Objekts
        audio_comment = AudioComment(skript=skript, audio=audio_path)
        audio_comment.save()

        # Zuweisen des gespeicherten AudioComment-Objekts zum Post
        post.audio = audio_comment
        post.save()





        # Optional: Rückkehr zur Liste der Posts oder zu einer Erfolgsmeldung
        return HttpResponseRedirect(reverse('list_posts'))
    except Exception as e:
        print("Error in create_ig_video:", e)
        return HttpResponse("Error occurred", status=500)

############################################################################################################## Article ###
##########################################################################################################################
def create_article(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)

        xml_string = ai.create_article(post)


        title, intro, subtitles, texts, cta_title, cta_text = util.extract_article(xml_string)

        # Erstellen eines neuen Article-Objekts
        article = Article(
            datetime= timezone.now(),
            title=title,
            intro=intro,
            subtitle_1=subtitles[0] if len(subtitles) > 0 else "",
            text_1=texts[0] if len(texts) > 0 else "",
            subtitle_2=subtitles[1] if len(subtitles) > 1 else "",
            text_2=texts[1] if len(texts) > 1 else "",
            subtitle_3=subtitles[2] if len(subtitles) > 2 else "",
            text_3=texts[2] if len(texts) > 2 else "",
            cta_title=cta_title,
            cta_text=cta_text
        )
        article.save()

        # Optional: Verknüpfen des Artikels mit dem Post (falls erforderlich)
        post.article = article
        post.save()

        # Optional: Rückkehr zur Liste der Posts oder zu einer Erfolgsmeldung
        return HttpResponseRedirect(reverse('list_posts'))
    except Exception as e:
        print("Error in create_ig_video:", e)
        return HttpResponse("Error occurred", status=500)



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
    reason_list = Reason.objects.all()
    paginator = Paginator(reason_list, 50)  # Zeigt 25 Ideen pro Seite

    page_number = request.GET.get('page')
    reasons = paginator.get_page(page_number)
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


def list_accounts(request):
    from django.shortcuts import render
    from .models import Pinterest, Facebook, Instagram, Youtube


    pinterest_accounts = Pinterest.objects.all()
    facebook_accounts = Facebook.objects.all()
    instagram_accounts = Instagram.objects.all()
    youtube_accounts = Youtube.objects.all()
    accounts = list(pinterest_accounts) + list(facebook_accounts) + list(instagram_accounts) + list(
        youtube_accounts)
    return render(request, 'core/account_list.html', {'accounts': accounts})


def create_pinterest_account(request):
    if request.method == 'POST':
        form = PinterestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_accounts')
    else:
        form = PinterestForm()
    return render(request, 'core/account_instagram_form.html', {'form': form})
def update_pinterest_account(request, pk):
    pinterest_account = get_object_or_404(Pinterest, pk=pk)
    if request.method == 'POST':
        form = PinterestForm(request.POST, request.FILES, instance=pinterest_account)
        if form.is_valid():
            form.save()
            return redirect('list_accounts')
    else:
        form = PinterestForm(instance=pinterest_account)
    return render(request, 'core/account_form.html', {'form': form})

def view_pinterest_account(request, pk):
    pinterest_account = get_object_or_404(Pinterest, pk=pk)
    return render(request, 'core/view_account.html', {'account': pinterest_account})

def delete_pinterest_account(request, pk):
    pinterest_account = get_object_or_404(Pinterest, pk=pk)
    if request.method == 'POST':
        pinterest_account.delete()
        return redirect('list_accounts')
    return render(request, 'core/delete_account.html', {'account': pinterest_account})


def create_facebook_account(request):
    if request.method == 'POST':
        form = FacebookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_accounts')
    else:
        form = FacebookForm()
    return render(request, 'core/account_facebook_form.html', {'form': form})
def update_facebook_account(request, pk):
    pass
def view_facebook_account(request, pk):
    pass
def delete_facebook_account(request, pk):
    pass

def create_instagram_account(request):
    if request.method == 'POST':
        form = InstagramForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_accounts')
    else:
        form = InstagramForm()
    return render(request, 'core/account_instagram_form.html', {'form': form})
def update_instagram_account(request, pk):
    instagram_account = get_object_or_404(Instagram, pk=pk)
    if request.method == 'POST':
        form = InstagramForm(request.POST, request.FILES, instance=instagram_account)
        if form.is_valid():
            form.save()
            return redirect('list_accounts')
    else:
        form = InstagramForm(instance=instagram_account)
    return render(request, 'core/account_instagram_form.html', {'form': form})
def view_instagram_account(request, pk):
    pass
def delete_instagram_account(request, pk):
    if request.method == 'POST':
        form = InstagramForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_accounts')
    else:
        form = InstagramForm()
    return render(request, 'core/account_instagram_form.html', {'form': form})

def create_youtube_account(request):
    if request.method == 'POST':
        form = YoutubeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_accounts')
    else:
        form = YoutubeForm()
    return render(request, 'core/account_youtube_form.html', {'form': form})
def update_youtube_account(request, pk):
    youtube_account = get_object_or_404(Youtube, pk=pk)
    if request.method == 'POST':
        form = YoutubeForm(request.POST, request.FILES, instance=youtube_account)
        if form.is_valid():
            form.save()
            return redirect('list_accounts')
    else:
        form = YoutubeForm(instance=youtube_account)
    return render(request, 'core/account_youtube_form.html', {'form': form})

def view_youtube_account(request, pk):
    pass
def delete_youtube_account(request, pk):
    pass




def list_links(request):
    pass
def create_link(request, pk):
    pass
def update_link(request, pk):
    pass
def delete_link(request, pk):
    pass
