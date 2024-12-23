class Node:
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class NodeMgmt:
    def __init__(self, data):
        if data is not None:
            self.head = Node(data)
            self.tail = self.head
            self.size = 1
        else:
            self.head = None
            self.tail = None
            self.size = 0

    def push_front(self, data):
        new_node = Node(data)
        node = self.head
        if node:
            new_node.next = node
            node.prev = new_node
            self.head = new_node
        else:
            self.head = new_node
            self.tail = self.head
        self.size += 1

    def push_back(self, data):
        new_node = Node(data)
        node = self.tail
        if node:
            node.next = new_node
            new_node.prev = node
            self.tail = new_node
        else:
            self.head = new_node
            self.tail = self.head
        self.size += 1

    def pop_front(self):
        node = self.head
        if node:
            if node.next:
                node.next.prev = None
                self.head = node.next
            else:
                self.head = None
                self.tail = None
            self.size -= 1
        print(node.data)
        del node

    def pop_back(self):
        node = self.tail
        if node:
            if node.prev:
                node.prev.next = None
                self.tail = node.prev
            else:
                self.head = None
                self.tail = None
            self.size -= 1
        print(node.data)
        del node

    def get_size(self):
        print(self.size)

    def is_empty(self):
        if self.size == 0:
            print(1)
        else:
            print(0)

    def front(self):
        print(self.head.data)

    def back(self):
        print(self.tail.data)


doubly = NodeMgmt(None)
N = int(input())
for _ in range(N):
    cmd = list(input().strip().split())
    if cmd[0] == 'push_front':
        doubly.push_front(int(cmd[1]))
    elif cmd[0] == 'push_back':
        doubly.push_back(int(cmd[1]))
    elif cmd[0] == 'pop_front':
        doubly.pop_front()
    elif cmd[0] == 'pop_back':
        doubly.pop_back()
    elif cmd[0] == 'size':
        doubly.get_size()
    elif cmd[0] == 'empty':
        doubly.is_empty()
    elif cmd[0] == 'front':
        doubly.front()
    elif cmd[0] == 'back':
        doubly.back()