# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 22:47:59 2018

Refer to 
https://wiki.osgeo.org/wiki/Taiwan_datums
http://www.sunriver.com.tw/grid_taipower.htm
http://site.whataiwant.com/?action-viewnews-itemid-174
"""
import os
import re
import math
from operator import itemgetter

def checkArea(type):
    if type == "A": return (170000,2750000)#新竹 竹北市 桃園新豐鄉
    if type == "B": return (250000,2750000)#台北 桃園 宜蘭北宜
    if type == "C": return (330000,2750000)#台北貢寮.宜蘭頭城
    if type == "D": return (170000,2700000)#苗栗 新竹
    if type == "E": return (250000,2700000)#桃園 新竹 苗栗 宜蘭
    if type == "F": return (330000,2700000)#宜蘭
    if type == "G": return (170000,2650000)#北彰化 台中縣市 南苗栗 南投
    if type == "H": return (250000,2650000)#南投 花蓮秀林 台中和平
    if type == "J": return (90000,2600000)#雲林沿海
    if type == "K": return (170000,2600000)#雲林 嘉義 南投
    if type == "L": return (250000,2600000)#南投 花蓮
    if type == "M": return (90000,2550000)#嘉義台南縣市沿海
    if type == "N": return (170000,2550000)#南嘉義 北台南 北高雄 台東
    if type == "O": return (250000,2550000)#台東花蓮交界
    if type == "P": return (90000,2500000)#台南市高雄沿海
    if type == "Q": return (170000,2500000)#北屏東 高雄 台東 南台南
    if type == "R": return (250000,2500000)#台東&#65288;綠島&#65311;&#65289;
    if type == "T": return (170000,2450000)#屏東 台東 南高雄
    if type == "U": return (250000,2450000)#台東太麻里&#65288;3.5公頃&#65289;
    if type == "V": return (170000,2400000)#屏東墾丁
    if type == "W": return (250000,2400000)#&#65288;蘭嶼&#65311;&#65289;

def poleToTWD67TM2(location):
    V,W=0,0
    word=['X','A','B','C','D','E','F','G','H']
    X,Y = checkArea(location[0])
    PP = int(location[1:3])
    QQ = int(location[3:5])
    R = word.index(location[5])
    S = word.index(location[6])
    T = int(location[7])
    U = int(location[8])
    try:
        V = int(location[9])
        W = int(location[10])
    except IndexError:
        pass
    
    x = X +(800*PP)+100*(R-1)+(10*T)+V
    y = Y +(500*QQ)+100*(S-1)+(10*U)+W
    return (x,y) 

def tWD67TM2toWGS84(x,y):
   out = {'status':False}
   lat = None
   lon = None
   
   # TWD67 to TWD97
   A = 0.00001549
   B = 0.000006521
   x = float(x)
   y = float(y)
   x = x + 807.8 + A * x + B * y
   y = y - 248.6 + A * y + B * x

   # TWD97 to WGS84
   result = os.popen('echo '+str(x)+' '+str(y)+' | proj -I +proj=tmerc +ellps=GRS80 +lon_0=121 +x_0=250000 +k=0.9999 -f "%.8f"').read().strip() # lat, lng 
   process = re.compile( '([0-9]+\.[0-9]+)', re.DOTALL )
   for item in process.findall(result):
      if lon == None:
         lon = float(item)
      elif lat == None:
         lat = float(item)
      else:
         break

   if lat == None or lon == None:
      return out
   out['lat'] = lat
   out['lng'] = lon
   out['status'] = True
   return out

#排序list裡面的dict
abc = [{'name':'aaa', 'age':30}, {'name':'bbb', 'age': 20}, {'name':'ccc', 'age': 40}]
newlist = sorted(abc, key=itemgetter('age'), reverse=True)
print(newlist)

#


#清理資料ETL
"""
臺北市	A
臺中市	B
基隆市	C
臺南市	D
高雄市	E
新北市	F
宜蘭縣	G
桃園縣	H
新竹縣	J
苗栗縣	K
臺中縣	L
南投縣	M
彰化縣	N
雲林縣	P
嘉義縣	Q
臺南縣	R
高雄縣	S
屏東縣	T
花蓮縣	U
臺東縣	V
澎湖縣	X
陽明山	Y
金門縣	W
連江縣	Z
嘉義市	I
新竹市	O
"""
#清理前後空白
def clear_data(input_data):
    return input_data.strip()

#個人ＩＤ
def clear_p_id(input_data):
    return input_data[0],input_data[1]

#找出尾巴的檔案(圖片)
#items=("jpg","gif","png")
#def check_filename(input_data):
#    return input_data.endswith(items)
    
    
