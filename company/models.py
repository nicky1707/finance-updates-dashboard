from django.db import models
from industry.models import Industry

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100)
    industries = models.ManyToManyField('Industry')

    def __str__(self):
        return self.name

    def src_link(self):
        link = self.name.replace(' ', '-')
        return f"images/{link.lower()}.svg"
