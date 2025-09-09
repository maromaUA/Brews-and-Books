import json
from pathlib import Path

BASE_DIR = Path("data")

def addData(file, object):
    file_path = BASE_DIR / f'{file}.json'
    with open(file_path, 'r+', encoding="utf-8") as f:
      data = json.load(f) 
      data.append(object)
      f.seek(0) 
      json.dump(data, f, indent=4)
      f.truncate()
      return object

def showAllData(file):
    file_path = BASE_DIR / f'{file}.json'
    with open(file_path, 'r', encoding="utf-8") as f:
       data = json.load(f)
       return data

def findData(file, key, value):
    file_path = BASE_DIR / f'{file}.json'
    with open(file_path, 'r', encoding="utf-8") as f:
       data = json.load(f)
       for obj in data:
          if(obj[key]==value):
             return obj
    return None

def updateData(file, key, value, updatedObject):
     file_path = BASE_DIR / f'{file}.json'
     with open(file_path, 'r+', encoding="utf-8") as f:
        if(findData(file, key, value)==False):
           return "no data to update"
        else:
           data = json.load(f)
           for i, obj in enumerate(data):
              if(obj[key]==value):
                 data[i] = updatedObject
                 f.seek(0) 
                 json.dump(data, f, indent=4)
                 f.truncate()
                 return updatedObject

            
           return None
        

