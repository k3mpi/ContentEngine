from django.db import models
from django.utils.text import slugify


class SocialMedia(models.Model):
    username = models.CharField(max_length=255)
    account_link = models.CharField(max_length=511, blank=True, null=True)
    password = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='', blank=True, null=True)

    def get_class_name(self):
        return self.__class__.__name__

    def get_update_url(self):
        class_name = self.__class__.__name__.lower()
        return f'update_{class_name}_account'

    def get_delete_url(self):
        class_name = self.__class__.__name__.lower()
        return f'delete_{class_name}_account'


class Pinterest(SocialMedia):
    access_token = models.CharField(max_length=511, null=True, blank=True)
    account_id = models.CharField(max_length=255, null=True, blank=True)

class Youtube(SocialMedia):
    access_token = models.CharField(max_length=511, null=True, blank=True)
    account_id = models.CharField(max_length=255, null=True, blank=True)

class Facebook(SocialMedia):
    access_token = models.CharField(max_length=511, null=True, blank=True)
    account_id = models.CharField(max_length=255, null=True, blank=True)


class Instagram(SocialMedia):

    access_token = models.CharField(max_length=511, null=True, blank=True)
    account_id = models.CharField(max_length=255, null=True, blank=True)


class Wordpress(SocialMedia):
    pass

class Publication(models.Model):
    datetime = models.DateTimeField()



class InstagramPublication(Publication):
    instagram_account = models.ForeignKey(Instagram, on_delete=models.CASCADE, null=True)
    pass


class FacebookPublication(Publication):
    facebook_account = models.ForeignKey(Facebook, on_delete=models.CASCADE, null=True)
    pass


class WordpressPublication(Publication):
    wordpress_account = models.ForeignKey(Wordpress, on_delete=models.CASCADE, null=True)

    pass


class YoutubePublication(Publication):
    youtube_account = models.ForeignKey(Youtube, on_delete=models.CASCADE, null=True)
    pass


class PinterestPublication(Publication):
    pinterest_account = models.ForeignKey(Pinterest, on_delete=models.CASCADE, null=True)
    pass
def project_directory_path(instance, filename):
    # Erzeugt einen Pfad im Format 'projects/{project_id}-{project_name_slug}/img/{filename}'
    project_name_slug = slugify(instance.name)
    return f'projects/{instance.id}-{project_name_slug}/img/{filename}'

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=project_directory_path, null=True, blank=True)
    watermark = models.ImageField(upload_to=project_directory_path, null=True, blank=True)

    slide_mask_first = models.ImageField(upload_to=project_directory_path, null=True, blank=True)
    slide_mask_regular = models.ImageField(upload_to=project_directory_path, null=True, blank=True)
    slide_mask_last = models.ImageField(upload_to=project_directory_path, null=True, blank=True)



    youtube_account = models.ForeignKey(Youtube, on_delete=models.CASCADE,blank=True, null=True)
    facebook_account = models.ForeignKey(Facebook, on_delete=models.CASCADE,blank=True, null=True)
    instagram_account = models.ForeignKey(Instagram, on_delete=models.CASCADE,blank=True, null=True)
    wordpress_account = models.ForeignKey(Wordpress, on_delete=models.CASCADE,blank=True, null=True)
    pinterest_account = models.ForeignKey(Pinterest, on_delete=models.CASCADE,blank=True, null=True)

    def instagram_publications(self):
        return InstagramPublication.objects.filter(instagram_account=self.instagram_account)

    def youtube_publications(self):
        return YoutubePublication.objects.filter(youtube_account=self.youtube_account)

    def facebook_publications(self):
        return FacebookPublication.objects.filter(facebook_account=self.facebook_account)

    def wordpress_publications(self):
        return WordpressPublication.objects.filter(wordpress_account=self.wordpress_account)

    def pinterest_publications(self):
        return PinterestPublication.objects.filter(pinterest_account=self.pinterest_account)



