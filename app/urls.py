# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('api/data/live', views.get_live_data, name='api-data'),
    path('api/data/archive', views.get_archive_data, name="archive"),
    path('api/data/report', views.GetReport, name="report"),
    path('api/data/report/map', views.get_map_report, name="report_map"),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
