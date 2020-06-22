# import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from apyori import apriori


def business_logic(dataset, period, purchaseTimes, minC):
    store_data = pd.read_csv(dataset, header = None)
    store_data.head()

    # Calculating support:
    totalTransaction = len(store_data.index)
    minS = (period * purchaseTimes) / totalTransaction
    minC = minC/100

    # Data Processing:
    records = []
    for i in range(0, totalTransaction):
        records.append([str(store_data.values[i, j]) for j in range(0, 7) if str(store_data.values[i, j]) != 'nan'])

    association_rules = apriori(records, min_support = minS, min_confidence = minC, min_lift = 3, min_length = 2)
    association_results = list(association_rules)

    assocRules = []
    for item in association_results:
        newRecord = [item[2][0][0], item[2][0][1], item[1], item[2][0][2], item[2][0][3]]
        assocRules.append(newRecord)

        """third index of the list located at 0th of the third index of the inner list"""

    # Dataframe
    df = pd.DataFrame(assocRules, columns = ['item_base', 'item_add', 'support', 'confidence', 'lift'])
    # print(df)
    heatmap_data = pd.pivot_table(df, values = 'lift', index = 'item_add', columns = 'item_base')
    sns.set(rc = {'figure.figsize': (18, 6)})
    sns.heatmap(heatmap_data, cmap = sns.color_palette('Blues', 30))
    sns.despine(left = 0.3, bottom = 0.5)
    plt.title('Association Rules using Lift values')
    plt.savefig('graph.png')
