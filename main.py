import requests
import os

# 从环境变量中获取 cookies
cookies_string = os.getenv('COOKIES')

# 将字符串转换为字典（假设 cookies 是以 `key=value` 格式存储的）
cookies = {}
if cookies_string:
    cookie_items = cookies_string.split(';')
    for item in cookie_items:
        key, value = item.split('=', 1)
        cookies[key.strip()] = value.strip()

# 创建会话对象
session = requests.Session()

# 使用 cookies 登录
def login_with_cookies():
    if not cookies:
        print('Cookies 未提供或格式错误！')
        return

    session.cookies.update(cookies)  # 将 cookie 添加到 session 中

    # 通过一个请求检查是否登录成功
    response = session.get('https://www.55188.com/')
    if '欢迎回来' in response.text:  # 登录成功后页面中的欢迎文本
        print('通过 Cookies 登录成功！')
    else:
        print('Cookies 登录失败！')

# 签到函数
def sign_in():
    sign_response = session.get('https://www.55188.com/plugin.php?id=sign&mod=add&jump=1')
    if '签到成功' in sign_response.text:
        print('签到成功！')
    elif '已签到' in sign_response.text:
        print('您今天已经签到！')
    else:
        print('签到失败！')

# 主函数
def main():
    login_with_cookies()  # 使用 cookies 登录
    sign_in()  # 执行签到操作

if __name__ == "__main__":
    main()
