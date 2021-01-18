from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as bs
import re
import random
import time
import lxml
import html
import pymysql
from lxml.html import fromstring 
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")
#获得中英文对照字典
Col_list_eng=['id', 'type1', 'type2', 'general_name', 'English_name', 'product_name','company','component', 'indication', 'dosage', 'ban', 'warn', 'notice', 'women',
       'pharmacology', 'dynamics', 'OTC', 'date_verify', 'date_alter','Toxicology', 'component_che', 'class', 'over_instruct','experiment','drug_and_food',"medication_instructions","other"]
Col_list=["id",'类别1', '类别2','通用名称', '英文名称', '商品名称','公司名', '成份','适应症', '用法用量', '禁忌', '警告', '注意事项', '孕妇及哺乳期妇女用药',
 '药理作用', '药代动力学', '是否OTC', '核准日期', '修改日期', '毒理研究', '化学成份', '药品监管分级','超说明书适应症',"临床试验","服药与进食","用药须知","其他未列类别"]
Col_dct=dict(zip(Col_list,Col_list_eng))
Col_dct
import json
with open('your_json.txt', 'r', encoding='utf-8') as f:
    content = f.read()
drugs = json.loads(content)
first_level_category_list = drugs['props']['pageProps']['firstLevelCategoryList']
category_dict = {category['id']: category['name'] for category in first_level_category_list}
second_level_category_list = drugs['props']['pageProps']['secondLevelCategoryList']
headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie':'_ga=GA1.2.1025650811.1609843956; __auc=026a677a176d22eb082ad4503ab; Hm_lvt_8a6dad3652ee53a288a11ca184581908=1609844043,1609901203; CLASS_CASTGC=24723b436e2d9e28eb8ffb327215874f126ffc06fa395f87dbcf92e765eb326cb5a30fe4af639e219dfe1bf266327ef4908c7b718bd7a99a1c056261882d86eeef21748818fd73ccf20325250f82814b1f79fe7c4c58789dfa2754afa92e08f17305a08e96ced587eaadd8410af9338cbbcb4bee735f1ba787678cd41ece30e0dd3f17c6854b2328b7640535f208f11e17cb90ac8966b7341518b68df4eed567a103121b8cdd79c2fa73fdbe88366e77a505d2d714a58808c621c06fe7b97e4139102878004cb134f7c79a721ad79b4c854965d78b6f5c82902c2f455aad76ae562f3490bcc1b93fcef36d9900d593b83878baca5383ea847cafc594f5c1ffc0; JUTE_BBS_DATA=c9de36bdf35923c20e0990fc518b1945ee2436752205d25331685934e59cf79620262f0989239e5de153effeb9a1d203f01cdcca69d920c85b480589906e51860b94d3072bf548ee7f7842797c9d6f92; CASTGC=TGT-107576-Nq2V4s4oeTUhzvPAetJJyQrVKb2fsjri5xb-50; route=6f2d12ae997a6e0b502275db208a27c1; JSESSIONID=075289E2F0F42D92E7CD97D6644A2BAC-n1',
    #'Cookie': 'dxy_da_cookie-id=68c174260fce8fad455602eb3af8447e1609746179672; route=76fe8badbf970cea48a83fee22e3ae12; _ga=GA1.2.1025650811.1609843956; _gid=GA1.2.1309324206.1609843956; __auc=026a677a176d22eb082ad4503ab; Hm_lvt_8a6dad3652ee53a288a11ca184581908=1609844043,1609901203; Hm_lpvt_8a6dad3652ee53a288a11ca184581908=1609901203; CMSSESSIONID=9E6A0BC95F161E7CE4E212DC8EDF2766-n2; __asc=6456049b176d596dccf5b3bebb9; DRUGSSESSIONID=0DD74EE9D01FB8A2EE37EC3EA9829537-n2; JUTE_BBS_DATA=fd8413ac73ad48dd31e8cf9fec47b066dd2215e58eacac992edc73ad220bbb9702f3eb461c7610039ec019daadd581a3e50fb3ca5fcda27e81d6b5a1ff3a8596ea2ffb39ab8f9c8daa69e73f540136f5; CLASS_CASTGC=7e626917bdba02c02e917f8832455dde97a1445b670b6496bc39a992917f3ee0d558ba889a4428f18257679da608c2665837e982e1dd8f45b4850140d3fdef6041c08d052055c8a3cbc7cca5a0ef6c3ceb8615483d53e89dfcf2231aba162c738e106cc8b0162b210f0e994848b21bcb8cdd442382b60ab00f5dfb0277c6def7ebd5ba10a1f25199e972396448da448082b2e3c758c4fb9cf8cc34b922c0950a8588eff3425ce0d725d1239176675d0ef258181aa218263e1bbf0e5c670ce5a2176300f0a5a79bed40f1247f2c3b7edc0f206588873499280a23b4f2c0ed04f2f826e77e8df5b2b980546ba638c1dd5e1ece8c330936c660791e68225072317f; _gat=1',
    'Host': 'drugs.dxy.cn',
    'Referer': 'https://auth.dxy.cn/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
}
#db = pymysql.connect(host='192.168.0.200',user='root', password='123456', port=3306, db='zeyu_test')
cursor = db.cursor()
table = 'Medicines_full_new'
#table = 'Medicines'
dxys_url = 'http://drugs.dxy.cn/'
session=requests.Session()
lst_fail=[]
for sec_category in tqdm(second_level_category_list):
    type1=category_dict[sec_category['supId']]
    type2=sec_category['name']
    type2_id=sec_category['id']
    type2_url=dxys_url+"category/"+str(type2_id)+"/"
    source=session.get(type2_url,headers=headers,verify=False).content.decode()
    selector=lxml.html.fromstring(source)
    page_lst=selector.xpath('//ul[@class="ant-pagination pagination__18yd"]')
    if page_lst==[]:
        max_page=1
    else:
        page_lst=selector.xpath('//ul[@class="ant-pagination pagination__18yd"]')[0]
        max_page=int(page_lst.xpath('li/@title')[-2])
    for page in range(max_page):
        url_page=type2_url[:-1]+"?page="+str(page)
        source=session.get(url_page,headers=headers,verify=False).content.decode()
        selector=lxml.html.fromstring(source)
        drug_list=selector.xpath('//h3[@class="drugs-item-name__3yfj"]')
        for i in range(len(drug_list)):
            lst2=drug_list[i].xpath('a/@href')#请注意
            company_name=drug_list[i].xpath('a/text()')
            for x in lst2:
                y=dxys_url+x[1:]#请注意
                url_source=session.get(y,headers=headers,verify=False).content.decode()
                selector1=lxml.html.fromstring(url_source)
                func_list=selector1.xpath('//div[@class="item__3ue7"]')
                name1="".join(selector1.xpath('//div[@class="drug-title__1KdV"]/h2/text()'))
                name_temp=selector1.xpath('//div[@class="drug-names__8L2q"]/p/text()')
                name_temp=[x.replace(": ","") for x in name_temp]
                try:
                    if len(name_temp)==5:
                        flag=bool(re.search('[a-z]', name_temp[3]))
                        if flag:
                            name_temp.insert(5,"")
                        else:
                            name_temp.insert(3,"")
                    elif len(name_temp)==4:
                        name_temp.insert(5,"")
                        name_temp.insert(3,"")
                    medicine=dict()
                    medicine["type1"]=type1
                    medicine["type2"]=type2
                    for i in range(0,len(name_temp),2):
                        medicine[Col_dct[name_temp[i]]]=name_temp[i+1]
                    medicine["company"]=company_name[-1]
                    type_lst=[]
                    contents=[]
                    for i in range(len(func_list)):
                        type_name="".join(func_list[i].xpath('div[@class="cnName__3Kpx"]/text()')).replace("【","").replace("】","")
                        if type_name in Col_dct.keys():#请注意
                            type_lst.append(Col_dct[type_name])
                            a=func_list[i].xpath('div[@class="content__1KNL"]')[0]
                            content=a.xpath("string(.)").replace("\n","")
                            contents.append(content)
                            medicine[Col_dct[type_name]]=content
                        else:
                            type_lst.append("other")
                            a=func_list[i].xpath('div[@class="content__1KNL"]')[0]
                            content=a.xpath("string(.)").replace("\n","")
                            contents.append(content)
                            medicine["other"]=type_name+": "+content
                    keys=', '.join(medicine.keys())
                    values=tuple(medicine.values())
                    sql = 'INSERT INTO {table} ({keys}) VALUES {values}'.format(table=table, keys=keys, values=values)
                    try:
                        cursor.execute(sql)
                        print('Successful')
                        db.commit()
                    except Exception as e:
                        print('Failed')
                        print(medicine["product_name"])
                        print(e)
                        lst_fail.append(y)
                        db.rollback()
                except Exception as e:
                    print(y)
                    print(e)
                    lst_fail.append(y)
                    
cursor.close()
db.close()
