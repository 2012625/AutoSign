import requests
import json
import time
import datetime
from bs4 import BeautifulSoup
import  base64
import execjs
from Crypto.Cipher import AES
print('请输入你的账号：',end='')
username = input()  # 账号
print('请输入你的密码：',end='')
passwd = input()  # 密码
ifhavesign = ''
# server酱推送
SCKEY = ''
name = ''  # 签到后老师那里显示的名字,空着的话就是默认
address = '火星'  # 地址
latitude = '32.2829260000'  # 纬度
longitude = '43.9237990000'  # 经度
picname = 'a.png'  # 同目录下的照片名字,如果不用就留空 picname='',不然会报错...
# 设置轮询间隔(单位:秒,建议不低于5)
speed = 6
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
coursedata = []
activeList = []
course_index = 0
status = 0
activates = []
a = 1
index = 0
transferKey ="u2oh6Vu^HWe40fj";
# 需要先将即将执行的代码块编译一下
compile_code = execjs.compile(open('./login.js', 'r', encoding='utf-8').read())

# 使用编译后的代码块call函数调用js文件中的函数
result = compile_code.call('encryptByDES',passwd,transferKey)


# python
# js=execjs.compile('''function encryptByDES(message, key){
# 	var keyHex = CryptoJS.enc.Utf8.parse(key);
# 	var encrypted = CryptoJS.DES.encrypt(message, keyHex, {
# 		mode: CryptoJS.mode.ECB,
# 		padding: CryptoJS.pad.Pkcs7
# 	});
# 	return encrypted.ciphertext.toString();
# }''')
# result=js.call('encryptByDes','293910xy',transferKey)
# print(result)
# mode = AES.MODE_ECB
# padding = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
# cryptos = AES.new(padding(transferKey.encode("utf-8")), mode)
# cipher_text = cryptos.encrypt('293910xy'.encode("utf-8"))
# print(cipher_text)

def login():
    url = 'http://passport2.chaoxing.com/fanyalogin'

    headers= {
        "Referer": "http://passport2.chaoxing.com/login?fid=&newversion=true&refer=http://i.chaoxing.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"
    }
    data ={
        "fid": -1,
        "uname": username,
        "password": result,
        "refer": "http%3A%2F%2Fi.chaoxing.com",
        "t": "true",
        "forbidotherlogin": 0,
        "validate": '',
        "doubleFactorLogin": 0,
        "independentId": 0,
    }
    response = requests.session().post(url,headers=headers,data=data)


    if response.status_code == 200:
        #soup = BeautifulSoup(response.text, 'lxml')
        #print(soup)
        pwd = requests.utils.dict_from_cookiejar(response.cookies)
        #print(pwd)
        return pwd
cookie = login()
uid = cookie['UID']

def token():  # 获取上传图片用的token
    url = 'https://pan-yz.chaoxing.com/api/token/uservalid'
    res = requests.get(url, headers=headers, cookies=cookie)
    tokendict = json.loads(res.text)
    return (tokendict['_token'])


def upload():  # 上传图片
    if picname.isspace() or len(picname) == 0:
        return
    else:
        url = 'https://pan-yz.chaoxing.com/upload'
        files = {'file': (picname, open(picname, 'rb'),
                          'image/webp,image/*',), }
        res = requests.post(url, data={'puid': uid, '_token': token(
        )}, files=files, headers=headers, cookies=cookie)
        resdict = json.loads(res.text)
        return (resdict['objectId'])


