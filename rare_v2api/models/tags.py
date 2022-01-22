from cProfile import label
import imp
from django.db import models

class Tag(models.Model):
  label = models.CharField(max_length=50)