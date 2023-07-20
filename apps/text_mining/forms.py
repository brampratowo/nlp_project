from django import forms
from django.forms import widgets
from django.forms.widgets import Widget
from .models import TextSimilarity
from .models import SpellingChecker
from .models import SearchDocumentsRanking


class TextSimilarityForm(forms.ModelForm):
    class Meta:
        model = TextSimilarity

        fields = ["text1", "text2", "cosine_similarity", "euclidean_distance"]
        widgets = {
            "text1": forms.Textarea(attrs={"rows": 10}),
            "text2": forms.Textarea(attrs={"rows": 10}),
        }
        readonly_fields = ["cosine_similarity", "euclidean_distance"]


class SpellingCheckerForm(forms.ModelForm):
    class Meta:
        model = SpellingChecker
        fields = ["sentence", "corrections"]
        widgets = {
            "sentence": forms.Textarea(attrs={"rows": 5}),
            "corrections": forms.Textarea(attrs={"rows": 5}),
        }
        readonly_fields = ["corrections"]


class SearchDocumentsRankingForm(forms.ModelForm):
    class Meta:
        model = SearchDocumentsRanking
        fields = [
            "query",
            "npm",
            "nama",
            "judul_skripsi",
            "abstraksi_skripsi",
            "similarity",
        ]
        widgets = { "query" : forms.TextInput() }
