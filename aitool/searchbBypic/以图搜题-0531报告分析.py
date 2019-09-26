# -*- coding: utf-8 -*-
import json
import requests
import os.path
import shutil
# from PIL import Image
import os

# 从Python 2或3之一导入urlopen()

from aitool.searchbBypic import Pyutil
import xlsxwriter
import numpy as np
import time
import cv2
from bs4 import BeautifulSoup
from urllib.parse import quote
from tqdm import tqdm


def request_download(IMAGE_URL):
    import requests
    r = requests.get(IMAGE_URL)
    if r.content=="" or r.status_code !=requests.codes.ok :
        print("error")
        return ""
    return r.content

def search_img(img_url):
    with open(img_url, 'rb') as fin:
        data = fin.read()

    # search_api_url = 'http://113.108.235.182:8132/standardquestion/search/uploadFile'
    # search_api_url = 'http://113.108.235.182:8132/retrieval/esearch/uploadFile'
    # search_api_url = 'http://113.108.235.182:8132/retrieval/questionSearch/uploadFile'
    # search_api_url = "http://106.75.177.192:8181/retrieval/questionSearchonSearch/uploadFile"
    # search_api_url = 'http://localhost:7080/questionSearch/uploadFile'
    # search_api_url = 'http://picsearch.eebbk.net/retrieval/questionSearch/uploadFile'
    search_api_url = 'http://106.75.177.192:8181/retrieval/questionSearch/uploadFile'
    response = requests.post(search_api_url, data={'size': 5},
                  files={'file': data}, timeout=300000)

    if response.status_code != requests.codes.ok:
        raise Exception(response.status_code)

    result = response.content.decode('utf-8')
    response.close()

    return result

def request_get(Id):
    param={"questionId":Id}
    r=requests.get("http://test.eebbk.net/social-search/test/search/getQuestionDetailById",params=param)
    if r.status_code !=200:
        print(r.status_code,"error code")
        return ""
    js=json.loads(r.content)
    try:
        img_src_str=js["data"]["questionTitle"]
    except:
        print("error code")
        return ""


    xml=BeautifulSoup(img_src_str,)
    img_tag=xml.img
    link=[]
    try:
        for key,val in img_tag.attrs.items():
            if val.find("http:")>=0 and (val.lower().find("png")>0 or val.lower().find("jpg")>0 or val.lower().find("bpm")>0   ):
                if val not in link:
                    link.append(val)
    except:
        print("error link")
        return ""

    try:
        return link[0]   #多图情况只返回第一个
    except:
        return ""


# ################找出所有没有搜出的图片ID
Failed_pic_path=r"F:\DATA\以图搜题\badcase分析\错误"
error_id_txt=r"F:\DATA\以图搜题\badcase分析\error_id.txt"
error_log=r"F:\DATA\以图搜题\badcase分析\error_search.log"
pics= Pyutil.travel_dir(Failed_pic_path, "jpg", recursive=False)

all_identy=[]
all_time=[]

fp_log=open(error_log,"wt",encoding='utf-8')
for p in pics:
    start=time.time()
    Id=search_img(p)
    if len(Id[1:-1].split(","))<5 :
        print(p)
        fp_log.write(p+"\n")
        continue
    try:
        int(Id[1:-1].split(",")[0])
    except:
        print(p)
        fp_log.write(p+"\n")
        continue
    all_time.append(time.time()-start)
    all_identy.append(np.fromstring(os.path.split(p)[-1].split(".")[0]+","+Id[1:-1],dtype=np.int64,sep=","))
fp_log.close()

# all_identy=np.array(all_identy)
all_time=np.array(all_time,np.float)
print(np.mean(all_time))

# np.savetxt(error_id_txt,all_identy,)
with  open(error_id_txt,"wt",encoding='utf-8') as fp:
    for dd in all_identy:
        line=""
        for d in dd:
            line+=str(d)+" "
        line=line.strip(" ")
        line+='\n'
        fp.write(line)
#################找出所有ID图片


error_url_txt=r"F:\DATA\以图搜题\badcase分析\error_url.txt"
all_identy=[]

for line in open(error_id_txt,"rt",encoding='utf-8'):
    dd=line.strip().split(" ")
    all_identy.append(dd)

