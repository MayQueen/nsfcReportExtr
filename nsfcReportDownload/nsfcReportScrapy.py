import requests,json,os,datetime
import urllib.request

rootWeb = "https://kd.nsfc.gov.cn"
# reportURL = "https://kd.nsfc.gov.cn/finalDetails?id=909b77c415424f932ea66f4c0551e13e"
reportURL = "https://kd.nsfc.gov.cn/finalDetails?id=4cb2524aebacf8db94002da1fcff9178"
APIurl="https://kd.nsfc.gov.cn/api/baseQuery/completeProjectReport" # 默认值
try:
    reportID = reportURL.split("?")[-1]
except:
    print("ERROR","请检查报告url是否有id关键字")
# print(reportID)

def gUrl(reportID):
    pngUrl=[]
    pageIndex = 1

    while True:
        # 获取img链接
        payload=reportID+"&"+"index="+str(pageIndex) 
        headers={'Content-Type':'application/x-www-form-urlencoded'}
        response=requests.request("POST",APIurl,headers=headers,data=payload)
        jsonRes = json.loads(response.text) # str数据转为json(dict)
        resUrl = jsonRes["data"]["url"]
        imgUrl = rootWeb+resUrl

        # 验证img链接是否有效
        try:
            imgRes = urllib.request.urlopen(imgUrl)
            print("INFO",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"正在获取...第%d页url"%(pageIndex))
        except Exception as err:
            print(err)
            break
        pageIndex += 1 # 循环获取报告全部页数
        pngUrl.append(imgUrl) # 保存img链接数据
    return pngUrl

def downloadPNG(imgUrl,i):
    # 创建png保存路径
    saveDir="./png"
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        print("INFO","创建文件夹")
    imgRes = urllib.request.urlopen(imgUrl)
    print("正在下载",i,imgUrl)
    with open(saveDir+"/%s.png"%(str(i)), 'wb') as f:
        f.write(imgRes.read()) # 保存图片

if __name__ == "__main__":
    res = gUrl(reportID)
    for ind,resU in enumerate(res):
        downloadPNG(resU,ind+1)