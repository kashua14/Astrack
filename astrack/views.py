# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import json
import os
from io import StringIO
from zipfile import ZipFile

from astrack import aprioriAlgorithm
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from django.http import HttpResponse, Http404
from django.shortcuts import render

from django.conf import settings

REPORT = os.path.dirname(os.path.abspath(__file__))


def index(request):
    return render(request, 'astrack/index.html')


def printResults(items, rules):
    """
    prints the generated itemsets sorted by support and
    the confidence rules sorted by confidence
    """

    freq_items = pd.DataFrame(data = items, columns = ['Item', 'Frequency', 'Support', 'Percentage(%)'])\
        .sort_values(by = 'Support', ascending = False)
    assoc_rules = pd.DataFrame(data = rules,
                               columns = ['Antecedent', 'Consequent', 'Frequency', 'Support', 'Confidence(%)', 'Lift']) \
        .sort_values(by = ['Support', 'Lift'], ascending = False)
    most_assoc_rules = pd.DataFrame(data = assoc_rules.head(20),
                                    columns = ['Antecedent', 'Consequent', 'Frequency', 'Support', 'Confidence(%)',
                                               'Lift'])

    most_freq_items = pd.DataFrame(data = freq_items.head(20),
                                   columns = ['Item', 'Frequency', 'Support', 'Percentage(%)'])

    with pd.ExcelWriter('Report.xlsx', engine = 'xlsxwriter') as writer:
        pd.DataFrame(data = ['Top 20 bought products'], index = None)\
            .to_excel(writer, index = None, header = False, sheet_name = 'Analysis', startrow = 1)
        most_freq_items.to_excel(writer, index = None, header = True, sheet_name = 'Analysis', startrow = 2)

        pd.DataFrame(data = ['Top 20 bought Combinations'], index = None)\
            .to_excel(writer, index = None, header = False, sheet_name = 'Analysis', startrow = 22)
        most_assoc_rules.to_excel(writer, index = None, header = True, sheet_name = 'Analysis', startrow = 23)

        assoc_rules.to_excel(writer, index = None, header = True, sheet_name = 'Association Rules')
        freq_items.to_excel(writer, index = None, header = True, sheet_name = 'Frequent Items')
    writer.save()

    if not assoc_rules.empty and assoc_rules.__len__() > 2:
        heatmap_data = pd.pivot_table(assoc_rules, values = 'Lift', index = 'Antecedent', columns = 'Consequent')
        sns.set(rc = {'figure.figsize': (40, 25)})
        sns.heatmap(heatmap_data, cmap = sns.color_palette('Blues', 30))
        plt.title('Products Associations')
        plt.savefig('HeatMap.png')

    """ Create a zip file """
    myFile = os.path.join(REPORT, 'templates\\astrack\\FinalReport.zip')
    with ZipFile(myFile, 'w') as zipObj:
        zipObj.write('Report.xlsx')
        if not assoc_rules.empty and assoc_rules.__len__() > 2:
            zipObj.write('HeatMap.png')


def upload_csv(request):
    if request.POST and request.FILES:
        try:
           csv_file = request.FILES['csv_file']
        except MultiValueDictKeyException as e:
            print(e.getMessage())
        
        file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(StringIO(file))


        """" Get a set of unique items and a list of all transactions."""
        transactionList = list()
        itemSet = set()
        for record in csv_data:
            # record = record.strip().rstrip(',')  # Remove trailing comma
            transaction = frozenset(record)
            transactionList.append(transaction)
            for item in transaction:
                itemSet.add(frozenset([item]))  # Generate 1-itemSets
        print("Finished Adding Records in records[]")

        """ pick the provided values from the web page."""
        period = float(request.POST.get('periodOfDataset'))
        confidence = float(request.POST.get('confidence'))
        pt = float(request.POST.get('freqP'))
        lift = float(request.POST.get('lift1'))

        # Calculating support:
        totalTransaction = len(transactionList)
        min_support = round(float(period * pt / totalTransaction), 4)
        min_confidence = confidence / 100
        min_lift = lift
        # print('totalTransaction: ', totalTransaction)
        # print('minS: ', min_support)
        # print('minC: ', min_confidence)
        # print('minL: ', min_lift)

        print("Running Apriori algorithm...")
        freq_items, association_rules = aprioriAlgorithm.runApriori(transactionList, itemSet, min_support,
                                                                    min_confidence, min_lift)
        print("writing in files...")
        # maxS, minS = max_min_Support(association_rules)
        print("Finished Running Apriori algorithm")
        printResults(freq_items, association_rules)
        print("Finished writing files")

        if association_rules.__len__() <= 0:
            return render(request, 'astrack/NoItems.html')

        return render(request, 'astrack/results.html')
        # return HttpResponseRedirect(reverse("astrack:upload_csv"))


def download_rar(request):
    file_path = os.path.join(REPORT, 'templates\\astrack\\FinalReport.zip')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type = "")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


# from celery.result import AsyncResult
#
#
# # result = AsyncResult(task_id)
# # print(result.state)  # will be set to PROGRESS_STATE
# # print(result.info)  # metadata will be here
#
#
# def get_progress(request, task_id):
#     result = AsyncResult(task_id)
#     response_data = {
#         'state': result.state,
#         'details': result.info,
#     }
#     return HttpResponse(json.dumps(response_data), content_type = 'application/json')
