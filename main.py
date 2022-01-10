#                     ！！！注意！！！

# 本项目（yibanAutocheakin）涉及的任何代码，仅供学习测试研究，禁止用于商业用途

# !!!!!!!!!!!!!!!!!!!!特别注意!!!!!!!!!!!!!!!!!!!!
# 如果出现发热、干咳、体寒、体不适、胸痛、鼻塞、流鼻涕、恶心、腹泻等症状。
# 请立即停止使用本项目（yibanAutocheakin），认真实履行社会义务，及时进行健康申报。
# !!!!!!!!!!!!!!!!!!!!特别注意!!!!!!!!!!!!!!!!!!!!

# 如有侵权，请提供相关证明，所有权证明，本人收到后删除相关文件。

# 无论以任何方式查看、复制或使用到本项目（yibanAutocheakin）中的任何脚本，都应该仔细阅读此声明。本人保留随时更改或补充的此免责声明的权利。

# 一旦使用并复制了本项目（yibanAutocheakin）的任何相关脚本，则默认视为您已经接受了此免责声明。

# 使用并复制了本项目（yibanAutocheakin）的任何相关脚本或本人制作的任何脚本，则默认视为您已经接受了此免责声明。请仔细阅读

# 运行要求：python3.6.4 ， requests库

# 使用方法————修改完成且正确后可选择：服务器shell脚本执行.py文件、Windows计划任务执行.py文件、每日手动执行

# 建议凌晨00：00开始执行

# 功能说明————自动进行易班打卡签到，签到间隔可由jiange()函数中的内容控制


#                     ！！！注意！！！
# 本代码中的每一处注释都有非常重要的意义，按注释操作绝对可以正常使用（截至2022年1月11日）
#                     ！！！注意！！！

import requests    # request库需另外安装，安装方法建议百度，不再赘述
import os
import json
import time
from threading import Thread


def jiange():
    time.sleep(10800)   # （）中的是签到成功后再次签到所间隔的秒数

class KSClient(object):

    # 经开发者测试，由于签到需要验证码，而验证码的识别难度又非常高，一般的图像处理后识别的方法很难实现正确读取
    # 为此开发者甚至通过卷积神经网络运算，跑了10万张验证码，训练了识别模型，可成功率依然有限
    # 故借用识别平台，该平台每天有20次免费识别机会，个人使用绰绰有余
    #  平台地址———— http://fast.net885.com/ 点左下角立即注册，注册完成后在下边各处填入用户名和密码，平台很便宜
    # ！！！在签到主函数中也有一处用户名和密码，千万别忘记填！！！
    # ！！！！！！！！！这不是识别平台的广告！！！！！！！！！！！

    def __init__(self):
        self.username = 'username'   # ''中填用户名

        self.Token = ''   # 不管

        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    # 获取taken
    def GetTaken(self, username, password):   # （self，用户名，密码）依次填入用户名和密码
        brtn = False
        r = requests.get('http://api.95man.com:8888/api/Http/UserTaken?user=' + username + '&pwd=' + password + '&isref=0',
                         headers=self.headers)   # 第一个加号后填用户名，第三个加号后填密码
        arrstr = r.text.split('|')
        if (arrstr[0] == '1'):
            self.username = username   # 等号后填用户名
            self.Token = arrstr[1]
            brtn = True
        return brtn

    # 识别图片
    def PostPic(self, filepath, codetype):
        """
        imbyte: 图片字节
        imgtype: 类型 1为通用类型 更多精准类型请参考 http://fast.net885.com/auth/main.html
        """
        strRtn = ''
        imbyte = open(filepath, 'rb').read()
        filename = os.path.basename(filepath)

        files = {'imgfile': (filename, imbyte)}
        r = requests.post(
            'http://api.95man.com:8888/api/Http/Recog?Taken=' + self.Token + '&imgtype=' + str(codetype) + '&len=0',
            files=files, headers=self.headers)
        arrstr = r.text.split('|')
        # 返回格式：识别ID|识别结果|用户余额
        if (int(arrstr[0]) > 0):
            strRtn = arrstr[1]

        return strRtn


