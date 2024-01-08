from django.contrib import admin
from .models import IGPost, Idea, IGSlide, Video, Post, Topic, Reason, Hashtag, Keyword, Article, AudioComment, Mode, \
    Music, BackgroundVideo, Theme, Category, SocialMedia, Project, Publication, Pinterest, Youtube, Instagram, \
    InstagramPublication, PinterestPublication, FacebookPublication, YoutubePublication, WordpressPublication, PostType, \
    BackgroundImage

admin.site.register(IGPost)
admin.site.register(Idea)
admin.site.register(IGSlide)
admin.site.register(Video)
admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Reason)
admin.site.register(Hashtag)
admin.site.register(Keyword)
admin.site.register(Article)
admin.site.register(Mode)
admin.site.register(Music)
admin.site.register(Theme)
admin.site.register(BackgroundVideo)
admin.site.register(BackgroundImage)
admin.site.register(Category)
admin.site.register(SocialMedia)
admin.site.register(Instagram)
admin.site.register(Youtube)
admin.site.register(Pinterest)
admin.site.register(Publication)
admin.site.register(Project)
admin.site.register(PostType)
admin.site.register(InstagramPublication)
admin.site.register(FacebookPublication)
admin.site.register(PinterestPublication)
admin.site.register(YoutubePublication)
admin.site.register(WordpressPublication)

admin.site.register(AudioComment)

# Register your models here.
