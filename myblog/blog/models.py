from django.db import models

from django.urls import reverse


class Item(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('item-list')


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    posted = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.item_id})
