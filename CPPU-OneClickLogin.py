import sys
import os
import requests
import ctypes
from bs4 import BeautifulSoup

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def is_gui_mode():
    return not sys.stdin or '--gui' in sys.argv

def show_error(message, is_gui):
    if is_gui:
        ctypes.windll.user32.MessageBoxW(0, message, "错误", 0x10)
    else:
        print(f"[错误] {message}")
        input('按回车键退出...')
    sys.exit(1)

def load_credentials():
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_path = os.path.join(script_dir, '账号密码.txt')
    
    if not os.path.exists(file_path):
        show_error("找不到账号密码.txt文件，请确保它与程序在同一目录", is_gui_mode())
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            username = f.readline().strip()
            password = f.readline().strip()
            if not username or not password:
                show_error("账号密码文件格式不正确，必须包含两行内容", is_gui_mode())
            return username, password
    except Exception as e:
        show_error(f"读取凭证文件失败: {str(e)}", is_gui_mode())

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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
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
    if is_gui_mode():
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    username, password = load_credentials()
    status, message = perform_login(username, password)
    
    if is_gui_mode():
        ctypes.windll.user32.MessageBoxW(0, message, status, 0x40)
    else:
        print(f"[{status}] {message}")
        if status == "错误":
            input('按回车键退出...')

if __name__ == "__main__":
    main()
