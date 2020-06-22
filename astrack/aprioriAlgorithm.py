"""
Description     : Python implementation of the Apriori Algorithm
"""

from collections import defaultdict
from itertools import chain, combinations, islice


def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    """calculates the support for items in the itemSet and returns a subset
       of the itemSet each of whose elements satisfies the minimum support"""
    _itemSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count) / len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet


def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


# def getItemSetTransactionList(data):
#     itemSet = set()
#     for record in data:
#         transaction = frozenset(record)
#         for item in transaction:
#             itemSet.add(frozenset([item]))  # Generate 1-itemSets
#     return itemSet


def runApriori(transactionList, itemSet, minSupport, minConfidence, minLift):
    """
    run the apriori algorithm. transactionList is a list of all transactions in the dataset
    Return both:
     - items (tuple, support)
     - rules ((ItemBase, ItemAdd), confidence)
    """

    # itemSet = getItemSetTransactionList(transactionList)

    freqSet = defaultdict(int)
    largeSet = dict()  # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)

    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
        """local function which Returns the support of an item"""
        return float(freqSet[item]) / len(transactionList)

    # Item with there respective support.
    toRetItems = []
    for key, value in islice(largeSet.items(), 0, 1):
        toRetItems.extend([(tuple(item), freqSet[item], round(getSupport(item), 4), round(getSupport(item) * 100, 2))
                           for item in value])

    # Association Rules.
    toRetRules = []
    for key, value in islice(largeSet.items(), 1, None):
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    lift = confidence / getSupport(remain)
                    if confidence > minConfidence and lift >= minLift:
                        toRetRules.append((tuple(element), tuple(remain), freqSet[item], round(getSupport(item), 4),
                                           round(confidence * 100, 2), round(lift, 4)))

    return toRetItems, toRetRules
