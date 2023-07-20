from typing_extensions import Required
from django.shortcuts import render, redirect
from .models import SearchDocumentsRanking
from nlp_project import settings

# Create your views here.
# from .models import TextSimilarity
from .language import LanguageTool
from .language import TextMiningEnum
from .forms import TextSimilarityForm
from .forms import SpellingCheckerForm
from .forms import SearchDocumentsRankingForm
from .helper import HelperFunction
import json
import os


def text_similarity(request):
    if request.method == "POST":
        form = TextSimilarityForm(request.POST)
        if form.is_valid():
            try:
                cosine_similarity_val = LanguageTool.getValueSimilarity(
                    request.POST["text1"], request.POST["text2"], TextMiningEnum.COSINE_SIMILARITY
                )
                euclidean_distance_val = LanguageTool.getValueSimilarity(
                    request.POST["text1"], request.POST["text2"], TextMiningEnum.EUCLIDEAN_DISTANCE
                )
                new_form = TextSimilarityForm()
                new_form.initial["text1"] = request.POST["text1"]
                new_form.initial["text2"] = request.POST["text2"]
                new_form.initial["cosine_similarity"] = cosine_similarity_val
                new_form.initial["euclidean_distance"] = euclidean_distance_val

                return render(request, "text_mining/similarity.html", {"form": new_form})
            except:
                pass
    else:
        form = TextSimilarityForm()
    return render(request, "text_mining/similarity.html", {"form": form})


def spell_checker(request):
    if request.method == "POST":
        form = SpellingCheckerForm(request.POST)
        if form.is_valid():
            try:
                spellCheckerValue = LanguageTool.spellChecker(request.POST["sentence"])
                new_form = SpellingCheckerForm()
                new_form.initial["sentence"] = request.POST["sentence"]
                new_form.initial["corrections"] = spellCheckerValue
                return render(request, "text_mining/spell_checker.html", {"form": new_form})
            except:
                pass
    else:
        form = SpellingCheckerForm()
        return render(request, "text_mining/spell_checker.html", {"form": form})

def search_document_ranking(request):
    if request.method == "POST":
        form = SearchDocumentsRankingForm(request.POST)
        if form.is_valid():
            try:
                query = request.POST["query"]
                new_form = SearchDocumentsRankingForm()
                new_form.initial["query"] = request.POST["query"]

                doc = HelperFunction.loadTextFile(
                    os.path.join(settings.BASE_DIR, os.path.normpath("static/data/data-skripsi-amikom.json")))
                data_skripsi = json.loads(doc)
                documents = []
                for doc in data_skripsi:
                    documents.append(doc)
        
                search_result = LanguageTool.searchDocumentRanking(query, documents, "AbstraksiSkripsi")
                result_list = []
                for data in search_result:
                    sdr = SearchDocumentsRanking()
                    sdr.npm = data["Npm"]
                    sdr.nama = data["Nama"]
                    sdr.judul_skripsi = data["JudulSkripsi"]
                    sdr.abstraksi_skripsi = data["AbstraksiSkripsi"]
                    sdr.similarity = data["Similarity"]
                    result_list.append(sdr)
                return render(request,"text_mining/search_document_ranking.html", { 'result_list':result_list, 'form':new_form})  
            except:
                pass
    else:
        form = SearchDocumentsRankingForm()
        return render(request, "text_mining/search_document_ranking.html", {"form":form})

