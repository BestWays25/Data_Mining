from itertools import combinations

def frequent_1_itemsets(transactions, min_support):
    items = []
    for transaction in transactions:
        for item in transaction:
            items.append(item)
    items = list(set(items))
    frequent_items = []
    for item in items:
        support = 0
        for transaction in transactions:
            if item in transaction:
                support += 1
        if min_support > 0.99:
            if support >= min_support and not any((item, support) == transaction for transaction in frequent_items):
                frequent_items.append({'item': {item}, 'support': support})
        else:
            if support / len(transactions) >= min_support and not any((item, support) == transaction for transaction in frequent_items):
                frequent_items.append({'item': {item}, 'support': support})
    return frequent_items

def apriori_gen(prev_frequent_itemsets):
    k = len(prev_frequent_itemsets[0]['item']) + 1
    C = []
    generated_itemsets = []
    for i in range(len(prev_frequent_itemsets)):
        for j in range(i + 1, len(prev_frequent_itemsets)):
            a = prev_frequent_itemsets[i]['item']
            b = prev_frequent_itemsets[j]['item']
            if len(a.intersection(b)) == k - 2:
                c = a.union(b)
                if c not in generated_itemsets:
                    generated_itemsets.append(c)
                    C.append({'item': c, 'support': 0})
    return C

def apriori(transactions, min_support):
    L = []
    L_1 = frequent_1_itemsets(transactions, min_support)
    L.append(L_1)
    k = 2
    while L_1 != []:
        C_k = apriori_gen(L_1)
        L_k = []
        for candidate in C_k:
            support = 0
            for transaction in transactions:
                if candidate['item'].issubset(set(transaction)): 
                    support += 1
            if min_support > 0.99:
                if support >= min_support:
                    candidate['support'] = support
                    L_k.append(candidate)
            else:
                if support / len(transactions) >= min_support:
                    candidate['support'] = support
                    L_k.append(candidate)
        L.append(L_k)
        k += 1
        L_1 = L_k
    return L

def find_support(L, itemset):
    itemset = set(itemset)
    for l in L:
        for item in l:
            if item['item'] == itemset:
                return item['support']
    return 0

def generate_association_rules(L, minconf):
    association_rules = []
    for l in L:
        for itemset in l:
            for i in range(1, len(itemset['item'])):
                subsets = list(combinations(itemset['item'], i))
                for subset in subsets:
                    subset = set(subset)
                    complement = itemset['item'] - subset
                    if len(complement) > 0:
                        conf = itemset['support'] / find_support(L, subset)
                        if conf >= minconf and not any((subset, complement, conf) == rule for rule in association_rules):
                            association_rules.append((subset, complement, conf))
    return association_rules

def print_frequent_itemsets(L):
    if len(L) == 0:
        print("Le tableau est nul.")
    else:
        for i, l in enumerate(L):
            if len(l) == 0:
                print("\n")
            else :
                print("\nFrequent itemsets of size {}:".format(i + 1))
                for itemset in l:
                    print("{}: {}".format(itemset['item'], itemset['support']))
     