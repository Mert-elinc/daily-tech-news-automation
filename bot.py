import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def get_news():
    news_list = []
    headers = {'User-Agent': 'Mozilla/5.0'} # Siteye "ben bir tarayıcıyım" diyoruz

    # 1. Kaynak: BleepingComputer (Siber Güvenlik)
    try:
        r = requests.get("https://www.bleepingcomputer.com/", headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Sadece ana haber listesindeki h2 başlıklarını alıyoruz
        cyber_items = soup.find_all('h2', limit=5) 
        for n in cyber_items:
            title = n.text.strip()
            if len(title) > 20: # Kısa buton isimlerini (Giriş, Kayıt vb.) elemek için
                news_list.append(f"🛡️ [Siber Güvenlik]: {title}")
                if len([x for x in news_list if "🛡️" in x]) >= 2: break
    except: pass

    # 2. Kaynak: HackerNoon (Yapay Zeka)
    try:
        r = requests.get("https://hackernoon.com/tagged/ai", headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # HackerNoon'da haber başlıkları genellikle h2 içindeki linklerdedir
        ai_items = soup.find_all('h2', limit=10)
        count = 0
        for n in ai_items:
            title = n.text.strip()
            # "Açık Mod", "Karanlık Mod" gibi kelimeleri engelliyoruz
            if len(title) > 25 and "Mod" not in title:
                news_list.append(f"🤖 [Yapay Zeka]: {title}")
                count += 1
                if count >= 2: break
    except: pass

    # Sonuçları Kaydet
    date_str = datetime.now().strftime('%Y-%m-%d')
    content = f"--- {date_str} Teknoloji Gündemi ---\n\n"
    content += "\n".join(news_list) if news_list else "⚠️ Haberler çekilemedi, seçiciler güncellenmeli."
    
    if not os.path.exists('logs'): os.makedirs('logs')
    with open(f"logs/news_{date_str}.txt", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    get_news()
