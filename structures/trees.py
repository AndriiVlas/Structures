import json
import pickle
from pathlib import Path 
from datetime import datetime

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
            self._log_act(key)
            return
        elif (key == current_node.key):
            current_node.value = value
        elif (key < current_node.key):
            if (current_node.left is None):
                current_node.left = Node(key, value)
                self._log_act(key)
            else:
                self.insert(key, value, current_node.left)
        else:
            if (current_node.right is None):
                current_node.right = Node(key, value)
                self._log_act(key)
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
    
    def save_to_json(self, path):
        path = Path(path)
        data = [{'key': k, 'value': v} for k, v in self.inorder_traversal()]
        with open(path, 'w', encoding = 'utf-8') as f:
            json.dump(data, f)

    def load_from_json(self, path):
        path = Path(path)
        try:
            with open(path, 'r', encoding = 'utf-8') as f:
                data = json.load(f)
                self.root = None
                for kv in data:
                    self.insert(kv['key'], kv['value'])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f'Файл {path} пошкоджений або відсутній')
    
    def save_to_pkl(self, path):
        path = Path(path)
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load_from_pkl(path):
        path = Path(path)
        with open(path, "rb") as f:
            return pickle.load(f)
        
    def _log_act(self, key):
        path = Path("tree_history.log")
        if (path.exists() and path.stat().st_size > 1024):
            old_log = Path("tree_history.log.old")
            if (old_log.exists()):
                old_log.unlink()
            path.rename(old_log)
            path.touch()
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Додано елемент: Ключ={key}\n")