from django.shortcuts import render,HttpResponse

import tabula
import os
import django
import json
from django import db as django_db
from django.forms.models import model_to_dict
from models import *
from django.core import serializers

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

def main(request):
    form = UploadFileForm()
    context = {'form' : form}
    return render(request,"reader/prashant.html",context)   

def handle_uploaded_file(f):
    print os.getcwd()
    with open(os.getcwd()+'/reader/file/name.pdf', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        handle_uploaded_file(request.FILES['file'])
        try:
            pid = Person.objects.get(name=request.POST.get('name'))
        except:
            pid = Person.objects.create(name=request.POST.get('name'))
        store_data(os.getcwd()+'/reader/file/name.pdf',pid)
        context = {
            'success' : True
        }
        return HttpResponseRedirect('/pdfreader/main/',context)

def store_data(path,pid):
    df = tabula.read_pdf(path,spreadsheet=True)
    df['Ref No./Cheque\rNo.'] = df['Ref No./Cheque\rNo.'].fillna(value="")
    df['Debit'] = df['Debit'].fillna(value=0.0)
    df['Credit'] = df['Credit'].fillna(value=0.0)
    df['Balance'] = df['Balance'].fillna(value=0.0)
    for i in range(len(df)):
        data = {
            "pid": pid,
            "txn_date":df.loc[i]['Txn Date'].replace('\r',' '),
            "value_date":df.loc[i]['Value\rDate'].replace('\r',' '),
            "description":df.loc[i]['Description'].replace('\r',' '),
            "ref":df.loc[i]['Ref No./Cheque\rNo.'].replace('\r',' '),
            "debit":df.loc[i]['Debit'],
            "credit":df.loc[i]['Credit'],
            "balance":df.loc[i]['Balance']
        }
        obj = Transaction(**data)
        obj.save()

def get_dump(obj):
    return {
        "txn_date":obj.txn_date,
        "value_date":obj.value_date,
        "description":obj.description,
        "ref":obj.ref,
        "debit":obj.debit,
        "credit":obj.credit,
        "balance":obj.balance
    }

def get_data(request):
    try:
        name = request.GET.get('name')
        print name
        try:
            pid = Person.objects.get(name=name)
            lst = Transaction.objects.filter(pid=pid)
            # return HttpResponse(json.dumps(lst))
            return HttpResponse(json.dumps([get_dump(lsti) for lsti in lst]))
        except Exception as e:
            print e
            return HttpResponse("No PDF Uploaded")
    except Exception as e:
        print e
        return render(request,'reader/ask.html')

if __name__=="__main__":
    Transaction.objects.all().delete()
    fname = "test.pdf"
    store_data(fname,1)
    print get_data(1)