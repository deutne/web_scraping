'''
sort_lib.py contains the functions related to sorting the list file_data in
descending order of file size.

By: Dena E. Utne
'''


def insertion_sort_alg(file_data):
    '''
    Uses an insertion sort algorithm to sort the elements of the list file_data
    in descending order of file size.

    Source: Insertion sort algorithm and code from Week 43 IBE 151 Canvas
            Modules:
            https://himolde.instructure.com/courses/1607/pages/sequence-algorithms-searching-and-sorting-lists?module_item_id=34576
    Returns: None
    '''

    for j in range(1, len(file_data)):
        key = file_data[j]
        # insert file_data[j] into the sorted list file_data[:j]
        i = j - 1
        while i >= 0 and file_data[i][1] < key[1]:
            # while we haven't reached the first position
            # and the left term is higher than me, shift him
            file_data[i + 1] = file_data[i]   # right shift
            i = i - 1
        file_data[i + 1] = key  # position file_data[j] in the right place


def bubble_sort_alg(file_data):
    '''
    Uses a bubble sort algorithm to sorts the elements of the list file_data in
    descending order of file_size.

    Source: Bubble sort algorithm based on Freeman, Head First Learn to Code,
            Ch. 4, part 2
    Returns: None
    '''
    swapped = True
    while swapped:
        swapped = False
        for i in range(0, len(file_data)-1):
            if file_data[i][1] < file_data[i+1][1]:
                tmp = file_data[i]
                file_data[i] = file_data[i+1]
                file_data[i+1] = tmp
                swapped = True


def merge(L1, L2):
    '''
    Merge function component of merge sort algorithm
    Source: Merge sort algorithm and code from Week 43 IBE 151 Canvas Modules:
            https://himolde.instructure.com/courses/1607/pages/sequence-algorithms-searching-and-sorting-lists?module_item_id=34576
    Returns L: the merged and sorted list of L1 and L2.
    '''
    L = []
    left, right = 0, 0
    while left < len(L1) and right < len(L2):
        if L1[left][1] >= L2[right][1]:
            L.append(L1[left])
            left += 1
        else:
            L.append(L2[right])
            right += 1
    if left < len(L1):
        L.extend(L1[left:])
    elif right < len(L2):
        L.extend(L2[right:])
    return L


def merge_sort_alg(file_data):
    '''
    Uses a merge sort algorithm to sort the elements of the list file_data in
    descending order of file size.

    This is a recursive function.
    Source: Merge sort algorithm and code from Week 43 IBE 151 Canvas Modules:
            https://himolde.instructure.com/courses/1607/pages/sequence-algorithms-searching-and-sorting-lists?module_item_id=34576
    '''
    if len(file_data) <= 1:
        return file_data
    n = len(file_data)//2
    return merge(merge_sort_alg(file_data[:n]), merge_sort_alg(file_data[n:]))
