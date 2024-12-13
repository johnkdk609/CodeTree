def push_back(num):
    array.append(num)
    return

def pop_back():
    array.pop()
    return

def size_():
    print(len(array))
    return

def get_(num):
    print(array[num - 1])
    return


N = int(input())
array = []
for _ in range(N):
    data = list(input().strip().split())
    if data[0] == 'push_back':
        push_back(int(data[1]))
    elif data[0] == 'pop_back':
        pop_back()
    elif data[0] == 'size':
        size_()
    elif data[0] == 'get':
        get_(int(data[1]))