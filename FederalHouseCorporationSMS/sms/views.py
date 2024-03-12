import requests
from telnetlib import STATUS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from sms.models import SMS
from sms.forms import SMSSend, DateFilter

SMSC = 'SMPP'
SOURCE = '9767'
TS = ''
SERVICE = ''
URL = ''
MASK = 31
STATUS = 1
BOXC = ''

def send_sms_api(text, to):

    from_ = "9999"
    username = "username"
    password = "password"
    coding="2" # used for non english characters only 70 characters is allowed
    # if you use enlgish character you should remove coding parameter, otherwise 
    # the smpp allowed only 70 characters. but if you remove it, then 160 character is allowed.
    charset="UTF-8"

    args = {
        'from_':from_, 
        'to':to, 
        'text':text, 
        'username': username, 
        'password': password,
        'coding': coding,
        'charset': charset
    }

    url = """http://127.0.0.1:6013/ethiotelecom/sendsms?"
        "from={from_}&to={to}&text={text}&username={username}&password={password}&coding={coding}&charset={charset}"""\
        .format(**args)

    try:
        r = requests.get(url, data={}, headers={}, verify=False)
    except Exception as e:
        print(e)
    return r.ok


def homepage(request):
    return render(request, "homepage.html")

def send_sms(request):
    if request.method == "POST":
        form = SMSSend(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            response = send_sms_api(post.text, post.destination)
            if not response:
                messages.error(request, "sms send failed")
            else:
                post.smsc = SMSC
                post.ts = TS
                post.source = SOURCE
                post.service = SERVICE
                post.url = URL
                post.mask = MASK
                post.status = STATUS
                post.save()
                messages.success(request, "send sms succesfully done.")
            return redirect('send_sms')
    else:
        form = SMSSend()
    return render(request, 'send_sms.html', {'form': form})


def sms_list(request):
    sms_list = SMS.objects.all()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(sms_list, 10) # Show 10 submits per page.

    try:
        sms_list = paginator.page(page_number)
    except PageNotAnInteger:
        sms_list = paginator.page(1)
    except EmptyPage:
        sms_list = paginator.page(paginator.num_pages)
    form = DateFilter()
    context = {
        'sms_list': sms_list,
        'paginator': paginator,
        'form': form,
    }
    return render(request, 'sms_list.html', context)

def sms_detail(request, sms_id):
    try:
        sms = SMS.objects.get(pk=sms_id)
    except SMS.DoesNotExist:
        return redirect('sms_list')
    return render(request, 'sms_detail.html', {'sms': sms})



def sms_filter(request):
    sms_list = SMS.objects.all()
    location = min_price = max_price = sms_type = None

    if request.method == "POST":
        form = DateFilter(request.POST)
        if form.is_valid():
            date = request.POST.get('date')

    else:
        form = DateFilter()

    if date:
        sms_list = sms_list.filter(created_at=date)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(sms_list, 10) # Show 10 submits per page.

    try:
        sms_list = paginator.page(page_number)
    except PageNotAnInteger:
        sms_list = paginator.page(1)
    except EmptyPage:
        sms_list = paginator.page(paginator.num_pages)
    context = {
        'sms_list': sms_list,
        'paginator': paginator,
        'form': form,
    }
    return render(request, 'sms_list.html', context)


def delete_sms(request, sms_id):
    sms = get_object_or_404(SMS, pk=sms_id)
    return render(request, 'delete_sms.html', {'sms': sms})


def delete_sms_done(request, sms_id):
    sms = get_object_or_404(SMS, pk=sms_id)
    sms.delete()
    messages.success(request, "sms was deleted successfully.")
    return redirect('homepage')
