import json
import pickle
from pathlib import Path 
from datetime import datetime

class MyHashTable:
    _DELETED = object()
    
    def __init__(self, capacity = 11):
        self.capacity = capacity
        self.size = 0
        self.keys_values = [None] * self.capacity
        self.current = -1
            
    def hash1(self, key):
        return hash(key) % self.capacity
    
    def hash2(self, key):
        return 1 + (hash(key) % (self.capacity - 1))

    def put(self, key, value):
        if (self.size / self.capacity > 0.7):
            self._rehashing()
        index = None
        deleted_index = None
        for i in range(self.capacity):
            temp = (self.hash1(key) + i * self.hash2(key)) % self.capacity
            key_value = self.keys_values[temp]
            if (key_value is None): index = deleted_index if deleted_index is not None else temp; break
            elif (key_value is MyHashTable._DELETED): deleted_index = temp
            elif (key_value[0] == key): index = temp; break
        if (index is None):
            if (deleted_index is not None): index = deleted_index
            else: raise Exception()
        if (self.keys_values[index] in (None, MyHashTable._DELETED)): self.size += 1
        self._log_act(key)
        self.keys_values[index] = (key, value)

    def get(self, key):
        for i in range(self.capacity):
            temp = (self.hash1(key) + i * self.hash2(key)) % self.capacity
            key_value = self.keys_values[temp]
            if (key_value is None): raise KeyError
            elif (key_value is MyHashTable._DELETED): continue
            elif (key_value[0] == key): return self.keys_values[temp][1]
        raise KeyError()

    def _rehashing(self):
        old_keys_values = self.keys_values
        self.capacity *= 2
        self.keys_values = [None] * self.capacity
        self.size = 0
        for key_value in old_keys_values:
            if ((key_value is not None) and key_value is not MyHashTable._DELETED):
                old_key = key_value[0]
                old_value = key_value[1]
                self.put(old_key, old_value)
    
    def remove(self, key):
        key_value = None
        for i in range(self.capacity):
            temp = (self.hash1(key) + i * self.hash2(key)) % self.capacity
            key_value = self.keys_values[temp]
            if (key_value is None): raise KeyError
            elif (key_value is MyHashTable._DELETED): continue
            elif (key_value[0] == key):
                self.keys_values[temp] = MyHashTable._DELETED
                self.size -= 1
                return
        raise KeyError()
    
    def __len__(self):
        return self.size

    def __setitem__(self, key, value):
        self.put(key, value)

    def __getitem__(self, key):
        return self.get(key)
    
    def __iter__(self):
        self.current = -1
        return self
    
    def __next__(self):
        while True:
            self.current += 1
            if (self.current > self.capacity - 1):
                raise StopIteration
            key_value = self.keys_values[self.current]
            if (key_value not in (None, MyHashTable._DELETED)):
                return key_value[1]
    
    def items(self):
        for key_value in self.keys_values:
            if (key_value not in (None, MyHashTable._DELETED)):
                yield key_value

    def save_to_json(self, path):
        data = [{'key': kv[0], 'value': kv[1]} for kv in self.items() if isinstance(kv, tuple)]
        with open(path, 'w', encoding = 'utf-8') as f:
            json.dump(data, f)

    def load_from_json(self, path):
        try:
            with open(path, 'r', encoding = 'utf-8') as f:
                data = json.load(f)
                self.capacity = 11
                self.keys_values = [None] * self.capacity
                for kv in data:
                    self.put(kv['key'], kv['value'])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f'Файл {path} пошкоджений або відсутній')

    def save_to_pkl(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load_from_pkl(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    
    def _log_act(self, key):
        path = Path("hashtable_history.log")
        if (path.exists() and path.stat().st_size > 1024):
            old_log = Path("hashtable_history.log.old")
            if (old_log.exists()):
                old_log.unlink()
            path.rename(old_log)
            path.touch()
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Додано елемент: Ключ={key}\n")