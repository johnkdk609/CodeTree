def bubble_sort(lst):
    for i in range(N - 1):
        swapped = False
        for j in range(N - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                swapped = True
        if not swapped:
            break
    return lst


N = int(input())
need_sort_lst = list(map(int, input().split()))

print(*bubble_sort(need_sort_lst))