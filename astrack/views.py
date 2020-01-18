# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .Businesslogic import business_logic


def index(request):
    return render(request, 'astrack/index.html')


def return_data(request):
    return HttpResponse('entered text:' + request.POST.get('periodOfDataset'))


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "astrack/upload_csv1.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file1"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("astrack:upload_csv"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("astrack:upload_csv"))

        # file_data = csv_file.read().decode("utf-8")
        # lines = file_data.split("\n")

        period = int(request.POST.get('periodOfDataset'))
        confidence = float(request.POST.get('confidence'))
        pt = int(request.POST.get('freqP'))
        business_logic(csv_file, period, pt, confidence)

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("astrack:upload_csv"))
