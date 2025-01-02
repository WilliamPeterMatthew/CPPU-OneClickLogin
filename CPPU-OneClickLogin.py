import requests
from random import randrange
from urllib.parse import quote
f=open('账号密码.txt','r+')
data={
    'callback':'dr1004',
    'DDDDD':f.readline()[:-1],
    'upass':f.readline()[:-1],
    '0MKKey':'123456',
    'R1':'0',
    'R3':'0',
    'R6':'0',
    'para':'00',
    'v6ip':'',
    'v':str(randrange(1000,9999))}
header={
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'DNT':'1',
    'Host':'192.168.9.18',
    'Referer':'http://192.168.9.18/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
url = 'http://192.168.9.18/drcom/login?callback=dr1004&DDDDD='+quote(data['DDDDD'])+'&upass='+quote(data['upass'])+'&0MKKey=&R1=0&R3=0&R6=0&para=00&v6ip=&v=6901'
response = requests.post(url,data=data,headers=header)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else ''
    if title == "信息页":
        print("连接失败，账号或密码不正确")
        input('请按回车键（Enter）结束。')
    elif title == "认证成功页":
        print('已连接（Code:200）')
    else:
        print("未知状态，title不是预期的值")
        input('请按回车键（Enter）结束。')
else:
    print('连接失败（Code:{}）'.format(response.status_code))
    input('请按回车键（Enter）结束。')
