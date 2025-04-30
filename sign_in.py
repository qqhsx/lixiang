import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 签到页面 URL
SIGN_URL = 'https://www.55188.com/plugin.php?id=sign&mod=add&jump=1'

# 替换为你自己的 Cookie
cookies = {
    'cookie': '55188_passport=jse99w68FdRbdClAGKT1ytAM6UVFVc1lR7BjKZVM5vllqvo2KE6miQl8fr8%2FULW78CgXilkvXUX7W5mfB6vAvb0QBwQnGLgMKgbWgE%2Fc9W9eKYydp3jO5EXTim2KREloPpsUszyYWY6OHhPlXSQQYMRzu0xKMdco1lCjcnF6jMk%3D; passport2bbs=oKvtgy64BAAkWOBWuQxg04JPI2xzUdnlvXXMNIHPFRqlVpBlMROVZFvxoGtBsuWb; cdb2_auth=2Cqu1WSfVNNHetdTv03Y2GnwxQN8%2F5RaXlSphRuFc6RnSHUFF%2BuxUjq%2BVuCuq641Iw; vOVx_56cc_saltkey=f115JJ4C; vOVx_56cc_lastvisit=1745976203; vOVx_56cc_auth=2751al30XL9yHoNpMIhs0R8BKUSxv9nyXtDDM8nIUDOQAIdeQoUoWHpkPiSrZF36nW6ebtSNgLjjOqbH1JzUksoUiZk%2F; vOVx_56cc_sid=aTUDja; vOVx_56cc_yfe_in=1; vOVx_56cc_pc_size_c=0; vOVx_56cc_ulastactivity=6fc8my1SlIRI%2BYycF8xA73K%2BTgQUxRjP2wXDjZ%2FvLljLF8iLZ9Xa; vOVx_56cc_atarget=1; vOVx_56cc_visitedfid=68; vOVx_56cc_forum_lastvisit=D_68_1745980098; vOVx_56cc_checkpm=1; vOVx_56cc_lastcheckfeed=4016791%7C1745981067; vOVx_56cc_checkfollow=1; vOVx_56cc_lastact=1745981067%09home.php%09misc; vOVx_56cc_sendmail=1',
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
