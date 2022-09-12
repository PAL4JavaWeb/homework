from re import findall,compile,search
from fake_useragent import UserAgent
from json import load,dump,loads
from requests import get
from random import choice,randint
from time import sleep


class REPLAY(object):
    def __init__(self):
        self.url_prefix="https://api.opendota.com/api/matches/"
        match_id_file="be_dire.txt"#你要从各大网站比如max+,dotabuff,opendota获取你要的dota2 matchid 然后保存到txt或其他格式文档里
        self.ua = UserAgent()
        self.headers={"user-agent":self.ua.random}
        with open(match_id_file,"r+",encoding="utf-8") as f:
            self.url_suffix_list=[i.strip() for i in f.readlines()]
        self.replay_path="replay_be_dire/"
    def crawl_replay(self):
        fail_list=[]
        for match_link in self.url_suffix_list:
            one_match=get(self.url_prefix+match_link,headers=self.headers)
            print (match_link)
            fname=match_link+".dem.bz2"
            print (fname)
            one_match_dict=loads(one_match.text)
            one_match_replay_bytes=get(one_match_dict["replay_url"],stream=True)
            print (one_match_dict["replay_url"])
            print(len(one_match_replay_bytes.content))
            if one_match_replay_bytes.status_code==200:
                try:
                    abs_path=self.replay_path+fname
                    print (abs_path)
                    with open(abs_path,"wb") as f:
                        f.write(one_match_replay_bytes.content)
                    print (fname,"写入成功")
                except:
                    print ("fail-",match_link)
                    fail_list.append(fname)
                    continue
            sleep(randint(1,3))
        print (fail_list,len(fail_list))
if __name__ == '__main__':
    instance=REPLAY()
    instance.crawl_replay()