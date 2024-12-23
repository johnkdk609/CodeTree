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
            self.cursor = (self.tail, None)
            self.size = 1
        else:
            self.head = None
            self.tail = None
            self.cursor = (None, None)
            self.size = 0

    def insert(self, data):
        if self.tail is None:
            self.head = Node(data)
            self.tail = self.head
        else:
            new_node = Node(data)
            node = self.tail
            node.next = new_node
            new_node.prev = node
            self.tail = new_node
        self.size += 1

    def reset_cursor(self):
        self.cursor = (self.tail, None)

    def cursor_move_left(self):
        prev_n, next_n = self.cursor
        if prev_n:
            self.cursor = (prev_n.prev, prev_n)

    def cursor_move_right(self):
        prev_n, next_n = self.cursor
        if next_n:
            self.cursor = (next_n, next_n.next)

    def delete_at_cursor(self):
        prev_n, next_n = self.cursor
        if next_n:
            if next_n.next:
                next_n.next.prev = prev_n
            else:
                self.tail = prev_n
            if prev_n:
                prev_n.next = next_n.next
            else:
                self.head = next_n.next
            self.cursor = (prev_n, next_n.next)
            del next_n
            self.size -= 1

    def insert_at_cursor(self, data):
        prev_n, next_n = self.cursor
        new_node = Node(data)
        if prev_n is None and next_n:
            new_node.next = next_n
            next_n.prev = new_node
            self.head = new_node
        elif prev_n and next_n:
            prev_n.next = new_node
            new_node.prev = prev_n
            new_node.next = next_n
            next_n.prev = new_node
        elif prev_n and next_n is None:
            prev_n.next = new_node
            new_node.prev = prev_n
            self.tail = new_node
        else:
            self.head = new_node
            self.tail = self.head
        self.size += 1
        self.cursor = (new_node, next_n)

    def desc(self):
        result = []
        node = self.head
        while node:
            result.append(node.data)
            node = node.next
        print("".join(result))


N, M = map(int, input().split())
input_string = list(input().strip())
DLL = NodeMgmt(None)
for toast in input_string:
    DLL.insert(toast)

DLL.reset_cursor()
for _ in range(M):
    cmd = list(input().strip().split())
    if cmd[0] == 'L':
        DLL.cursor_move_left()
    elif cmd[0] == 'R':
        DLL.cursor_move_right()
    elif cmd[0] == 'D':
        DLL.delete_at_cursor()
    elif cmd[0] == 'P':
        DLL.insert_at_cursor(cmd[1])

DLL.desc()