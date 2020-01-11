from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, template_name='base.html')


def new_search(request):
    search_txt = request.POST.get('search')
    context = {'search': search_txt}
    return render(request, template_name='mobile/new_search.html', context=context)
