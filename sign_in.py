import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os


# 签到页面 URL
SIGN_URL = 'https://www.55188.com/plugin.php?id=sign&mod=add&jump=1'

# 替换为你自己的 Cookie
# cookies = {
#     'cookie': '',
# }
cookies = {
    'cookie': os.getenv('BBS_COOKIE'),  # 从环境变量读取 Cookie
}

# 获取当前日期
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

# 检查是否已经签到（根据页面结构判断是否显示“已签到”）
def check_if_signed(session):
    response = session.get(SIGN_URL, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找是否存在“已签到”标记
    signed_message = soup.find('a', {'class': 'btn btnvisted'})  # 已签到状态
    if signed_message:
        return True
    return False

# 执行签到操作
def sign_in(session):
    response = session.get(SIGN_URL, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 判断页面是否为登录失败，可能 Cookie 失效
    if '登录' in response.text or '请先登录' in response.text:
        print("登录失败，Cookie 可能已失效。")
        return
    
    # 判断是否今天已签到
    not_signed_message = soup.find('a', {'id': 'addsign'})  # 未签到状态
    if not_signed_message:
        # 签到按钮存在，说明可以签到
        sign_button = not_signed_message.get('href')
        sign_url = 'https://www.55188.com/' + sign_button
        post_response = session.get(sign_url, cookies=cookies)
        
        # 判断签到是否成功
        if '签到成功' in post_response.text or '您的签到排名' in post_response.text:
            print("今天签到任务完成！")
        else:
            print("签到失败，未检测到签到成功的提示。")
    else:
        # 已签到的情况
        print("您今天已经签到了，无需再次签到。")
        print(soup.prettify())  # 可选：调试时输出页面内容，帮助排查问题

# 主程序入口
def main():
    print(f"尝试在 {get_current_date()} 签到...")
    with requests.Session() as session:
        # 检查并执行签到
        if check_if_signed(session):
            print("您今天已经签到过了，签到任务已完成。")
        else:
            sign_in(session)

if __name__ == "__main__":
    main()
