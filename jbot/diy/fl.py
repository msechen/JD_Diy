from telethon import events
from .. import jdbot, chat_id, JD_DIR, BOT_SET, ch_name
from urllib import parse
import requests, time, os, json, sys


def gettimestamp():
    return str(int(time.time() * 1000))


# 登录青龙 返回值 token
def get_qltoken(username, password):
    print("Token失效, 新登陆\n")
    url = "http://127.0.0.1:5700/api/login"
    payload = {'username': username, 'password': password}
    payload = json.dumps(payload)
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    try:
        res = requests.post(url=url, headers=headers, data=payload)
        token = json.loads(res.text)["data"]['token']
    except:
        print("青龙登录失败, 请检查面板状态!")
        sys.exit(1)
    else:
        return token


# 返回值 Token
def ql_login():
    path = '/ql/config/auth.json'
    if os.path.isfile(path):
        with open(path, "r") as file:
            auth = file.read()
            file.close()
        auth = json.loads(auth)
        username = auth["username"]
        password = auth["password"]
        token = auth["token"]
        if token == '':
            return get_qltoken(username, password)
        else:
            url = "http://127.0.0.1:5700/api/user"
            headers = {
                'Authorization':
                'Bearer {0}'.format(token),
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'
            }
            res = requests.get(url=url, headers=headers)
            if res.status_code == 200:
                return token
            else:
                return get_qltoken(username, password)
    else:
        print("没有发现auth文件, 你这是青龙吗???")
        sys.exit(0)


def search_ck1():
    token = ql_login()
    global s
    s = requests.session()
    s.headers.update({"authorization": "Bearer " + str(token)})
    s.headers.update({"Content-Type": "application/json;charset=UTF-8"})
    url = "http://127.0.0.1:5700/api/envs?searchValue=JD_COOKIE&t={}".format(
        gettimestamp())

    r = s.get(url).text
    ck1 = json.loads(r)['data'][0]['value']
    # print(ck1)
    return ck1


# 反利
@jdbot.on(events.NewMessage(chats=chat_id, pattern=r'^/fl'))
async def rebate_sku(event):
    # with open('cklist.txt', 'r', encoding='utf-8') as f:
    #     lines = f.readlines()
    #     ck1 = lines[0].rstrip("\n")
    ck1 = search_ck1()
    url = "https://api.m.jd.com/api?functionId=ConvertSuperLink&appid=u&_=1643900110941&body=%7B%22funName%22%3A%22getSuperClickUrl%22%2C%22param%22%3A%7B%22materialInfo%22%3A%22"
    url2 = "%7C%22%7D%2C%22unionId%22%3A2020618941%7D&loginType=2"
    payload = ""
    headers = {
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'Connection': 'keep-alive',
        'Cookie': ck1,
        'Host': 'api.m.jd.com',
        'Referer':
        'https://servicewechat.com/wxf463e50cd384beda/134/page-frame.html',
        'User-Agent':
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001023) NetType/WIFI Language/zh_CN',
        'content-type': 'application/json'
    }
    url1 = parse.quote_plus(event.text)
    urllist = url + url1 + url2
    try:
        response = requests.request("GET",
                                    urllist,
                                    headers=headers,
                                    data=payload)
        if response.json()['code'] == 200:
            if "skuName" in response.json()["data"]:
                skuname = "商品名称：" + str(response.json()["data"]["skuName"])
                promotionUrl = "返利链接：" + str(
                    response.json()["data"]["promotionUrl"])
                price = "抢购价：" + str(response.json()["data"]["price"]) + "元"
                wlCommission = "返利金额：" + str(
                    response.json()["data"]["wlCommission"]) + "元"
                wlCommissionShare = "返利比例：" + str(
                    response.json()["data"]["wlCommissionShare"]) + "%"
                result = skuname + '\n' + promotionUrl + '\n' + price + '\n' + wlCommission + '\n' + wlCommissionShare
                await jdbot.send_message(chat_id, result)
            else:
                formatContext = response.json()["data"]["formatContext"].split(
                    "抢购链接：")[1]
                await jdbot.send_message(chat_id, formatContext)
        else:
            await jdbot.send_message(chat_id, 'code错误，可能是因为商品不在返利中')
    except Exception as e:
        print(e)


if ch_name:
    jdbot.add_event_handler(
        rebate_sku,
        events.NewMessage(chats=chat_id, pattern=BOT_SET['命令别名']['fl']))