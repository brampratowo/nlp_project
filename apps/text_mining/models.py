from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.base import Model


# Create your models here.
class TextSimilarity(models.Model):
    class Meta:
        managed = False

    text1 = models.CharField(max_length=5000, null=True, blank=True)
    text2 = models.CharField(max_length=5000, null=True, blank=True)
    cosine_similarity = models.FloatField(null=True, blank=True)
    euclidean_distance = models.FloatField(null=True, blank=True)

    class Meta:
        managed = False


class SpellingChecker(models.Model):
    class Meta:
        managed = False

    sentence = models.CharField(max_length=5000, null=True, blank=True)
    corrections = models.CharField(max_length=5000, null=True, blank=True)

class SearchDocumentsRanking(models.Model):
    class Meta:
        managed = False

    query = models.CharField(max_length=5000, null=True, blank=True)
    npm = models.CharField(max_length=5000, null=True, blank=True)
    nama = models.CharField(max_length=5000, null=True, blank=True)
    judul_skripsi = models.CharField(max_length=5000, null=True, blank=True)
    abstraksi_skripsi = models.CharField(max_length=10000, null=True, blank=True)
    similarity = models.FloatField(null=True, blank=True)