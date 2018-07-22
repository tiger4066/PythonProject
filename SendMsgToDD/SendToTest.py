import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
url = 'http://lkzx.net/index_main.aspx?tabid=1'
UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"

header = {
    "User-Agent": UA,
    "Connection":"close" #加上这一行，解决：Failed to establish a new connection: [WinError 10048]
}
v2ex_session = requests.Session()
f = v2ex_session.get(url, headers=header)
'''
xpath方法获取值：对隐藏的不能用浏览器直接获取到xpath的效果不好

tree=etree.HTML(f.content)

nodes=tree.xpath('//*[@id="_ctl2_Btn_Login"]')[0].get('type')
print(nodes)
'''

'''BeautifulSoup方法获取值，不乱码效果正好，可能速度慢一些
soup = BeautifulSoup(f.content,"html.parser")
value = soup.find('input', {'id': '_ctl2_Btn_Login'}).get('value')
print(value)
'''
soup = BeautifulSoup(f.content, "html.parser")
# print(soup)
# 以下两种方法都可以获取到value的值
#value = soup.find('input', {'name': '__VIEWSTATE'})['value']
VIEWSTATE = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
UserName = '林文彪'
UserName = UserName.encode('gb2312')
Btn_Login = '登录'
Btn_Login = Btn_Login.encode('gb2312')
postData = {
    '__VIEWSTATE': VIEWSTATE,
    '_ctl2:Txt_UserName': UserName,
    '_ctl2:Txt_Password': '3874',
    '_ctl2:Btn_Login': Btn_Login,
    '_ctl8:Txt_Title': ''
}
v2ex_session.post(url,
                  data=postData,
                  headers=header)

txt = open('test.txt', 'w', encoding='GBK')
for p in range(1, 2):
    #url = 'http://www.lkzx.net/page/message/EN_MessageBox.aspx?pageindex=' + \
    #    str(p)+'&&action=getbox&&isdel=0'#我的信息列表
    url = 'http://www.lkzx.net/Page/Document/EN_DocumentMoreList.aspx?pageindex='+\
        str(p)+'&moduleid=138&tabid=12'#通知公告列表
    print(url)
    f = v2ex_session.get(url, headers=header)
    soup = BeautifulSoup(f.content, "html.parser")

# for i in soup.find_all(id=re.compile('_ctl1_DL_AnounceAdmi')):
# for i in soup.find_all(id=re.compile('_ctl1_DL_AnounceAdmin__ctl[1-9][0-9]?_Lbl_Title')):
    for i in soup.find_all(id=re.compile('_ctl0_DL_DocumentList__ctl[1-9][0-9]?_tr1')):
        # print(type(x))  <tr id="_ctl0_DL_DocumentList__ctl1_tr1
        i = i.decode()        
        #txt.write(i)
        pattern = re.compile(r'<span id.*?>(.*?)</span>.*?documentid=(.*?)\".*?title=\"(.*?)\".*?Lbl_ModuleName\">(.*?)</span>',re.S)
        items = re.findall(pattern, i)
        '''for item in items:
            print(item)'''
        for item in items:
            print(item[0],item[1],item[2],item[3])


# print(soup.get_text())
# print(f.text)

txt.close()

#向群机器人发送消息
#https://oapi.dingtalk.com/robot/send?access_token=718c7852eb9a0687f5559dc4503de013d523c5addf9fd3057eb1de4ba7be426f
mesUrl='https://oapi.dingtalk.com/robot/send?access_token=718c7852eb9a0687f5559dc4503de013d523c5addf9fd3057eb1de4ba7be426f'

data={
     "msgtype": "text",
     "text": {
         "content": "我就是我, 是不一样的烟火"
     },
     "at": {
         "atMobiles": [
             "18928686223"
         ], 
         "isAtAll": false
     }
 }
 r=requests.post(url=mesUrl,data=data)
 print(r.text)