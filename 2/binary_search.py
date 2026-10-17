# binary_search.py

def is_sorted(s):   
    ### TODO 1: 补全判断是否排序 ###

    ### TODO 1 结束 ### 

def qsort(s):   
    if len(s) <= 1: return s 
    s_less = []; s_greater = []; s_equal = [] 
    for k in s: 
        if k < s[0]: 
            s_less.append(k) 
        elif k > s[0]: 
            s_greater.append(k) 
        else: 
            s_equal.append(k) 
    return qsort(s_less) + s_equal + qsort(s_greater)

def binary_search(s, low, high, k):   
    ### TODO 2: 补全递归二分查找 ###

    ### TODO 2 结束 ###

s = [5, 6, 21, 32, 51, 60, 67, 73, 77, 99] 
if not is_sorted(s): 
    s = qsort(s) 
    print(s) 
 
print(binary_search(s, 0, len(s) - 1, 5))   
print(binary_search(s, 0, len(s) - 1, 31))  
print(binary_search(s, 0, len(s) - 1, 99))  
print(binary_search(s, 0, len(s) - 1, 64))  
print(binary_search(s, 0, len(s) - 1, 51))