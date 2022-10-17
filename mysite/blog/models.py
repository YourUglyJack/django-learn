from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
            .filter(status='published')


class Post(models.Model):
    # 用于页面上的选择框标签，需要先提供一个二维的二元元组，第一个元素表示存在数据库内真实的值，第二个表示页面上显示的具体内容
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique_for_date='publish')  # what is unique_for_date
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')  # 外键 关联User表 在创建多对一的关系的,需要在Foreign的第二参数中加入on_delete=models.CASCADE 删除主表数据的时候 这个也一起删除
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)  # 会在model对象第一次被创建时，将字段的值设置为创建时的时间，以后修改对象时，字段的值不会再更新
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()

    # manager
    objects = models.Manager()  # the default manager
    published = PublishedManager()  # our custom manager

    class Meta:
        ordering = ('-publish',)  # - 表示降序

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    # post.comments.all() 可以通过主表查询子表信息 即返回所有该post的评论; comment.post 可以获取该评论对应的post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)  # 谁评论
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
