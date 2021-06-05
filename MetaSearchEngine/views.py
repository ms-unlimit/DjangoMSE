from django.shortcuts import render,redirect
import MetaSearchEngine.metaSE as metaSE
from django.http import HttpResponse
from .models import Query
from .forms import QueryForm

def results_list(request):
    query_form=QueryForm(request.GET)
    if query_form.is_valid():

        #query_form.save()
        query = query_form.cleaned_data['query']
        ms = metaSE.MSE(query)
        items=ms.runMSE()
        ms.__del__()
        return render(request, 'MSE.html', {'items': items, 'query': query, 'number':len(items)})
    else:
        return render(request, 'home.html', {'items': "item", 'query': 'else'})


def home(request):
    return render(request, 'home.html', {'items': "item", 'query': 'home'})