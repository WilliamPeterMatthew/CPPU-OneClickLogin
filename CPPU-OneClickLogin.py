import sys
import os
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def load_credentials():
    try:
        with open(resource_path('账号密码.txt'), 'r', encoding='utf-8') as f:
            return f.readline().strip(), f.readline().strip()
    except Exception as e:
        print(f"读取凭证文件失败: {str(e)}")
        input('请按回车键（Enter）结束。')
        sys.exit(1)

def perform_login(username, password):
    params = {
        'callback': 'dr1004',
        'DDDDD': username,
        'upass': password,
        '0MKKey': '123456',
        'R1': '0',
        'R3': '0',
        'R6': '0',
        'para': '00',
        'v6ip': '',
        'v': generate_random(4)
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.post(
            'http://192.168.9.18/drcom/login',
            params=params,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()
        return parse_response(response)
    except requests.RequestException as e:
        return ("错误", f"网络请求失败: {str(e)}")

def generate_random(length):
    return str(int.from_bytes(os.urandom(length), byteorder='big'))[:length]

def parse_response(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else ''
    
    status_mapping = {
        "信息页": ("错误", "连接失败，账号或密码不正确"),
        "认证成功页": ("成功", "已连接（Code:200）")
    }
    
    return status_mapping.get(title, ("错误", f"未知响应状态（Title: {title}）"))

def main():
    username, password = load_credentials()
    if not username or not password:
        print("账号或密码为空，程序退出。")
        input('请按回车键（Enter）结束。')
        return
    
    status, message = perform_login(username, password)
    print(f"[{status}] {message}")
    if status == "错误":
        input('请按回车键（Enter）结束。')

if __name__ == "__main__":
    main()
