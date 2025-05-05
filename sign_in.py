import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import http.cookies

# 签到页面 URL
SIGN_URL = 'https://www.55188.com/plugin.php?id=sign&mod=add&jump=1'

# 浏览器请求头（模拟真实浏览器）
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Referer': 'https://www.55188.com/',
}

# 将 Cookie 字符串转换为 dict
def parse_cookie_string(cookie_string):
    cookie_jar = http.cookies.SimpleCookie()
    cookie_jar.load(cookie_string)
    return {key: morsel.value for key, morsel in cookie_jar.items()}

# 获取当前日期
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

# 检查是否已经签到
def check_if_signed(session, cookies):
    response = session.get(SIGN_URL, cookies=cookies, headers=HEADERS)

    print("请求 URL:", response.url)
    print("状态码:", response.status_code)

    if 'Access Denied' in response.text:
        print("❌ 访问被拒绝，可能是 Cookie 或 User-Agent 设置错误。")
        return None  # 特殊状态，表示无法确认

    soup = BeautifulSoup(response.text, 'html.parser')
    signed_message = soup.find('a', {'class': 'btn btnvisted'})
    return signed_message is not None

# 执行签到操作
def sign_in(session, cookies):
    response = session.get(SIGN_URL, cookies=cookies, headers=HEADERS)

    if '登录' in response.text or '请先登录' in response.text:
        print("❌ 登录失败，Cookie 可能已失效。")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    not_signed_message = soup.find('a', {'id': 'addsign'})

    if not_signed_message:
        sign_button = not_signed_message.get('href')
        sign_url = 'https://www.55188.com/' + sign_button
        post_response = session.get(sign_url, cookies=cookies, headers=HEADERS)

        if '签到成功' in post_response.text or '您的签到排名' in post_response.text:
            print("✅ 今天签到任务完成！")
        else:
            print("❌ 签到失败，未检测到成功提示。")
    else:
        print("✅ 您今天已经签到了，无需再次签到。")

# 主程序入口
def main():
    print(f"📅 尝试在 {get_current_date()} 签到...")

    raw_cookie = os.getenv('BBS_COOKIE')
    if not raw_cookie:
        print("❌ 未设置环境变量 BBS_COOKIE")
        return

    cookies = parse_cookie_string(raw_cookie)

    with requests.Session() as session:
        signed_status = check_if_signed(session, cookies)
        if signed_status is None:
            print("❌ 无法确定签到状态，程序退出。")
        elif signed_status:
            print("✅ 您今天已经签到过了，签到任务已完成。")
        else:
            sign_in(session, cookies)

if __name__ == "__main__":
    main()
