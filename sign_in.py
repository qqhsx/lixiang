import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 登录和签到的 URL
LOGIN_URL = 'https://www.55188.com/member.php?mod=logging&action=login'
SIGN_URL = 'https://www.55188.com/plugin.php?id=sign&mod=add&jump=1'

# 用户的 cookie 信息（你可以从浏览器的开发者工具中获取）
cookies = {
    'cookie': '55188_passport=jse99w68FdRbdClAGKT1ytAM6UVFVc1lR7BjKZVM5vllqvo2KE6miQl8fr8%2FULW78CgXilkvXUX7W5mfB6vAvb0QBwQnGLgMKgbWgE%2Fc9W9eKYydp3jO5EXTim2KREloPpsUszyYWY6OHhPlXSQQYMRzu0xKMdco1lCjcnF6jMk%3D; passport2bbs=oKvtgy64BAAkWOBWuQxg04JPI2xzUdnlvXXMNIHPFRqlVpBlMROVZFvxoGtBsuWb; cdb2_auth=2Cqu1WSfVNNHetdTv03Y2GnwxQN8%2F5RaXlSphRuFc6RnSHUFF%2BuxUjq%2BVuCuq641Iw; vOVx_56cc_saltkey=f115JJ4C; vOVx_56cc_lastvisit=1745976203; vOVx_56cc_auth=2751al30XL9yHoNpMIhs0R8BKUSxv9nyXtDDM8nIUDOQAIdeQoUoWHpkPiSrZF36nW6ebtSNgLjjOqbH1JzUksoUiZk%2F; vOVx_56cc_sid=aTUDja; vOVx_56cc_yfe_in=1; vOVx_56cc_pc_size_c=0; vOVx_56cc_ulastactivity=6fc8my1SlIRI%2BYycF8xA73K%2BTgQUxRjP2wXDjZ%2FvLljLF8iLZ9Xa; vOVx_56cc_atarget=1; vOVx_56cc_visitedfid=68; vOVx_56cc_forum_lastvisit=D_68_1745980098; vOVx_56cc_checkpm=1; vOVx_56cc_lastcheckfeed=4016791%7C1745981067; vOVx_56cc_checkfollow=1; vOVx_56cc_lastact=1745981067%09home.php%09misc; vOVx_56cc_sendmail=1',  # 用你的 cookie 替换这里
}

# 用来获取当前日期的函数
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

# 检查今天是否已经签到
def check_if_signed(session):
    response = session.get(SIGN_URL, cookies=cookies)
    if '您今天已经签到过了' in response.text:
        return True
    return False

# 执行签到操作
def sign_in(session):
    response = session.get(SIGN_URL, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 输出整个页面的 HTML 供调试
    print(soup.prettify())  # 可以打印出 HTML 内容看看页面是否有变化
    # 找到签到按钮并提交
    sign_button = soup.find('button', {'name': 'qiandao'})  # 这里的按钮可能需要根据网页结构调整
    if sign_button:
        response = session.post(SIGN_URL, cookies=cookies)
        if '签到成功' in response.text:
            print("签到成功！")
        else:
            print("签到失败")
    else:
        print("没有找到签到按钮")

# 主逻辑
def main():
    with requests.Session() as session:
        # 登录部分（如果需要额外的步骤，可以添加在这里）
        print(f"尝试在 {get_current_date()} 签到...")

        # 检查是否已经签到
        if not check_if_signed(session):
            sign_in(session)
        else:
            print("今天已经签到过了。")

# 运行主逻辑
if __name__ == "__main__":
    main()
