import re

import requests
import execjs
import pymongo

url = 'https://www.guazi.com/www/buy'
header = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
"Connection":"keep-alive",
"Host":"www.guazi.com",
"Sec-Fetch-Dest":"document",
"Sec-Fetch-Mode":"navigate",
"Sec-Fetch-Site":"none",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
}

response = requests.get(url,headers=header)
response.encoding = 'utf-8'

mymongo = pymongo.MongoClient("mongodb://admin:abc123456@localhost:27017")
mongo_db = mymongo['guazi_db']
my_collections = mongo_db['guazi_collections']
if '正在打开中,请稍后' in response.text:
    #表示203页面
    p = re.compile(r"anti\('(.*?)','(.*?)'\);")
    value_search = p.search(response.text)
    string = value_search.group(1)
    key = value_search.group(2)
    with open('guazi.js','r',encoding='utf-8') as f:
        js_read = f.read()
    js = execjs.compile(js_read)
    js_return = js.call('anti',string,key)
    cookie_value = 'antipas='+js_return
    header['Cookie'] = cookie_value
    response_second = requests.get(url,headers=header)
    response_second.encoding = 'utf-8'

    response_second_str = response_second.text
    #爬取城市
    city_p = re.compile(r'{"id":\d*,"domain":"(.*?)","name":"(.*?)","firstC":".*?","active":.*?}')
    #爬取品牌
    brand_p = re.compile(r'<a data-gzlog=tracking_type=click&eventid=92458035&filter=brand&brand=.*?\s+href="/.*?\/(.*?)\/.*?/#bread"\s+>(.*?)</a>')
    city_list = city_p.findall(response_second_str)
    brand_list = brand_p.findall(response_second_str)
    for city in city_list:
        mongo_insert_list = []
        for brand in brand_list:
            #https://www.guazi.com/anji/dazhong/#bread
            city_name = city[1].encode('utf-8').decode('unicode_escape')
            city_code = city[0]
            brand_name = brand[1]
            brand_code = brand[0]
            url = 'https://www.guazi.com/{}/{}/#bread'.format(city_code,brand_code)
            info = {'city_name':city_name,
                    'brand_name':brand_name,
                    'url':url}
            mongo_insert_list.append(info)
            print(info)
        #插入数据库
        # my_collections.insert_many(mongo_insert_list)


