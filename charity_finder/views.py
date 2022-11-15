import xmltodict
from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint


from charity_finder import charity_api

# Create your views here.
def home(request):

    themes = charity_api.get_charity_data("/themes")
    # pprint("TRENDING: ", trending)

    themes = xmltodict.parse(themes.content)
    print(themes)
    context = {"themes": themes}
    
    return render(request, "home.html", context)
