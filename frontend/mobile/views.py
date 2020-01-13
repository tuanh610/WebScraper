import sys
from django.shortcuts import render
sys.path.append('../')
from backend.database.sourceDBEngine import sourceDBEngine
from backend.database.phoneDBEngine import phoneDBEngine
from django.core.paginator import Paginator
# Create your views here.


def home(request):
    sourceDB = sourceDBEngine()
    allSources = sourceDB.getAllDataFromTable()

    return render(request, 'home.html', {'sources': allSources})


def new_search(request):
    search_txt = request.POST.get('search')
    context = {'search': search_txt, }
    context_object_name = 'search_txt'
    return render(request, template_name='mobile/new_search.html', context=context)


def all_mobiles(request, source, page):
    # Retrieve all data from amazonDB
    sourceDB = sourceDBEngine()
    allSources = sourceDB.getAllDataFromTable()
    phoneDB = phoneDBEngine(tableName=source)
    phones = phoneDB.getAllDataFromTable()
    paginator = Paginator(phones, 12)
    allData = paginator.get_page(page)

    return render(request, 'mobile/all_mobiles.html', {'allData': allData, 'source': source, 'AllSources': allSources})
