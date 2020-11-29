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
from app.operations import searchdata, getlivedata, getdevicedata, getreport, getmapreport, get_device_parameters
from .decorators import allowed_users, unauthenticated_user,verified_users


@login_required(login_url="/login/")
@allowed_users(allowed_roles=['sysadmin', 'owner'])
@verified_users()
def index(request):
    return render(request, "indexsolar.html")


@login_required(login_url="/login/")
def get_live_data(request):
    datalist = getlivedata()
    dataobj = []
    for data in datalist:
        rno, vin, vbat, edt, spdk, lat, lng = data
        data1 = {"rno": rno, "vbat": vbat, "vin": vin, "spdk": spdk, "time": edt.strftime("%Y-%m-%d %H:%M:%S%z"),
                 "lat": lat,
                 "lng": lng}
        dataobj.append(data1)
    # print(data1)
    cont = {"data": dataobj}
    return JsonResponse(cont)


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
        print(param)
        Data = searchdata(fromData, toData, param)
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
