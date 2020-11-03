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
from app.operations import searchdata, getlivedata, getdevicedata


@login_required(login_url="/login/")
def index(request):
    return render(request, "indexsolar.html")

@login_required(login_url="/login/")
def get_live_data(request):
    datalist = getlivedata()
    dataobj = []
    for data in datalist:
        rno, vin, vbat, edt, spdk, lat, lng, appd, tp, celv, ect, es = data
        data1 = {"rno": rno, "vbat": vbat, "vin": vin, "spdk": spdk, "time": edt.strftime("%Y-%m-%d %H:%M:%S%z"),
                 "lat": lat,
                 "lng": lng, "appd": appd, "tp": tp, "celv": celv, "ect": ect, "es": es}
        dataobj.append(data1)

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
        fromData = (datetime.strptime(request.POST["from"], '%Y-%m-%d %H:%M:%S'))
        toData = (datetime.strptime(request.POST["to"], '%Y-%m-%d %H:%M:%S'))
        edt, vin, vbat, appt, tp, spdk, celv, ect, es = searchdata(fromData, toData)
        for i in range(0, len(edt) - 2):
            # if appt[i] is None or tp[i] is None:
            #     appt[i] = "None"
            #     tp[i] = "None"
            if fromData <= edt[i] <= toData:
                newtime.append(edt[i].strftime('%Y-%m-%d %H:%M:%S%z'))
                newVin.append(vin[i])
                newVbat.append(vbat[i])
                newAppt.append(appt[i])
                newTp.append(tp[i])
                newCelv.append(celv[i])
                newEct.append(ect[i])
                newEs.append(es[i])
                if (edt[i + 1] - edt[i]) > timedelta(seconds=5):
                    difference = int(edt[i + 1].timestamp() - edt[i].timestamp())
                    # print(difference)
                    for sec in range(1, difference):
                        temptimedate = edt[i] + timedelta(seconds=5)
                        newtime.append(temptimedate.strftime('%Y-%m-%d %H:%M:%S%z'))
                        newVin.append(None)
                        newVbat.append(None)
                        newAppt.append(None)
                        newTp.append(None)
                        newCelv.append(None)
                        newEct.append(None)
                        newEs.append(None)

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

        context = {"fromData": fromData, "toData": toData, "labels": newtime, "Vin": newVin,
                   "Vbat": newVbat, "Appd": newAppt, "Tp": newTp, "Celv": newCelv, "Ect": newEct, "Es": newEs}
        # print(context.get("Vin"))
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
