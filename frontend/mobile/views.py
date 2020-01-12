import sys
from django.shortcuts import render
sys.path.append('../')
from backend.database.sourceDBEngine import sourceDBEngine
from backend.database.phoneDBEngine import phoneDBEngine
# Create your views here.


def home(request):
    return render(request, template_name='home.html')


def new_search(request):
    search_txt = request.POST.get('search')
    context = {'search': search_txt, }
    context_object_name = 'search_txt'
    return render(request, template_name='mobile/new_search.html', context=context)


def all_mobiles(request):
    # Retrieve all data from amazonDB
    sourceDB = sourceDBEngine()
    allSources = sourceDB.getAllDataFromTable()

    allData = {}
    for source in allSources:
        phoneDB = phoneDBEngine(tableName=source.name)
        phones = phoneDB.getAllDataFromTable()
        allData[source.name] = phones
    context = {'allData': allData}
    return render(request, template_name='mobile/all_mobiles.html', context=context)
