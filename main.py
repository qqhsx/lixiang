import requests
from bs4 import BeautifulSoup
import os

# 从环境变量中获取用户名和密码
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

# 登录和签到的URL
login_url = 'https://www.55188.com/member.php?mod=logging&action=login'
sign_url = 'https://www.55188.com/plugin.php?id=sign&mod=add&jump=1'

# 创建会话对象
session = requests.Session()

# 登录的表单数据
login_data = {
    'username': username,
    'password': password,
    'formhash': '',  # 需要动态获取
    'referer': 'https://www.55188.com/',
}

# 模拟登录，获取登录的formhash


def get_formhash():
    url = "https://www.55188.com/"  # 请确认这个 URL 是你要提取 formhash 的页面
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查状态码是否为 200
    except Exception as e:
        print("请求页面失败：", e)
        return None

    # 打印页面源码，用于调试（可以暂时注释掉）
    print("页面内容如下（前1000字）:")
    print(response.text[:1000])

    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find('input', {'name': 'formhash'})
    if tag:
        formhash = tag['value']
        print("成功提取 formhash:", formhash)
        return formhash
    else:
        print("❌ 页面中未找到 formhash，请检查页面结构是否改变，或是否被重定向。")
        return None


# 登录函数
def login():
    login_data['formhash'] = get_formhash()  # 更新formhash
    response = session.post(login_url, data=login_data)
    if '欢迎回来' in response.text:  # 登录成功后页面中的欢迎文本
        print('登录成功！')
    else:
        print('登录失败！')

# 签到函数
def sign_in():
    # 获取表单数据
    sign_response = session.get(sign_url)
    if '签到成功' in sign_response.text:
        print('签到成功！')
    elif '已签到' in sign_response.text:
        print('您今天已经签到！')
    else:
        print('签到失败！')

# 主函数
def main():
    login()
    sign_in()

if __name__ == "__main__":
    main()
