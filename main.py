from structures import trees
from structures import hashtable
from rich.console import Console
from datetime import datetime

def run(description, action, *args, **kwargs):
    c = Console()
    c.print(f'[[yellow]INFO[/]] [rgb(110,110,110)]{description}[/] виконується. . .')
    try:
        result = action(*args, **kwargs)
        c.print(f"[[green]SUCCESS[/]] [rgb(110,110,110)]{description}[/] виконано успішно!")
        return result
    except Exception as e:
        c.print(f"[[red]ERROR[/]] Під час [rgb(110,110,110)]{description}[/] виникла помилка: {e.__class__.__name__}")
        return e

table = run('Створення хеш-таблиці', hashtable.MyHashTable, capacity=7)
run('Вставлення у хеш-таблицю {\'apple\': 10}', table.put, 'apple', 10)
run('Вставлення у хеш-таблицю {\'banane\': 20}', table.put, 'banane', 20)
run('Видалення з хеш-таблиці \'cherry\'', table.remove, "cherry")

tree = run('Створення бінарного дерева', trees.BinarySearchTree)
run('Вставлення у бінарне дерево {\'0: \'root\'}', tree.insert, 0, 'root')
run('Видалення з бінарного дерева {\'0: \'root\'}', tree.delete, 0)
run('Пошук значення з ключем 0 у бінарному дереві ', tree.search, 0)

run('Збереження хеш-таблиці у JSON', table.save_to_json, 'hashtable.json')
run('Завантаження хеш-таблиці з JSON', table.load_from_json, 'hashtable.json')
for k, v in table.items():
    print(f'{k}: {v}')