def qiandao(hbnd, hbndt):   # 主签到函数
    global wdnmd
    s = requests.Session()
    Ks95man = KSClient()
    code = None
    web = "http://211.68.191.30/epidemic/index?token=%s" % (hbnd)
    r = s.get(web)
    r = s.get("http://211.68.191.30/epidemic/captcha")
    with open("1.png", "wb+") as f:
        f.write(r.content)
        f.close()
    if Ks95man.GetTaken('username', 'password'):   # 按（用户名，密码）的格式依次填入
        code = Ks95man.PostPic('1.png', 1)
    sign_content = hbndt
    dat = {"data": sign_content, "captcha": code}
    r = s.post("http://211.68.191.30/epidemic/student/sign", data=dat)
    text = json.loads(r.text)
    print(text)
    try:
        nmd = text["code"]
    except:
        rnm = text["status"]
        if (rnm) == 500:
            cnm = 0
            while (cnm) < 10:
                print(cnm)
                chongshi(hbnd, hbndt)
                if (wdnmd) == 1:
                    jiange()
                    qiandao(hbnd, hbndt)
                else:
                    cnm = cnm + 1
                    time.sleep(5)
            else:
                print("签到失败")
                tongzhi("签到失败")   # 调用通知函数，并发送（）中的内容
    else:
        print(nmd)
        if (nmd) == -1:
            time.sleep(1)
            qiandao(hbnd, hbndt)
        else:
            jiange()
            qiandao(hbnd, hbndt)


def chongshi(hbnd, hbndt):    # 失败重试函数
    global wdnmd
    s = requests.Session()
    Ks95man = KSClient()
    code = None
    web = "http://211.68.191.30/epidemic/index?token=%s" % (hbnd)
    r = s.get(web)
    r = s.get("http://211.68.191.30/epidemic/captcha")
    with open("1.png", "wb+") as f:
        f.write(r.content)
        f.close()
    if Ks95man.GetTaken('zwxym', 'zhao0427'):
        code = Ks95man.PostPic('1.png', 1)
    sign_content = hbndt
    dat = {"data": sign_content, "captcha": code}
    r = s.post("http://211.68.191.30/epidemic/student/sign", data=dat)
    text = json.loads(r.text)
    try:
        nmd = text["code"]
    except:
        wdnmd = 0
    else:
        wdnmd = 1


def tongzhi(text):   # 通知函数
    key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 百度搜”server酱“用微信扫码登录后获取一个key，粘贴到这里
    url = "https://sctapi.ftqq.com/%s.send" % (key)
    title = u"通知"    # 通知标题，可自定义
    content = text    # 通知内容修改qiandao（）函数中，130行tongzhi（）括号中的内容即可
    data = {"text": title, "desp": content}
    requests.post(url, data)


