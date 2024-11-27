block = '''
[
    {
        "id": 1,
        "title": "ка",
        "author": "ауа",
        "year": 34,
        "status": true
    }
]
'''

id_pos = block.rfind('"id":')
print(id_pos)
id_str = block[id_pos:].split(',')[0]
print(id_str)