all_pic_url=[]
for id_row in all_identy:

    tmp_url=[]
    for id_col in id_row:
        url_t=request_get(id_col)
        tmp_url.append(url_t)
    all_pic_url.append(tmp_url)


with open(error_url_txt,"wt",encoding='utf-8') as fp:
    for id_row in all_pic_url:
        line=""
        for id_col in id_row:
            if id_col=="":
                line+="##\t"
            else:
                line+=id_col+"\t"
        line=line.strip("\t")+"\n"
        fp.write(line)

print("Url 分析 Done")

###################写入excel

all_pic_url=[]
for line in open(error_url_txt,"rt",encoding='utf-8'):
    id_row=line.strip("\n").split('\t')
    all_pic_url.append(id_row)

rows=len(all_pic_url)
cols=len(id_row)

print(rows, cols)


def wexcel(all_pic_url):
    rec_x = 60
    rec_y = 200
    excel_report = r"F:\DATA\以图搜题\badcase分析\Error_report_analyse_new.xls"

    new_dir=r"F:\DATA\以图搜题\badcase分析\new"
    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)
    os.mkdir(new_dir)

    # 写入excel
    workbook = xlsxwriter.Workbook(excel_report)
    # 工作页
    worksheet = workbook.add_worksheet('搜题图片展示')
    worksheet.set_tab_color('red')
    bold = workbook.add_format({
        'bold': 1,  # 字体加粗
        'fg_color': 'green',  # 单元格背景颜色
        'align': 'center',  # 对齐方式
        'valign': 'vcenter',  # 字体对齐方式
    })
    headings = ['用户图片', '题库图片', 'Top1图片', 'Top2图片', 'Top3图片', 'Top4图片', 'Top5图片', ]  # 设置表头
    worksheet.write_row(0,0, headings, bold,)  # 行插入操作

    worksheet.set_column(0, 7, rec_x)
    r = 1
    for id_row in tqdm(all_pic_url):
        worksheet.set_row(r, rec_y)

        #写入第一张本地图片
        user_pic=Failed_pic_path +"\\"+all_identy[r-1][0]+".jpg"
        img= Pyutil.cv_imread(user_pic)
        img=cv2.resize(img,(400,200))
        Pyutil.cv_imwrite(new_dir + "\\" + all_identy[r - 1][0] + ".jpg", img)
        # h, w, ch = img.shape
        # if h > rec_y:
        #     sacle_h = h / rec_y
        # else:
        #     sacle_h = rec_y / h
        # if w > rec_x:
        #     sacle_w = w / rec_x
        # else:
        #     sacle_w = rec_x / w

        worksheet.insert_image(row=r, col=0,filename=new_dir+"\\"+all_identy[r-1][0]+".jpg")

        #写入剩下6张网络图片
        c=1
        for  id_col in tqdm(id_row):
            if id_col=="##":
                c+=1
                continue
            # try:
            #     img_data=urlopen(quote(id_col,safe='/:?='),timeout=3000).read()
            # except:
            #     c+=1
            #     print(id_col,"找不到图片")
            #     continue
            img_data=request_download(quote(id_col,safe='/:?='))
            if len(img_data)<256:
                c+=1
                continue
            # image_data = BytesIO(img_data)
            try:
                img = cv2.imdecode(np.fromstring(img_data, dtype=np.uint8), cv2.IMREAD_COLOR)
                # h, w, ch = img.shape
            except:
                c+=1
                print("cv decode img error datalen={}".format(len(img_data)),id_col,)
                continue
            if img is None:
                c+=1
                print("cv decode img error datalen={}".format(len(img_data)),id_col,)
                continue
            img = cv2.resize(img, (400, 200))

            Pyutil.cv_imwrite(new_dir + "\\" + all_identy[r - 1][c - 1] + "{}_{}.jpg".format(r - 1, c - 1), img)

            # if h >rec_y:
            #     sacle_h = h / rec_y
            # else:
            #     sacle_h=rec_y/h
            # if w>rec_x:
            #     sacle_w = w / rec_x
            # else:
            #     sacle_w=rec_x/w
            worksheet.insert_image(row=r, col=c, filename=new_dir + "\\" + all_identy[r - 1][c-1] + "{}_{}.jpg".format(r-1,c-1), )
            c+=1
        r += 1

    workbook.close()


wexcel(all_pic_url)





if __name__=='__main__':

    pass

