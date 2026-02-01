import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def get_news():
    # RSS beslemeleri saf veridir, tasarım değişiminden etkilenmez.
    # Yapay Zeka, Siber Güvenlik ve Yazılım konuları filtrelenmiştir.
    sources = [
        "https://hnrss.org/newest?q=AI",
        "https://hnrss.org/newest?q=Cybersecurity",
        "https://hnrss.org/newest?q=Software+Development"
    ]
    
    news_list = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in sources:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            # RSS bir XML yapısıdır, bu yüzden 'xml' parser kullanıyoruz
            soup = BeautifulSoup(response.content, features="xml")
            items = soup.find_all('item', limit=2) # Her konudan en yeni 2 haberi al
            
            for item in items:
                title = item.title.text.strip()
                # Kategori belirleme
                category = "🤖 AI" if "AI" in url else "🛡️ Cyber" if "Cyber" in url else "💻 Dev"
                news_list.append(f"{category}: {title}")
        except Exception as e:
            print(f"Hata oluştu: {e}")

    # Dosyaya kaydetme işlemi
    date_str = datetime.now().strftime('%Y-%m-%d')
    content = f"--- {date_str} Teknoloji Gündemi ---\n\n"
    content += "\n".join(news_list) if news_list else "⚠️ Kaynaklara ulaşılamadı."
    
    if not os.path.exists('logs'): os.makedirs('logs')
    with open(f"logs/news_{date_str}.txt", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    get_news()
