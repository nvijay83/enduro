from clubspeedapi import *
from db import *

def temp(x, init_fuel, max_fuel, num_qual, heatno):
  l, cached= get_cust_heats(x, False)
  s = 0
  race = {}
  print l
  print l[x]
  print l[x][0]
  if len(l) > 0:
    s = l[x][0][0]
  print s
  data,a,b = get_heat(s, None, True)
  race['init_fuel'] = int(init_fuel)
  race['max_fuel'] = int(max_fuel)
  race['num_qual'] = int(num_qual)
  race['qual_heat'] = int(s)
  with open("config.json",'w') as fp:
    json.dump(race, fp)
  l = data['details']
  f = open('init.txt','w')
  count = 1
  kart_id = {}
  for i in l:
    kart_id[i['id']] = count
    st = "1,"+str(i['totlap'])+','+str(count)+"\n"
    count = count +1
    f.write(st)
  f.close()
  create_race()
  init_race(kart_id,heatno)
 
temp(1103991,180,180,1,164056)
