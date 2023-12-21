from django.db import models



class Topic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()

class Reason(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

class IGPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    hashtags = models.TextField()

class IGSlide(models.Model):
    ig_post = models.ForeignKey(IGPost, on_delete=models.CASCADE)
    number = models.IntegerField()
    png = models.ImageField()

class Video(models.Model):
    videoPath = models.CharField(max_length=255)

class SpreadshirtDesign(models.Model):
    pass

class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    IGPost = models.ForeignKey(IGPost, on_delete=models.CASCADE)
    Video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Idea(models.Model):
    idea = models.TextField()
    post_created = models.DateTimeField(null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)






