from django.http import HttpResponse
from django.shortcuts import render
from .utils import apriori, generate_association_rules
import csv

def apriori_results_csv(request):
    if request.method == 'POST':
        transactions = []
        try:
            file = request.FILES['csv_file']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            for row in reader:
                transactions.append(row)
        # except MultiValueDictKeyError:
        #     return render(request, 'add_csv.html', {'error_message': 'No file selected.'})
        # 
        except csv.Error:
            return render(request, 'add_csv.html', {'error_message': 'Invalid CSV format.'})
        min_support = float(request.POST.get('min_support', 0.1))
        min_confidence = float(request.POST.get('min_confidence', 0.5))
        L = apriori(transactions, min_support)
        association_rules = generate_association_rules(L, min_confidence)
        frequent_items = []
        for l in L:
            for itemset in l:
                support = itemset['support']
                itemset = itemset['item']
                containing_transactions = [t for t in transactions if set(itemset).issubset(set(t))]
                frequent_items.append({'item': itemset, 'support': support, 'transactions': containing_transactions})
        return render(request, 'apriori_results.html', {'transactions': transactions, 'frequent_items': frequent_items,'association_rules': association_rules})
    else:
        return render(request, 'add_csv.html')
def apriori_results(request):

    if request.method == 'POST':
        transactions = []
        transactions_list = request.POST.get('transactions')
        transactions_list = transactions_list.split(';')
        for transaction in transactions_list:
            transactions.append(tuple(transaction.split()))
        min_support = float(request.POST.get('min_support', 0.1))
        min_confidence = float(request.POST.get('min_confidence', 0.5))

        L = apriori(transactions, min_support)
        association_rules = generate_association_rules(L, min_confidence)
        frequent_items = []
        for l in L:
            for itemset in l:
                support = itemset['support']
                itemset = itemset['item']
                containing_transactions = [t for t in transactions if set(itemset).issubset(set(t))]
                frequent_items.append({'item': itemset, 'support': support, 'transactions': containing_transactions})
        return render(request, 'apriori_results.html', {'transactions': transactions, 'frequent_items': frequent_items,'association_rules': association_rules})
    else:
        return render(request, 'add_tans.html')
def home_apriori(request):
    return render(request, 'Home_apriori.html')
