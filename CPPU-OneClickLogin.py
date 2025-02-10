import sys
import os
import requests
import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.iconbitmap(resource_path("favicon.ico"))

    def show_message(self, title, message):
        messagebox.showinfo(title, message)
        self.destroy()

def load_credentials(app):
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_path = os.path.join(script_dir, '账号密码.txt')
    
    if not os.path.exists(file_path):
        app.show_message("错误", "找不到账号密码.txt文件")
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            username = f.readline().strip()
            password = f.readline().strip()
            if not username or not password:
                app.show_message("错误", "账号密码文件格式不正确")
                sys.exit(1)
            return username, password
    except Exception as e:
        app.show_message("错误", f"读取凭证失败: {str(e)}")
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
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
    app = App()
    
    try:
        username, password = load_credentials(app)
        status, message = perform_login(username, password)
        app.show_message(status, message)
    except Exception as e:
        app.show_message("错误", str(e))

if __name__ == "__main__":
    main()
