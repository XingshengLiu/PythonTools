# @File  : schedule_test.py
# @Author: LiuXingsheng
# @Date  : 2020/4/27
# @Desc  :

import requests
import schedule


def job():
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b7229b62-998f-4c24-a156-981aeaaa9d06'
    params = {'msgtype': 'news', "news": {
        "articles": [
            {
                "title": "又到了每天的日报时间了~",
                "description": "大家动起来",
                "url": "www.qq.com",
                "picurl": "http://file.eebbk.net/server-fileserve/cloudIDN/fileServer/2020/04/28/155804561_377994aabbe78089.png"
            }
        ]
    }}
    result = requests.post(url=url, json=params)
    print(result.text)


# schedule.every().monday.at("20:45").do(job)
schedule.every().tuesday.at("16:02").do(job)
# schedule.every().wednesday.at("20:45").do(job)
# schedule.every().thursday.at("20:45").do(job)
# schedule.every().friday.at("20:45").do(job)
# schedule.every().saturday.at("18:00").do(job)

# while True:
#     schedule.run_pending()



