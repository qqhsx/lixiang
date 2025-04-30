import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 签到页面 URL
SIGN_URL = 'https://www.55188.com/plugin.php?id=sign&mod=add&jump=1'

# 用户的 cookie 信息（从浏览器复制填入）
cookies = {
    'cookie': '55188_passport=jse99w68FdRbdClAGKT1ytAM6UVFVc1lR7BjKZVM5vllqvo2KE6miQl8fr8%2FULW78CgXilkvXUX7W5mfB6vAvb0QBwQnGLgMKgbWgE%2Fc9W9eKYydp3jO5EXTim2KREloPpsUszyYWY6OHhPlXSQQYMRzu0xKMdco1lCjcnF6jMk%3D; passport2bbs=oKvtgy64BAAkWOBWuQxg04JPI2xzUdnlvXXMNIHPFRqlVpBlMROVZFvxoGtBsuWb; cdb2_auth=2Cqu1WSfVNNHetdTv03Y2GnwxQN8%2F5RaXlSphRuFc6RnSHUFF%2BuxUjq%2BVuCuq641Iw; vOVx_56cc_saltkey=f115JJ4C; vOVx_56cc_lastvisit=1745976203; vOVx_56cc_auth=2751al30XL9yHoNpMIhs0R8BKUSxv9nyXtDDM8nIUDOQAIdeQoUoWHpkPiSrZF36nW6ebtSNgLjjOqbH1JzUksoUiZk%2F; vOVx_56cc_sid=aTUDja; vOVx_56cc_yfe_in=1; vOVx_56cc_pc_size_c=0; vOVx_56cc_ulastactivity=6fc8my1SlIRI%2BYycF8xA73K%2BTgQUxRjP2wXDjZ%2FvLljLF8iLZ9Xa; vOVx_56cc_atarget=1; vOVx_56cc_visitedfid=68; vOVx_56cc_forum_lastvisit=D_68_1745980098; vOVx_56cc_checkpm=1; vOVx_56cc_lastcheckfeed=4016791%7C1745981067; vOVx_56cc_checkfollow=1; vOVx_56cc_lastact=1745981067%09home.php%09misc; vOVx_56cc_sendmail=1'  # 请替换为你自己的 Cookie
}

# 获取当前日期（仅用于打印）
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

# 检查是否已经签到
def check_if_signed(session):
    response = session.get(SIGN_URL, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    visited_btn = soup.find('a', {'class': 'btn btnvisted'})
    if visited_btn:
        return True
    return False

# 执行签到操作
def sign_in(session):
    response = session.get(SIGN_URL, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    addsign = soup.find('a', {'id': 'addsign'})
    if addsign and 'href' in addsign.attrs:
        sign_href = addsign['href']
        sign_url = 'https://www.55188.com/' + sign_href.replace('&amp;', '&')

        # 模拟点击签到链接
        response = session.get(sign_url, cookies=cookies)
        if '签到成功' in response.text or '签到排名' in response.text:
            print("签到成功！")
        else:
            print("签到失败，未发现成功提示。")
    else:
        print("今天已经签到过了或找不到签到按钮。")

# 主程序逻辑
def main():
    with requests.Session() as session:
        print(f"尝试在 {get_current_date()} 签到...")

        if not check_if_signed(session):
            sign_in(session)
        else:
            print("今天已经签到过了。")

if __name__ == "__main__":
    main()
