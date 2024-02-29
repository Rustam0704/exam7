from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE

from .utils import avatar_path


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, AbstractModel):
    avatar = models.ImageField(upload_to=avatar_path, default='avatar.JPG')

    @property
    def like_count(self):
        return self.userlike_set.count()


class Category(models.Model):
    name = models.CharField(max_length=48)
    def __str__(self):
        return self.name


class Item(AbstractModel):
    title = models.CharField(max_length=256)
    description = models.TextField()
    author = models.ForeignKey(User, CASCADE, 'items')
    category = models.ForeignKey(Category, CASCADE, 'items')
    image = models.ImageField(upload_to=avatar_path, default='avatar.jpg')
    ends_in = models.DateField(default="2025-04-17")
    price = models.IntegerField(default=0)
    owner_name = models.CharField(max_length=128)
    owner_username = models.CharField(max_length=128)


    @property
    def like_count(self):
        return self.itemlike_set.count()


    def __str__(self):
        return self.title


class UserLike(AbstractModel):
    user = models.ForeignKey(User, CASCADE)
    author = models.ForeignKey(User, CASCADE, 'like')

    def __str__(self):
        return f"{self.author}-{self.user}"

class ItemLike(AbstractModel):
    User = models.ForeignKey(User, CASCADE, 'likes')
    Item = models.ForeignKey(Item, CASCADE)