def main():
    global nmd
    global code
    global rnm
    global cnm
    global wdnmd
    global hbnd
    global hbndt
    global xxx       # 这个变量名可以自己换
    xxx = ""         # 此处填写的是你的 token
    #                         获取方法
    # 你的签到token，获取方法：进入“易办大厅”点右上角三点，再点复制链接，将链接发送到电脑，复制到chrome浏览器打开
    # 右击页面，点击检查，点击右侧区域上边一排选项中的“网络”，再在左侧页面中点击“疫情放控签到”
    # 此时左侧会出现一些网址，当中的第一个是一个包含了token的链接，复制链接，留下“token=“后变的内容
    # 并将该内容粘贴于上方双引号中，完成token配置
    #                     ！！！注意！！！
    # token不是一成不变的，会不定时重置，本程序还不能实现自动跟随重置
    # 故当收到server酱通知时，请首先检查token是否发生更改
    # 方法是——登录对应账号的，查看进入易办大厅时，查看是否需要重新授权，如需要，请重复上述获取token的操作
    # 如您有一定的渗透基础，有抓包经验，麻烦您将授权过程的抓包结果发送至 learnzhao@yzui.onmicrosoft.com ，帮助开发者完成易班第三方网站verify_request的获取
    # 如您没有基础，麻烦您在授权页面右上角点击复制链接，并将此链接发送至 learnzhao@yzui.onmicrosoft.com ，帮助开发者完成易班第三方网站verify_request的获取
    #                     !谢谢各位的支持!
    xxxt = '''{
                "realName":"你的名字————例：”大猛子“",
                "collegeName":"你的学院全称————例：”城乡建设学院“",
                "className":"你的专业全程和班级如————例：”土木工程1701“",
                "studentId":"你的学号————例”没有例“",
                "answer":
                        "{
                           \\"q1\\":\\"是\\",
                           \\"q2\\":\\"是\\",
                           \\"q3\\":\\"是\\",
                           \\"q4\\":\\"是\\",
                           \\"q4_1\\":\\"\\",
                           \\"q5\\":\\"是\\",
                           \\"q6\\":\\"是\\",
                           \\"q6_1\\":\\"\\",
                           \\"position\\":\\"你的地址\\ "
                        }"
                }'''
    #                     ！！！注意！！！
    # 上边四项需要根据签到者的实际信息来填写，一定要填写在" "之间，删掉例子，在" "中间填写。
    # answer中的内容只要签到页面不改，就不会失效，需要注意的是最后的地址，删掉”你的地址“，在"后填写你的住址
    # 如果签到内容发生变化，可参照获取token的那个办法，复制易办大厅的地址后，进入”疫情防控签到页面“，再点击签到按键，进入签到页面，再右击检查
    # 自行查看源码中的各个”q“（问题）是否发生变化，根据网页内容，参照现有程序，增加或修改answer中的内容
    # 一般出问题都是签到增加了问题，就在位置行上变，仿照上文自行插入内容
    # 本开发者承诺本开源代码没有任何”后门“来获取同学们的个人信息
    # -------------------------------------------------------------------------------------------------------------------
    #                     ！！！注意！！！
    # 本开源程序采用”极为先进“的多线程方式，可并行运行多个任务，添加方式如下
    # 将第二个人的token填如下方”yyy“的""中
    # global yyy
    # yyy = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    # 将第二个人的信息与地址填到下方的”yyyt“中，地址在最后，第三个人的依次类推，切记要先定义全局变量——global xxx
    # global yyyt
    # yyyt = '''{"realName":"xx","collegeName":"xxxxxx","className":"xxxxxxxxx","studentId":"xxxxxxxxxxxxx","answer":"{\\"q1\\":\\"是\\",\\"q2\\":\\"是\\",\\"q3\\":\\"是\\",\\"q4\\":\\"是\\",\\"q4_1\\":\\"\\",\\"q5\\":\\"是\\",\\"q6\\":\\"是\\",\\"q6_1\\":\\"\\",\\"position\\":\\"xxxxxxxxxx\\"}"}'''
    # global zzz
    # zzz = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    # global zzzt
    # zzzt = '''{"realName":"xx","collegeName":"xxxxxxx","className":"xxxxxxxxx","studentId":"xxxxxxxxxxxxx","answer":"{\\"q1\\":\\"是\\",\\"q2\\":\\"是\\",\\"q3\\":\\"是\\",\\"q4\\":\\"是\\",\\"q4_1\\":\\"\\",\\"q5\\":\\"是\\",\\"q6\\":\\"是\\",\\"q6_1\\":\\"\\",\\"position\\":\\"xxxxxxxxx\\"}"}'''
    # ......
    t1 = Thread(target=qiandao, args=(xxx, xxxt,))  # 定义线程t1，线程任务为调用qiandao()函数，参数是xxx和xxxt,进行第一个人的签到
    # t2 = Thread(target=qiandao, args=(yyy,yyyt,)) # 定义线程t2，线程任务为调用qiandao()函数，进行第二个人的签到
    # t3 = Thread(target=qiandao, args=(zzz,zzzt,)) #定义线程t3，线程任务为调用qiandao()函数，进行第三个人的签到
    # ......
    t1.start()  # 开始运行t1线程,要签那个人的就运行那个线程
    # t2.start()
    # t3.start()
    # ......


if __name__ == "__main__":   #入口函数
    main()
