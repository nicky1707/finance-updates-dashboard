from django.db import models
from company.models import Company

# Create your models here.


class Watchlist(models.Model):
    name = models.CharField(max_length=100)
    companies = models.ManyToManyField(Company)

    def __str__(self):
        return self.name

    def add_companies(self, companies):
        self.companies.add(*companies)

    def remove_companies(self, companies):
        self.companies.remove(*companies)
