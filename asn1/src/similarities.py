# https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50
def jaccard_sim(str1, str2): 
    a = set(str1.split()) 
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))
