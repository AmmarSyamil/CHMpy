import os
from pathlib import Path
import stat
import subprocess
from pathlib import Path
from pprint import pprint

def tree(dir):
    for subdir in dir.iterdir():
        if subdir.is_dir():
            print(subdir)



path = Path(".")


def get_permissions(chmod: str):


    data_type = chmod[0]
    if data_type == 'd':
        data_type = 'directory'
    elif data_type == '-':
        data_type = 'file'

    owner = chmod[1:4]
    group = chmod[4:7]
    others = chmod[7:10]

    perm_dict = {
        'owner': {
            'chmod':owner,
            'data': []
        },
        'group': {
            'chmod':group,
            'data': []
        }, 
        'others': {
            'chmod': others,
            'data': []
        }
    }


    for u in ['owner', 'group', 'others']:
        #print(perm_dict[u]['chmod'])
        #x = perm_dict[u]
        #print(x.keys())
        y = perm_dict[u]["chmod"]
        #print(y)
        for i in range(len(y)):
            #print(range(len(u)))
            #print(u)

            if y[i] == 'r':
                perm_dict[u]["data"].append('read')
            elif y[i] == 'w':
                perm_dict[u]["data"].append('write')
            elif y[i] == 'x':
                perm_dict[u]["data"].append('execute')
        
        

                
    
    #print(f"Permissions: {chmod} - Type: {data_type}, Owner: {owner}, Group: {group}, Others: {others}")
    return perm_dict, data_type

def version_1():
    for item in path.iterdir():
        mode = item.stat().st_mode
        permissions = stat.filemode(mode)
        data, file_type = get_permissions(permissions)
        #print(data)
        print(f'{item} : {file_type}')

        for i in data:
            print(f'{i}: {data[i]["data"]} ')

        
        #print(item, permissions)

def version_2():

    def tree(dir):
        dir = Path(dir)
        a=0
        if dir.name.startswith(".") or dir.name in {"__pycache__", ".venv", "venv", ".git", "myenv"}:
            return
        for subdir in dir.iterdir():
            #print(a)
            #a+=1#
            mode = subdir.stat().st_mode
            permissions = stat.filemode(mode)
            data_get, file_type = get_permissions(permissions)
            #print(f'{subdir} : {file_type}')
            #subdir = str(subdir)
            data.setdefault(subdir.name, {"data": {}, "type": file_type})
            #data.update({subdir: {
            #    "type":file_type
            #}})


            #pprint(data_get)
            for i in data_get:   
            
                #print(f'{i}: {data[i]["data"]} ')
                #print(data)
                data.setdefault(subdir.name, {}).setdefault("data", {})[i] = data_get.setdefault(i, {})["data"]
                #data[subdir]["data"][i] = data_get[i]["data"]

                #data.update({subdir: {
                #    "data": {
                #        i : data_get[i]["data"]
                #    }
                #}})
            if subdir.is_dir():
                tree(subdir)

    tree('.')
    pprint(data)

data: dict[str, dict[str, str | dict[str, str]]] = {}
version_2()

