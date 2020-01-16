import sys
from django.shortcuts import render
sys.path.append('../')
from backend.database.phoneDBEngine import phoneDBEngine
from django.core.paginator import Paginator
import backend.constant as constants
import backend.utilityHelper as helper
import backend.constant as constant
# Create your views here.


def home(request):
    return render(request, 'home.html', {'sources': constants.scrapingSources})


def about(request):
    return render(request, 'about.html')


def new_search(request):
    phoneDBAdapter = phoneDBEngine(tableName=constant.dynamoDBTableName)
    all_brands = phoneDBAdapter.getAllBrandData()
    return render(request, template_name='mobile/new_search.html', context={"all_brands": all_brands})


def all_mobiles(request, page):
    # Retrieve all data from amazonDB
    phoneDB = phoneDBEngine(tableName=constants.dynamoDBTableName)
    phones = phoneDB.getAllDataFromTable()
    processedList = helper.getLowestPriceList(phones)
    paginator = Paginator(list(processedList.values()), 12)
    allData = paginator.get_page(page)

    return render(request, 'mobile/all_mobiles.html',
                  {'allData': allData})

