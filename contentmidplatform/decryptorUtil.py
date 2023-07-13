# @File  : decryptorUtil.py
# @Author: LiuXingsheng
# @Date  : 2020/10/28
# @Desc  :
import json
import jpype
from jpype import shutdownJVM
from pyDes import des,PAD_PKCS5,ECB
import base64

jarpath = (r'1.3.3_encrypt.jar')
jpype.startJVM(r'D:\JDK18\jre\bin\server\jvm.dll', "-ea",
               "-Djava.class.path=%s" % jarpath)  # 当有依赖的JAR包存在时，一定要使用-Djava.ext.dirs参数进行引入
jar = jpype.JClass(r"com.eebbk.encrypt.base.algorithm.DESCoder")

def releaseJVM():
    shutdownJVM()

# 解密后四屏幕ID
def decryption_Qids(list):
    all_id = []
    for i in list:
        if i == 'xiaoyuanID':
            id = 'xiaoyuan'
        else:
            id = jar.decrypt(i, "eeBBK@52")
        all_id = all_id + [id]
    return all_id

# 解密后四屏幕ID python版本
def decryption_Qids_py(questionlist):
    all_id = []
    for question in questionlist:
        if question == 'xiaoyuanID':
            id = 'xiaoyuan'
        else:
            id = decrypt_py(question,"eeBBK@52")
        all_id = all_id + [id]
    return all_id

# 单个id解密
def decryption_Qid(str):
    id = jar.decrypt(str, "eeBBK@52")
    return id

# 单个id解密 python版本
def decryption_Qid_py(str):
    id = decrypt_py(str, "eeBBK@52")
    return id

# 解密首屏ID
def decryption_Q(list):
    for i in list:
        # print(i)
        question = jar.decrypt(i, "eeBBK@DES\\123encrypt.que")
        question = json.loads(str(question))
        return question

# 解密首屏ID python 版本
def decryption_Q_py(questionlist):
    for question in questionlist:
        question = decrypt_py(question, "eeBBK@DE")
        questionobj = json.loads(str(question))
        return questionobj

# des解密方法 python 版本
def decrypt_py(data,secretkey):
    des_obj = des(secretkey, ECB, secretkey, padmode=PAD_PKCS5)
    decodebs64data = base64.b64decode(data)
    return des_obj.decrypt(decodebs64data).decode('utf-8')


if __name__ == '__main__':
    ids = [
        "DAO6lzuE494k0p34g96CKg==",
        "S7y30sB5NYjeIV6oH/cVXA==",
        "Fs42GRPe0oZ8f4viy1e2hg==",
        "44Q0Jh6MbuXlG1h6b/wjBQ=="
    ]
    print(decryption_Qids(ids))
    releaseJVM()
    # numlist = [1,2,3]
    des_key = 'eeBBK@52'
    des_obj = des(des_key,ECB,des_key,padmode=PAD_PKCS5)
    decodedata = base64.b64decode("DAO6lzuE494k0p34g96CKg==")
    decodedata1 = base64.b64decode("S7y30sB5NYjeIV6oH/cVXA==")
    decodedata2 = base64.b64decode("Fs42GRPe0oZ8f4viy1e2hg==")
    decodedata3 = base64.b64decode("44Q0Jh6MbuXlG1h6b/wjBQ==")
    s = des_obj.decrypt(decodedata)
    s1 = des_obj.decrypt(decodedata1)
    s2 = des_obj.decrypt(decodedata2)
    s3 = des_obj.decrypt(decodedata3)
    print(s,s1,s2,s3)