class Mode(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Music(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='music')
    mode = models.ForeignKey(Mode ,on_delete = models.CASCADE, null=True)

    def __str__(self):
        return self.name

class BackgroundVideo(models.Model):


    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='background_video')
    theme = models.ForeignKey(Theme, on_delete = models.CASCADE, null=True)


    def __str__(self):
        return self.name

class BackgroundImage(models.Model):


    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='background_image', null=True, blank=True)
    theme = models.ForeignKey(Theme, on_delete = models.CASCADE, null=True)


    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    date = models.DateField()

class Reason(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

class IGPost(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    hashtags = models.TextField()


    def get_post_category(self):
        post = Post.objects.filter(IGPost=self).first()
        return post.category if post else None

class IGSlide(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    ig_post = models.ForeignKey(IGPost, on_delete=models.CASCADE)
    number = models.IntegerField()
    png = models.ImageField()

class Video(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    videoPath = models.CharField(max_length=255)

class SpreadshirtDesign(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    pass

class Hashtag(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    name = models.TextField()
class Keyword(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    name = models.TextField()

class Article(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255)
    intro = models.TextField(null=True)
    date = models.DateField(null=True)
    subtitle_1 = models.TextField(null=True)
    text_1 = models.TextField(null=True)
    subtitle_2 = models.TextField(null=True)
    text_2 = models.TextField(null=True)
    subtitle_3 = models.TextField(null=True)
    text_3 = models.TextField(null=True)
    cta_title = models.TextField(null=True)
    cta_text = models.TextField(null=True)
class AudioComment(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    audio = models.FileField()
    skript = models.TextField()

class LongVideo(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    videoPath = models.CharField(max_length=255)
    audio = models.ForeignKey(AudioComment, on_delete=models.CASCADE)

class PostType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)


class Post(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    post_type = models.CharField(max_length=255, null=True, blank=True)
    POST_TYPE_CHOICES = [
        ('1', 'Instagram Image'),
        ('2', 'Instagram Video'),
        ('3', 'Instagram Slider'),
    ]
    mode = models.ForeignKey(Mode, on_delete=models.CASCADE, null=True, blank=True)

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    IGPost = models.ForeignKey(IGPost, on_delete=models.CASCADE, null=True)
    Video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    audio = models.ForeignKey(AudioComment, on_delete=models.CASCADE, null=True)
    LongVideo = models.ForeignKey(LongVideo, on_delete=models.CASCADE, null=True)

    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)  # Many-to-Many-Beziehung zu Hashtag
    keywords = models.ManyToManyField(Keyword, blank=True)  # Many-to-Many-Beziehung zu Hashtag
    meta = models.TextField(null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    instagram_publication = models.ForeignKey(InstagramPublication, on_delete=models.CASCADE, null=True)
    facebook_publication = models.ForeignKey(FacebookPublication, on_delete=models.CASCADE, null=True)
    pinterest_publication = models.ForeignKey(PinterestPublication, on_delete=models.CASCADE, null=True)
    youtube_publication = models.ForeignKey(YoutubePublication, on_delete=models.CASCADE, null=True)
    wordpress_publication = models.ForeignKey(WordpressPublication, on_delete=models.CASCADE, null=True)



    def get_full_content(self):
        content = f"Topic: {self.topic.name}\nDescription: {self.topic.description}\n\nReasons:\n"
        reasons = Reason.objects.filter(topic=self.topic)

        for reason in reasons:
            content += f"- {reason.name}: {reason.description}\n"

        # Hinzufügen der Hashtags zum Inhalt
        hashtags = ", ".join([hashtag.name for hashtag in self.hashtags.all()])
        if hashtags:
            content += f"\nHashtags: {hashtags}"

        # Hinzufügen der Keywords zum Inhalt
        keywords = ", ".join([keyword.name for keyword in self.keywords.all()])
        if keywords:
            content += f"\nKeywords: {keywords}"

        # Hinzufügen von Meta und Artikel zum Inhalt
        if self.meta:
            content += f"\nMeta: {self.meta}"

        return content
class Idea(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    idea = models.TextField()
    post_created = models.DateTimeField(null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)







