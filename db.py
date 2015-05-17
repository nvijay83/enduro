import json
from pprint import pprint
import time
import os
import shutil
import io
from clubspeedapi import *
import threading

def create_race():
  t = get_race_folder()
  try:
    os.stat(t)
  except:
    os.mkdir(t)
  try:
    os.stat(t+"/temp")
  except:
    os.mkdir(t+"/temp")
  shutil.copyfile('config.json',t+'/config.json')
  shutil.copyfile('init.txt',t+'/init.txt')

def get_race_folder():
  return ".db/"+time.strftime("%m-%d-%Y")

def get_init_race():
  return 'init.txt'

def get_db():
  return get_race_folder()+'/db.json'

def get_config():
  f = get_race_folder()+"/config.json"
  with open(f) as data_file:
    data = json.load(data_file)
  init_fuel = data['init_fuel']
  max_fuel = data['max_fuel']
  return init_fuel,max_fuel

def get_kart_ids():
  with open(get_race_folder()+"/kart_id.json",'r') as fp:
    kart_id = json.load(fp)
  return kart_id

def init_race(kart_id, heatno):
  kart = {}
  kart_log = {}
  fol = get_race_folder()
  f = open(get_init_race(),'r')
  (init_fuel, max_fuel) = get_config()
  for i in f:
    if '#' in i:
      continue
    else:
      token = i.split(',')
      lap_empty = int(init_fuel) - int(token[1].strip())
      l = []
      l.append((0, lap_empty))
      kart[int(token[2].strip())] = (lap_empty, l)
  f.close()
  with open(get_db(),'w') as fp:
    json.dump(kart, fp, ensure_ascii=False)
  with open(get_race_folder()+"/kart_id.json",'w') as fp:
    json.dump(kart_id, fp)
  thread = threading.Thread(target = monitor,args=(heatno,))
#thread.daemon = True
  thread.start()


def update_db(kart,fuel,cur_lap):
  kart = str(kart)
  with open(get_db()) as fp:
    db = json.load(fp)
  (init_fuel, max_fuel) = get_config()
  lap_empty = db[kart][0]
  lap_empty = min(cur_lap+max_fuel, lap_empty+fuel)
  db[kart][0] = lap_empty
  db[kart][1].append((cur_lap, fuel))
  with open(get_db(),'w') as fp:
    json.dump(db, fp, ensure_ascii=False)
  return lap_empty


def get_db_lap():
  l = os.listdir(get_race_folder()+"/temp")
  maxi = 0
  for i in l:
    f = int(i.split('.')[0])
    maxi = max(f, maxi)
  if maxi == 0:
    return {}
  with open(get_race_folder()+"/temp/"+str(maxi)+".json",'r') as fp:
    return json.load(fp)

def monitor(heatno):
  kart_id = {}
  with open(get_race_folder()+"/kart_id.json",'r') as fp:
    kart_id = json.load(fp)
  while True:
    url = get_url_heat(heatno)
    tree = get_tree(url)
    data = {}
    if True: #is_heat_in_progress(tree) or not is_heat_complete(tree):
      laps = get_alllaps(tree)
      laps = get_numlaps(laps)
      for i in laps:
        data[kart_id[i]] = laps[i]
    else:
      break
    with open(get_race_folder()+"/temp/"+str(int(time.time()))+".json",'w') as fp:
      json.dump(data,fp)

def get_race():
  with open(get_db()) as fp:
    db = json.load(fp)
  return db

#create_race()
#init_race()
