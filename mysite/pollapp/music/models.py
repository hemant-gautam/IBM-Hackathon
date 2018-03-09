from django.db import models


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class mediau(models.Model):
    url=models.CharField(max_length=1000,null=True)
    name=models.CharField(max_length=1000,null=True)
