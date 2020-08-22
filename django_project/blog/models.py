from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


class Catogary(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
#
choices = Catogary.objects.all().values_list('name','name')

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images", default='default_post.jpg', blank=True)
    catogary = models.ForeignKey(Catogary, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def __str__(self):
        return self.title + ' - ' + str(self.author)

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    """ def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk}) """

    # @property
    # def image_url(self):
    #     if self.image and hasattr(self.image, 'url'):
    #         return self.image.url

class Comment(models.Model):
    comment = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commented_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment
