from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=600, primary_key=True)
