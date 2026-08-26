import os
import requests
from bs4 import BeautifulSoup
import urllib3

# SSL 보안 무시 경고창 숨기기
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 깃허브 비밀 금고(Secrets)에서 토큰과 ID를 몰래 꺼내옴!
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

URL = "https://ameyokovip.com/shop/item.php?it_id=1783341800"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def send_telegram_msg(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': msg}
    requests.post(url, data=data)

def check_stock():
    try:
        response = requests.get(URL, headers=HEADERS, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        target_element = soup.select_one('#sit_ov_soldout, .sit_ov_soldout')
        
        # 품절 버튼이 안 보이면 재고가 있는 것!
        if target_element is None:
            return True
        return False
    except Exception:
        return False

# 깃허브가 이 파일을 실행하면 딱 한 번만 찔러보고 퇴근함
if __name__ == "__main__":
    if check_stock():
        send_telegram_msg(f"🚨 재고 들어옴!! 당장 결제 갈겨!!\n바로가기: {URL}")
    else:
        print("아직 품절 상태...")
