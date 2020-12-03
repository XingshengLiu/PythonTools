# @File  : decryptorUtil.py
# @Author: LiuXingsheng
# @Date  : 2020/10/28
# @Desc  :
import json
import jpype
from jpype import shutdownJVM

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

# 单个id解密
def decryption_Qid(str):
    id = jar.decrypt(str, "eeBBK@52")
    return id

# 解密首屏ID
def decryption_Q(list):
    for i in list:
        # print(i)
        question = jar.decrypt(i, "eeBBK@DES\\123encrypt.que")
        question = json.loads(str(question))
        return question


if __name__ == '__main__':
    ids = [
        "DAO6lzuE494k0p34g96CKg==",
        "S7y30sB5NYjeIV6oH/cVXA==",
        "Fs42GRPe0oZ8f4viy1e2hg==",
        "44Q0Jh6MbuXlG1h6b/wjBQ=="
    ]
    print(decryption_Qids(ids))
    releaseJVM()
    numlist = [1,2,3]