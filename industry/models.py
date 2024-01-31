from django.db import models

# Create your models here.


class Industry(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'company'

    def __str__(self):
        return self.name

    def src_link(self):
        link = self.name.replace(' ', '-')
        return f"images/{link.lower()}.png"
