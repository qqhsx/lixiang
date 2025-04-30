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

# 使用 cookies 登录
def login_with_cookies():
    # 提前设置 cookies，如果你已有登录时的 cookies，可以将其复制到这里
    cookies = {
        'cookie': '55188_passport=jse99w68FdRbdClAGKT1ytAM6UVFVc1lR7BjKZVM5vllqvo2KE6miQl8fr8%2FULW78CgXilkvXUX7W5mfB6vAvb0QBwQnGLgMKgbWgE%2Fc9W9eKYydp3jO5EXTim2KREloPpsUszyYWY6OHhPlXSQQYMRzu0xKMdco1lCjcnF6jMk%3D; passport2bbs=oKvtgy64BAAkWOBWuQxg04JPI2xzUdnlvXXMNIHPFRqlVpBlMROVZFvxoGtBsuWb; cdb2_auth=2Cqu1WSfVNNHetdTv03Y2GnwxQN8%2F5RaXlSphRuFc6RnSHUFF%2BuxUjq%2BVuCuq641Iw; vOVx_56cc_saltkey=f115JJ4C; vOVx_56cc_lastvisit=1745976203; vOVx_56cc_auth=2751al30XL9yHoNpMIhs0R8BKUSxv9nyXtDDM8nIUDOQAIdeQoUoWHpkPiSrZF36nW6ebtSNgLjjOqbH1JzUksoUiZk%2F; vOVx_56cc_yfe_in=1; vOVx_56cc_pc_size_c=0; vOVx_56cc_ulastactivity=6fc8my1SlIRI%2BYycF8xA73K%2BTgQUxRjP2wXDjZ%2FvLljLF8iLZ9Xa; vOVx_56cc_atarget=1; vOVx_56cc_visitedfid=68; vOVx_56cc_nofavfid=1; vOVx_56cc_cooNameAnse=1; vOVx_56cc_st_t=4016791%7C1745981811%7C293e39f6e418298b2c899a00353100db; vOVx_56cc_forum_lastvisit=D_68_1745981811; vOVx_56cc_plugin_sign_cookie=afd3cc475e5f97a27d6e9c29c6972c7f; vOVx_56cc_lastcheckfeed=4016791%7C1745982807; vOVx_56cc_sid=FZKK9R; vOVx_56cc_lip=59.61.207.78%2C1745984372; vOVx_56cc_lastact=1745984377%09forum.php%09guide',  # 在此替换为实际的 cookie 名称和值
        # 你可以从浏览器的开发者工具中获取实际的 cookie
    }
    session.cookies.update(cookies)  # 将 cookie 添加到 session 中

    # 通过一个请求检查是否登录成功
    response = session.get('https://www.55188.com/')
    if '欢迎回来' in response.text:  # 登录成功后页面中的欢迎文本
        print('通过 Cookies 登录成功！')
    else:
        print('Cookies 登录失败！')

# 签到函数
def sign_in():
    sign_response = session.get(sign_url)
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
