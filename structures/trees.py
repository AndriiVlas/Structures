class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
    

class BinarySearchTree:
    _START = object()

    def __init__(self):
        self.root = None
    
    def insert(self, key, value, current_node = _START):
        if (current_node is BinarySearchTree._START):
            current_node = self.root
        if (self.root is None):
            self.root = Node(key, value)
            return
        elif (key == current_node.key):
            current_node.value = value
        elif (key < current_node.key):
            if (current_node.left is None):
                current_node.left = Node(key, value)
            else:
                self.insert(key, value, current_node.left)
        else:
            if (current_node.right is None):
                current_node.right = Node(key, value)
            else:
                self.insert(key, value, current_node.right)

    def search(self, key):
        return self.search_node(key).value
    
    def search_node(self, key, current_node = _START):
        if (current_node is BinarySearchTree._START): current_node = self.root
        if (current_node is None): raise KeyError()
        if (key < current_node.key): return self.search_node(key, current_node.left)
        elif (key > current_node.key): return self.search_node(key, current_node.right)
        else: return current_node

    def find_min(self, current_node = _START):
        if (current_node is BinarySearchTree._START): current_node = self.root
        if (current_node is None): raise Exception()
        elif (current_node.left is None): return current_node.key, current_node.value
        else: return self.find_min(current_node.left)
    
    def find_max(self, current_node = _START):
        if (current_node is BinarySearchTree._START): current_node = self.root
        if (current_node is None): raise Exception()
        elif (current_node.right is None): return current_node.key, current_node.value
        else: return self.find_max(current_node.right)

    def inorder_traversal(self, current_node = _START):
        if (current_node is BinarySearchTree._START): current_node = self.root
        if (current_node is None): return
        yield from self.inorder_traversal(current_node.left)
        yield (current_node.key, current_node.value)
        yield from self.inorder_traversal(current_node.right)
    
    def get_height(self, key = _START):
        if (key == BinarySearchTree._START): current_node = self.root
        else: current_node = self.search_node(key)
        def find_height(current_node):
            if (current_node is None):
                return 0
            return 1 + max(find_height(current_node.left), find_height(current_node.right))
        return find_height(current_node)
    
    def find_range(self, min_key, max_key):
        value_range = []
        def finder(current_node):
            if (current_node is None): return
            if (current_node.key > min_key): finder(current_node.left)
            if (current_node.key >= min_key and current_node.key <= max_key): value_range.append((current_node.key, current_node.value))
            if (current_node.key < max_key): finder(current_node.right)
        finder(self.root)
        return value_range

    def delete(self, key, current_node = _START):
        start = False
        if (current_node is BinarySearchTree._START): current_node = self.root; start = True
        if (current_node is None): return None
        if (key < current_node.key): current_node.left = self.delete(key, current_node.left)
        elif (key > current_node.key): current_node.right = self.delete(key, current_node.right)
        else:
            if (current_node.left is None):
                return current_node.right
            elif (current_node.right is None):
                return current_node.left
            suc_key, suc_value = self.find_min(current_node.right)
            current_node.key = suc_key
            current_node.value = suc_value
            current_node.right = self.delete(suc_key, current_node.right)
        if (start): self.root = current_node
        return current_node

    def is_valid_bst(self, current_node = _START, min = float('-inf'), max = float('inf')):
        if (current_node is BinarySearchTree._START): current_node = self.root
        if (current_node is None): return True
        if ((current_node.key < min) or (current_node.key > max)): return False
        return (self.is_valid_bst(current_node.left, min, current_node.key) and
                self.is_valid_bst(current_node.right, current_node.key, max))