def taskactivelist(courseId, classId):  # 查找签到任务
    global a
    url="https://mobilelearn.chaoxing.com/widget/pcpick/stu/index?courseId="+str(courseId)+"&jclassId="+str(classId)
    #url = "https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist"
    #payload = {'courseId': str(courseId), 'classId': str(classId), 'uid': uid}
    #res = requests.get(url, params=payload, headers=headers, cookies=cookie)
    res = requests.get(url,cookies=cookie)
    respon = res.status_code
    if respon ==200:
        if(res.text.find('qd qdhover')!=-1) :
            print('有正在进行的签到活动，签到状态：',end='')
            global  ifhavesign
            activeid =''
            a = 2
            i = 1
            #print(res.text.find(',2,null'))
            No = res.text.find(',2,null')-13
            while (i<=13):
                activeid = activeid +res.text[No]
                No = No +1
                i = i+1
            if activeid!=ifhavesign:
                ifhavesign = activeid
                urls = 'https://mobilelearn.chaoxing.com/widget/sign/pcStuSignController/preSign?activeId='+activeid+'&classId='+str(classId)+'&fid=542&courseId='+str(courseId)
                signed = requests.get(urls,cookies=cookie)
                if signed.status_code ==200:
                    print('签到成功！')
            else:
                print('已经签到过了！！！')
    #print(soup)
    #print(respon)
    #if respon == 200:  # 网页状态码正常
        # data = json.loads(res.text)
        # activeList = data['activeList']  # 把所有任务提出来
        # print(data)
        # for item in activeList:
        #     if ("nameTwo" not in item):
        #         continue
        #     if (item['activeType'] == 2 and item['status'] == 1):  # 查找进行中的签到任务
        #         # signurl = item['url']  # 提取activePrimaryId
        #         aid = item['id']  # 提取activePrimaryId
        #         if (aid not in activates):  # 查看是否签到过
        #             print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        #                   '[签到]', coursedata[i]['name'], '查询到待签到活动 活动名称:%s 活动状态:%s 活动时间:%s aid:%s' % (
        #                   item['nameOne'], item['nameTwo'], item['nameFour'], aid))
        #             sign(aid, uid)  # 调用签到函数
        #             a = 2
    #else:
        #print('error', respon)  # 不知道为啥...


# def sign(aid, uid):  # 签到,偷了个懒,所有的签到类型都用这个,我测试下来貌似都没问题
#     global status, activates
#     url = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax"
#     objectId = upload()
#     data = {'name': name, 'address': address, 'activeId': aid, 'uid': uid,
#             'longitude': longitude, 'latitude': latitude, 'objectId': objectId}
#     res = requests.post(url, data=data, headers=headers, cookies=cookie)
#     push(SCKEY, res.text)
#     print("签到状态:", res.text)
#     activates.append(aid)
#     status = 2


def push(SCKEY, msg):
    if SCKEY.isspace() or len(SCKEY) == 0:
        return
    else:
        api = 'https://sc.ftqq.com/' + SCKEY + '.send'
        title = u"签到辣!"
        content = '课程: ' + coursedata[i]['name'] + '\n\n签到状态:' + msg
        data = {
            "text": title,
            "desp": content
        }
        req = requests.post(api, data=data)


url = "http://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1"
res = requests.get(url, headers=headers, cookies=cookie)
cdata = json.loads(res.text)
if (cdata['result'] != 1):
    print("课程列表获取失败")
for item in cdata['channelList']:
    if ("course" not in item['content']):
        continue
    pushdata = {}
    pushdata['courseid'] = item['content']['course']['data'][0]['id']
    pushdata['name'] = item['content']['course']['data'][0]['name']
    # pushdata['imageurl']=item['content']['course']['data'][0]['imageurl']
    pushdata['classid'] = item['content']['id']
    coursedata.append(pushdata)
print("获取成功:")

for item in coursedata:  # 打印课程
    print(str(index) + ".课程名称:" + item['name'])
    index += 1

while 1:
    for i in range(index):
        time.sleep(speed)  # 休眠
        taskactivelist(coursedata[i]['courseid'], coursedata[i]['classid'])
        if a == 2:
            a = 0
        else:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                  '[监控运行中]课程:', coursedata[i]['name'], '未查询到签到活动')
# import  requests
# url = "https://fanyi.baidu.com/#en/zh/"
# res = requests.post(url=url)
# i = 1
# while(1):
#     print(res.text[197032+i])
#     i = i +1
