# @File  : DESCoder.py
# @Author: LiuXingsheng
# @Date  : 2020/12/21
# @Desc  : DES加解密工具
import json
from pyDes import des,PAD_PKCS5,ECB
import base64

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

# 单个id解密 python版本
def decryption_Qid_py(str):
    id = decrypt_py(str, "eeBBK@52")
    return id

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
    print(decryption_Qids_py(ids))
