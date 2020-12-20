# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from django.db import connection
from datetime import datetime, timedelta
import pytz
from app.operations import searchdata, getlivedata, getdevicedata, getreport, getmapreport, get_device_parameters, \
    get_all_data, get_livedata_device
from .decorators import *
from .models import FirmProfile
from django.contrib.auth.models import User
from userforms.models import *
import os
from django.conf import settings


@login_required(login_url="/login/")
@allowed_users(allowed_roles=['sysadmin', 'owner'])
@verified_users()
def index(request):
    print(request.user.username)
    device = Device.objects.filter(firm=FirmProfile.objects.get(user=User.objects.get(username=request.user.username)))
    get_all_data(device)
    context = {'device': device}
    return render(request, "indexsolar.html", context)


@login_required(login_url="/login/")
def tempdevice(request):
    file = open(os.path.join(settings.BASE_DIR, '../AssetTrack_Backend/log/data.csv'), 'r')
    lines = file.read().splitlines()
    lines.reverse()
    return JsonResponse(lines[0:1000], safe=False)


@login_required(login_url="/login/")
def get_live_data(request):
    device = Device.objects.filter(firm=FirmProfile.objects.get(user=User.objects.get(username=request.user.username)))
    datalist = get_livedata_device(device)
    dataobj = []
    arr = []
    dev = []
    for k in device:
        dev.append(k.device_parameters.split(","))

    # print(dev)
    # if data is none set device params to None
    for i in range(0, len(dev)):
        # dev = device[i].device_parameters.split(",")
        x = {}
        for j in range(0, len(dev[i])):
            if datalist[i] is None:
                x[dev[i][j]] = None
            else:
                x[dev[i][j]] = datalist[i][j]
        arr.append(x)
    ctx = {"data": arr}
    # print(ctx)
    # for data in datalist:
    #     rno, vin, vbat, edt, spdk, lat, lng = data
    #     data1 = {"rno": rno, "vbat": vbat, "vin": vin, "spdk": spdk, "time": edt.strftime("%Y-%m-%d %H:%M:%S%z"),
    #              "lat": lat,
    #              "lng": lng}
    #     dataobj.append(data1)
    # # print(data1)
    # cont = {"data": dataobj}
    return JsonResponse(ctx)


@login_required(login_url="/login/")
def get_archive_data(request):
    context = {}
    utc = pytz.UTC

    if request.method == "POST":
        newtime = []
        newVin = []
        newVbat = []
        newAppt = []
        newTp = []
        newCelv = []
        newEct = []
        newEs = []
        param = []
        Time = []
        Yaxis = []
        Data = []
        fromData = (datetime.strptime(request.POST["from"], '%Y-%m-%d %H:%M:%S'))
        toData = (datetime.strptime(request.POST["to"], '%Y-%m-%d %H:%M:%S'))
        param = request.POST.getlist("parameters[]")
        device = request.POST["device"]
        print(param)
        Data = searchdata(fromData, toData, param, device)
        # edt, vin, vbat, appt, tp, spdk, celv, ect, es = searchdata(fromData, toData,param)
        for _ in range(0, len(param)):
            Yaxis.append([])

        for i in range(0, len(Data) - 2):
            if fromData <= Data[i][0] <= toData:
                Time.append(Data[i][0].strftime('%Y-%m-%d %H:%M:%S%z'))
                for j in range(0, len(param)):
                    Yaxis[j].append(Data[i][j + 1])
                if (Data[i + 1][0] - Data[i][0]) > timedelta(seconds=5):
                    difference = int(Data[i + 1][0].timestamp() - Data[i][0].timestamp())
                    # print(difference)
                    for sec in range(1, difference):
                        temptimedate = Data[i][0] + timedelta(seconds=5)
                        Time.append(temptimedate.strftime('%Y-%m-%d %H:%M:%S%z'))
                        for j in range(0, len(param)):
                            Yaxis[j].append(None)

            # while True:
            #     if(fromData > toData):
            #         break
            #     elif(fromData == i.edt):
            #         newtime.append(i.edt.strftime("%H:%M:%S"))
            #         newVin.append(i.vin)
            #     else:
            #         newtime.append(fromData.strftime("%H:%M:%S"))
            #         newVin.append("s")
            #         fromData += timedelta(seconds=1)

        context = {"fromData": fromData, "toData": toData, "labels": Time, "selected": Yaxis, "param": param}
        # print(context.get("Vin"))
        return JsonResponse(context)
    else:
        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def device_list(request):
    context = {"devicelist": getdevicedata()}

    return JsonResponse(context)


@login_required(login_url="/login/")
def device_parameters(request):
    context = {}
    if request.method == "POST":
        context = {"deviceparameters": get_device_parameters(request.POST["deviceid"])}
        return JsonResponse(context)
    else:
        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def GetReport(request):
    context = {"data": getreport()}

    return JsonResponse(context)


@login_required(login_url="/login/")
def get_map_report(request):
    context = {}
    utc = pytz.UTC
    if request.method == "POST":
        tripid = request.POST["tripid"]
        context = {"data": getmapreport(tripid)}
        return JsonResponse(context)
    else:
        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
@superuser_only
def superuser_page(request):
    return render(request, "superuser.html")


@login_required(login_url="/login/")
def pages(request):
    context = {"1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template(load_template)

        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def get_userinfo(request):
    devicelist = []
    pref = []
    chart_pref = []
    device = Device.objects.filter(firm=FirmProfile.objects.get(user=User.objects.get(username=request.user.username)))
    for i in device:
        devicelist.append(i.device_id)
        pref.append(i.device_parameters.split(","))
        chart_pref.append(i.chart_parameters.split(","))
    context = {"all_devices": devicelist, "prefrence": pref, "chartprefrence": chart_pref}
    return JsonResponse(context)


def firm_register(request):
    msg = "Error"
    if request.method == "POST":
        company_name = request.POST["name"]
        company_email = request.POST["email"]
        company_telephone = request.POST["telephone"]
        company_address1 = request.POST["address1"]
        company_address2 = request.POST["address2"]
        company_country = request.POST["country"]
        company_state = request.POST["state"]
        company_city = request.POST["city"]
        company_zip = request.POST["zip"]
        company_gstn = request.POST["gstn"]
        company_owner = request.POST["owner"]
        owner = User.objects.filter(username=company_owner)
        if len(owner) == 0:
            msg = "Owner Not Found"
        elif len(owner[0].groups.filter(name='owner')) == 0:
            msg = "User is not Owner"
        else:
            firm = FirmProfile(user=owner[0], company_name=company_name, company_email=company_email,
                               company_telephone=company_telephone, company_address1=company_address1,
                               company_address2=company_address2,
                               company_country=company_country, company_state=company_state, company_city=company_city,
                               company_zip=company_zip, company_gstn=company_gstn,
                               )
            firm.save()
            msg = "Form Saved Successfully"
        return JsonResponse({'msg': msg})
    else:
        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render({"msg": msg}, request))
