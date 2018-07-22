#coding=utf-8
#import urllib2
import requests
import json
import sqlite3
mesUrl='https://oapi.dingtalk.com/robot/send?access_token=718c7852eb9a0687f5559dc4503de013d523c5addf9fd3057eb1de4ba7be426f'

data={
     "msgtype": "text",
     "text": {
         "content": "2018学年新初一分班方案 ——校长办公室【详细内容请在学校网查看】"
     },
     "at": {
         "atMobiles": [
             ""
         ], 
         "isAtAll": True
     }
 }

headers = {
  'Content-Type': 'application/json',
  "Connection":"close"
}
r=requests.post(url=mesUrl,headers=headers, data=json.dumps(data))
print(r.text)