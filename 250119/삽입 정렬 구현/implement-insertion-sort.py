def insertion_sort(lst):
    for i in range(1, len(lst)):
        for j in range(i, 0, -1):
            if lst[j] < lst[j - 1]:
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
            else:
                break

    return lst


n = int(input())
arr = list(map(int, input().split()))

# Write your code here!
print(*insertion_sort(arr))