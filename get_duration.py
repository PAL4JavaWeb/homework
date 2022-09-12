from urllib.request import urlopen, Request
import re
import pandas as pd

def get_durations(match_id):
    url="https://api.opendota.com/api/matches/"+match_id
    # 该网址的源码(以该网页的原编码方式进行编码，特殊字符编译不能编码就设置ignore)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57'}
    ret = Request(url, headers=headers)
    res = urlopen(ret)
    contents = res.read()
    txt = contents.decode()
    duration = eval(re.findall(r'(?<=duration":).{4}',txt)[0])
    return duration

f = open("D:\\Desktop\\DOTA2\\DOTA2\\teamspirit_radiant.txt",'r')
lst=[]
for line in f.readlines():
    line=line.strip()
    duration = get_durations(line)
    print(line,duration)
    lst.append([line,duration])

data=pd.DataFrame(lst,columns=['match_id','duration'])
data.to_csv("D:\\Desktop\\teamspirit_radiant_duration.csv",index=None)