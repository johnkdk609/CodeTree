def selection_sort(lst):
    for i in range(N):
        min_index = i
        for j in range(i + 1, N):
            if lst[min_index] > lst[j]:
                min_index = j
        if min_index != i:
            lst[i], lst[min_index] = lst[min_index], lst[i]
    return lst


N = int(input())
need_sort_lst = list(map(int, input().split()))

print(*selection_sort(need_sort_lst))