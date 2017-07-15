from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from lists.models import Item,List

# Create your views here.

def home_page(request):
    # item = Item()
    # item.text = request.POST.get('item_text','')
    # item.save()

    # if request.method == 'POST':
    #     new_item_text = request.POST['item_text']
    #     Item.objects.create(text=new_item_text)
    #     return redirect('/lists/the-only-list-in-the-world/')

    return render(request, 'home.html')
#模版的证书，填入模版中，单元测试时会报错，不填时，功能测试报错
#{% csrf_token %}

def view_list(request,list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})

def new_list(request):
    list_ = List.objects.create()
    new_item_text = request.POST['item_text']
    Item.objects.create(text=new_item_text,list=list_)
    return redirect('/lists/%d/' % (list_.id,))

def add_item(request,list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'],list=list_)
    return redirect('/lists/%d/' % (list_.id,))