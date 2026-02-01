import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def get_news():
    news_list = []
    
    # 1. Kaynak: BleepingComputer (Siber Güvenlik)
    try:
        r = requests.get("https://www.bleepingcomputer.com/", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Ana sayfadaki ilk 2 siber güvenlik haberini al
        cyber_news = soup.find_all('h4', limit=2)
        for n in cyber_news:
            news_list.append(f"🛡️ [Cyber]: {n.text.strip()}")
    except: pass

    # 2. Kaynak: HackerNoon (AI ve Yazılım)
    try:
        r = requests.get("https://hackernoon.com/tagged/ai", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        ai_news = soup.find_all('h2', limit=2)
        for n in ai_news:
            news_list.append(f"🤖 [AI/Dev]: {n.text.strip()}")
    except: pass

    # Sonuçları Kaydet
    date_str = datetime.now().strftime('%Y-%m-%d')
    content = f"--- {date_str} Teknoloji Gündemi ---\n\n"
    content += "\n".join(news_list) if news_list else "Haber bulunamadı, bağlantı kontrol edilmeli."
    
    if not os.path.exists('logs'): os.makedirs('logs')
    with open(f"logs/news_{date_str}.txt", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    get_news()
